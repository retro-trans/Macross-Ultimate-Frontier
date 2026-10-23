"""EBOOT patch: song lyrics on screen while a song plays in a mission (docs/lyrics.md).

Usage:
  python tools/lyrics_patch.py <in EBOOT.BIN> <out EBOOT.BIN>

Run it on a decrypted EBOOT that went through tools/vwf_build.py (the lyrics use
the VWF font), after tools/voice_subs_patch.py when both are used: the draw hook
calls whatever the hooked call went to before, so the voice subtitles keep
working.

Where the lyrics come from
  Each song's lines are stored at the end of its own file,
  PSP_GAME/USRDIR/data/sound/bgm/bgmNN.at3 (tools/lyrics.py build):

      ... ATRAC3 RIFF file ... | pad to 4 | blob | u32 blob_len | "LYR1"

      blob = u32 loop_start, u32 loop_end, u32 count,
             count x (u32 start, u32 end, u32 text offset from the blob),
             the texts (Shift-JIS, NUL-terminated, "\\n" between lines)

  Times are in samples (44,100 a second). The RIFF sizes are not changed, so the
  player never reads the tail. The game loads a BGM file whole into the buffer of
  its ATRAC stream object (stream +0x34, size at +0x30), so the lyrics arrive with
  the song: no extra file read and no extra memory.

How the song time is known
  Every ATRAC stream object (0x6C bytes; +8 = its sound channel, 0 = BGM,
  1 = voice, 2 = the third channel) is started by the method 0x26C8DC, which calls
  sceAtracSetDataAndGetID at 0x26C8F0: that call goes to SET_HOOK, which records
  the stream for its channel and sets the channel's sample counter to 0.
  The stream thread decodes with sceAtracDecodeData at 0x26CA88 (about 2,048
  samples at a time, a few ahead of playback): that call goes to DEC_HOOK, which
  adds the samples decoded to the channel's counter. The counter follows the
  music: it stops when the game pauses the sound and does not move for a song
  that is loaded but not playing. After the loop end the song continues from its
  loop start, and so does the lyric time (loop points from the file's smpl chunk).

When it is shown
  The mission's 2D layer ends with the call at 0x140D68 (see
  docs/voice_subtitles.md). That call goes to DRAW_HOOK, which first runs the
  previous target (the voice subtitles' hook, or the game's cut-in step
  0x1A024C), then picks the channel that decoded in the last IDLE_MAX frames,
  carries a lyrics tail, and was started last; finds the line whose
  [start, end) holds the current time; and draws it with the game's text
  routine 0x15ABC0, a shadow 1 px down-right and then the text. Position, size,
  colours and the timing lag are config words at CFG (CONFIG below), so a layout
  can be tried live in the debugger.

Space
  SET_HOOK, DEC_HOOK and DRAW_HOOK, and the state and config words, go in a run
  of unused VFPU vector helpers at 0x2A1A5C-0x2A26DC (800 words, no relocations,
  nothing calls or points to them; found by tools-side reference analysis).
  The replaced words are `jal` with an R_MIPS_26 relocation, which stays valid
  for the new target; the new code carries no relocation (it finds its load
  address with `bal`).
"""

import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vwf_build import Eboot  # noqa: E402
from voice_subs_patch import (Asm, _r, addiu, andi, lw, sw, addu, subu, slt, slti, sll, srl,  # noqa: E402
                              jr, jalr, move, nop, beq, bne, blez, bltz, bal, b, li32, runtime,
                              call, prologue, epilogue, jal_word)

CAVE = (0x2A1A5C, 0x2A26DC)                 # unused VFPU vector helpers
DATA = 0x2A2600                              # state and config words (inside CAVE, after the code)
D_STREAM = 0x00                              # 4 words: stream object of channel k (0 = none yet)
D_COUNT = 0x10                               # 4 words: samples decoded since the stream was started
D_SEQ = 0x20                                 # 4 words: start order (higher = started later)
D_LAST = 0x30                                # 4 words: counter seen by the last draw
D_IDLE = 0x40                                # 4 words: draws since the counter last moved
D_GSEQ = 0x50                                # next start number
CFG = DATA + 0x54                            # config words (CONFIG)
DATA_END = CFG + 4 * 11
assert DATA_END <= CAVE[1]

MAGIC = 0x3152594C                           # "LYR1" as a little-endian word
IDLE_MAX = 20                                # a channel that did not decode for this many draws is silent

SET_SITE = 0x26C8F0                          # jal sceAtracSetDataAndGetID (stream start)
DEC_SITE = 0x26CA88                          # jal sceAtracDecodeData (stream thread)
DRAW_SITE = 0x140D68                         # jal 0x1A024C (or the voice subtitles' draw hook)
STUB_SETDATA = 0x2C8BB0                      # sceAtrac3plus import stubs
STUB_DECODE = 0x2C8BA8
F_LAYER_END = 0x1A024C
F_TEXT = 0x15ABC0          # (str, x, y, size, size2, box w, z, colour, [sp0] font, [sp4] align, [sp8] line step)

# x, y, size, box width, alignment (3 = centred on x, lines going down from y), colour (ABGR),
# shadow colour, line step, sprite depth, lag (samples subtracted from the decoded count: the
# decoder runs a little ahead of the speaker), idle frames.
# The box (x 95-385, y 4-30) is the top band between the partner/team panels on the left and
# the mission timer and radar on the right; the voice subtitles sit at the bottom (y 208-248).
CONFIG = [240, 4, 12, 290, 3, 0xFFA0F0FF, 0xFF000000, 13, 0xFFFF, 2048, IDLE_MAX]
C_X, C_Y, C_SIZE, C_BOX, C_ALIGN, C_COL, C_SHADOW, C_STEP, C_Z, C_LAG, C_IDLE = range(11)


def sltu(rd, rs, rt): return lambda pc, L: _r(rs, rt, rd, 0, 0x2B)
def divu(rs, rt): return lambda pc, L: _r(rs, rt, "zero", 0, 0x1B)
def mfhi(rd): return lambda pc, L: _r("zero", "zero", rd, 0, 0x10)
def bgez(rs, t): return lambda pc, L: (0x01 << 26) | (__import__("vwf_build").R[rs] << 21) | (1 << 16) | \
    __import__("voice_subs_patch")._br(pc, L, t)


def chan_slot(a, reg, stream, data):
    """reg = data + 4 * (channel of `stream` & 3)."""
    a.op(lw(reg, 8, stream))
    a.op(andi(reg, reg, 3))
    a.op(sll(reg, reg, 2))
    a.op(addu(reg, reg, data))


def build(prev_draw):
    a = Asm(CAVE[0])

    # SET_HOOK(a0 = data, a1 = size); s0 = the stream object (caller's)
    F = 0x20
    a.label("set_hook")
    a.op(addiu("sp", "sp", -F))
    a.op(sw("ra", F - 4, "sp"))
    a.op(sw("s1", F - 8, "sp"))
    a.op(bal("s_here"))
    a.op(nop())
    a.label("s_here")
    li32(a, "at", a.labels["s_here"])
    a.op(subu("s1", "ra", "at"))
    call(a, "s1", STUB_SETDATA)
    a.op(nop())
    runtime(a, "t0", DATA, "s1")
    chan_slot(a, "t1", "s0", "t0")
    a.op(sw("s0", D_STREAM, "t1"))
    a.op(sw("zero", D_COUNT, "t1"))
    a.op(sw("zero", D_LAST, "t1"))
    a.op(addiu("t2", "zero", 0x7FFF))
    a.op(sw("t2", D_IDLE, "t1"))           # silent until it decodes
    a.op(lw("t2", D_GSEQ, "t0"))
    a.op(addiu("t2", "t2", 1))
    a.op(sw("t2", D_GSEQ, "t0"))
    a.op(sw("t2", D_SEQ, "t1"))
    a.op(lw("ra", F - 4, "sp"))
    a.op(lw("s1", F - 8, "sp"))
    a.op(jr("ra"))
    a.op(addiu("sp", "sp", F))

    # DEC_HOOK(a0 = id, a1 = out, a2 = &samples, a3 = &finished, t0 = &remain); s0 = the stream
    a.label("dec_hook")
    a.op(addiu("sp", "sp", -F))
    a.op(sw("ra", F - 4, "sp"))
    a.op(sw("s1", F - 8, "sp"))
    a.op(sw("a2", F - 12, "sp"))
    a.op(bal("d_here"))
    a.op(nop())
    a.label("d_here")
    li32(a, "at", a.labels["d_here"])
    a.op(subu("s1", "ra", "at"))
    li32(a, "t9", STUB_DECODE)              # t0 (the 5th argument) is left alone
    a.op(addu("t9", "t9", "s1"))
    a.op(jalr("t9"))
    a.op(nop())
    a.op(bltz("v0", "d_ret"))
    a.op(lw("t1", F - 12, "sp"))
    a.op(lw("t1", 0, "t1"))                 # samples decoded
    runtime(a, "t2", DATA, "s1")
    chan_slot(a, "t3", "s0", "t2")
    a.op(lw("t4", D_COUNT, "t3"))
    a.op(addu("t4", "t4", "t1"))
    a.op(sw("t4", D_COUNT, "t3"))
    a.label("d_ret")
    a.op(lw("ra", F - 4, "sp"))
    a.op(lw("s1", F - 8, "sp"))
    a.op(jr("ra"))
    a.op(addiu("sp", "sp", F))

    # DRAW_HOOK(): run the previous target, then draw the current lyric line
    F = 0x30                                 # frame: sp+0..8 stack arguments, +0x18 line
    a.label("draw_hook")
    prologue(a, "w_here", "s1", F)
    call(a, "s1", prev_draw)
    a.op(nop())
    runtime(a, "s0", DATA, "s1")
    runtime(a, "s3", CFG, "s1")
    a.op(addiu("s2", "zero", -1))           # s2 = chosen channel slot address (-1 = none)
    a.op(move("t8", "zero"))                # t8 = its start number
    a.op(move("t0", "s0"))                  # t0 = data + 4k
    a.op(addiu("t9", "s0", 16))
    a.label("w_chan")
    a.op(lw("t1", D_STREAM, "t0"))
    a.op(beq("t1", "zero", "w_next"))
    a.op(lw("t2", D_COUNT, "t0"))
    a.op(lw("t3", D_LAST, "t0"))
    a.op(beq("t2", "t3", "w_still"))
    a.op(lw("t4", D_IDLE, "t0"))
    a.op(sw("t2", D_LAST, "t0"))
    a.op(b("w_active"))
    a.op(sw("zero", D_IDLE, "t0"))
    a.label("w_still")
    a.op(slti("t5", "t4", 0x7FFF))
    a.op(addu("t4", "t4", "t5"))
    a.op(sw("t4", D_IDLE, "t0"))
    a.op(lw("t5", 4 * C_IDLE, "s3"))
    a.op(slt("t5", "t4", "t5"))
    a.op(beq("t5", "zero", "w_next"))
    a.op(nop())
    a.label("w_active")
    a.op(lw("t5", 0x34, "t1"))              # data (the whole file)
    a.op(srl("t7", "t5", 25))
    a.op(addiu("t7", "t7", -4))             # user RAM 0x08000000-0x09FFFFFF only
    a.op(bne("t7", "zero", "w_next"))
    a.op(lw("t6", 0x30, "t1"))              # (delay) its size
    a.op(slti("t7", "t6", 16))
    a.op(bne("t7", "zero", "w_next"))
    a.op(addu("t5", "t5", "t6"))            # t5 = end of the file
    a.op(andi("t7", "t5", 3))
    a.op(bne("t7", "zero", "w_next"))
    a.op(nop())
    a.op(lw("t6", -4, "t5"))
    li32(a, "t7", MAGIC)
    a.op(bne("t6", "t7", "w_next"))
    a.op(lw("t6", D_SEQ, "t0"))
    a.op(sltu("t7", "t8", "t6"))
    a.op(beq("t7", "zero", "w_next"))
    a.op(nop())
    a.op(move("t8", "t6"))
    a.op(move("s2", "t0"))
    a.label("w_next")
    a.op(addiu("t0", "t0", 4))
    a.op(bne("t0", "t9", "w_chan"))
    a.op(nop())
    a.op(bltz("s2", "w_ret"))
    a.op(nop())
    # blob of the chosen channel
    a.op(lw("t1", D_STREAM, "s2"))
    a.op(lw("t5", 0x34, "t1"))
    a.op(lw("t7", 0x30, "t1"))
    a.op(addu("t5", "t5", "t7"))
    a.op(lw("t6", -8, "t5"))                # blob length: below the file size, a multiple of 4
    a.op(sltu("t4", "t6", "t7"))
    a.op(beq("t4", "zero", "w_ret"))
    a.op(andi("t4", "t6", 3))
    a.op(bne("t4", "zero", "w_ret"))
    a.op(subu("t5", "t5", "t6"))
    a.op(addiu("t5", "t5", -8))             # t5 = blob
    a.op(lw("t2", D_COUNT, "s2"))
    a.op(lw("t3", 4 * C_LAG, "s3"))
    a.op(subu("t2", "t2", "t3"))
    a.op(bltz("t2", "w_ret"))               # t2 = song time in samples
    a.op(lw("t3", 0, "t5"))                 # loop start
    a.op(lw("t4", 4, "t5"))                 # loop end
    a.op(sltu("t6", "t3", "t4"))
    a.op(beq("t6", "zero", "w_find"))
    a.op(sltu("t6", "t2", "t4"))
    a.op(bne("t6", "zero", "w_find"))
    a.op(nop())
    a.op(subu("t2", "t2", "t3"))
    a.op(subu("t6", "t4", "t3"))
    a.op(divu("t2", "t6"))
    a.op(mfhi("t2"))
    a.op(addu("t2", "t2", "t3"))            # past the loop end: back into the loop
    a.label("w_find")
    a.op(lw("t3", 8, "t5"))                 # count
    a.op(addiu("t4", "t5", 12))             # t4 = entry
    a.label("w_entry")
    a.op(blez("t3", "w_ret"))
    a.op(lw("t6", 0, "t4"))                 # start
    a.op(sltu("t7", "t2", "t6"))
    a.op(bne("t7", "zero", "w_skip"))
    a.op(lw("t6", 4, "t4"))                 # end
    a.op(sltu("t7", "t2", "t6"))
    a.op(bne("t7", "zero", "w_show"))
    a.op(lw("t6", 8, "t4"))                 # text offset
    a.label("w_skip")
    a.op(addiu("t3", "t3", -1))
    a.op(b("w_entry"))
    a.op(addiu("t4", "t4", 12))
    a.label("w_show")
    a.op(addu("t6", "t5", "t6"))
    a.op(sw("t6", 0x18, "sp"))
    a.op(addiu("s2", "zero", 1))            # pass 1: shadow (+1, +1); pass 0: text
    a.label("w_pass")
    a.op(lw("a1", 4 * C_X, "s3"))
    a.op(lw("a2", 4 * C_Y, "s3"))
    a.op(addu("a1", "a1", "s2"))
    a.op(addu("a2", "a2", "s2"))
    a.op(lw("a3", 4 * C_SIZE, "s3"))
    a.op(move("t0", "a3"))
    a.op(lw("t1", 4 * C_BOX, "s3"))
    a.op(lw("v0", 4 * C_ALIGN, "s3"))
    a.op(sw("v0", 4, "sp"))                 # [sp4] alignment mode
    a.op(lw("v0", 4 * C_STEP, "s3"))
    a.op(sw("v0", 8, "sp"))                 # [sp8] line step
    a.op(sw("zero", 0, "sp"))               # [sp0] font 0 (VWF)
    a.op(lw("t2", 4 * C_Z, "s3"))
    a.op(beq("s2", "zero", "w_col"))
    a.op(lw("t3", 4 * C_COL, "s3"))
    a.op(lw("t3", 4 * C_SHADOW, "s3"))
    a.label("w_col")
    call(a, "s1", F_TEXT)
    a.op(lw("a0", 0x18, "sp"))              # (delay) the line
    runtime(a, "s3", CFG, "s1")             # s3 survives the call, but be safe
    a.op(bne("s2", "zero", "w_pass"))
    a.op(addiu("s2", "s2", -1))
    a.label("w_ret")
    epilogue(a, F)

    words = a.assemble()
    if CAVE[0] + 4 * len(words) > DATA:
        raise ValueError("lyrics hooks do not fit before the data: %d words" % len(words))
    return words, a.labels


def patch(data):
    eb = Eboot(data)
    cur = eb.word(DRAW_SITE)
    if cur >> 26 != 0x03:
        raise ValueError("%x is not a jal" % DRAW_SITE)
    prev_draw = (cur & 0x3FFFFFF) << 2
    words, labels = build(prev_draw)
    if prev_draw == labels["draw_hook"]:
        raise ValueError("EBOOT already has the lyrics patch")
    # the cave must still hold the original VFPU helpers
    if eb.word(CAVE[0]) != 0x00801021 or eb.word(CAVE[1] - 8) != 0x03E00008:
        raise ValueError("code cave at %x does not look untouched" % CAVE[0])
    for va in range(CAVE[0], DATA_END, 4):
        if va in eb.reloc_sites:
            raise ValueError("relocation inside the cave at %x" % va)
    for i, w in enumerate(words):
        eb.put_word(CAVE[0] + 4 * i, w)
    for va in range(DATA, CFG, 4):
        eb.put_word(va, 0)
    for i, w in enumerate(CONFIG):
        eb.put_word(CFG + 4 * i, w & 0xFFFFFFFF)
    hooks = [(SET_SITE, STUB_SETDATA, labels["set_hook"]),
             (DEC_SITE, STUB_DECODE, labels["dec_hook"]),
             (DRAW_SITE, prev_draw, labels["draw_hook"])]
    for va, target, hook in hooks:
        if va not in eb.reloc_sites:
            raise ValueError("%x has no relocation" % va)
        if eb.word(va) != jal_word(target):
            raise ValueError("%x is not jal %x" % (va, target))
        struct.pack_into("<I", eb.d, eb.foff(va), jal_word(hook))
    return bytes(eb.d), len(words), prev_draw, labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("eboot")
    ap.add_argument("out")
    a = ap.parse_args()
    data, n, prev, labels = patch(open(a.eboot, "rb").read())
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "wb").write(data)
    print("lyrics: %d words at %x (set %x, decode %x, draw %x -> then %x), data at %x"
          % (n, CAVE[0], labels["set_hook"], labels["dec_hook"], labels["draw_hook"], prev, DATA))


if __name__ == "__main__":
    main()
