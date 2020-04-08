# -*- coding: utf-8 -*-

# Copyright 2019 David Conran (crankyoldgit)
# Support for an IR controlled Robot Toilet

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Supports:
#   Brand: Lixil,  Model: Inax DT-BA283 Toilet

# Documentation:
#   https:#www.lixil-manual.com/GCW-1365-16050/GCW-1365-16050.pdf

# Constants
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/706
kInaxTick = 500
kInaxHdrMark = 9000
kInaxHdrSpace = 4500
kInaxBitMark = 560
kInaxOneSpace = 1675
kInaxZeroSpace = kInaxBitMark
kInaxMinGap = 40000


# Send a Inax Toilet formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The bit size of the message being sent. typically kInaxBits.
#   repeat: The number of times the message is to be repeated.
#
# Status: BETA / Should be working.
#
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/706
def sendInax(data, nbits, repeat):
    sendGeneric(
        kInaxHdrMark,
        kInaxHdrSpace,
        kInaxBitMark,
        kInaxOneSpace,
        kInaxBitMark,
        kInaxZeroSpace,
        kInaxBitMark,
        kInaxMinGap,
        data,
        nbits,
        38,
        True,
        repeat,
        kDutyDefault
    )


# Decode the supplied Inax Toilet message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kInaxBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Stable / Known working.
#
def decodeInax(results, nbits, strict):
    if strict and nbits != kInaxBits:
        return False  # We expect Inax to be a certain sized message.

    data = 0
    offset = kStartOffset

    # Match Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kInaxHdrMark,
        kInaxHdrSpace,
        kInaxBitMark,
        kInaxOneSpace,
        kInaxBitMark,
        kInaxZeroSpace,
        kInaxBitMark,
        kInaxMinGap,
        True
    ):
        return False

    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = INAX
    results.command = 0
    results.address = 0
    return True
