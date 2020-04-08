# -*- coding: utf-8 -*-

# Copyright 2018 David Conran

# Supports:
#   Brand: Carrier/Surrey,  Model: 42QG5A55970 remote
#   Brand: Carrier/Surrey,  Model: 619EGX0090E0 A/C
#   Brand: Carrier/Surrey,  Model: 619EGX0120E0 A/C
#   Brand: Carrier/Surrey,  Model: 619EGX0180E0 A/C
#   Brand: Carrier/Surrey,  Model: 619EGX0220E0 A/C
#   Brand: Carrier/Surrey,  Model: 53NGK009/012 Inverter

from .IRrecv import *
from .IRutils import *
from .IRsend import *

# Constants
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/385
kCarrierAcHdrMark = 8532
kCarrierAcHdrSpace = 4228
kCarrierAcBitMark = 628
kCarrierAcOneSpace = 1320
kCarrierAcZeroSpace = 532
kCarrierAcGap = 20000


# Send a Carrier HVAC formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The bit size of the message being sent. typically kCarrierAcBits.
#   repeat: The number of times the message is to be repeated.
#
# Status: BETA / Appears to work on real devices.
#
def sendCarrierAC(self, data, nbits, repeat):
    temp_data = data

    for _ in range(repeat + 1):
        # Carrier sends the data block three times. normal + inverted + normal.
        for __ in range(3):
            self.send_generic(
                kCarrierAcHdrMark,
                kCarrierAcHdrSpace,
                kCarrierAcBitMark,
                kCarrierAcOneSpace,
                kCarrierAcBitMark,
                kCarrierAcZeroSpace,
                kCarrierAcBitMark,
                kCarrierAcGap,
                temp_data,
                nbits,
                38,
                True,
                0,
                kDutyDefault
            )
        temp_data = invertBits(temp_data, nbits)


IRsend.sendCarrierAC = sendCarrierAC


# Decode the supplied Carrier HVAC message.
# Carrier HVAC messages contain only 32 bits, but it is sent three(3) times.
# i.e. normal + inverted + normal
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kCarrierAcBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Untested.
#
def decodeCarrierAC(self, results, nbits, strict):
    if results.rawlen < ((2 * nbits + kHeader + kFooter) * 3) - 1:
        return False  # Can't possibly be a valid Carrier message.
    if strict and nbits != kCarrierAcBits:
        return False  # We expect Carrier to be 32 bits of message.

    data = 0
    offset = kStartOffset

    for ii in range(3):
        prev_data = data
        # Match Header + Data + Footer
        used = self.match_generic(
            results.rawbuf + offset,
            data,
            results.rawlen - offset,
            nbits,
            kCarrierAcHdrMark,
            kCarrierAcHdrSpace,
            kCarrierAcBitMark,
            kCarrierAcOneSpace,
            kCarrierAcBitMark,
            kCarrierAcZeroSpace,
            kCarrierAcBitMark,
            kCarrierAcGap,
            True
        )
        if not used:
            return False

        offset += used

        # Compliance.
        if strict:
            # Check if the data is an inverted copy of the previous data.
            if ii > 0 and prev_data != invertBits(data, nbits):
                return False

    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = CARRIER_AC
    results.address = data >> 16
    results.command = data & 0xFFFF
    return True


IRrecv.decodeCarrierAC = decodeCarrierAC
