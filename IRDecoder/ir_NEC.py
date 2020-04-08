"""
# Copyright 2009 Ken Shirriff
# Copyright 2017, 2018 David Conran

# NEC originally added from https:#github.com/shirriff/Arduino-IRremote/

#ifndef IR_NEC_H_
#define IR_NEC_H_

#include <stdint.h>
#include "IRremoteESP8266.h"

# Supports:
#   Brand: Yamaha,   Model: RAV561 remote
#   Brand: Yamaha,   Model: RXV585B A/V Receiver
#   Brand: Aloka,    Model: SleepyLights LED Lamp
#   Brand: Toshiba,  Model: 42TL838 LCD TV

# Constants
# Ref:
#  http:#www.sbprojects.com/knowledge/ir/nec.php
kNecTick = 560
kNecHdrMarkTicks = 16
kNecHdrMark = kNecHdrMarkTicks * kNecTick
kNecHdrSpaceTicks = 8
kNecHdrSpace = kNecHdrSpaceTicks * kNecTick
kNecBitMarkTicks = 1
kNecBitMark = kNecBitMarkTicks * kNecTick
kNecOneSpaceTicks = 3
kNecOneSpace = kNecOneSpaceTicks * kNecTick
kNecZeroSpaceTicks = 1
kNecZeroSpace = kNecZeroSpaceTicks * kNecTick
kNecRptSpaceTicks = 4
kNecRptSpace = kNecRptSpaceTicks * kNecTick
kNecRptLength = 4
kNecMinCommandLengthTicks = 193
kNecMinCommandLength = kNecMinCommandLengthTicks * kNecTick
kNecMinGap =
    kNecMinCommandLength -
    (kNecHdrMark + kNecHdrSpace + kNECBits * (kNecBitMark + kNecOneSpace) +
     kNecBitMark)
kNecMinGapTicks =
    kNecMinCommandLengthTicks -
    (kNecHdrMarkTicks + kNecHdrSpaceTicks +
     kNECBits * (kNecBitMarkTicks + kNecOneSpaceTicks) + kNecBitMarkTicks)

# IR codes and structure for kids ALOKA SleepyLights LED Lamp.
# https:#aloka-designs.com/
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/1004
#
# May be useful for someone wanting to control the lamp.
#
# The lamp is toggled On and Off with the same power button.
# The colour, when selected, is the brightest and there are 4 levels of
# brightness that decrease on each send of the colour. A fifth send of the
# colour resets to brightest again.
#
# Remote buttons defined left to right, top line to bottom line on the remote.
kAlokaPower =         0xFF609F
kAlokaLedWhite =      0xFF906F
kAlokaLedGreen =      0xFF9867
kAlokaLedBlue =       0xFFD827
kAlokaLedPinkRed =    0xFF8877
kAlokaLedRed =        0xFFA857
kAlokaLedLightGreen = 0xFFE817
kAlokaLedMidBlue =    0xFF48B7
kAlokaLedPink =       0xFF6897
kAlokaLedOrange =     0xFFB24D
kAlokaLedYellow =     0xFF00FF
kAlokaNightFade =     0xFF50AF
kAlokaNightTimer =    0xFF7887
kAlokaLedRainbow =    0xFF708F
# Didn't have a better description for it...
kAlokaLedTreeGrow =   0xFF58A7
#endif  # IR_NEC_H_

"""
# Copyright 2009 Ken Shirriff
# Copyright 2017 David Conran

# NEC originally added from https:#github.com/shirriff/Arduino-IRremote/

#define __STDC_LIMIT_MACROS
#include "ir_NEC.h"
#include <stdint.h>
#include <algorithm>
#include "IRrecv.h"
#include "IRsend.h"
#include "IRutils.h"

#if (SEND_NEC or SEND_SHERWOOD or SEND_AIWA_RC_T501 or SEND_SANYO)
# Send a raw NEC(Renesas) formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The number of bits of the message to be sent. Typically kNECBits.
#   repeat: The number of times the command is to be repeated.
#
# Status: STABLE / Known working.
#
# Ref:
#  http:#www.sbprojects.com/knowledge/ir/nec.php
void IRsend.sendNEC(data, nbits, repeat) {
  sendGeneric(kNecHdrMark, kNecHdrSpace, kNecBitMark, kNecOneSpace, kNecBitMark,
              kNecZeroSpace, kNecBitMark, kNecMinGap, kNecMinCommandLength,
              data, nbits, 38, True, 0,  # Repeats are handled later.
              33)
  # Optional command repeat sequence.
  if (repeat)
    sendGeneric(kNecHdrMark, kNecRptSpace, 0, 0, 0, 0,  # No actual data sent.
                kNecBitMark, kNecMinGap, kNecMinCommandLength, 0,
                0,                     # No data to be sent.
                38, True, repeat - 1,  # We've already sent a one message.
                33)
}

# Calculate the raw NEC data based on address and command.
# Args:
#   address: An address value.
#   command: An 8-bit command value.
# Returns:
#   A raw 32-bit NEC message.
#
# Status: BETA / Expected to work.
#
# Ref:
#  http:#www.sbprojects.com/knowledge/ir/nec.php
IRsend.encodeNEC(address, command) {
  command &= 0xFF  # We only want the least significant byte of command.
  # sendNEC() sends MSB first, but protocol says this is LSB first.
  command = reverseBits(command, 8)
  command = (command << 8) + (command ^ 0xFF)  # Calculate the new command.
  if (address > 0xFF) {                         # Is it Extended NEC?
    address = reverseBits(address, 16)
    return ((address << 16) + command)  # Extended.
  } else {
    address = reverseBits(address, 8)
    return (address << 24) + ((address ^ 0xFF) << 16) + command  # Normal.
  }
}
#endif  # (SEND_NEC or SEND_SHERWOOD or SEND_AIWA_RC_T501 or SEND_SANYO )

#if (DECODE_NEC or DECODE_SHERWOOD or DECODE_AIWA_RC_T501 or DECODE_SANYO)
# Decode the supplied NEC message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kNECBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Known good.
#
# Notes:
#   NEC protocol has three varients/forms.
#     Normal:   an 8 bit address & an 8 bit command in 32 bit data form.
#               i.e. address + inverted(address) + command + inverted(command)
#     Extended: a 16 bit address & an 8 bit command in 32 bit data form.
#               i.e. address + command + inverted(command)
#     Repeat:   a 0-bit code. i.e. No data bits. Just the header + footer.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/nec.php
bool IRrecv.decodeNEC(decode_results *results, nbits, bool strict) {
  if (results->rawlen < 2 * nbits + kHeader + kFooter - 1 and
      results->rawlen != kNecRptLength)
    return False  # Can't possibly be a valid NEC message.
  if (strict and nbits != kNECBits)
    return False  # Not strictly an NEC message.

  data = 0
  offset = kStartOffset

  # Header
  if (!matchMark(results->rawbuf[offset++], kNecHdrMark)) return False
  # Check if it is a repeat code.
  if (results->rawlen == kNecRptLength and
      matchSpace(results->rawbuf[offset], kNecRptSpace) and
      matchMark(results->rawbuf[offset + 1], kNecBitMark)) {
    results->value = kRepeat
    results->decode_type = NEC
    results->bits = 0
    results->address = 0
    results->command = 0
    results->repeat = True
    return True
  }

  # Match Header (cont.) + Data + Footer
  if (!matchGeneric(results->rawbuf + offset, &data,
                    results->rawlen - offset, nbits,
                    0, kNecHdrSpace,
                    kNecBitMark, kNecOneSpace,
                    kNecBitMark, kNecZeroSpace,
                    kNecBitMark, kNecMinGap, True)) return False
  # Compliance
  # Calculate command and optionally enforce integrity checking.
  command = (data & 0xFF00) >> 8
  # Command is sent twice, once as plain and then inverted.
  if ((command ^ 0xFF) != (data & 0xFF)) {
    if (strict) return False  # Command integrity failed.
    command = 0  # The command value isn't valid, so default to zero.
  }

  # Success
  results->bits = nbits
  results->value = data
  results->decode_type = NEC
  # NEC command and address are technically in LSB first order so the
  # final versions have to be reversed.
  results->command = reverseBits(command, 8)
  # Normal NEC protocol has an 8 bit address sent, followed by it inverted.
  address = (data & 0xFF000000) >> 24
  address_inverted = (data & 0x00FF0000) >> 16
  if (address == (address_inverted ^ 0xFF))
    # Inverted, so it is normal NEC protocol.
    results->address = reverseBits(address, 8)
  else  # Not inverted, so must be Extended NEC protocol, thus 16 bit address.
    results->address = reverseBits((data >> 16) & UINT16_MAX, 16)
  return True
}
#endif  # DECODE_NEC or DECODE_SHERWOOD or DECODE_AIWA_RC_T501 or DECODE_SANYO
