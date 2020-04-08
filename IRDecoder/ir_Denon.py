# -*- coding: utf-8 -*-

# Copyright 2016 Massimiliano Pinto
# Copyright 2017 David Conran

from .IRrecv import *
from .IRsend import *

# Original Denon support added by https:#github.com/csBlueChip
# Ported over by Massimiliano Pinto

# Constants
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_Denon.cpp
kDenonTick = 263
kDenonHdrMarkTicks = 1
kDenonHdrMark = kDenonHdrMarkTicks * kDenonTick
kDenonHdrSpaceTicks = 3
kDenonHdrSpace = kDenonHdrSpaceTicks * kDenonTick
kDenonBitMarkTicks = 1
kDenonBitMark = kDenonBitMarkTicks * kDenonTick
kDenonOneSpaceTicks = 7
kDenonOneSpace = kDenonOneSpaceTicks * kDenonTick
kDenonZeroSpaceTicks = 3
kDenonZeroSpace = kDenonZeroSpaceTicks * kDenonTick
kDenonMinCommandLengthTicks = 510
kDenonMinGapTicks = (
    kDenonMinCommandLengthTicks -
    (kDenonHdrMarkTicks + kDenonHdrSpaceTicks +
     kDenonBits * (kDenonBitMarkTicks + kDenonOneSpaceTicks) +
     kDenonBitMarkTicks)
)
kDenonMinGap = kDenonMinGapTicks * kDenonTick
kDenonManufacturer = 0x2A4C


# Send a Denon message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kDenonBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: BETA / Should be working.
#
# Notes:
#   Some Denon devices use a Kaseikyo/Panasonic 48-bit format
#   Others use the Sharp protocol.
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_Denon.cpp
#   http:#assets.denon.com/documentmaster/us/denon%20master%20ir%20hex.xls
def sendDenon(self, data, nbits, repeat):
    if nbits >= kPanasonicBits:  # Is this really Panasonic?
        self.sendPanasonic64(data, nbits, repeat)
    elif nbits == kDenonLegacyBits:
        # Support legacy (broken) calls of sendDenon().
        self.sendSharpRaw(data & (~0x2000), nbits + 1, repeat)
    else:
        self.sendSharpRaw(data, nbits, repeat)


IRsend.sendDenon = sendDenon


# Decode a Denon message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Expected nr. of data bits. (Typically kDenonBits)
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Should work fine.
#
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_Denon.cpp
def decodeDenon(self, results, nbits, strict):
    # Compliance
    if strict and nbits not in (kDenonBits, kDenon48Bits, kDenonLegacyBits):
        return False

    # Denon uses the Sharp & Panasonic(Kaseikyo) protocol for some
    # devices, so check for those first.
    # It is not exactly like Sharp's protocols, but close enough.
    # e.g. The expansion bit is not set for Denon vs. set for Sharp.
    # Ditto for Panasonic, it's the same except for a different
    # manufacturer code.

    if (
        not self.decodeSharp(results, nbits, True, False) and
        not self.decodePanasonic(results, nbits, True, kDenonManufacturer)
    ):
        # We couldn't decode it as expected, so try the old legacy method.
        # NOTE: I don't think this following protocol actually exists.
        #       Looks like a partial version of the Sharp protocol.
        if strict and nbits != kDenonLegacyBits:
            return False

        data = 0
        offset = kStartOffset

        # Match Header + Data + Footer
        if not self.match_generic(
            results.rawbuf + offset,
            data,
            results.rawlen - offset,
            nbits,
            kDenonHdrMark,
            kDenonHdrSpace,
            kDenonBitMark,
            kDenonOneSpace,
            kDenonBitMark,
            kDenonZeroSpace,
            kDenonBitMark,
            0,
            False
        ):
            return False

        # Success
        results.bits = nbits
        results.value = data
        results.address = 0
        results.command = 0
        # Legacy decode.

    # Compliance
    if strict and nbits != results.bits:
        return False

    # Success
    results.decode_type = DENON
    return True


IRrecv.decodeDenon = decodeDenon
