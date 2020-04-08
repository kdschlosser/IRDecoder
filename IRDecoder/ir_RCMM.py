# -*- coding: utf-8 -*-

# Copyright 2017 David Conran

# Send & decode support for Phillips RC-MM added by David Conran

# Supports:
#   Brand: Microsoft,  Model: XBOX 360

from .IRrecv import *
from .IRsend import *
from .IRtimer import *
from .IRutils import *

# Constants
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/rcmm.php
kRcmmTick = 28  # Technically it would be 27.777*
kRcmmHdrMarkTicks = 15
kRcmmHdrMark = 416
kRcmmHdrSpaceTicks = 10
kRcmmHdrSpace = 277
kRcmmBitMarkTicks = 6
kRcmmBitMark = 166
kRcmmBitSpace0Ticks = 10
kRcmmBitSpace0 = 277
kRcmmBitSpace1Ticks = 16
kRcmmBitSpace1 = 444
kRcmmBitSpace2Ticks = 22
kRcmmBitSpace2 = 611
kRcmmBitSpace3Ticks = 28
kRcmmBitSpace3 = 777
kRcmmRptLengthTicks = 992
kRcmmRptLength = 27778
kRcmmMinGapTicks = 120
kRcmmMinGap = 3360
# Use a tolerance of +/-10% when matching some data spaces.
kRcmmTolerance = 10
kRcmmExcess = 50


# Send a Philips RC-MM packet.
#
# Args:
#   data: The data we want to send. MSB first.
#   nbits: The number of bits of data to send. (Typically 12, 24, or 32[Nokia])
#   repeat: The nr. of times the message should be sent.
#
# Status:  BETA / Should be working.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/rcmm.php
def sendRCMM(data, nbits, repeat):
    # Set 36kHz IR carrier frequency & a 1/3 (33%) duty cycle.
    enableIROut(36, 33)
    usecs = IRtimer()

    for r in range(repeat + 1):
        usecs.reset()
        # Header
        mark(kRcmmHdrMark)
        space(kRcmmHdrSpace)
        # Data
        mask = 0b11 << (nbits - 2)
        # RC-MM sends data 2 bits at a time.
        for i in range(nbits, -1, -2):
            mark(kRcmmBitMark)
            # Grab the next Most Significant Bits to send.
            switch = (data & mask) >> (i - 2)
            if switch == 0b00:
                space(kRcmmBitSpace0)
            elif switch == 0b01:
                space(kRcmmBitSpace1)
            elif switch == 0b10:
                space(kRcmmBitSpace2)
            elif switch == 0b11:
                space(kRcmmBitSpace3)

            mask >>= 2

        # Footer
        mark(kRcmmBitMark)
        # Protocol requires us to wait at least kRcmmRptLength usecs from the
        # start or kRcmmMinGap usecs.
        space(max(kRcmmRptLength - usecs.elapsed(), kRcmmMinGap))


# Decode a Philips RC-MM packet (between 12 & 32 bits) if possible.
# Places successful decode information in the results pointer.
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion. Typically kRCMMBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status:  BETA / Should be working.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/rcmm.php
def decodeRCMM(results, nbits, strict):
    data = 0
    offset = kStartOffset

    if results.rawlen <= 4:
        return False  # Not enough entries to ever be RCMM.

    # Calc the maximum size in bits, the message can be, or that we can accept.
    maxBitSize = min(results.rawlen - 5, 64)
    # Compliance
    if strict:
        # Technically the spec says bit sizes should be 12 xor 24. however
        # 32 bits has been seen from a device. We are going to assume
        # 12 <= bits <= 32 is the 'required' bit length for the spec.
        if maxBitSize < 12 or maxBitSize > 32:
            return False

        if maxBitSize < nbits:
            return False  # Short cut, we can never reach the expected nr. of bits.

    # Header decode
    if not matchMark(results.rawbuf[offset], kRcmmHdrMark):
        return False

    # Calculate how long the common tick time is based on the header mark.
    offset += 1

    m_tick = results.rawbuf[offset] * kRawTick / kRcmmHdrMarkTicks
    if not matchSpace(results.rawbuf[offset], kRcmmHdrSpace):
        return False

    offset += 1
    # Calculate how long the common tick time is based on the header space.
    s_tick = results.rawbuf[offset] * kRawTick / kRcmmHdrSpaceTicks

    # Data decode
    # RC-MM has two bits of data per mark/space pair.
    actualBits = 0
    while actualBits < maxBitSize:
        offset += 1
        if not match(results.rawbuf[offset], kRcmmBitMarkTicks * m_tick):
            return False

        data <<= 2
        # Use non-default tolerance & excess for matching some of the spaces as the
        # defaults are too generous and causes mis-matches in some cases.
        if match(results.rawbuf[offset], kRcmmBitSpace0Ticks * s_tick):
            data += 0
        elif match(results.rawbuf[offset], kRcmmBitSpace1Ticks * s_tick):
            data += 1
        elif match(results.rawbuf[offset], kRcmmBitSpace2Ticks * s_tick, kRcmmTolerance):
            data += 2
        elif match(results.rawbuf[offset], kRcmmBitSpace3Ticks * s_tick, kRcmmTolerance):
            data += 3
        else:
            return False

        actualBits += 2
        offset += 1

    offset += 1
    # Footer decode
    if not match(results.rawbuf[offset], kRcmmBitMarkTicks * m_tick):
        return False

    if offset < results.rawlen and not matchAtLeast(results.rawbuf[offset], kRcmmMinGapTicks * s_tick):
        return False

    # Compliance
    if strict and actualBits != nbits:
        return False

    # Success
    results.value = data
    results.decode_type = RCMM
    results.bits = actualBits
    results.address = 0
    results.command = 0
    return True
