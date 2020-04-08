# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2017, 2018 David Conran
# Copyright 2018 Kamil Palczewski
# Copyright 2019 s-hadinger

# Pioneer remote emulation

from .IRrecv import *
from .IRsend import *
from .IRutils import *


# Constants
# Ref:
#  http:#www.adrian-kingston.com/IRFormatPioneer.htm
kPioneerTick = 534
kPioneerHdrMarkTicks = 16
kPioneerHdrMark = kPioneerHdrMarkTicks * kPioneerTick
kPioneerHdrSpaceTicks = 8
kPioneerHdrSpace = kPioneerHdrSpaceTicks * kPioneerTick
kPioneerBitMarkTicks = 1
kPioneerBitMark = kPioneerBitMarkTicks * kPioneerTick
kPioneerOneSpaceTicks = 3
kPioneerOneSpace = kPioneerOneSpaceTicks * kPioneerTick
kPioneerZeroSpaceTicks = 1
kPioneerZeroSpace = kPioneerZeroSpaceTicks * kPioneerTick
kPioneerMinCommandLengthTicks = 159
kPioneerMinCommandLength = kPioneerMinCommandLengthTicks * kPioneerTick
kPioneerMinGapTicks = 47
kPioneerMinGap = kPioneerMinGapTicks * kPioneerTick


# Send a raw Pioneer formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The number of bits of the message to be sent.
#           Typically kPioneerBits.
#   repeat: The number of times the command is to be repeated.
#
# Status: BETA / Expected to be working.
#
# Ref:
#  http:#adrian-kingston.com/IRFormatPioneer.htm
def sendPioneer(data, nbits, repeat):
    # If nbits is to big, abort.
    if nbits > len(data) * 8:
        return

    for r in range(repeat + 1):
        # don't use NEC repeat but repeat the whole sequence
        if nbits > 32:
            sendGeneric(
                kPioneerHdrMark,
                kPioneerHdrSpace,
                kPioneerBitMark,
                kPioneerOneSpace,
                kPioneerBitMark,
                kPioneerZeroSpace,
                kPioneerBitMark,
                kPioneerMinGap,
                kPioneerMinCommandLength,
                data >> 32,
                nbits - 32,
                40,
                True,
                0,
                33
            )

    sendGeneric(
        kPioneerHdrMark,
        kPioneerHdrSpace,
        kPioneerBitMark,
        kPioneerOneSpace,
        kPioneerBitMark,
        kPioneerZeroSpace,
        kPioneerBitMark,
        kPioneerMinGap,
        kPioneerMinCommandLength,
        data,
        32 if nbits > 32 else nbits,
        40,
        True,
        0,
        33
    )


# Calculate the raw Pioneer data code based on two NEC sub-codes
# Args:
#   address A 16-bit "published" NEC value.
#   command: A 16-bit "published" NEC value.
# Returns:
#   A raw 64-bit Pioneer message code.
#
# Status: BETA / Expected to work.
#
# Note:
#   Address & Command can be take from a decode result OR from the spreadsheets
#   located at:
#     https:#www.pioneerelectronics.com/PUSA/Support/Home-Entertainment-Custom-Install/IR+Codes/A+V+Receivers
#   where the first part is considered the address,
#   and the second the command.
#   e.g.
#   "A556+AF20" is an Address of 0xA556 & a Command of 0xAF20.
def encodePioneer(address, command):
    return ((encodeNEC(address >> 8, address & 0xFF)) << 32) | encodeNEC(command >> 8, command & 0xFF)


# Decode the supplied Pioneer message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kPioneerBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Should be working. (Self decodes & real examples)
#
def decodePioneer(results, nbits, strict):
    if results.rawlen < 2 * (nbits + kHeader + kFooter) - 1:
        return False  # Can't possibly be a valid Pioneer message.

    if strict and nbits != kPioneerBits:
        return False  # Not strictly an Pioneer message.

    data = 0
    offset = kStartOffset
    results.value = 0
    for section in range(2):
        # Match Header + Data + Footer

        used = matchGeneric(
            results.rawbuf + offset,
            data,
            results.rawlen - offset,
            nbits / 2,
            kPioneerHdrMark,
            kPioneerHdrSpace,
            kPioneerBitMark,
            kPioneerOneSpace,
            kPioneerBitMark,
            kPioneerZeroSpace,
            kPioneerBitMark,
            kPioneerMinGap,
            True
        )
        if not used:
            return False

        offset += used
        command = data >> 8
        command_inverted = data
        address = data >> 24
        address_inverted = data >> 16
        # Compliance
        if strict:
            if command != (command_inverted ^ 0xFF):
                return False  # Command integrity failed.
            if address != (address_inverted ^ 0xFF):
                return False  # Address integrity failed.

        results.value = (results.value << (nbits / 2)) + data
        # NEC-like commands and addresses are technically in LSB first order so the
        # final versions have to be reversed.
        code = reverseBits((command << 8) + address, 16)
        if section:
            results.command = code
        else:
            results.address = code

    # Success
    results.bits = nbits
    results.decode_type = PIONEER
    return True
