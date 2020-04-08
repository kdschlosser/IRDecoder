# -*- coding: utf-8 -*-

# Copyright 2018 David Conran
# G.I. Cable

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Ref:
#   https:#github.com/cyborg5/IRLib2/blob/master/IRLibProtocols/IRLib_P09_GICable.h
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/447

# Constants
kGicableHdrMark = 9000
kGicableHdrSpace = 4400
kGicableBitMark = 550
kGicableOneSpace = 4400
kGicableZeroSpace = 2200
kGicableRptSpace = 2200
kGicableMinCommandLength = 99600
kGicableMinGap = (
    kGicableMinCommandLength -
    (kGicableHdrMark + kGicableHdrSpace +
     kGicableBits * (kGicableBitMark + kGicableOneSpace) + kGicableBitMark)
)


# Send a raw G.I. Cable formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The number of bits of the message to be sent.
#           Typically kGicableBits.
#   repeat: The number of times the command is to be repeated.
#
# Status: Alpha / Untested.
#
# Ref:
def sendGICable(data, nbits, repeat):
    sendGeneric(
        kGicableHdrMark,
        kGicableHdrSpace,
        kGicableBitMark,
        kGicableOneSpace,
        kGicableBitMark,
        kGicableZeroSpace,
        kGicableBitMark,
        kGicableMinGap,
        kGicableMinCommandLength,
        data,
        nbits,
        39,
        True,
        0,  # Repeats are handled later.
        50
    )
    # Message repeat sequence.
    if repeat:
        sendGeneric(
            kGicableHdrMark,
            kGicableRptSpace,
            0,
            0,
            0,
            0,  # No actual data sent.
            kGicableBitMark,
            kGicableMinGap,
            kGicableMinCommandLength,
            0,
            0,  # No data to be sent.
            39,
            True,
            repeat - 1,
            50
        )


# Decode the supplied G.I. Cable message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kGicableBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Not tested against a real device.
def decodeGICable(results, nbits, strict):
    if strict and nbits != kGicableBits:
        return False  # Not strictly an GICABLE message.

    data = 0
    offset = kStartOffset
    # Match Header + Data + Footer

    used = matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kGicableHdrMark,
        kGicableHdrSpace,
        kGicableBitMark,
        kGicableOneSpace,
        kGicableBitMark,
        kGicableZeroSpace,
        kGicableBitMark,
        kGicableMinGap,
        True
    )
    if not used:
        return False

    offset += used
    # Compliance
    if strict:
        # We expect a repeat frame.
        offset += 1
        if not matchMark(results.rawbuf[offset], kGicableHdrMark):
            return False

        offset += 1
        if not matchSpace(results.rawbuf[offset], kGicableRptSpace):
            return False

        offset += 1
        if not matchMark(results.rawbuf[offset], kGicableBitMark):
            return False

    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = GICABLE
    results.command = 0
    results.address = 0
    return True
