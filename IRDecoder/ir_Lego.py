# -*- coding: utf-8 -*-

# Copyright 2019 David Conran

from .IRrecv import *
from .IRsend import *
from .IRutils import *
# LEGO
# (LEGO is a Registrated Trademark of the Lego Group.)
#
# Supports:
#   Brand: LEGO Power Functions,  Model: IR Receiver
#
# Ref:
# - https:#github.com/crankyoldgit/IRremoteESP8266/issues/641
# - https:#github.com/crankyoldgit/IRremoteESP8266/files/2974525/LEGO_Power_Functions_RC_v120.pdf

# Constants
kLegoPfBitMark = 158
kLegoPfHdrSpace = 1026
kLegoPfZeroSpace = 263
kLegoPfOneSpace = 553
kLegoPfMinCommandLength = 16000  # 16ms


# Send a LEGO Power Functions message.
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kLegoPfBits.
#   repeat: Nr. of additional times the message is to be sent.
#           Note: Non-zero repeats results in at least 5 messages per spec.
#
# Status: Beta / Should work.
def sendLegoPf(data, nbits, repeat):
    channelid = ((data >> (nbits - 4)) & 0b11) + 1
    if repeat:
        # We are in repeat mode.
        # Spec says a pause before transmittion.
        if channelid < 4:
            space((4 - channelid) * kLegoPfMinCommandLength)

        # Spec says there are a minimum of 5 message repeats.
        for r in range(max(repeat, 5)):
            # Lego has a special repeat mode which repeats a message with varying
            # start to start times.
            sendGeneric(
                kLegoPfBitMark,
                kLegoPfHdrSpace,
                kLegoPfBitMark,
                kLegoPfOneSpace,
                kLegoPfBitMark,
                kLegoPfZeroSpace,
                kLegoPfBitMark,
                kLegoPfHdrSpace,
                (5 if r < 2 else 6 + 2 * channelid) * kLegoPfMinCommandLength,
                data,
                nbits,
                38000,
                True,
                0,
                kDutyDefault)
    else:  # No repeat, just a simple message.
        sendGeneric(
            kLegoPfBitMark,
            kLegoPfHdrSpace,
            kLegoPfBitMark,
            kLegoPfOneSpace,
            kLegoPfBitMark,
            kLegoPfZeroSpace,
            kLegoPfBitMark,
            kLegoPfHdrSpace,
            kLegoPfMinCommandLength * 5,
            data,
            nbits,
            38000,
            True,
            0,
            kDutyDefault
        )


# Decode the supplied LEGO Power Functions message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kLegoPfBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Untested.
def decodeLegoPf(results, nbits, strict):
    # Check if can possibly be a valid LEGO message.
    if results.rawlen < 2 * nbits + kHeader + kFooter - 1:
        return False

    if strict and nbits != kLegoPfBits:
        return False  # Not what is expected

    data = 0
    offset = kStartOffset

    # Match Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kLegoPfBitMark,
        kLegoPfHdrSpace,
        kLegoPfBitMark,
        kLegoPfOneSpace,
        kLegoPfBitMark,
        kLegoPfZeroSpace,
        kLegoPfBitMark,
        kLegoPfMinCommandLength,
        True
    ):
        return False

    # Compliance
    if strict:
        # Verify the Longitudinal Redundancy Check (LRC)
        lrc_data = data
        lrc = 0xF
        for i in range(4):
            lrc ^= (lrc_data & 0xF)
            lrc_data >>= 4

        if lrc:
            return False

    # Success
    results.decode_type = LEGOPF
    results.bits = nbits
    results.value = data
    results.address = ((data >> (nbits - 4)) & 0b11) + 1  # Channel Id
    results.command = (data >> 4) & 0xFF  # Stuff between Channel Id and LRC.
    return True
