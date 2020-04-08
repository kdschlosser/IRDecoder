# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2016 marcosamarinho
# Copyright 2017 David Conran

# Sony Remote Emulation

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Sony originally added from https:#github.com/shirriff/Arduino-IRremote/
# Updates from marcosamarinho

# Constants
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sirc.php
kSonyTick = 200
kSonyHdrMarkTicks = 12
kSonyHdrMark = kSonyHdrMarkTicks * kSonyTick
kSonySpaceTicks = 3
kSonySpace = kSonySpaceTicks * kSonyTick
kSonyOneMarkTicks = 6
kSonyOneMark = kSonyOneMarkTicks * kSonyTick
kSonyZeroMarkTicks = 3
kSonyZeroMark = kSonyZeroMarkTicks * kSonyTick
kSonyRptLengthTicks = 225
kSonyRptLength = kSonyRptLengthTicks * kSonyTick
kSonyMinGapTicks = 50
kSonyMinGap = kSonyMinGapTicks * kSonyTick


# Send a Sony/SIRC(Serial Infra-Red Control) message.
#
# Args:
#   data: message to be sent.
#   nbits: Nr. of bits of the message to be sent.
#   repeat: Nr. of additional times the message is to be sent. (Default: 2)
#
# Status: STABLE / Known working.
#
# Notes:
#   sendSony() should typically be called with repeat=2 as Sony devices
#   expect the message to be sent at least 3 times.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sirc.php
def sendSony(data, nbits, repeat):
    sendGeneric(
        kSonyHdrMark,
        kSonySpace,
        kSonyOneMark,
        kSonySpace,
        kSonyZeroMark,
        kSonySpace,
        0,  # No Footer mark.
        kSonyMinGap,
        kSonyRptLength,
        data,
        nbits,
        40,
        True,
        repeat,
        33
    )


# Convert Sony/SIRC command, address, & extended bits into sendSony format.
# Args:
#   nbits:    Sony protocol bit size.
#   command:  Sony command bits.
#   address:  Sony address bits.
#   extended: Sony extended bits.
# Returns:
#   A sendSony compatible data message.
#
# Status: BETA / Should be working.
def encodeSony(nbits, command, address, extended):
    if nbits == 12:
        result = address & 0x1F
    elif nbits == 15:
        result = address & 0xFF
    elif nbits == 20:
        result = address & 0x1F
        result |= (extended & 0xFF) << 5
    else:
        return 0  # This is not an expected Sony bit size/protocol.

    result = (result << 7) | (command & 0x7F)  # All sizes have 7 command bits.
    return reverseBits(result, nbits)  # sendSony uses reverse ordered bits.


# Decode the supplied Sony/SIRC message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Should be working. strict mode is ALPHA / Untested.
#
# Notes:
#   SONY protocol, SIRC (Serial Infra-Red Control) can be 12,15,20 bits long.
# Ref:
# http:#www.sbprojects.com/knowledge/ir/sirc.php
def decodeSony(results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader - 1:
        return False  # Message is smaller than we expected.

    # Compliance
    if strict and nbits not in (12, 15, 20):
        return False

    data = 0
    offset = kStartOffset
    actualBits = 0

    # Header
    if not matchMark(results.rawbuf[offset], kSonyHdrMark):
        return False

    offset += 1
    # Calculate how long the common tick time is based on the header mark.
    tick = results.rawbuf[offset] * kRawTick / kSonyHdrMarkTicks

    # Data

    while offset < results.rawlen - 1:
        # The gap after a Sony packet for a repeat should be kSonyMinGap according
        # to the spec.
        if matchAtLeast(results.rawbuf[offset], kSonyMinGapTicks * tick):
            break

        offset += 1
        if not matchSpace(results.rawbuf[offset], kSonySpaceTicks * tick):
            return False

        if matchMark(results.rawbuf[offset], kSonyOneMarkTicks * tick):
            data = (data << 1) | 1
        elif matchMark(results.rawbuf[offset], kSonyZeroMarkTicks * tick):
            data <<= 1
        else:
            return False

        actualBits += 1
        offset += 1

    # No Footer for Sony.

    # Compliance
    if strict and actualBits != nbits:
        return False  # We got the wrong number of bits.

    # Success
    results.bits = actualBits
    results.value = data
    results.decode_type = SONY
    # Message comes in LSB first. Convert ot MSB first.
    data = reverseBits(data, actualBits)
    # Decode the address & command from raw decode value.
    if actualBits in (12, 15):
        results.command = data & 0x7F  # Bits 0-6
        results.address = data >> 7    # Bits 7-14
    elif actualBits == 20:
        results.command = (data & 0x7F) + ((data >> 12) << 7)  # Bits 0-6,12-19
        results.address = (data >> 7) & 0x1F                   # Bits 7-11
    else:  # Shouldn't happen, but just in case.
        results.address = 0
        results.command = 0

    return True
