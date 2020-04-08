# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2017 David Conran

# Nikai

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Constants
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/309
kNikaiTick = 500
kNikaiHdrMarkTicks = 8
kNikaiHdrMark = kNikaiHdrMarkTicks * kNikaiTick
kNikaiHdrSpaceTicks = 8
kNikaiHdrSpace = kNikaiHdrSpaceTicks * kNikaiTick
kNikaiBitMarkTicks = 1
kNikaiBitMark = kNikaiBitMarkTicks * kNikaiTick
kNikaiOneSpaceTicks = 2
kNikaiOneSpace = kNikaiOneSpaceTicks * kNikaiTick
kNikaiZeroSpaceTicks = 4
kNikaiZeroSpace = kNikaiZeroSpaceTicks * kNikaiTick
kNikaiMinGapTicks = 17
kNikaiMinGap = kNikaiMinGapTicks * kNikaiTick


# Send a Nikai TV formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The bit size of the message being sent. typically kNikaiBits.
#   repeat: The number of times the message is to be repeated.
#
# Status: STABLE / Working.
#
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/309
def sendNikai(data, nbits, repeat):
    sendGeneric(
        kNikaiHdrMark,
        kNikaiHdrSpace,
        kNikaiBitMark,
        kNikaiOneSpace,
        kNikaiBitMark,
        kNikaiZeroSpace,
        kNikaiBitMark,
        kNikaiMinGap,
        data,
        nbits,
        38,
        True,
        repeat,
        33
    )


# Decode the supplied Nikai message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kNikaiBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Working.
#
def decodeNikai(results, nbits, strict):
    if strict and nbits != kNikaiBits:
        return False  # We expect Nikai to be a certain sized message.

    data = 0
    offset = kStartOffset

    # Match Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kNikaiHdrMark,
        kNikaiHdrSpace,
        kNikaiBitMark,
        kNikaiOneSpace,
        kNikaiBitMark,
        kNikaiZeroSpace,
        kNikaiBitMark,
        kNikaiMinGap,
        True
    ):
        return False

    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = NIKAI
    results.command = 0
    results.address = 0
    return True
