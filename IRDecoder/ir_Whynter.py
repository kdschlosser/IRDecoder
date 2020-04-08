# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2017 David Conran

# Whynter A/C ARC-110WD added by Francesco Meschia
# Whynter originally added from https:#github.com/shirriff/Arduino-IRremote/

# Supports:
#   Brand: Whynter,  Model: ARC-110WD A/C

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Constants

kWhynterTick = 50
kWhynterHdrMarkTicks = 57
kWhynterHdrMark = kWhynterHdrMarkTicks * kWhynterTick
kWhynterHdrSpaceTicks = 57
kWhynterHdrSpace = kWhynterHdrSpaceTicks * kWhynterTick
kWhynterBitMarkTicks = 15
kWhynterBitMark = kWhynterBitMarkTicks * kWhynterTick
kWhynterOneSpaceTicks = 43
kWhynterOneSpace = kWhynterOneSpaceTicks * kWhynterTick
kWhynterZeroSpaceTicks = 15
kWhynterZeroSpace = kWhynterZeroSpaceTicks * kWhynterTick
kWhynterMinCommandLengthTicks = 2160  # Totally made up value.
kWhynterMinCommandLength = kWhynterMinCommandLengthTicks * kWhynterTick
kWhynterMinGapTicks = (
    kWhynterMinCommandLengthTicks -
    (2 * (kWhynterBitMarkTicks + kWhynterZeroSpaceTicks) +
     kWhynterBits * (kWhynterBitMarkTicks + kWhynterOneSpaceTicks))
)
kWhynterMinGap = kWhynterMinGapTicks * kWhynterTick


# Send a Whynter message.
#
# Args:
#   data: message to be sent.
#   nbits: Nr. of bits of the message to be sent.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: STABLE
#
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_Whynter.cpp
def sendWhynter(data, nbits, repeat):
    # Set IR carrier frequency
    enableIROut(38)

    for i in range(repeat + 1):
        # (Pre-)Header
        mark(kWhynterBitMark)
        space(kWhynterZeroSpace)
        sendGeneric(
            kWhynterHdrMark,
            kWhynterHdrSpace,
            kWhynterBitMark,
            kWhynterOneSpace,
            kWhynterBitMark,
            kWhynterZeroSpace,
            kWhynterBitMark,
            kWhynterMinGap,
            kWhynterMinCommandLength - (kWhynterBitMark + kWhynterZeroSpace),
            data,
            nbits,
            38,
            True,
            0,  # Repeats are already handled.
            50
        )


# Decode the supplied Whynter message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA  Strict mode is ALPHA.
#
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_Whynter.cpp
def decodeWhynter(results, nbits, strict):
    if results.rawlen < 2 * nbits + 2 * kHeader + kFooter - 1:
        return False  # We don't have enough entries to possibly match.

    # Compliance
    if strict and nbits != kWhynterBits:
        return False  # Incorrect nr. of bits per spec.

    offset = kStartOffset
    data = 0
    # Pre-Header
    # Sequence begins with a bit mark and a zero space.
    offset += 1
    if not matchMark(results.rawbuf[offset], kWhynterBitMark):
        return False
    offset += 1
    if not matchSpace(results.rawbuf[offset], kWhynterZeroSpace):
        return False

    # Match Main Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kWhynterHdrMark,
        kWhynterHdrSpace,
        kWhynterBitMark,
        kWhynterOneSpace,
        kWhynterBitMark,
        kWhynterZeroSpace,
        kWhynterBitMark,
        kWhynterMinGap,
        True
    ):
        return False

    # Success
    results.decode_type = WHYNTER
    results.bits = nbits
    results.value = data
    results.address = 0
    results.command = 0
    return True
