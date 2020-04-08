# -*- coding: utf-8 -*-

# Copyright Todd Treece
# Copyright 2017 David Conran

from .IRrecv import *
from .IRutils import *
from .IRsend import *

# DISH support originally by Todd Treece
#   http:#unionbridge.org/design/ircommand

# Supports:
#   Brand: DISH NETWORK,  Model: echostar 301

# Constants
# Ref:
#   https:#github.com/marcosamarinho/IRremoteESP8266/blob/master/ir_Dish.cpp
#   http:#www.hifi-remote.com/wiki/index.php?title=Dish
kDishTick = 100
kDishHdrMarkTicks = 4
kDishHdrMark = kDishHdrMarkTicks * kDishTick
kDishHdrSpaceTicks = 61
kDishHdrSpace = kDishHdrSpaceTicks * kDishTick
kDishBitMarkTicks = 4
kDishBitMark = kDishBitMarkTicks * kDishTick
kDishOneSpaceTicks = 17
kDishOneSpace = kDishOneSpaceTicks * kDishTick
kDishZeroSpaceTicks = 28
kDishZeroSpace = kDishZeroSpaceTicks * kDishTick
kDishRptSpaceTicks = kDishHdrSpaceTicks
kDishRptSpace = kDishRptSpaceTicks * kDishTick


# Send an IR command to a DISH NETWORK device.
#
# Args:
#   data:   The contents of the command you want to send.
#   nbits:  The bit size of the command being sent.
#   repeat: The number of times you want the command to be repeated.
#
# Status: BETA / Previously working.
#
# Note:
#   Dishplayer is a different protocol.
#   Typically a DISH device needs to get a command a total of at least 4
#   times to accept it. e.g. repeat=3
#
#   Here is the LIRC file I found that seems to match the remote codes from the
#   oscilloscope:
#     DISH NETWORK (echostar 301):
#     http:#lirc.sourceforge.net/remotes/echostar/301_501_3100_5100_58xx_59xx
#
# Ref:
#   http:#www.hifi-remote.com/wiki/index.php?title=Dish
def sendDISH(self, data, nbits, repeat):
    self.enable_ir_out(57600)  # Set modulation freq. to 57.6kHz.
    # Header is only ever sent once.
    self.mark(kDishHdrMark)
    self.space(kDishHdrSpace)

    self.send_generic(
        0,
        0,  # No headers from here on in.
        kDishBitMark,
        kDishOneSpace,
        kDishBitMark,
        kDishZeroSpace,
        kDishBitMark,
        kDishRptSpace,
        data,
        nbits,
        57600,
        True,
        repeat,
        50
    )


IRsend.sendDISH = sendDISH


# Decode the supplied DISH NETWORK message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion. Typically kDishBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status:  ALPHA (untested and unconfirmed.)
#
# Note:
#   Dishplayer is a different protocol.
#   Typically a DISH device needs to get a command a total of at least 4
#   times to accept it.
# Ref:
#   http:#www.hifi-remote.com/wiki/index.php?title=Dish
#   http:#lirc.sourceforge.net/remotes/echostar/301_501_3100_5100_58xx_59xx
#   https:#github.com/marcosamarinho/IRremoteESP8266/blob/master/ir_Dish.cpp
def decodeDISH(self, results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader + kFooter - 1:
        return False  # Not enough entries to be valid.

    if strict and nbits != kDishBits:
        return False  # Not strictly compliant.

    data = 0
    offset = kStartOffset

    # Match Header + Data + Footer
    if not self.match_generic(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        kDishHdrMark,
        kDishHdrSpace,
        kDishBitMark,
        kDishOneSpace,
        kDishBitMark,
        kDishZeroSpace,
        kDishBitMark,
        # The DISH protocol calls for a repeated message, so
        # strictly speaking there should be a code following this.
        # Only require it if we are set to strict matching.
        kDishRptSpace if strict else 0,
        False
    ):
        return False

    # Success
    results.decode_type = DISH
    results.bits = nbits
    results.value = data
    results.address = 0
    results.command = 0
    return True


IRrecv.decodeDISH = decodeDISH
