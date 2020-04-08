# -*- coding: utf-8 -*-
# Copyright 2015 Kristian Lauszus
# Copyright 2017 David Conran
# Copyright 2020 Kevin Schlosser

# JVC originally added by Kristian Lauszus
# (Thanks to zenwheel and other people at the original blog post)

from .IRrecv import *
from .IRutils import *
from .IRsend import *
from .IRtimer import *

# Constants
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
kJvcTick = 75
kJvcHdrMarkTicks = 112
kJvcHdrMark = kJvcHdrMarkTicks * kJvcTick
kJvcHdrSpaceTicks = 56
kJvcHdrSpace = kJvcHdrSpaceTicks * kJvcTick
kJvcBitMarkTicks = 7
kJvcBitMark = kJvcBitMarkTicks * kJvcTick
kJvcOneSpaceTicks = 23
kJvcOneSpace = kJvcOneSpaceTicks * kJvcTick
kJvcZeroSpaceTicks = 7
kJvcZeroSpace = kJvcZeroSpaceTicks * kJvcTick
kJvcRptLengthTicks = 800
kJvcRptLength = kJvcRptLengthTicks * kJvcTick
kJvcMinGapTicks = (
    kJvcRptLengthTicks -
    (kJvcHdrMarkTicks + kJvcHdrSpaceTicks +
     kJvcBits * (kJvcBitMarkTicks + kJvcOneSpaceTicks) + kJvcBitMarkTicks)
)
kJvcMinGap = kJvcMinGapTicks * kJvcTick


# Send a JVC message.
#
# Args:
#   data:   The contents of the command you want to send.
#   nbits:  The bit size of the command being sent. (kJvcBits)
#   repeat: The number of times you want the command to be repeated.
#
# Status: STABLE.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
def sendJVC(self, data, nbits, repeat):
    # Set 38kHz IR carrier frequency & a 1/3 (33%) duty cycle.
    self.enable_ir_out(38, 33)

    usecs = IRtimer()
    # Header
    # Only sent for the first message.
    self.mark(kJvcHdrMark)
    self.space(kJvcHdrSpace)

    # We always send the data & footer at least once, hence '<= repeat'.
    for _ in range(repeat + 1):
        self.send_generic(
            0,
            0,  # No Header
            kJvcBitMark,
            kJvcOneSpace,
            kJvcBitMark,
            kJvcZeroSpace,
            kJvcBitMark,
            kJvcMinGap,
            data,
            nbits,
            38,
            True,
            0,  # Repeats are handles elsewhere.
            33
        )

        # Wait till the end of the repeat time window before we send another code.
        elapsed = usecs.elapsed()
        # Avoid potential unsigned integer underflow.
        # e.g. when elapsed > kJvcRptLength.
        if elapsed < kJvcRptLength:
            self.space(kJvcRptLength - elapsed)
            usecs.reset()


IRsend.sendJVC = sendJVC


# Calculate the raw JVC data based on address and command.
#
# Args:
#   address: An 8-bit address value.
#   command: An 8-bit command value.
# Returns:
#   A raw JVC message.
#
# Status: BETA / Should work fine.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
def encodeJVC(_, address, command):
    return reverseBits((command << 8) | address, 16)


IRsend.encodeJVC = encodeJVC


# Decode the supplied JVC message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits of data to expect. Typically kJvcBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE
#
# Note:
#   JVC repeat codes don't have a header.
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
def decodeJVC(self, results, nbits, strict):
    if strict and nbits != kJvcBits:
        return False  # Must be called with the correct nr. of bits.

    if results.rawlen < 2 * nbits + kFooter - 1:
        return False  # Can't possibly be a valid JVC message.

    data = 0
    offset = kStartOffset
    isRepeat = True

    # Header
    # (Optional as repeat codes don't have the header)
    if self.match_mark(results.rawbuf[offset], kJvcHdrMark):
        isRepeat = False
        offset += 1
        if results.rawlen < 2 * nbits + 4:
            return False  # Can't possibly be a valid JVC message with a header.

        offset += 1
        if not self.match_space(results.rawbuf[offset], kJvcHdrSpace):
            return False

    # Data + Footer
    if not self.match_generic(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        0,
        0,
        kJvcBitMark,
        kJvcOneSpace,
        kJvcBitMark,
        kJvcZeroSpace,
        kJvcBitMark,
        kJvcMinGap,
        True
    ):
        return False

    # Success
    results.decode_type = JVC
    results.bits = nbits
    results.value = data
    # command & address are transmitted LSB first, so we need to reverse them.
    results.address = reverseBits(data >> 8, 8)    # The first 8 bits sent.
    results.command = reverseBits(data & 0xFF, 8)  # The last 8 bits sent.
    results.repeat = isRepeat
    return True


IRrecv.decodeJVC = decodeJVC
