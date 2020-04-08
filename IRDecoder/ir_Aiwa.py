# -*- coding: utf-8 -*-

# Copyright 2017 David Conran


from IRrecv import *
from IRsend import *

#                         AAA   IIIII  W   W   AAA
#                        A   A    I    W   W  A   A
#                        AAAAA    I    W W W  AAAAA
#                        A   A    I    W W W  A   A
#                        A   A  IIIII   WWW   A   A

# Based off the RC-T501 RCU
# Added by David Conran. (Inspired by IRremoteESP8266's implementation:
#                         https:#github.com/z3t0/Arduino-IRremote)
# Supports:
#   Brand: Aiwa,  Model: RC-T501 RCU

kAiwaRcT501PreBits = 26
kAiwaRcT501PostBits = 1
# NOTE: These are the compliment (inverted) of lirc values as
#       lirc uses a '0' for a mark, and a '1' for a space.
kAiwaRcT501PreData = 0x1D8113  # 26-bits
kAiwaRcT501PostData = 1


# Send an Aiwa RC T501 formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The number of bits of the message to be sent.
#           Typically kAiwaRcT501Bits. Max is 37 = (64 - 27)
#   repeat: The number of times the command is to be repeated.
#
# Status: BETA / Should work.
#
# Ref:
#  http:#lirc.sourceforge.net/remotes/aiwa/RC-T501
def sendAiwaRCT501(self, data, nbits, repeat):
    # Appears to be an extended NEC1 protocol. i.e. 42 bits instead of 32 bits.
    # So use sendNEC instead, however the twist is it has a fixed 26 bit
    # prefix, and a fixed postfix bit.
    new_data = (
        (kAiwaRcT501PreData << (nbits + kAiwaRcT501PostBits)) |
        (data << kAiwaRcT501PostBits) |
        kAiwaRcT501PostData
    )

    nbits += kAiwaRcT501PreBits + kAiwaRcT501PostBits
    if nbits > new_data / 8:
        return  # We are overflowing. Abort, and don't send.

    self.sendNEC(new_data, nbits, repeat)


IRrecv.sendAiwaRCT501 = sendAiwaRCT501


# Decode the supplied Aiwa RC T501 message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kAiwaRcT501Bits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, false if it can't.
#
# Status: BETA / Should work.
#
# Notes:
#   Aiwa RC T501 appears to be a 42 bit variant of the NEC1 protocol.
#   However, we historically (original Arduino IRremote project) treats it as
#   a 15 bit (data) protocol. So, we expect nbits to typically be 15, and we
#   will remove the prefix and postfix from the raw data, and use that as
#   the result.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/nec.php
def decodeAiwaRCT501(self, results, nbits, strict):
    # Compliance
    if strict and nbits != kAiwaRcT501Bits:
        return False  # Doesn't match our protocol defn.

    # Add on the pre & post bits to our requested bit length.
    expected_nbits = nbits + kAiwaRcT501PreBits + kAiwaRcT501PostBits
    if expected_nbits > 64:
        return False  # We can't possibly match something that big.

    # Decode it as a much bigger (non-standard) NEC message, so we have to turn
    # off strict mode checking for NEC.
    if not self.decodeNEC(results, expected_nbits, False):
        return False  # The NEC decode had a problem, so we should too.

    actual_bits = results.bits
    new_data = results.value

    if actual_bits < expected_nbits:
        return False  # The data we caught was undersized. Throw it back.

    if (new_data & 0x1) != kAiwaRcT501PostData:
        return False  # The post data doesn't match, so it can't be this protocol.

    # Trim off the post data bit.
    new_data >>= kAiwaRcT501PostBits
    actual_bits -= kAiwaRcT501PostBits

    # Extract out our likely new value and put it back in the results.
    actual_bits -= kAiwaRcT501PreBits
    results.value = new_data & ((1L << actual_bits) - 1)

    # Check the prefix data matches.
    new_data >>= actual_bits  # Trim off the new data to expose the prefix.

    if new_data != kAiwaRcT501PreData:  # Check the prefix.
        return False

    # Compliance
    if strict and results.bits != expected_nbits:
        return False

    # Success
    results.decode_type = AIWA_RC_T501
    results.bits = actual_bits
    results.address = 0
    results.command = 0
    return True


IRrecv.decodeAiwaRCT501 = decodeAiwaRCT501
