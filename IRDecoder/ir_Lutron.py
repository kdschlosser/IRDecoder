# -*- coding: utf-8 -*-

# Copyright 2018 David Conran
# Lutron

from .IRrecv import *
from .IRsend import *
from .IRutils import *

# Notes:
#   The Lutron protocol uses a sort of Run Length encoding to encode
#   its data. There is no header or footer per-se.
#   As a mark is the first data we will notice, we always assume the First
#   bit of the technically 36-bit protocol is '1'. So it is assumed, and thus
#   we only care about the 35 bits of data.

# Constants
# Ref:
#  https:#github.com/crankyoldgit/IRremoteESP8266/issues/515
kLutronTick = 2288
kLutronGap = 150000  # Completely made up value.
kLutronDelta = 400   # +/- 300 usecs.


# Send a Lutron formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The number of bits of the message to be sent. Typically kLutronBits
#   repeat: The number of times the command is to be repeated.
#
# Status: Stable / Appears to be working for real devices.

# Notes:
#   Protocol is really 36 bits long, but the first bit is always a 1.
#   So, assume the 1 and only have a normal payload of 35 bits.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/515
def sendLutron(data, nbits, repeat):
    enableIROut(40000, 40)  # 40Khz & 40% dutycycle.
    for _ in range(repeat + 1):
        mark(kLutronTick)  # 1st bit is always '1'.
        # Send the supplied data in MSB First order.
        mask = 1 << (nbits - 1)
        while mask:
            if data & mask:
                mark(kLutronTick)  # Send a 1
            else:
                space(kLutronTick)  # Send a 0

            mask >>= 1

        space(kLutronGap)       # Inter-message gap.


# Decode the supplied Lutron message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kLutronBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Untested.
#
# Notes:
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/515
def decodeLutron(results, nbits, strict):
    # Technically the smallest number of entries for the smallest message is '1'.
    # i.e. All the bits set to 1, would produce a single huge mark signal.
    # So no minimum length check is required.
    if strict and nbits != kLutronBits:
        return False  # Not strictly an Lutron message.

    data = 0
    bitsSoFar = -1
    offset = kStartOffset

    if nbits > 64:
        return False  # To large to store the data.

    while bitsSoFar < nbits and offset < results.rawlen:
        entry = results.rawbuf[offset]
        # It has to be large enough to qualify as a bit.
        if not matchAtLeast(entry, kLutronTick, 0, kLutronDelta):
            return False

        # Keep reading bits of the same value until we run out.
        while entry != 0 and matchAtLeast(entry, kLutronTick, 0, kLutronDelta):
            bitsSoFar += 1

            if offset % 2:  # Is Odd?
                data = (data << 1) + 1  # Append a '1'.
            else:       # Is it Even?
                data <<= 1  # Append a '0'.

            if bitsSoFar == nbits and matchAtLeast(entry, kLutronGap):
                break  # We've likely reached the end of a message.

        # Remove a bit length from the current entry.
        entry = max(entry, (kLutronTick / kRawTick)) - kLutronTick / kRawTick
        offset += 1

        if offset % 2 and not match(entry, kLutronDelta, 0, kLutronDelta):
            return False  # Too much left over to be a good value. Reject it.

        if offset % 2 == 0 and offset <= results.rawlen - 1 and not matchAtLeast(entry, kLutronDelta, 0, kLutronDelta):
            return False  # Too much left over to be a good value. Reject it.

    # We got too many bits.
    if bitsSoFar > nbits or bitsSoFar < 0:
        return False

    # If we got less bits than we were expecting, we need to pad with zeros
    # until we get the correct number of bits.
    if bitsSoFar < nbits:
        data <<= (nbits - bitsSoFar)

    # Success
    results.decode_type = LUTRON
    results.bits = bitsSoFar
    results.value = data ^ (1 << nbits)  # Mask off the initial '1'.
    results.address = 0
    results.command = 0
    return True
