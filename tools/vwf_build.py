"""Build the variable-width font (VWF) patch: patched EBOOT + rebuilt 14 px font.

Usage:
  python tools/vwf_build.py [--eboot work/source/eboot/EBOOT.dec.bin]
                            [--font work/source/dat/data/extra/gpsp3_font14.fnt]
                            [--out work/output/vwf]

Writes <out>/PSP_GAME/SYSDIR/EBOOT.BIN (decrypted ELF, patched),
<out>/data/extra/gpsp3_font14.fnt (overlay for tools/muf_archive.py repack),
<out>/vwf_widths.json and <out>/vwf_preview.png.

How it works (details in docs/vwf.md):
- English is written as single-byte ASCII. The game maps each ASCII byte to a
  Shift-JIS code (table at 0x347E4C) and draws that code's 14x14 glyph. We point
  the 96 ASCII codes 0x20-0x7F at 96 consecutive glyph slots that hold rare kanji
  no game string uses (glyph numbers G0..G0+95), and draw our own glyphs there.
- The game already has a proportional mode (font flag 0x20 + a table of
  left/right bearings per ASCII code) for its small HUD fonts. We switch it on
  for the 14 px font, give it a table (L = 0, R = 14 - advance) and route the
  single-byte branches of the printer, the width measurer and the line
  truncator into that code.
- The glyph-array text path (unit labels in 3D) has no proportional code, so a
  21-instruction helper in an unused function computes the advance there.
- The EBOOT is a relocatable PRX, so: no patched word may carry a relocation,
  jumps are PC-relative branches, and the one new pointer (font descriptor +0x24
  -> width table) gets a new R_MIPS_32 relocation appended to the reloc table.
"""

import argparse
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vwf_font  # noqa: E402

TEXT_OFF = 0xA0          # file offset of vaddr 0 (text segment)
DATA_VA, DATA_OFF = 0x3C1500, 0x3C1580
FONT14_DESC = 0x3FAE20   # font descriptor of gpsp3_font14.fnt (font index 0)
ASCII_TABLE = 0x347E4C   # ASCII 0x20.. -> Shift-JIS code, 2 bytes each (big-endian bytes)
CODES_TABLE = 0x3F769C   # glyph number -> code
GROUP_OFFSETS = 0x3FACF0  # 17 s16: first glyph number of each code group
TABLE_CAVE = 0x2A4CCC    # unused function (1264 bytes, no relocations): width table
HELPER_CAVE = 0x1740F8   # unused function, first 96 bytes free of relocations: helper
CELL = 14
DEFAULT_TTF = os.path.join("work", "fonts", "GenEiLateGo_v2.ttc")  # okoneya.jp, SIL OFL 1.1

# ------------------------------------------------------------- tiny assembler
R = {n: i for i, n in enumerate("zero at v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 t4 t5 t6 t7 "
                                "s0 s1 s2 s3 s4 s5 s6 s7 t8 t9 k0 k1 gp sp fp ra".split())}


def _r(rs, rt, rd, sa, fn):
    return (R[rs] << 21) | (R[rt] << 16) | (R[rd] << 11) | (sa << 6) | fn


def _i(op, rs, rt, imm):
    return (op << 26) | (R[rs] << 21) | (R[rt] << 16) | (imm & 0xFFFF)


def _off(pc, target):
    off = (target - (pc + 4)) >> 2
    if not -0x8000 <= off < 0x8000:
        raise ValueError("branch out of range %x -> %x" % (pc, target))
    return off


NOP = 0
def move(rd, rs): return _r(rs, "zero", rd, 0, 0x21)
def addu(rd, rs, rt): return _r(rs, rt, rd, 0, 0x21)
def subu(rd, rs, rt): return _r(rs, rt, rd, 0, 0x23)
def sll(rd, rt, sa): return _r("zero", rt, rd, sa, 0x00)
def mult(rs, rt): return _r(rs, rt, "zero", 0, 0x18)
def div(rs, rt): return _r(rs, rt, "zero", 0, 0x1A)
def mflo(rd): return _r("zero", "zero", rd, 0, 0x12)
def jr(rs): return _r(rs, "zero", "zero", 0, 0x08)
def addiu(rt, rs, imm): return _i(0x09, rs, rt, imm)
def andi(rt, rs, imm): return _i(0x0C, rs, rt, imm)
def sltiu(rt, rs, imm): return _i(0x0B, rs, rt, imm)
def lw(rt, off, base): return _i(0x23, base, rt, off)
def lh(rt, off, base): return _i(0x21, base, rt, off)
def sw(rt, off, base): return _i(0x2B, base, rt, off)
def beq(rs, rt, pc, target): return _i(0x04, rs, rt, _off(pc, target))
def b(pc, target): return beq("zero", "zero", pc, target)
def beqz(rs, pc, target): return beq(rs, "zero", pc, target)
def bal(pc, target): return (0x01 << 26) | (0x11 << 16) | (_off(pc, target) & 0xFFFF)
def bne(rs, rt, pc, target): return _i(0x05, rs, rt, _off(pc, target))
def sh(rt, off, base): return _i(0x29, base, rt, off)
def lui(rt, imm): return _i(0x0F, "zero", rt, imm)
def ori(rt, rs, imm): return _i(0x0D, rs, rt, imm)
def mov_s(fd, fs): return (0x11 << 26) | (0x10 << 21) | (fs << 11) | (fd << 6) | 0x06


# ------------------------------------------------------------- ELF helpers

class Eboot:
    def __init__(self, data):
        self.d = bytearray(data)
        if self.d[:4] != b"\x7fELF":
            raise ValueError("EBOOT is not a decrypted ELF")
        self.reloc_sites = self._reloc_sites()

    def _sections(self):
        shoff = struct.unpack_from("<I", self.d, 32)[0]
        shnum = struct.unpack_from("<H", self.d, 48)[0]
        return shoff, [list(struct.unpack_from("<10I", self.d, shoff + 40 * i)) for i in range(shnum)]

    def _reloc_sites(self):
        _, secs = self._sections()
        sites = set()
        for s in secs:
            if s[1] == 0x700000A0:
                for k in range(s[5] // 8):
                    off, info = struct.unpack_from("<2I", self.d, s[4] + 8 * k)
                    seg = (info >> 8) & 0xFF
                    sites.add(off + (DATA_VA if seg == 1 else 0))
        return sites

    @staticmethod
    def foff(va):
        return va + (DATA_OFF - DATA_VA if va >= DATA_VA else TEXT_OFF)

    def word(self, va):
        return struct.unpack_from("<I", self.d, self.foff(va))[0]

    def disasm(self, va):
        import capstone
        md = capstone.Cs(capstone.CS_ARCH_MIPS, capstone.CS_MODE_MIPS32 + capstone.CS_MODE_LITTLE_ENDIAN)
        o = self.foff(va)
        for ins in md.disasm(bytes(self.d[o:o + 4]), va):
            return ("%s %s" % (ins.mnemonic, ins.op_str)).strip()
        return "?"

    def put_word(self, va, w, expect=None):
        if va in self.reloc_sites:
            raise ValueError("refusing to patch relocated word at %x" % va)
        if expect is not None and self.disasm(va) != expect:
            raise ValueError("unexpected instruction at %x: %r (wanted %r)" % (va, self.disasm(va), expect))
        struct.pack_into("<I", self.d, self.foff(va), w)

    def put_bytes(self, va, data):
        for a in range(va & ~3, va + len(data), 4):
            if a in self.reloc_sites:
                raise ValueError("refusing to overwrite relocated word at %x" % a)
        o = self.foff(va)
        self.d[o:o + len(data)] = data

    def append_reloc(self, r_offset, info):
        """Append one PSP relocation to the last relocation section and segment."""
        shoff, secs = self._sections()
        last = max((i for i, s in enumerate(secs) if s[1] == 0x700000A0), key=lambda i: secs[i][4])
        end = secs[last][4] + secs[last][5]
        self.d[end:end] = struct.pack("<2I", r_offset, info)
        for i, s in enumerate(secs):
            if i == last:
                s[5] += 8
            elif s[4] >= end and s[1] != 8:
                s[4] += 8
        shoff += 8
        struct.pack_into("<I", self.d, 32, shoff)
        for i, s in enumerate(secs):
            struct.pack_into("<10I", self.d, shoff + 40 * i, *s)
        # program header of type 0x700000A0 (what the PSP kernel reads)
        phoff = struct.unpack_from("<I", self.d, 28)[0]
        phnum = struct.unpack_from("<H", self.d, 44)[0]
        for i in range(phnum):
            p = list(struct.unpack_from("<8I", self.d, phoff + 32 * i))
            if p[0] == 0x700000A0:
                if p[1] + p[4] != end:
                    raise ValueError("reloc segment does not end where the last reloc section ends")
                p[4] += 8
                struct.pack_into("<8I", self.d, phoff + 32 * i, *p)


# ------------------------------------------------------------- the patch

G0 = 1210  # group 2, codes 0x9F82..0xE772: 96 kanji that no game string uses


def glyph_slots(eb):
    """The 96 glyph numbers reserved for ASCII: a run of rare kanji (see docs/vwf.md)."""
    offs = struct.unpack_from("<17h", eb.d, eb.foff(GROUP_OFFSETS))
    codes = [struct.unpack_from(">H", eb.d, eb.foff(CODES_TABLE) + 2 * i)[0] for i in range(offs[16])]
    if not (offs[2] <= G0 and G0 + 96 <= offs[3]) or codes[G0] != 0x9F82 or codes[G0 + 95] != 0xE772:
        raise ValueError("glyph code table is not the original one")
    return G0, codes[G0:G0 + 96]


def helper_code(pc):
    """t7 = advance of glyph t7 (0x4000 flag allowed) at size t8, font t9. Uses $at."""
    full = pc + 19 * 4
    code = [
        andi("t7", "t7", 0x3FFF),
        addiu("t7", "t7", -G0),
        sltiu("at", "t7", 96),
        None,                                  # beqz at, full
        lw("t9", 0x24, "t9"),                  # table pointer (delay slot)
        None,                                  # beqz t9, full
        sll("t7", "t7", 3),
        addu("t9", "t9", "t7"),
        lw("t7", 0, "t9"),                     # L
        lw("t9", 4, "t9"),                     # R
        addu("t7", "t7", "t9"),
        mult("t7", "t8"),
        mflo("t7"),
        addiu("t7", "t7", CELL // 2),
        addiu("t9", "zero", CELL),
        div("t7", "t9"),
        mflo("t7"),
        jr("ra"),
        subu("t7", "t8", "t7"),                # advance = size - round((L+R)*size/14)
        jr("ra"),                              # full: not one of ours
        move("t7", "t8"),
    ]
    code[3] = beqz("at", pc + 12, full)
    code[5] = beqz("t9", pc + 20, full)
    return code


def code_patches(H):
    """(vaddr, new word, original instruction as capstone prints it) for each change."""
    p = []

    def at(va, new, orig):
        p.append((va, new, orig))

    def run(va, words, origs):
        assert len(words) == len(origs)
        for i, (w, o) in enumerate(zip(words, origs)):
            at(va + 4 * i, w, o)

    # main printer 0x159560 -------------------------------------------------
    at(0x159B84, b(0x159B84, 0x15984C), "mtc1 $zero, $f1")        # SB advance -> bearing-table code
    at(0x159D18, NOP, "mul.s $f2, $f2, $f0")                      # SB glyph drawn full size, not x0.8
    at(0x15A0AC, NOP, "mul.s $f2, $f2, $f0")                      # same, '{' '}' path
    at(0x159ED4, move("a2", "s6"), "subu $a2, $s6, $v0")          # '(' '[' drawn at the pen
    at(0x1598C8, addiu("v0", "zero", 0x100), "addiu $v0, $zero, 0x20")   # space uses the table too
    at(0x159C2C, addiu("v1", "zero", 0x100), "addiu $v1, $zero, 0x40")   # '`' is no longer special
    at(0x159C34, sltiu("v0", "a0", 0x60), "sltiu $v0, $a0, 0x5b")        # ASCII table covers 0x20-0x7F
    # width of a string 0x1590A8 -----------------------------------------
    at(0x15917C, NOP, "beqz $t0, 0x159238")                       # SB chars always use the table
    at(0x159144, addiu("t7", "zero", 0x100), "addiu $t7, $zero, 0x20")
    # line truncation 0x15937C --------------------------------------------
    at(0x1594FC, b(0x1594FC, 0x1593E0), "mtc1 $a1, $f1")
    at(0x1593C0, addiu("t9", "zero", 0x100), "addiu $t9, $zero, 0x20")
    # string -> glyph array 0x158ECC --------------------------------------
    at(0x158FD0, addiu("v0", "zero", 0x100), "addiu $v0, $zero, 0x40")
    at(0x158FDC, sltiu("v0", "v1", 0x60), "sltiu $v0, $v1, 0x5b")
    # glyph-array drawer 0x1586B8 -----------------------------------------
    at(0x158818, mov_s(1, 20), "mul.s $f1, $f20, $f1")            # glyph drawn full size
    at(0x158840, sw("a0", 0x2C, "sp"), "add.s $f0, $f1, $f0")     # keep the font pointer
    at(0x15885C, move("t0", "s2"), "mfc1 $t0, $f0")               # width = size
    # advance after a half-width glyph (0x15887C carries a relocation: kept)
    run(0x158868, [lh("t7", -2, "s3"), move("t8", "s2"), bal(0x158870, H), lw("t9", 0x2C, "sp"), NOP],
        ["mtc1 $zero, $f1", "mul.s $f2, $f20, $f0", "c.le.s $f1, $f2", "nop", "bc1f 0x158a1c"])
    run(0x158880, [move("v0", "t7"), NOP, NOP],
        ["add.s $f0, $f2, $f0", "trunc.w.s $f0, $f0", "mfc1 $v0, $f0"])
    # centring pre-pass, mode 3 (0x1589C8 carries a relocation: kept)
    run(0x1589A4, [move("t7", "v0"), move("t8", "s2"), bal(0x1589AC, H), move("t9", "s0"), move("v0", "t7"),
                   NOP, NOP, NOP, NOP],
        ["cvt.s.w $f0, $f4", "mul.s $f0, $f0, $f3", "c.le.s $f1, $f0", "nop", "bc1fl 0x158a30",
         "sub.s $f0, $f0, $f2", "add.s $f0, $f0, $f2", "trunc.w.s $f0, $f0", "mfc1 $v0, $f0"])
    # centring pre-pass, mode 1 (0x158A60, 0x158A64 and 0x158A74 carry relocations: kept)
    run(0x158A48, [move("t7", "v1"), move("t8", "s2"), bal(0x158A50, H), move("t9", "s0"), NOP, NOP],
        ["cvt.s.w $f2, $f0", "mtc1 $zero, $f0", "mul.s $f2, $f2, $f1", "c.le.s $f0, $f2", "nop",
         "bc1f 0x158a7c"])
    run(0x158A68, [move("v0", "t7"), NOP, NOP],
        ["add.s $f0, $f2, $f0", "trunc.w.s $f0, $f0", "mfc1 $v0, $f0"])
    return p


# ------------------------------------------------------------- HD glyphs (docs/vwf.md "HD text")
#
# The 96 English glyphs also get a 4x copy (56 px cells) in a page appended to the
# font file. The game draws every glyph as a sprite whose screen size comes from the
# text size and whose texture coordinates come from the font's cell size, so a 4x
# texture drawn into the same 14 px box gives PPSSPP real detail at 2x/4x rendering.
#
# - glyph lookup 0x15787C (binds the page, picks the CLUT layer, returns column/row)
#   now starts with a branch to a dispatcher. For an English glyph of the 14 px font
#   it points the descriptor's base (+0x3C) at the 4x page and its cells per row
#   (+0x10) at 8, calls the original body with the page-local glyph number, and puts
#   both fields back. Width, height, page size and the TSIZE command stay valid: the
#   4x page is also 448 px wide and bound as 512x512.
# - the texture cell size the sprite emitters use is written to descriptor +0x18/+0x1A
#   (halfwords; +0x18 is read nowhere in the text code): 56 for a 4x glyph, otherwise
#   the font's own cell size. The emitters' loads of +0x08/+0x0C for texture
#   coordinates become loads of +0x18/+0x1A. The printer still reads +0x08 for the
#   advance, which stays 14.

LOOKUP = 0x15787C          # glyph lookup: addiu sp,-0x30 / sw ra,0x24(sp) / ...
LOOKUP_BODY = LOOKUP + 8
DISPATCH_CAVE = 0x15744C   # unused string-width routine 0x1573DC: 68 words free of relocations

# texture-coordinate loads in the four sprite emitters (0x157A44, 0x157F10, 0x15802C, 0x15E6xx)
EMITTER_LOADS = [
    (0x157AC4, "a1", "s6", 8), (0x157ACC, "t2", "s6", 0xC), (0x157B80, "v1", "s6", 8), (0x157B88, "t2", "s6", 0xC),
    (0x157BE4, "a0", "s6", 8), (0x157BEC, "t3", "s6", 0xC),
    (0x157F88, "v1", "s1", 8), (0x157F90, "t3", "s1", 0xC),
    (0x1580B4, "a0", "s1", 8), (0x1580BC, "a1", "s1", 0xC), (0x1581A4, "v1", "s1", 8), (0x1581AC, "t2", "s1", 0xC),
    (0x1581FC, "t2", "s1", 8), (0x158204, "t1", "s1", 0xC), (0x158254, "t2", "s1", 8), (0x15825C, "t1", "s1", 0xC),
    (0x1582BC, "a0", "s1", 8), (0x1582D0, "t3", "s1", 0xC),
    (0x15E6D4, "t3", "s2", 8), (0x15E6DC, "v0", "s2", 0xC), (0x15E764, "v0", "s2", 8), (0x15E76C, "v1", "s2", 0xC),
    (0x15E7F0, "t3", "s2", 8), (0x15E7F8, "t2", "s2", 0xC), (0x15E868, "v1", "s2", 8), (0x15E870, "t2", "s2", 0xC),
    (0x15E8DC, "t1", "s2", 8), (0x15E8D4, "a0", "s2", 0xC), (0x15E94C, "t3", "s2", 8), (0x15E954, "v1", "s2", 0xC),
]


def dispatcher_code(pc, g0, hd_off):
    """Entered from LOOKUP with a0 = font, a1 = glyph, a2/a3 = &column/&row."""
    big = vwf_font.BIG
    code = []

    def emit(w):
        code.append(w)

    def here():
        return pc + 4 * len(code)

    labels = {}
    emit(addiu("sp", "sp", -0x20))
    emit(sw("ra", 0x10, "sp"))
    emit(sw("s0", 0x14, "sp"))
    emit(move("s0", "a0"))
    emit(lw("t0", 8, "a0"))
    emit(lw("t1", 0xC, "a0"))
    emit(sh("t0", 0x18, "a0"))                 # texture cell = the font's own cell
    emit(sh("t1", 0x1A, "a0"))
    emit(addiu("t2", "zero", CELL))
    fix_bne = len(code); emit(None)            # bne t0, t2, normal
    emit(addiu("t3", "a1", -g0))               # delay: page-local glyph number
    emit(sltiu("t4", "t3", 96))
    fix_beqz = len(code); emit(None)           # beqz t4, normal
    emit(NOP)
    # 4x glyph
    emit(addiu("t5", "zero", big))
    emit(sh("t5", 0x18, "a0"))
    emit(sh("t5", 0x1A, "a0"))
    emit(lw("t6", 0x3C, "a0"))
    emit(lw("t7", 0x10, "a0"))
    emit(sw("t6", 0x18, "sp"))
    emit(sw("t7", 0x1C, "sp"))
    emit(lui("t8", hd_off >> 16))
    emit(ori("t8", "t8", hd_off & 0xFFFF))
    emit(addu("t6", "t6", "t8"))
    emit(sw("t6", 0x3C, "a0"))
    emit(addiu("t7", "zero", vwf_font.HD_PER_ROW))
    emit(sw("t7", 0x10, "a0"))
    emit(move("a1", "t3"))
    emit(addiu("sp", "sp", -0x30))             # the two instructions LOOKUP lost
    fix_bal1 = len(code); emit(None)           # bal LOOKUP_BODY
    emit(sw("ra", 0x24, "sp"))                 # delay slot: the body returns here
    emit(lw("t6", 0x18, "sp"))
    emit(lw("t7", 0x1C, "sp"))
    emit(sw("t6", 0x3C, "s0"))
    fix_b = len(code); emit(None)              # b done
    emit(sw("t7", 0x10, "s0"))
    labels["normal"] = here()
    emit(addiu("sp", "sp", -0x30))
    fix_bal2 = len(code); emit(None)
    emit(sw("ra", 0x24, "sp"))
    labels["done"] = here()
    emit(lw("ra", 0x10, "sp"))
    emit(lw("s0", 0x14, "sp"))
    emit(jr("ra"))
    emit(addiu("sp", "sp", 0x20))
    code[fix_bne] = bne("t0", "t2", pc + 4 * fix_bne, labels["normal"])
    code[fix_beqz] = beqz("t4", pc + 4 * fix_beqz, labels["normal"])
    code[fix_bal1] = bal(pc + 4 * fix_bal1, LOOKUP_BODY)
    code[fix_b] = b(pc + 4 * fix_b, labels["done"])
    code[fix_bal2] = bal(pc + 4 * fix_bal2, LOOKUP_BODY)
    return code


def hd_patches(eb, g0, hd_off):
    code = dispatcher_code(DISPATCH_CAVE, g0, hd_off)
    if len(code) > 68:
        raise ValueError("dispatcher does not fit the cave")
    for i, w in enumerate(code):
        eb.put_word(DISPATCH_CAVE + 4 * i, w)
    eb.put_word(LOOKUP, b(LOOKUP, DISPATCH_CAVE), "addiu $sp, $sp, -0x30")
    eb.put_word(LOOKUP + 4, NOP, "sw $ra, 0x24($sp)")
    for va, rt, base, off in EMITTER_LOADS:
        eb.put_word(va, lh(rt, 0x18 if off == 8 else 0x1A, base), "lw $%s, %s($%s)" % (rt, "8" if off == 8 else "0xc", base))
    return len(code)


def build(eboot_path, font_path, out, weight=vwf_font.DEFAULT_WEIGHT, ttf=vwf_font.DEFAULT_FONT, ttf_index=0,
          hd=False):
    eb = Eboot(open(eboot_path, "rb").read())
    g0, codes = glyph_slots(eb)

    if hd:
        glyphs, widths, info, hd_glyphs = vwf_font.build_set(ttf, weight, ttf_index, hd=True)
    else:
        glyphs, widths, info = vwf_font.build_set(ttf, weight, ttf_index)

    # font: our glyphs into slots g0..g0+95 (+ the 4x page appended)
    font_in = open(font_path, "rb").read()
    atlas = vwf_font.read_atlas(font_in)
    for i, g in enumerate(glyphs):
        vwf_font.put_glyph(atlas, g0 + i, g)
    font_bytes = vwf_font.write_atlas(atlas)
    if hd:
        hd_off = len(font_bytes)
        if hd_off % 16:
            raise ValueError("font size is not 16-byte aligned")
        font_bytes += vwf_font.hd_page(hd_glyphs)
        info["hd_page_offset"] = hd_off
    font_out = os.path.join(out, "data", "extra", "gpsp3_font14.fnt")
    os.makedirs(os.path.dirname(font_out), exist_ok=True)
    open(font_out, "wb").write(font_bytes)

    # ASCII -> code table
    eb.put_bytes(ASCII_TABLE, b"".join(struct.pack(">H", c) for c in codes))

    # width table: guard entry (index -1, used for single-byte kana) + 96 entries
    table = struct.pack("<2i", 0, 0) + b"".join(struct.pack("<2i", 0, CELL - w) for w in widths)
    eb.put_bytes(TABLE_CAVE, table)
    table_va = TABLE_CAVE + 8

    # font descriptor: proportional flag + table pointer (with a new relocation)
    flags = struct.unpack_from("<H", eb.d, eb.foff(FONT14_DESC))[0]
    if flags != 0 or eb.word(FONT14_DESC + 0x24) != 0:
        raise ValueError("font descriptor is not the original one")
    struct.pack_into("<H", eb.d, eb.foff(FONT14_DESC), flags | 0x20)
    eb.put_word(FONT14_DESC + 0x24, table_va)
    # R_MIPS_32, word in segment 1 (data), value relative to segment 0 (text)
    eb.append_reloc(FONT14_DESC + 0x24 - DATA_VA, 2 | (1 << 8) | (0 << 16))

    # helper + code patches
    for i, w in enumerate(helper_code(HELPER_CAVE)):
        eb.put_word(HELPER_CAVE + 4 * i, w)
    for va, w, orig in code_patches(HELPER_CAVE):
        eb.put_word(va, w, orig)
    if hd:
        n = hd_patches(eb, g0, info["hd_page_offset"])
        print("HD text: 4x page at font offset 0x%X, dispatcher %d words at 0x%X, %d emitter loads"
              % (info["hd_page_offset"], n, DISPATCH_CAVE, len(EMITTER_LOADS)))

    eboot_out = os.path.join(out, "PSP_GAME", "SYSDIR", "EBOOT.BIN")
    os.makedirs(os.path.dirname(eboot_out), exist_ok=True)
    open(eboot_out, "wb").write(eb.d)

    json.dump({"info": info, "first_code": vwf_font.FIRST, "glyph_base": g0,
               "codes": ["%04X" % c for c in codes], "advance": widths},
              open(os.path.join(out, "vwf_widths.json"), "w"), indent=1)
    samples = [s.replace("…", chr(0x7F)) for s in vwf_font.SAMPLES]
    vwf_font.preview(os.path.join(out, "vwf_preview.png"), glyphs, widths, samples)
    if hd:
        vwf_font.hd_preview(os.path.join(out, "vwf_preview_hd.png"), hd_glyphs, widths, samples)
    print("glyph slots %d-%d, %s" % (g0, g0 + 95, info))
    print("wrote", eboot_out, "and", font_out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eboot", default=os.path.join("work", "source", "eboot", "EBOOT.dec.bin"))
    ap.add_argument("--font", default=os.path.join("work", "source", "dat", "data", "extra", "gpsp3_font14.fnt"))
    ap.add_argument("--out", default=os.path.join("work", "output", "vwf"))
    ap.add_argument("--weight", type=int, default=vwf_font.DEFAULT_WEIGHT)
    ap.add_argument("--ttf", default=DEFAULT_TTF if os.path.exists(DEFAULT_TTF) else vwf_font.DEFAULT_FONT,
                    help="TrueType font for the English glyphs (default: GenEi LateGo v2, SIL OFL 1.1)")
    ap.add_argument("--ttf-index", type=int, default=0, help="face index in a .ttc collection")
    ap.add_argument("--no-hd", action="store_true", help="native 14 px glyphs only (no 4x page)")
    args = ap.parse_args()
    build(args.eboot, args.font, args.out, args.weight, args.ttf, args.ttf_index, hd=not args.no_hd)


if __name__ == "__main__":
    main()
