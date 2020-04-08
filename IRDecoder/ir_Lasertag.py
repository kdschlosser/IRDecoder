# -*- coding: utf-8 -*-

# Copyright 2017 David Conran
# Lasertag

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Constants
kLasertagMinSamples = 13
kLasertagTick = 333
kLasertagMinGap = kDefaultMessageGap  # Just a guess.
kLasertagTolerance = 0     # Percentage error margin.
kLasertagExcess = 0       # See kMarkExcess.
kLasertagDelta = 150  # Use instead of Excess and Tolerance.
kSpace = 1
kMark = 0


# Send a Lasertag packet.
# This protocol is pretty much just raw Manchester encoding.
#
# Args:
#   data:    The message you wish to send.
#   nbits:   Bit size of the protocol you want to send.
#   repeat:  Nr. of extra times the data will be sent.
#
# Status: STABLE / Working.
#
def sendLasertag(data, nbits, repeat):
    if nbits > 64:
        return  # We can't send something that big.

    # Set 36kHz IR carrier frequency & a 1/4 (25%) duty cycle.
    # NOTE: duty cycle is not confirmed. Just guessing based on RC5/6 protocols.
    enableIROut(36, 25)

    for _ in range(repeat + 1):
        # Data
        mask = 1 << (nbits - 1)

        while mask:
            if data & mask:  # 1
                space(kLasertagTick)  # 1 is space, then mark.
                mark(kLasertagTick)
            else:  # 0
                mark(kLasertagTick)  # 0 is mark, then space.
                space(kLasertagTick)

            mask >>= 1
    # Footer
    space(kLasertagMinGap)


# Decode the supplied Lasertag message.
# This protocol is pretty much just raw Manchester encoding.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Appears to be working 90% of the time.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/rc5.php
#   https:#en.wikipedia.org/wiki/RC-5
#   https:#en.wikipedia.org/wiki/Manchester_code
def decodeLasertag(results, nbits, strict):
    if results.rawlen < kLasertagMinSamples:
        return False

    # Compliance
    if strict and nbits != kLasertagBits:
        return False

    offset = kStartOffset
    used = 0
    data = 0
    actual_bits = 0

    # No Header

    # Data
    while offset <= results.rawlen:
        levelA = getRClevel(
            results,
            offset,
            used,
            kLasertagTick,
            kLasertagTolerance,
            kLasertagExcess,
            kLasertagDelta
        )

        levelB = getRClevel(
            results,
            offset,
            used,
            kLasertagTick,
            kLasertagTolerance,
            kLasertagExcess,
            kLasertagDelta
        )

        if levelA == kSpace and levelB == kMark:
            data = (data << 1) | 1  # 1
        elif levelA == kMark and levelB == kSpace:
            data <<= 1  # 0
        else:
            break

    # Footer (None)

    # Compliance
    if actual_bits < nbits:
        return False  # Less data than we expected.

    if strict and actual_bits != kLasertagBits:
        return False

    # Success
    results.decode_type = LASERTAG
    results.value = data
    results.address = data & 0xF  # Unit
    results.command = data >> 4   # Team
    results.repeat = False
    results.bits = actual_bits
    return True
