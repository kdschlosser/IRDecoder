"""
# Copyright 2009 Ken Shirriff
# Copyright 2017-2019 David Conran
# Copyright 2019 Mark Kuchel

# Mitsubishi

# Supports:
#   Brand: Mitsubishi,  Model: TV
#   Brand: Mitsubishi,  Model: HC3000 Projector
#   Brand: Mitsubishi,  Model: MS-GK24VA A/C
#   Brand: Mitsubishi,  Model: KM14A 0179213 remote
#   Brand: Mitsubishi Electric,  Model: PEAD-RP71JAA Ducted A/C
#   Brand: Mitsubishi Electric,  Model: 001CP T7WE10714 remote
#   Brand: Mitsubishi Electric,  Model: MSH-A24WV / MUH-A24WV A/C
#   Brand: Mitsubishi Electric,  Model: KPOA remote

#ifndef IR_MITSUBISHI_H_
#define IR_MITSUBISHI_H_

#define __STDC_LIMIT_MACROS
#include <stdint.h>
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Mitsubishi (TV) decoding added from https:#github.com/z3t0/Arduino-IRremote
# Mitsubishi (TV) sending & Mitsubishi A/C support added by David Conran

# Constants
kMitsubishiAcModeOffset = 3
kMitsubishiAcAuto = 0b100
kMitsubishiAcCool = 0b011
kMitsubishiAcDry =  0b010
kMitsubishiAcHeat = 0b001
kMitsubishiAcPowerOffset = 5
kMitsubishiAcPower = 1 << kMitsubishiAcPowerOffset  # 0x20
kMitsubishiAcFanOffset = 0
kMitsubishiAcFanSize = 3  # Mask 0b111
kMitsubishiAcFanAuto = 0
kMitsubishiAcFanAutoOffset = 7
kMitsubishiAcFanMax = 5
kMitsubishiAcFanRealMax = 4
kMitsubishiAcFanSilent = 6
kMitsubishiAcFanQuiet = kMitsubishiAcFanSilent
kMitsubishiAcMinTemp = 16  # 16C
kMitsubishiAcMaxTemp = 31  # 31C
kMitsubishiAcVaneBitOffset = 6
kMitsubishiAcVaneOffset = 3
kMitsubishiAcVaneSize = 3
kMitsubishiAcVaneAuto = 0
kMitsubishiAcVaneAutoMove = 7
kMitsubishiAcNoTimer = 0
kMitsubishiAcStartTimer = 5
kMitsubishiAcStopTimer = 3
kMitsubishiAcStartStopTimer = 7
kMitsubishiAcWideVaneAuto = 8

kMitsubishi136PowerByte = 5
kMitsubishi136PowerOffset = 6
kMitsubishi136PowerBit = 1 << kMitsubishi136PowerOffset
kMitsubishi136TempByte = 6
kMitsubishi136MinTemp = 17  # 17C
kMitsubishi136MaxTemp = 30  # 30C
kMitsubishi136ModeByte = kMitsubishi136TempByte
kMitsubishi136ModeOffset = 0
kMitsubishi136Fan =             0b000
kMitsubishi136Cool =            0b001
kMitsubishi136Heat =            0b010
kMitsubishi136Auto =            0b011
kMitsubishi136Dry =             0b101
kMitsubishi136SwingVByte = 7
kMitsubishi136SwingVLowest =   0b0000
kMitsubishi136SwingVLow =      0b0001
kMitsubishi136SwingVHigh =     0b0010
kMitsubishi136SwingVHighest =  0b0011
kMitsubishi136SwingVAuto =     0b1100
kMitsubishi136FanByte = kMitsubishi136SwingVByte
#                          FanMask =    0b00000110
kMitsubishi136FanOffset = 1
kMitsubishi136FanSize = 2  # Bits
kMitsubishi136FanMin =          0b00
kMitsubishi136FanLow =          0b01
kMitsubishi136FanMed =          0b10
kMitsubishi136FanMax =          0b11
kMitsubishi136FanQuiet = kMitsubishi136FanMin

# Mitsubishi112

# remote_state[5]
kMitsubishi112PowerByte = 5
kMitsubishi112PowerOffset = 2  # 0b00000100
# remote_state[6]
kMitsubishi112ModeByte = 6
kMitsubishi112ModeOffset = 0  # Mask 0b00000111
kMitsubishi112Cool =                        0b011
kMitsubishi112Heat =                        0b001
kMitsubishi112Auto =                        0b111
kMitsubishi112Dry =                         0b010
# remote_state[7]
kMitsubishi112TempByte = 7
kMitsubishi112TempSize = 4  # Mask 0b00001111
kMitsubishi112MinTemp = 16  # 16C
kMitsubishi112MaxTemp = 31  # 31C
# remote_state[8]
kMitsubishi112FanByte = 8
kMitsubishi112FanOffset = 0  # Mask 0b00000111
kMitsubishi112FanSize = 3
kMitsubishi112FanMin =                     0b010
kMitsubishi112FanLow =                     0b011
kMitsubishi112FanMed =                     0b101
kMitsubishi112FanMax =                     0b000
kMitsubishi112FanQuiet = kMitsubishi112FanMin
kMitsubishi112SwingVByte = kMitsubishi112FanByte
kMitsubishi112SwingVOffset = 3  # Mask 0b00111000
kMitsubishi112SwingVSize = 3    # Mask 0b00111000
kMitsubishi112SwingVLowest =               0b101
kMitsubishi112SwingVLow =                  0b100
kMitsubishi112SwingVMiddle =               0b011
kMitsubishi112SwingVHigh =                 0b010
kMitsubishi112SwingVHighest =              0b001
kMitsubishi112SwingVAuto =                 0b111
# remote_state[12]
kMitsubishi112SwingHByte = 12
kMitsubishi112SwingHSize = 4
kMitsubishi112SwingHOffset = 2  # Mask 0b00111100
kMitsubishi112SwingHLeftMax =              0b0001
kMitsubishi112SwingHLeft =                 0b0010
kMitsubishi112SwingHMiddle =               0b0011
kMitsubishi112SwingHRight =                0b0100
kMitsubishi112SwingHRightMax =             0b0101
kMitsubishi112SwingHWide =                 0b1000
kMitsubishi112SwingHAuto =                 0b1100

# Legacy defines (Deprecated)
#define MITSUBISHI_AC_VANE_AUTO_MOVE kMitsubishiAcVaneAutoMove
#define MITSUBISHI_AC_VANE_AUTO kMitsubishiAcVaneAuto
#define MITSUBISHI_AC_POWER kMitsubishiAcPower
#define MITSUBISHI_AC_MIN_TEMP kMitsubishiAcMinTemp
#define MITSUBISHI_AC_MAX_TEMP kMitsubishiAcMaxTemp
#define MITSUBISHI_AC_HEAT kMitsubishiAcHeat
#define MITSUBISHI_AC_FAN_SILENT kMitsubishiAcFanSilent
#define MITSUBISHI_AC_FAN_REAL_MAX kMitsubishiAcFanRealMax
#define MITSUBISHI_AC_FAN_MAX kMitsubishiAcFanMax
#define MITSUBISHI_AC_FAN_AUTO kMitsubishiAcFanAuto
#define MITSUBISHI_AC_DRY kMitsubishiAcDry
#define MITSUBISHI_AC_COOL kMitsubishiAcCool
#define MITSUBISHI_AC_AUTO kMitsubishiAcAuto

class IRMitsubishiAC {
 public:
  explicit IRMitsubishiAC(pin, bool inverted = False,
                          bool use_modulation = True)
  void stateReset(void)
  static bool validChecksum(uint8_t* data)
#if SEND_MITSUBISHI_AC
  void send(repeat = kMitsubishiACMinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_MITSUBISHI_AC
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(degrees)
  getTemp(void)
  void setFan(speed)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setVane(position)
  void setWideVane(position)
  getVane(void)
  getWideVane(void)
  uint8_t* getRaw(void)
  void setRaw(uint8_t* data)
  getClock(void)
  void setClock(clock)
  getStartClock(void)
  void setStartClock(clock)
  getStopClock(void)
  void setStopClock(clock)
  getTimer(void)
  void setTimer(timer)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static convertSwingV(stdAc.swingv_t position)
  static convertSwingH(stdAc.swingh_t position)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static stdAc.swingv_t toCommonSwingV(pos)
  static stdAc.swingh_t toCommonSwingH(pos)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  remote_state[kMitsubishiACStateLength]
  void checksum(void)
  static calculateChecksum(uint8_t* data)
}

class IRMitsubishi136 {
 public:
  explicit IRMitsubishi136(pin, bool inverted = False,
                           bool use_modulation = True)


  void stateReset(void)
#if SEND_MITSUBISHI136
  void send(repeat = kMitsubishi136MinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_MITSUBISHI136
  void begin(void)
  static bool validChecksum(uint8_t* data,
                            len = kMitsubishi136StateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(degrees)
  getTemp(void)
  void setFan(speed)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setSwingV(position)
  getSwingV(void)
  void setQuiet(bool on)
  bool getQuiet(void)
  uint8_t* getRaw(void)
  void setRaw(uint8_t* data)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static convertSwingV(stdAc.swingv_t position)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static stdAc.swingv_t toCommonSwingV(pos)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  remote_state[kMitsubishi136StateLength]
  void checksum(void)
}


class IRMitsubishi112 {
 public:
  explicit IRMitsubishi112(pin, bool inverted = False,
                           bool use_modulation = True)


  void stateReset(void)
#if SEND_MITSUBISHI112
  void send(repeat = kMitsubishi112MinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_MITSUBISHI112
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(degrees)
  getTemp(void)
  void setFan(speed)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setSwingV(position)
  getSwingV(void)
  void setSwingH(position)
  getSwingH(void)
  void setQuiet(bool on)
  bool getQuiet(void)
  uint8_t* getRaw(void)
  void setRaw(uint8_t* data)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static convertSwingV(stdAc.swingv_t position)
  static convertSwingH(stdAc.swingh_t position)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static stdAc.swingv_t toCommonSwingV(pos)
  static stdAc.swingh_t toCommonSwingH(pos)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  remote_state[kMitsubishi112StateLength]
  void checksum(void)
}

#endif  # IR_MITSUBISHI_H_

"""
# Copyright 2009 Ken Shirriff
# Copyright 2017-2019 David Conran
# Copyright 2019 Mark Kuchel
# Copyright 2018 Denes Varga

# Mitsubishi

#include "ir_Mitsubishi.h"
#include <algorithm>
#include <cstring>
#ifndef ARDUINO
#include <string>
#endif
#include "IRrecv.h"
#include "IRsend.h"
#include "IRtext.h"
#include "IRutils.h"
#include "ir_Tcl.h"

# Mitsubishi (TV) decoding added from https:#github.com/z3t0/Arduino-IRremote
# Mitsubishi (TV) sending & Mitsubishi A/C support added by David Conran

# Constants
# Mitsubishi TV
# period time is 1/33000Hz = 30.303 uSeconds (T)
# Ref:
#   GlobalCache's Control Tower's Mitsubishi TV data.
#   https:#github.com/marcosamarinho/IRremoteESP8266/blob/master/ir_Mitsubishi.cpp
kMitsubishiTick = 30
kMitsubishiBitMarkTicks = 10
kMitsubishiBitMark = kMitsubishiBitMarkTicks * kMitsubishiTick
kMitsubishiOneSpaceTicks = 70
kMitsubishiOneSpace = kMitsubishiOneSpaceTicks * kMitsubishiTick
kMitsubishiZeroSpaceTicks = 30
kMitsubishiZeroSpace =
    kMitsubishiZeroSpaceTicks * kMitsubishiTick
kMitsubishiMinCommandLengthTicks = 1786
kMitsubishiMinCommandLength =
    kMitsubishiMinCommandLengthTicks * kMitsubishiTick
kMitsubishiMinGapTicks = 936
kMitsubishiMinGap = kMitsubishiMinGapTicks * kMitsubishiTick

# Mitsubishi Projector (HC3000)
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/441

kMitsubishi2HdrMark = 8400
kMitsubishi2HdrSpace = kMitsubishi2HdrMark / 2
kMitsubishi2BitMark = 560
kMitsubishi2ZeroSpace = 520
kMitsubishi2OneSpace = kMitsubishi2ZeroSpace * 3
kMitsubishi2MinGap = 28500

# Mitsubishi A/C
# Ref:
#   https:#github.com/r45635/HVAC-IR-Control/blob/master/HVAC_ESP8266/HVAC_ESP8266.ino#L84

kMitsubishiAcHdrMark = 3400
kMitsubishiAcHdrSpace = 1750
kMitsubishiAcBitMark = 450
kMitsubishiAcOneSpace = 1300
kMitsubishiAcZeroSpace = 420
kMitsubishiAcRptMark = 440
kMitsubishiAcRptSpace = 17100
 kMitsubishiAcExtraTolerance = 5

# Mitsubishi 136 bit A/C
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/888

kMitsubishi136HdrMark = 3324
kMitsubishi136HdrSpace = 1474
kMitsubishi136BitMark = 467
kMitsubishi136OneSpace = 1137
kMitsubishi136ZeroSpace = 351
kMitsubishi136Gap = kDefaultMessageGap

# Mitsubishi 112 bit A/C
# Ref:
#   https:#github.com/kuchel77

kMitsubishi112HdrMark = 3450
kMitsubishi112HdrSpace = 1696
kMitsubishi112BitMark = 450
kMitsubishi112OneSpace = 1250
kMitsubishi112ZeroSpace = 385
kMitsubishi112Gap = kDefaultMessageGap
# Total tolerance percentage to use for matching the header mark.
 kMitsubishi112HdrMarkTolerance = 5


using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.minsToString
using irutils.setBit
using irutils.setBits

#if SEND_MITSUBISHI
# Send a Mitsubishi message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kMitsubishiBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: ALPHA / untested.
#
# Notes:
#   This protocol appears to have no header.
# Ref:
#   https:#github.com/marcosamarinho/IRremoteESP8266/blob/master/ir_Mitsubishi.cpp
#   GlobalCache's Control Tower's Mitsubishi TV data.
void IRsend.sendMitsubishi(data, nbits, repeat) {
  sendGeneric(0, 0,  # No Header
              kMitsubishiBitMark, kMitsubishiOneSpace, kMitsubishiBitMark,
              kMitsubishiZeroSpace, kMitsubishiBitMark, kMitsubishiMinGap,
              kMitsubishiMinCommandLength, data, nbits, 33, True, repeat, 50)
}
#endif  # SEND_MITSUBISHI

#if DECODE_MITSUBISHI
# Decode the supplied Mitsubishi message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / previously working.
#
# Notes:
#   This protocol appears to have no header.
#
# Ref:
#   GlobalCache's Control Tower's Mitsubishi TV data.
bool IRrecv.decodeMitsubishi(decode_results *results, nbits,
                              bool strict) {
  if (strict and nbits != kMitsubishiBits)
    return False  # Request is out of spec.

  offset = kStartOffset
  data = 0

  # Match Data + Footer
  if (!matchGeneric(results->rawbuf + offset, &data,
                    results->rawlen - offset, nbits,
                    0, 0,  # No header
                    kMitsubishiBitMark, kMitsubishiOneSpace,
                    kMitsubishiBitMark, kMitsubishiZeroSpace,
                    kMitsubishiBitMark, kMitsubishiMinGap,
                    True, 30)) return False
  # Success
  results->decode_type = MITSUBISHI
  results->bits = nbits
  results->value = data
  results->address = 0
  results->command = 0
  return True
}
#endif  # DECODE_MITSUBISHI

#if SEND_MITSUBISHI2
# Send a Mitsubishi2 message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kMitsubishiBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: ALPHA / untested.
#
# Notes:
#   Based on a Mitsubishi HC3000 projector's remote.
#   This protocol appears to have a manditory in-protocol repeat.
#   That is in *addition* to the entire message needing to be sent twice
#   for the device to accept the command. That is separate from the repeat.
#   i.e. Allegedly, the real remote requires the "Off" button pressed twice.
#        You will need to add a suitable gap yourself.
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/441
void IRsend.sendMitsubishi2(data, nbits, repeat) {
  for (i = 0 i <= repeat i++) {
    # First half of the data.
    sendGeneric(kMitsubishi2HdrMark, kMitsubishi2HdrSpace, kMitsubishi2BitMark,
                kMitsubishi2OneSpace, kMitsubishi2BitMark,
                kMitsubishi2ZeroSpace, kMitsubishi2BitMark,
                kMitsubishi2HdrSpace, data >> (nbits / 2), nbits / 2, 33, True,
                0, 50)
    # Second half of the data.
    sendGeneric(0, 0,  # No header for the second data block
                kMitsubishi2BitMark, kMitsubishi2OneSpace, kMitsubishi2BitMark,
                kMitsubishi2ZeroSpace, kMitsubishi2BitMark, kMitsubishi2MinGap,
                data & ((1 << (nbits / 2)) - 1), nbits / 2, 33, True, 0, 50)
  }
}
#endif  # SEND_MITSUBISHI2

#if DECODE_MITSUBISHI2
# Decode the supplied Mitsubishi2 message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Works with simulated data.
#
# Notes:
#   Hardware supported:
#     * Mitsubishi HC3000 projector's remote.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/441
bool IRrecv.decodeMitsubishi2(decode_results *results, nbits,
                               bool strict) {
  if (results->rawlen < 2 * nbits + kHeader + (kFooter * 2) - 1)
    return False  # Shorter than shortest possibly expected.
  if (strict and nbits != kMitsubishiBits)
    return False  # Request is out of spec.

  offset = kStartOffset
  results->value = 0

  # Header
  if (!matchMark(results->rawbuf[offset++], kMitsubishi2HdrMark)) return False
  if (!matchSpace(results->rawbuf[offset++], kMitsubishi2HdrSpace))
    return False
  for (i = 0 i < 2 i++) {
    # Match Data + Footer
    used
    data = 0
    used = matchGeneric(results->rawbuf + offset, &data,
                        results->rawlen - offset, nbits / 2,
                        0, 0,  # No header
                        kMitsubishi2BitMark, kMitsubishi2OneSpace,
                        kMitsubishi2BitMark, kMitsubishi2ZeroSpace,
                        kMitsubishi2BitMark, kMitsubishi2HdrSpace,
                        i % 2)
    if (!used) return False
    offset += used
    results->value <<= (nbits / 2)
    results->value |= data
  }

  # Success
  results->decode_type = MITSUBISHI2
  results->bits = nbits
  results->address = GETBITS64(results->value, nbits / 2, nbits / 2)
  results->command = GETBITS64(results->value, 0, nbits / 2)
  return True
}
#endif  # DECODE_MITSUBISHI2

#if SEND_MITSUBISHI_AC
# Send a Mitsubishi A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kMitsubishiACStateLength)
#   repeat: Nr. of times the message is to be repeated.
#          (Default = kMitsubishiACMinRepeat).
#
# Status: BETA / Appears to be working.
#
void IRsend.sendMitsubishiAC(unsigned char data[], nbytes,
                              repeat) {
  if (nbytes < kMitsubishiACStateLength)
    return  # Not enough bytes to send a proper message.

  sendGeneric(kMitsubishiAcHdrMark, kMitsubishiAcHdrSpace, kMitsubishiAcBitMark,
              kMitsubishiAcOneSpace, kMitsubishiAcBitMark,
              kMitsubishiAcZeroSpace, kMitsubishiAcRptMark,
              kMitsubishiAcRptSpace, data, nbytes, 38, False, repeat, 50)
}
#endif  # SEND_MITSUBISHI_AC

#if DECODE_MITSUBISHI_AC
# Decode the supplied Mitsubishi message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Under development
#
# Ref:
# https:#www.analysir.com/blog/2015/01/06/reverse-engineering-mitsubishi-ac-infrared-protocol/
bool IRrecv.decodeMitsubishiAC(decode_results *results, nbits,
                                bool strict) {
  if (results->rawlen < ((kMitsubishiACBits * 2) + 2)) {
    DPRINTLN("Shorter than shortest possibly expected.")
    return False  # Shorter than shortest possibly expected.
  }
  if (strict and nbits != kMitsubishiACBits) {
    DPRINTLN("Request is out of spec.")
    return False  # Request is out of spec.
  }
  offset = kStartOffset
  for (i = 0 i < kMitsubishiACStateLength i++) {
    results->state[i] = 0
  }
  bool failure = False
  rep = 0
  do {
    failure = False
    # Header:
    #  Sometime happens that junk signals arrives before the real message
    bool headerFound = False
    while (!headerFound and
           offset < (results->rawlen - (kMitsubishiACBits * 2 + 2))) {
      headerFound =
          matchMark(results->rawbuf[offset], kMitsubishiAcHdrMark) and
          matchSpace(results->rawbuf[offset + 1], kMitsubishiAcHdrSpace)
      offset += 2
    }
    if (!headerFound) {
      DPRINTLN("Header mark not found.")
      return False
    }
    DPRINT("Header mark found at #")
    DPRINTLN(offset - 2)
    # Decode byte-by-byte:
    match_result_t data_result
    for (i = 0 i < kMitsubishiACStateLength and !failure i++) {
      results->state[i] = 0
      data_result =
          matchData(&(results->rawbuf[offset]), 8, kMitsubishiAcBitMark,
                    kMitsubishiAcOneSpace, kMitsubishiAcBitMark,
                    kMitsubishiAcZeroSpace,
                    _tolerance + kMitsubishiAcExtraTolerance, 0, False)
      if (data_result.success == False) {
        failure = True
        DPRINT("Byte decode failed at #")
        DPRINTLN((uint16_t)i)
      } else {
        results->state[i] = data_result.data
        offset += data_result.used
        DPRINT((uint16_t)results->state[i])
        DPRINT(",")
      }
      DPRINTLN("")
    }
    # HEADER validation:
    if (failure or results->state[0] != 0x23 or results->state[1] != 0xCB or
        results->state[2] != 0x26 or results->state[3] != 0x01 or
        results->state[4] != 0x00) {
      DPRINTLN("Header mismatch.")
      failure = True
    } else {
      # DATA part:

      # FOOTER checksum:
      if (!IRMitsubishiAC.validChecksum(results->state)) {
        DPRINTLN("Checksum error.")
        failure = True
      }
    }
    if (rep != kMitsubishiACMinRepeat and failure) {
      bool repeatMarkFound = False
      while (!repeatMarkFound and
             offset < (results->rawlen - (kMitsubishiACBits * 2 + 4))) {
        repeatMarkFound =
            matchMark(results->rawbuf[offset], kMitsubishiAcRptMark) and
            matchSpace(results->rawbuf[offset + 1], kMitsubishiAcRptSpace)
            offset += 2
      }
      if (!repeatMarkFound) {
        DPRINTLN("First attempt failure and repeat mark not found.")
        return False
      }
    }
    rep++
    # Check if the repeat is correct if we need strict decode:
    if (strict and !failure) {
      DPRINTLN("Strict repeat check enabled.")
      # Repeat mark and space:
      if (!matchMark(results->rawbuf[offset++], kMitsubishiAcRptMark) or
          !matchSpace(results->rawbuf[offset++], kMitsubishiAcRptSpace)) {
        DPRINTLN("Repeat mark error.")
        return False
      }
      # Header mark and space:
      if (!matchMark(results->rawbuf[offset++], kMitsubishiAcHdrMark) or
          !matchSpace(results->rawbuf[offset++], kMitsubishiAcHdrSpace)) {
        DPRINTLN("Repeat header error.")
        return False
      }
      # Payload:
      for (i = 0 i < kMitsubishiACStateLength i++) {
        data_result =
            matchData(&(results->rawbuf[offset]), 8, kMitsubishiAcBitMark,
                      kMitsubishiAcOneSpace, kMitsubishiAcBitMark,
                      kMitsubishiAcZeroSpace,
                      _tolerance + kMitsubishiAcExtraTolerance, 0, False)
        if (data_result.success == False or
            data_result.data != results->state[i]) {
          DPRINTLN("Repeat payload error.")
          return False
        }
        offset += data_result.used
      }
    }  # strict repeat check
  } while (failure and rep <= kMitsubishiACMinRepeat)
  results->decode_type = MITSUBISHI_AC
  results->bits = nbits
  return !failure
}
#endif  # DECODE_MITSUBISHI_AC

# Code to emulate Mitsubishi A/C IR remote control unit.
# Inspired and derived from the work done at:
#   https:#github.com/r45635/HVAC-IR-Control
#
# Warning: Consider this very alpha code. Seems to work, but not validated.
#
# Equipment it seems compatible with:
#  * <Add models (A/C & remotes) you've gotten it working with here>
# Initialise the object.
IRMitsubishiAC.IRMitsubishiAC(pin, bool inverted,
                               bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRMitsubishiAC.stateReset(void) {
  # The state of the IR remote in IR code form.
  # Known good state obtained from:
  #   https:#github.com/r45635/HVAC-IR-Control/blob/master/HVAC_ESP8266/HVAC_ESP8266.ino#L108
  static kReset[kMitsubishiACStateLength] = {
      0x23, 0xCB, 0x26, 0x01, 0x00, 0x20, 0x08, 0x06, 0x30, 0x45, 0x67}
  setRaw(kReset)
}

# Configure the pin for output.
void IRMitsubishiAC.begin(void) { _irsend.begin() }

#if SEND_MITSUBISHI_AC
# Send the current desired state to the IR LED.
void IRMitsubishiAC.send(repeat) {
  _irsend.sendMitsubishiAC(getRaw(), kMitsubishiACStateLength, repeat)
}
#endif  # SEND_MITSUBISHI_AC

# Return a pointer to the internal state date of the remote.
*IRMitsubishiAC.getRaw(void) {
  this->checksum()
  return remote_state
}

void IRMitsubishiAC.setRaw(*data) {
  memcpy(remote_state, data, kMitsubishiACStateLength)
}

# Calculate the checksum for the current internal state of the remote.
void IRMitsubishiAC.checksum(void) {
  remote_state[kMitsubishiACStateLength - 1] = calculateChecksum(remote_state)
}

bool IRMitsubishiAC.validChecksum(*data) {
  return calculateChecksum(data) == data[kMitsubishiACStateLength - 1]
}

IRMitsubishiAC.calculateChecksum(*data) {
  return sumBytes(data, kMitsubishiACStateLength - 1)
}

# Set the requested power state of the A/C to on.
void IRMitsubishiAC.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRMitsubishiAC.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRMitsubishiAC.setPower(bool on) {
  setBit(&remote_state[5], kMitsubishiAcPowerOffset, on)
}

# Return the requested power state of the A/C.
bool IRMitsubishiAC.getPower(void) {
  return GETBIT8(remote_state[5], kMitsubishiAcPowerOffset)
}

# Set the temp. in deg C
void IRMitsubishiAC.setTemp(degrees) {
  temp = std.max((uint8_t)kMitsubishiAcMinTemp, degrees)
  temp = std.min((uint8_t)kMitsubishiAcMaxTemp, temp)
  remote_state[7] = temp - kMitsubishiAcMinTemp
}

# Return the set temp. in deg C
IRMitsubishiAC.getTemp(void) {
  return (remote_state[7] + kMitsubishiAcMinTemp)
}

# Set the speed of the fan, 0-6.
# 0 is auto, 1-5 is the speed, 6 is silent.
void IRMitsubishiAC.setFan(speed) {
  fan = speed
  # Bounds check
  if (fan > kMitsubishiAcFanSilent)
    fan = kMitsubishiAcFanMax        # Set the fan to maximum if out of range.
  # Auto has a special bit.
  setBit(&remote_state[9], kMitsubishiAcFanAutoOffset,
         fan == kMitsubishiAcFanAuto)
  if (fan >= kMitsubishiAcFanMax)
    fan--  # There is no spoon^H^H^Heed 5 (max), pretend it doesn't exist.
  setBits(&remote_state[9], kMitsubishiAcFanOffset, kMitsubishiAcFanSize, fan)
}

# Return the requested state of the unit's fan.
IRMitsubishiAC.getFan(void) {
  fan = GETBITS8(remote_state[9], kMitsubishiAcFanOffset,
                         kMitsubishiAcFanSize)
  if (fan == kMitsubishiAcFanMax) return kMitsubishiAcFanSilent
  return fan
}

# Return the requested climate operation mode of the a/c unit.
IRMitsubishiAC.getMode(void) {
  return GETBITS8(remote_state[6], kMitsubishiAcModeOffset, kModeBitsSize)
}

# Set the requested climate operation mode of the a/c unit.
void IRMitsubishiAC.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    case kMitsubishiAcAuto: remote_state[8] = 0b00110000 break
    case kMitsubishiAcCool: remote_state[8] = 0b00110110 break
    case kMitsubishiAcDry:  remote_state[8] = 0b00110010 break
    case kMitsubishiAcHeat: remote_state[8] = 0b00110000 break
    default:
      this->setMode(kMitsubishiAcAuto)
      return
  }
  setBits(&remote_state[6], kMitsubishiAcModeOffset, kModeBitsSize, mode)
}

# Set the requested vane operation mode of the a/c unit.
void IRMitsubishiAC.setVane(position) {
  pos = std.min(position, kMitsubishiAcVaneAutoMove)  # bounds check
  setBit(&remote_state[9], kMitsubishiAcVaneBitOffset)
  setBits(&remote_state[9], kMitsubishiAcVaneOffset, kMitsubishiAcVaneSize,
          pos)
}

# Set the requested wide-vane operation mode of the a/c unit.
void IRMitsubishiAC.setWideVane(position) {
  setBits(&remote_state[8], kHighNibble, kNibbleSize,
          std.min(position, kMitsubishiAcWideVaneAuto))
}

# Return the requested vane operation mode of the a/c unit.
IRMitsubishiAC.getVane(void) {
  return GETBITS8(remote_state[9], kMitsubishiAcVaneOffset,
                  kMitsubishiAcVaneSize)
}

# Return the requested wide vane operation mode of the a/c unit.
IRMitsubishiAC.getWideVane(void) {
  return GETBITS8(remote_state[8], kHighNibble, kNibbleSize)
}

# Return the clock setting of the message. 1=1/6 hour. e.g. 4pm = 48
IRMitsubishiAC.getClock(void) { return remote_state[10] }

# Set the current time. 1 = 1/6 hour. e.g. 6am = 36.
void IRMitsubishiAC.setClock(clock) {
  remote_state[10] = clock
}

# Return the desired start time. 1 = 1/6 hour. e.g. 1am = 6
IRMitsubishiAC.getStartClock(void) { return remote_state[12] }

# Set the desired start time of the AC.  1 = 1/6 hour. e.g. 8pm = 120
void IRMitsubishiAC.setStartClock(clock) {
  remote_state[12] = clock
}

# Return the desired stop time of the AC. 1 = 1/6 hour. e.g 10pm = 132
IRMitsubishiAC.getStopClock(void) { return remote_state[11] }

# Set the desired stop time of the AC. 1 = 1/6 hour. e.g 10pm = 132
void IRMitsubishiAC.setStopClock(clock) {
  remote_state[11] = clock
}

# Return the timer setting. Possible values: kMitsubishiAcNoTimer,
#  kMitsubishiAcStartTimer, kMitsubishiAcStopTimer,
#  kMitsubishiAcStartStopTimer
IRMitsubishiAC.getTimer(void) {
  return GETBITS8(remote_state[13], 0, 3)
}

# Set the timer setting. Possible values: kMitsubishiAcNoTimer,
#  kMitsubishiAcStartTimer, kMitsubishiAcStopTimer,
#  kMitsubishiAcStartStopTimer
void IRMitsubishiAC.setTimer(timer) {
  setBits(&remote_state[13], 0, 3, timer)
}

# Convert a standard A/C mode into its native mode.
IRMitsubishiAC.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kMitsubishiAcCool
    case stdAc.opmode_t.kHeat: return kMitsubishiAcHeat
    case stdAc.opmode_t.kDry:  return kMitsubishiAcDry
    default:                     return kMitsubishiAcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMitsubishiAC.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:    return kMitsubishiAcFanSilent
    case stdAc.fanspeed_t.kLow:    return kMitsubishiAcFanRealMax - 3
    case stdAc.fanspeed_t.kMedium: return kMitsubishiAcFanRealMax - 2
    case stdAc.fanspeed_t.kHigh:   return kMitsubishiAcFanRealMax - 1
    case stdAc.fanspeed_t.kMax:    return kMitsubishiAcFanRealMax
    default:                         return kMitsubishiAcFanAuto
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishiAC.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kHighest: return kMitsubishiAcVaneAutoMove - 6
    case stdAc.swingv_t.kHigh:    return kMitsubishiAcVaneAutoMove - 5
    case stdAc.swingv_t.kMiddle:  return kMitsubishiAcVaneAutoMove - 4
    case stdAc.swingv_t.kLow:     return kMitsubishiAcVaneAutoMove - 3
    case stdAc.swingv_t.kLowest:  return kMitsubishiAcVaneAutoMove - 2
    case stdAc.swingv_t.kAuto:    return kMitsubishiAcVaneAutoMove
    default:                        return kMitsubishiAcVaneAuto
  }
}

# Convert a standard A/C wide wane swing into its native setting.
IRMitsubishiAC.convertSwingH(stdAc.swingh_t position) {
  switch (position) {
    case stdAc.swingh_t.kLeftMax:  return kMitsubishiAcWideVaneAuto - 7
    case stdAc.swingh_t.kLeft:     return kMitsubishiAcWideVaneAuto - 6
    case stdAc.swingh_t.kMiddle:   return kMitsubishiAcWideVaneAuto - 5
    case stdAc.swingh_t.kRight:    return kMitsubishiAcWideVaneAuto - 4
    case stdAc.swingh_t.kRightMax: return kMitsubishiAcWideVaneAuto - 3
    case stdAc.swingh_t.kWide:     return kMitsubishiAcWideVaneAuto - 2
    case stdAc.swingh_t.kAuto:     return kMitsubishiAcWideVaneAuto
    default:                         return kMitsubishiAcWideVaneAuto - 5
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRMitsubishiAC.toCommonMode(mode) {
  switch (mode) {
    case kMitsubishiAcCool: return stdAc.opmode_t.kCool
    case kMitsubishiAcHeat: return stdAc.opmode_t.kHeat
    case kMitsubishiAcDry:  return stdAc.opmode_t.kDry
    default:                return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMitsubishiAC.toCommonFanSpeed(speed) {
  switch (speed) {
    case kMitsubishiAcFanRealMax:     return stdAc.fanspeed_t.kMax
    case kMitsubishiAcFanRealMax - 1: return stdAc.fanspeed_t.kHigh
    case kMitsubishiAcFanRealMax - 2: return stdAc.fanspeed_t.kMedium
    case kMitsubishiAcFanRealMax - 3: return stdAc.fanspeed_t.kLow
    case kMitsubishiAcFanSilent:      return stdAc.fanspeed_t.kMin
    default:                          return stdAc.fanspeed_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRMitsubishiAC.toCommonSwingV(pos) {
  switch (pos) {
    case 1:  return stdAc.swingv_t.kHighest
    case 2:  return stdAc.swingv_t.kHigh
    case 3:  return stdAc.swingv_t.kMiddle
    case 4:  return stdAc.swingv_t.kLow
    case 5:  return stdAc.swingv_t.kLowest
    default: return stdAc.swingv_t.kAuto
  }
}

# Convert a native horizontal swing to it's common equivalent.
stdAc.swingh_t IRMitsubishiAC.toCommonSwingH(pos) {
  switch (pos) {
    case 1:  return stdAc.swingh_t.kLeftMax
    case 2:  return stdAc.swingh_t.kLeft
    case 3:  return stdAc.swingh_t.kMiddle
    case 4:  return stdAc.swingh_t.kRight
    case 5:  return stdAc.swingh_t.kRightMax
    case 6:  return stdAc.swingh_t.kWide
    default: return stdAc.swingh_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMitsubishiAC.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.MITSUBISHI_AC
  result.model = -1  # No models used.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->toCommonSwingV(this->getVane())
  result.swingh = this->toCommonSwingH(this->getWideVane())
  result.quiet = this->getFan() == kMitsubishiAcFanSilent
  # Not supported.
  result.turbo = False
  result.clean = False
  result.econo = False
  result.filter = False
  result.light = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRMitsubishiAC.toString(void) {
  String result = ""
  result.reserve(110)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kMitsubishiAcAuto, kMitsubishiAcCool,
                            kMitsubishiAcHeat, kMitsubishiAcDry,
                            kMitsubishiAcAuto)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kMitsubishiAcFanRealMax,
                           kMitsubishiAcFanRealMax - 3,
                           kMitsubishiAcFanAuto, kMitsubishiAcFanQuiet,
                           kMitsubishiAcFanRealMax - 2)
  result += addIntToString(this->getVane(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (this->getVane()) {
    case kMitsubishiAcVaneAuto:
      result += kAutoStr
      break
    case kMitsubishiAcVaneAutoMove:
      result += kAutoStr
      result += ' '
      result += kMoveStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addIntToString(this->getWideVane(), kSwingHStr)
  result += kSpaceLBraceStr
  switch (this->getWideVane()) {
    case kMitsubishiAcWideVaneAuto: result += kAutoStr break
    default:                        result += kUnknownStr
  }
  result += ')'
  result += addLabeledString(minsToString(getClock() * 10), kClockStr)
  result += addLabeledString(minsToString(getStartClock() * 10), kOnTimerStr)
  result += addLabeledString(minsToString(getStopClock() * 10), kOffTimerStr)
  result += kCommaSpaceStr
  result += kTimerStr
  result += kColonSpaceStr
  switch (this->getTimer()) {
    case kMitsubishiAcNoTimer:
      result += '-'
      break
    case kMitsubishiAcStartTimer:
      result += kStartStr
      break
    case kMitsubishiAcStopTimer:
      result += kStopStr
      break
    case kMitsubishiAcStartStopTimer:
      result += kStartStr
      result += '+'
      result += kStopStr
      break
    default:
      result += F("? (")
      result += this->getTimer()
      result += ')'
  }
  return result
}

#if SEND_MITSUBISHI136
# Send a Mitsubishi136 A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kMitsubishi136StateLength)
#   repeat: Nr. of times the message is to be repeated.
#          (Default = kMitsubishi136MinRepeat).
#
# Status: ALPHA / Probably working. Needs to be tested against a real device.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/888
void IRsend.sendMitsubishi136(unsigned char data[],
                               nbytes,
                               repeat) {
  if (nbytes < kMitsubishi136StateLength)
    return  # Not enough bytes to send a proper message.

  sendGeneric(kMitsubishi136HdrMark, kMitsubishi136HdrSpace,
              kMitsubishi136BitMark, kMitsubishi136OneSpace,
              kMitsubishi136BitMark, kMitsubishi136ZeroSpace,
              kMitsubishi136BitMark, kMitsubishi136Gap,
              data, nbytes, 38, False, repeat, 50)
}
#endif  # SEND_MITSUBISHI136

#if DECODE_MITSUBISHI136
# Decode the supplied Mitsubishi136 message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Reported as working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/888
bool IRrecv.decodeMitsubishi136(decode_results *results, nbits,
                                 bool strict) {
  # Too short to match?
  if (results->rawlen < (2 * nbits) + kHeader + kFooter - 1) return False
  if (nbits % 8 != 0) return False  # Not a multiple of an 8 bit byte.
  if (strict) {  # Do checks to see if it matches the spec.
    if (nbits != kMitsubishi136Bits) return False
  }
  used = matchGeneric(results->rawbuf + kStartOffset, results->state,
                               results->rawlen - kStartOffset, nbits,
                               kMitsubishi136HdrMark, kMitsubishi136HdrSpace,
                               kMitsubishi136BitMark, kMitsubishi136OneSpace,
                               kMitsubishi136BitMark, kMitsubishi136ZeroSpace,
                               kMitsubishi136BitMark, kMitsubishi136Gap,
                               True, _tolerance, 0, False)
  if (!used) return False
  if (strict) {
    # Header validation: Codes start with 0x23CB26
    if (results->state[0] != 0x23 or results->state[1] != 0xCB or
        results->state[2] != 0x26) return False
    if (!IRMitsubishi136.validChecksum(results->state, nbits / 8))
      return False
  }
  results->decode_type = MITSUBISHI136
  results->bits = nbits
  return True
}
#endif  # DECODE_MITSUBISHI136

# Code to emulate Mitsubishi 136bit A/C IR remote control unit.
#
# Equipment it seems compatible with:
#   Brand: Mitsubishi Electric,  Model: PEAD-RP71JAA Ducted A/C
#   Brand: Mitsubishi Electric,  Model: 001CP T7WE10714 remote

# Initialise the object.
IRMitsubishi136.IRMitsubishi136(pin, bool inverted,
                                 bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRMitsubishi136.stateReset(void) {
  # The state of the IR remote in IR code form.
  # Known good state obtained from:
  #   https:#docs.google.com/spreadsheets/d/1f8EGfIbBUo2B-CzUFdrgKQprWakoYNKM80IKZN4KXQE/edit#gid=312397579&range=A10
  static kReset[kMitsubishi136StateLength] = {
      0x23, 0xCB, 0x26, 0x21, 0x00, 0x40, 0xC2, 0xC7, 0x04}
  memcpy(remote_state, kReset, kMitsubishi136StateLength)
}

# Calculate the checksum for the current internal state of the remote.
void IRMitsubishi136.checksum(void) {
  for (i = 0 i < 6 i++)
    remote_state[kMitsubishi136PowerByte + 6 + i] =
        ~remote_state[kMitsubishi136PowerByte + i]
}

bool IRMitsubishi136.validChecksum(*data, len) {
  if (len < kMitsubishi136StateLength) return False
  half = (len - kMitsubishi136PowerByte) / 2
  for (i = 0 i < half i++) {
    # This variable is needed to avoid the warning: (known compiler issue)
    # warning: comparison of promoted ~unsigned with unsigned [-Wsign-compare]
    inverted = ~data[kMitsubishi136PowerByte + half + i]
    if (data[kMitsubishi136PowerByte + i] != inverted) return False
  }
  return True
}

# Configure the pin for output.
void IRMitsubishi136.begin(void) { _irsend.begin() }

#if SEND_MITSUBISHI136
# Send the current desired state to the IR LED.
void IRMitsubishi136.send(repeat) {
  _irsend.sendMitsubishi136(getRaw(), kMitsubishi136StateLength, repeat)
}
#endif  # SEND_MITSUBISHI136

# Return a pointer to the internal state date of the remote.
*IRMitsubishi136.getRaw(void) {
  checksum()
  return remote_state
}

void IRMitsubishi136.setRaw(*data) {
  memcpy(remote_state, data, kMitsubishi136StateLength)
}

# Set the requested power state of the A/C to off.
void IRMitsubishi136.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRMitsubishi136.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRMitsubishi136.setPower(bool on) {
  setBit(&remote_state[kMitsubishi136PowerByte], kMitsubishi136PowerOffset, on)
}

# Return the requested power state of the A/C.
bool IRMitsubishi136.getPower(void) {
  return GETBIT8(remote_state[kMitsubishi136PowerByte],
                 kMitsubishi136PowerOffset)
}

# Set the temp. in deg C
void IRMitsubishi136.setTemp(degrees) {
  temp = std.max((uint8_t)kMitsubishi136MinTemp, degrees)
  temp = std.min((uint8_t)kMitsubishi136MaxTemp, temp)
  setBits(&remote_state[kMitsubishi136TempByte], kHighNibble, kNibbleSize,
          temp - kMitsubishiAcMinTemp)
}

# Return the set temp. in deg C
IRMitsubishi136.getTemp(void) {
  return GETBITS8(remote_state[kMitsubishi136TempByte], kHighNibble,
                  kNibbleSize) + kMitsubishiAcMinTemp
}

void IRMitsubishi136.setFan(speed) {
  setBits(&remote_state[kMitsubishi136FanByte], kMitsubishi136FanOffset,
          kMitsubishi136FanSize, std.min(speed, kMitsubishi136FanMax))
}

# Return the requested state of the unit's fan.
IRMitsubishi136.getFan(void) {
  return GETBITS8(remote_state[kMitsubishi136FanByte], kMitsubishi136FanOffset,
                  kMitsubishi136FanSize)
}

# Return the requested climate operation mode of the a/c unit.
IRMitsubishi136.getMode(void) {
  return GETBITS8(remote_state[kMitsubishi136ModeByte],
                  kMitsubishi136ModeOffset, kModeBitsSize)
}

# Set the requested climate operation mode of the a/c unit.
void IRMitsubishi136.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    case kMitsubishi136Fan:
    case kMitsubishi136Cool:
    case kMitsubishi136Heat:
    case kMitsubishi136Auto:
    case kMitsubishi136Dry:
      setBits(&remote_state[kMitsubishi136ModeByte], kMitsubishi136ModeOffset,
              kModeBitsSize, mode)
      break
    default:
      setMode(kMitsubishi136Auto)
  }
}

# Set the requested vane operation mode of the a/c unit.
void IRMitsubishi136.setSwingV(position) {
  # If we get an unexpected mode, default to auto.
  switch (position) {
    case kMitsubishi136SwingVLowest:
    case kMitsubishi136SwingVLow:
    case kMitsubishi136SwingVHigh:
    case kMitsubishi136SwingVHighest:
    case kMitsubishi136SwingVAuto:
      setBits(&remote_state[kMitsubishi136SwingVByte], kHighNibble, kNibbleSize,
              position)
      break
    default:
      setMode(kMitsubishi136SwingVAuto)
  }
}

# Return the requested vane operation mode of the a/c unit.
IRMitsubishi136.getSwingV(void) {
  return GETBITS8(remote_state[kMitsubishi136SwingVByte], kHighNibble,
                  kNibbleSize)
}

# Emulate a quiet setting. There is no True quiet setting on this a/c
void IRMitsubishi136.setQuiet(bool on) {
  if (on) setFan(kMitsubishi136FanQuiet)
  else if (getQuiet()) setFan(kMitsubishi136FanLow)
}

# Return the requested power state of the A/C.
bool IRMitsubishi136.getQuiet(void) {
  return getFan() == kMitsubishi136FanQuiet
}

# Convert a standard A/C mode into its native mode.
IRMitsubishi136.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kMitsubishi136Cool
    case stdAc.opmode_t.kHeat: return kMitsubishi136Heat
    case stdAc.opmode_t.kDry:  return kMitsubishi136Dry
    case stdAc.opmode_t.kFan:  return kMitsubishi136Fan
    default:                     return kMitsubishi136Auto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMitsubishi136.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin: return kMitsubishi136FanMin
    case stdAc.fanspeed_t.kLow: return kMitsubishi136FanLow
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax: return kMitsubishi136FanMax
    default:                      return kMitsubishi136FanMed
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishi136.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kHighest: return kMitsubishi136SwingVHighest
    case stdAc.swingv_t.kHigh:
    case stdAc.swingv_t.kMiddle:  return kMitsubishi136SwingVHigh
    case stdAc.swingv_t.kLow:     return kMitsubishi136SwingVLow
    case stdAc.swingv_t.kLowest:  return kMitsubishi136SwingVLowest
    default:                        return kMitsubishi136SwingVAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRMitsubishi136.toCommonMode(mode) {
  switch (mode) {
    case kMitsubishi136Cool: return stdAc.opmode_t.kCool
    case kMitsubishi136Heat: return stdAc.opmode_t.kHeat
    case kMitsubishi136Dry:  return stdAc.opmode_t.kDry
    case kMitsubishi136Fan:  return stdAc.opmode_t.kFan
    default:                 return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMitsubishi136.toCommonFanSpeed(speed) {
  switch (speed) {
    case kMitsubishi136FanMax: return stdAc.fanspeed_t.kMax
    case kMitsubishi136FanMed: return stdAc.fanspeed_t.kMedium
    case kMitsubishi136FanLow: return stdAc.fanspeed_t.kLow
    case kMitsubishi136FanMin: return stdAc.fanspeed_t.kMin
    default:                   return stdAc.fanspeed_t.kMedium
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRMitsubishi136.toCommonSwingV(pos) {
  switch (pos) {
    case kMitsubishi136SwingVHighest: return stdAc.swingv_t.kHighest
    case kMitsubishi136SwingVHigh:    return stdAc.swingv_t.kHigh
    case kMitsubishi136SwingVLow:     return stdAc.swingv_t.kLow
    case kMitsubishi136SwingVLowest:  return stdAc.swingv_t.kLowest
    default:                          return stdAc.swingv_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMitsubishi136.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.MITSUBISHI136
  result.model = -1  # No models used.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->toCommonSwingV(this->getSwingV())
  result.quiet = this->getQuiet()
  # Not supported.
  result.swingh = stdAc.swingh_t.kOff
  result.turbo = False
  result.clean = False
  result.econo = False
  result.filter = False
  result.light = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRMitsubishi136.toString(void) {
  String result = ""
  result.reserve(80)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kMitsubishi136Auto, kMitsubishi136Cool,
                            kMitsubishi136Heat, kMitsubishi136Dry,
                            kMitsubishi136Fan)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kMitsubishi136FanMax,
                           kMitsubishi136FanLow,  kMitsubishi136FanMax,
                           kMitsubishi136FanQuiet, kMitsubishi136FanMed)
  result += addIntToString(getSwingV(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (getSwingV()) {
    case kMitsubishi136SwingVHighest: result += kHighestStr break
    case kMitsubishi136SwingVHigh: result += kHighStr break
    case kMitsubishi136SwingVLow: result += kLowStr break
    case kMitsubishi136SwingVLowest: result += kLowestStr break
    case kMitsubishi136SwingVAuto: result += kAutoStr break
    default: result += kUnknownStr
  }
  result += ')'
  result += addBoolToString(getQuiet(), kQuietStr)
  return result
}


#if SEND_MITSUBISHI112
# Send a Mitsubishi112 A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kMitsubishi112StateLength)
#   repeat: Nr. of times the message is to be repeated.
#          (Default = kMitsubishi112MinRepeat).
#
# Status: Stable / Reported as working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/947
void IRsend.sendMitsubishi112(unsigned char data[],
                               nbytes,
                               repeat) {
  if (nbytes < kMitsubishi112StateLength)
    return  # Not enough bytes to send a proper message.

  sendGeneric(kMitsubishi112HdrMark, kMitsubishi112HdrSpace,
              kMitsubishi112BitMark, kMitsubishi112OneSpace,
              kMitsubishi112BitMark, kMitsubishi112ZeroSpace,
              kMitsubishi112BitMark, kMitsubishi112Gap,
              data, nbytes, 38, False, repeat, 50)
}
#endif  # SEND_MITSUBISHI112

#if DECODE_MITSUBISHI112 or DECODE_TCL112AC
# Decode the supplied Mitsubishi112 / Tcl112Ac message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Reported as working.
#
# Note: Mitsubishi112 & Tcl112Ac are basically the same protocol.
#       The only significant difference I can see is Mitsubishi112 has a
#       slightly longer header mark. We will use that to determine which
#       varient it should be. The other differences require full decoding and
#       only only with certain settings.
#       There are some other timing differences too, but the tolerances will
#       overlap.
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/619
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/947
bool IRrecv.decodeMitsubishi112(decode_results *results, nbits,
                                 bool strict) {
  if (results->rawlen < ((2 * nbits) + kHeader + kFooter - 1)) return False
  if (nbits % 8 != 0) return False  # Not a multiple of an 8 bit byte.
  if (strict) {  # Do checks to see if it matches the spec.
    if (nbits != kMitsubishi112Bits and nbits != kTcl112AcBits) return False
  }
  offset = kStartOffset
  decode_type_t typeguess = decode_type_t.UNKNOWN
  hdrspace
  bitmark
  onespace
  zerospace
  gap
  tolerance = _tolerance

  # Header
#if DECODE_MITSUBISHI112
  if (matchMark(results->rawbuf[offset], kMitsubishi112HdrMark,
                kMitsubishi112HdrMarkTolerance, 0)) {
    typeguess = decode_type_t.MITSUBISHI112
    hdrspace = kMitsubishi112HdrSpace
    bitmark = kMitsubishi112BitMark
    onespace = kMitsubishi112OneSpace
    zerospace = kMitsubishi112ZeroSpace
    gap = kMitsubishi112Gap
  }
#endif  # DECODE_MITSUBISHI112
#if DECODE_TCL112AC
  if (typeguess == decode_type_t.UNKNOWN and  # We didn't match Mitsubishi112
      matchMark(results->rawbuf[offset], kTcl112AcHdrMark,
                kTcl112AcHdrMarkTolerance, 0)) {
    typeguess = decode_type_t.TCL112AC
    hdrspace = kTcl112AcHdrSpace
    bitmark = kTcl112AcBitMark
    onespace = kTcl112AcOneSpace
    zerospace = kTcl112AcZeroSpace
    gap = kTcl112AcGap
    tolerance += kTcl112AcTolerance
  }
#endif  # DECODE_TCL112AC
  if (typeguess == decode_type_t.UNKNOWN) return False  # No header matched.
  offset++

  used = matchGeneric(results->rawbuf + offset, results->state,
                               results->rawlen - offset, nbits,
                               0,  # Skip the header as we matched it earlier.
                               hdrspace, bitmark, onespace, bitmark, zerospace,
                               bitmark, gap,
                               True, tolerance, 0, False)
  if (!used) return False
  if (strict) {
    # Header validation: Codes start with 0x23CB26
    if (results->state[0] != 0x23 or results->state[1] != 0xCB or
        results->state[2] != 0x26) return False
    # TCL112 and MITSUBISHI112 share the exact same checksum.
    if (!IRTcl112Ac.validChecksum(results->state, nbits / 8)) return False
  }
  # Success
  results->decode_type = typeguess
  results->bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result->state, we don't record value, address, or command as it
  # is a union data type.
  return True
}
#endif  # DECODE_MITSUBISHI112 or DECODE_TCL112AC

# Code to emulate Mitsubishi 112bit A/C IR remote control unit.
#
# Equipment it seems compatible with:
#   Brand: Mitsubishi Electric,  Model: MSH-A24WV / MUH-A24WV A/C
#   Brand: Mitsubishi Electric,  Model: KPOA remote

# Initialise the object.
IRMitsubishi112.IRMitsubishi112(pin, bool inverted,
                                 bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRMitsubishi112.stateReset(void) {
  kReset[kMitsubishi112StateLength] = {
      0x23, 0xCB, 0x26, 0x01, 0x00, 0x24, 0x03, 0x0B, 0x10,
      0x00, 0x00, 0x00, 0x30}
  setRaw(kReset)
}

# Calculate the checksum for the current internal state of the remote.
void IRMitsubishi112.checksum(void) {
  remote_state[kMitsubishi112StateLength - 1] = IRTcl112Ac.calcChecksum(
      remote_state, kMitsubishi112StateLength)
}

# Configure the pin for output.
void IRMitsubishi112.begin(void) { _irsend.begin() }

#if SEND_MITSUBISHI112
# Send the current desired state to the IR LED.
void IRMitsubishi112.send(repeat) {
  _irsend.sendMitsubishi112(getRaw(), kMitsubishi112StateLength, repeat)
}
#endif  # SEND_MITSUBISHI112

# Return a pointer to the internal state date of the remote.
*IRMitsubishi112.getRaw(void) {
  checksum()
  return remote_state
}

void IRMitsubishi112.setRaw(*data) {
  memcpy(remote_state, data, kMitsubishi112StateLength)
}

# Set the requested power state of the A/C to off.
void IRMitsubishi112.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRMitsubishi112.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRMitsubishi112.setPower(bool on) {
  setBit(&remote_state[kMitsubishi112PowerByte], kMitsubishi112PowerOffset, on)
}

# Return the requested power state of the A/C.
bool IRMitsubishi112.getPower(void) {
  return GETBIT8(remote_state[kMitsubishi112PowerByte],
                 kMitsubishi112PowerOffset)
}

# Set the temp. in deg C
void IRMitsubishi112.setTemp(degrees) {
  temp = std.max((uint8_t)kMitsubishi112MinTemp, degrees)
  temp = std.min((uint8_t)kMitsubishi112MaxTemp, temp)
  setBits(&remote_state[kMitsubishi112TempByte], kLowNibble,
          kMitsubishi112TempSize, kMitsubishiAcMaxTemp - temp)
}

# Return the set temp. in deg C
IRMitsubishi112.getTemp(void) {
  return kMitsubishiAcMaxTemp - GETBITS8(remote_state[kMitsubishi112TempByte],
                                         kLowNibble, kMitsubishi112TempSize)
}

void IRMitsubishi112.setFan(speed) {
  switch (speed) {
    case kMitsubishi112FanMin:
    case kMitsubishi112FanLow:
    case kMitsubishi112FanMed:
    case kMitsubishi112FanMax:
      setBits(&remote_state[kMitsubishi112FanByte], kMitsubishi112FanOffset,
              kMitsubishi112FanSize, speed)
      break
    default:
      setFan(kMitsubishi112FanMax)
  }
}

# Return the requested state of the unit's fan.
IRMitsubishi112.getFan(void) {
  return GETBITS8(remote_state[kMitsubishi112FanByte], kMitsubishi112FanOffset,
                  kMitsubishi112FanSize)
}

# Return the requested climate operation mode of the a/c unit.
IRMitsubishi112.getMode(void) {
  return GETBITS8(remote_state[kMitsubishi112ModeByte],
                  kMitsubishi112ModeOffset, kModeBitsSize)
}

# Set the requested climate operation mode of the a/c unit.
void IRMitsubishi112.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    # Note: No Fan Only mode.
    case kMitsubishi112Cool:
    case kMitsubishi112Heat:
    case kMitsubishi112Auto:
    case kMitsubishi112Dry:
      setBits(&remote_state[kMitsubishi112ModeByte], kMitsubishi112ModeOffset,
              kModeBitsSize, mode)
      break
    default:
      setMode(kMitsubishi112Auto)
  }
}

# Set the requested vane operation mode of the a/c unit.
void IRMitsubishi112.setSwingV(position) {
  # If we get an unexpected mode, default to auto.
  switch (position) {
    case kMitsubishi112SwingVLowest:
    case kMitsubishi112SwingVLow:
    case kMitsubishi112SwingVMiddle:
    case kMitsubishi112SwingVHigh:
    case kMitsubishi112SwingVHighest:
    case kMitsubishi112SwingVAuto:
      setBits(&remote_state[kMitsubishi112SwingVByte],
              kMitsubishi112SwingVOffset, kMitsubishi112SwingVSize, position)
      break
    default:
      setMode(kMitsubishi112SwingVAuto)
  }
}

# Return the requested vane operation mode of the a/c unit.
IRMitsubishi112.getSwingV(void) {
  return GETBITS8(remote_state[kMitsubishi112SwingVByte],
                  kMitsubishi112SwingVOffset, kMitsubishi112SwingVSize)
}

# Set the requested vane operation mode of the a/c unit.
void IRMitsubishi112.setSwingH(position) {
  # If we get an unexpected mode, default to auto.
  switch (position) {
    case kMitsubishi112SwingHLeftMax:
    case kMitsubishi112SwingHLeft:
    case kMitsubishi112SwingHMiddle:
    case kMitsubishi112SwingHRight:
    case kMitsubishi112SwingHRightMax:
    case kMitsubishi112SwingHWide:
    case kMitsubishi112SwingHAuto:
      setBits(&remote_state[kMitsubishi112SwingHByte],
              kMitsubishi112SwingHOffset, kMitsubishi112SwingHSize, position)
      break
    default:
      setSwingH(kMitsubishi112SwingHAuto)
  }
}

# Return the requested vane operation mode of the a/c unit.
IRMitsubishi112.getSwingH(void) {
  return GETBITS8(remote_state[kMitsubishi112SwingHByte],
                  kMitsubishi112SwingHOffset, kMitsubishi112SwingHSize)
}

# Emulate a quiet setting. There is no True quiet setting on this a/c
void IRMitsubishi112.setQuiet(bool on) {
  if (on)
    setFan(kMitsubishi112FanQuiet)
  else if (getQuiet()) setFan(kMitsubishi112FanLow)
}

# Return the requested power state of the A/C.
bool IRMitsubishi112.getQuiet(void) {
  return getFan() == kMitsubishi112FanQuiet
}


# Convert a standard A/C mode into its native mode.
IRMitsubishi112.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kMitsubishi112Cool
    case stdAc.opmode_t.kHeat: return kMitsubishi112Heat
    case stdAc.opmode_t.kDry: return kMitsubishi112Dry
    # Note: No Fan Only mode.
    default: return kMitsubishi112Auto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMitsubishi112.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin: return kMitsubishi112FanMin
    case stdAc.fanspeed_t.kLow: return kMitsubishi112FanLow
    case stdAc.fanspeed_t.kMedium: return kMitsubishi112FanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax: return kMitsubishi112FanMax
    default: return kMitsubishi112FanMed
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishi112.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kHighest: return kMitsubishi112SwingVHighest
    case stdAc.swingv_t.kHigh: return kMitsubishi112SwingVHigh
    case stdAc.swingv_t.kMiddle: return kMitsubishi112SwingVMiddle
    case stdAc.swingv_t.kLow: return kMitsubishi112SwingVLow
    case stdAc.swingv_t.kLowest: return kMitsubishi112SwingVLowest
    default: return kMitsubishi112SwingVAuto
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishi112.convertSwingH(stdAc.swingh_t position) {
  switch (position) {
    case stdAc.swingh_t.kLeftMax: return kMitsubishi112SwingHLeftMax
    case stdAc.swingh_t.kLeft: return kMitsubishi112SwingHLeft
    case stdAc.swingh_t.kMiddle: return kMitsubishi112SwingHMiddle
    case stdAc.swingh_t.kRight: return kMitsubishi112SwingHRight
    case stdAc.swingh_t.kRightMax: return kMitsubishi112SwingHRightMax
    case stdAc.swingh_t.kWide: return kMitsubishi112SwingHWide
    case stdAc.swingh_t.kAuto: return kMitsubishi112SwingHAuto
    default: return kMitsubishi112SwingHAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRMitsubishi112.toCommonMode(mode) {
  switch (mode) {
    case kMitsubishi112Cool: return stdAc.opmode_t.kCool
    case kMitsubishi112Heat: return stdAc.opmode_t.kHeat
    case kMitsubishi112Dry: return stdAc.opmode_t.kDry
    default: return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMitsubishi112.toCommonFanSpeed(speed) {
  switch (speed) {
    case kMitsubishi112FanMax: return stdAc.fanspeed_t.kMax
    case kMitsubishi112FanMed: return stdAc.fanspeed_t.kMedium
    case kMitsubishi112FanLow: return stdAc.fanspeed_t.kLow
    case kMitsubishi112FanMin: return stdAc.fanspeed_t.kMin
    default: return stdAc.fanspeed_t.kMedium
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRMitsubishi112.toCommonSwingV(pos) {
  switch (pos) {
    case kMitsubishi112SwingVHighest: return stdAc.swingv_t.kHighest
    case kMitsubishi112SwingVHigh:    return stdAc.swingv_t.kHigh
    case kMitsubishi112SwingVMiddle:  return stdAc.swingv_t.kMiddle
    case kMitsubishi112SwingVLow:     return stdAc.swingv_t.kLow
    case kMitsubishi112SwingVLowest:  return stdAc.swingv_t.kLowest
    default:                          return stdAc.swingv_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingh_t IRMitsubishi112.toCommonSwingH(pos) {
  switch (pos) {
    case kMitsubishi112SwingHLeftMax:  return stdAc.swingh_t.kLeftMax
    case kMitsubishi112SwingHLeft:     return stdAc.swingh_t.kLeft
    case kMitsubishi112SwingHMiddle:   return stdAc.swingh_t.kMiddle
    case kMitsubishi112SwingHRight:    return stdAc.swingh_t.kRight
    case kMitsubishi112SwingHRightMax: return stdAc.swingh_t.kRightMax
    case kMitsubishi112SwingHWide:     return stdAc.swingh_t.kWide
    default:                           return stdAc.swingh_t.kAuto
  }
}


# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMitsubishi112.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.MITSUBISHI112
  result.model = -1  # No models used.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->toCommonSwingV(this->getSwingV())
  result.swingh = this->toCommonSwingH(this->getSwingH())
  result.quiet = this->getQuiet()
  # Not supported.
  result.econo = False  # Need to figure this part from stdAc
  result.clock = -1
  result.sleep = -1
  result.turbo = False
  result.clean = False
  result.filter = False
  result.light = False
  result.beep = False


  return result
}

# Convert the internal state into a human readable string.
String IRMitsubishi112.toString(void) {
  String result = ""
  result.reserve(80)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kMitsubishi112Auto, kMitsubishi112Cool,
                            kMitsubishi112Heat, kMitsubishi112Dry,
                            kMitsubishi112Auto)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kMitsubishi112FanMax,
                           kMitsubishi112FanLow,  kMitsubishi112FanMax,
                           kMitsubishi112FanQuiet, kMitsubishi112FanMed)
  result += addIntToString(getSwingV(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (getSwingV()) {
    case kMitsubishi112SwingVHighest: result += kHighestStr break
    case kMitsubishi112SwingVHigh:    result += kHighStr break
    case kMitsubishi112SwingVMiddle:  result += kMiddleStr break
    case kMitsubishi112SwingVLow:     result += kLowStr break
    case kMitsubishi112SwingVLowest:  result += kLowestStr break
    case kMitsubishi112SwingVAuto:    result += kAutoStr break
    default:                          result += kUnknownStr
  }
  result += ')'
  result += addIntToString(getSwingH(), kSwingHStr)
  result += kSpaceLBraceStr
  switch (getSwingH()) {
    case kMitsubishi112SwingHLeftMax:  result += kLeftMaxStr break
    case kMitsubishi112SwingHLeft:     result += kLeftStr break
    case kMitsubishi112SwingHMiddle:   result += kMiddleStr break
    case kMitsubishi112SwingHRight:    result += kRightStr break
    case kMitsubishi112SwingHRightMax: result += kRightMaxStr break
    case kMitsubishi112SwingHWide:     result += kWideStr break
    case kMitsubishi112SwingHAuto:     result += kAutoStr break
    default:                           result += kUnknownStr
  }
  result += ')'
  result += addBoolToString(getQuiet(), kQuietStr)
  return result
}
