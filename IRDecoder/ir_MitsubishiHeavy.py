"""
# Copyright 2019 David Conran

# Supports:
#   Brand: Mitsubishi Heavy Industries,  Model: RLA502A700B remote
#   Brand: Mitsubishi Heavy Industries,  Model: SRKxxZM-S A/C
#   Brand: Mitsubishi Heavy Industries,  Model: SRKxxZMXA-S A/C
#   Brand: Mitsubishi Heavy Industries,  Model: RKX502A001C remote
#   Brand: Mitsubishi Heavy Industries,  Model: SRKxxZJ-S A/C

#ifndef IR_MITSUBISHIHEAVY_H_
#define IR_MITSUBISHIHEAVY_H_

#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/660
#   https:#github.com/ToniA/Raw-IR-decoder-for-Arduino/blob/master/MitsubishiHeavy.cpp
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/MitsubishiHeavyHeatpumpIR.cpp

# Constants.
kMitsubishiHeavySigLength = 5


# ZMS (152 bit)
kMitsubishiHeavyZmsSig[kMitsubishiHeavySigLength] = {
    0xAD, 0x51, 0x3C, 0xE5, 0x1A}
# Byte[5]
kMitsubishiHeavyModeOffset = 0
#                           Mode Mask =      0b00000111  # Byte 9 on ZJS
kMitsubishiHeavyAuto = 0         # 0b000
kMitsubishiHeavyCool = 1         # 0b001
kMitsubishiHeavyDry =  2         # 0b010
kMitsubishiHeavyFan =  3         # 0b011
kMitsubishiHeavyHeat = 4         # 0b100
kMitsubishiHeavyPowerOffset = 3  # Byte 9 on ZJS
kMitsubishiHeavyCleanOffset = 5
kMitsubishiHeavyFilterOffset = 6
# Byte[7]
kMitsubishiHeavyMinTemp = 17   # 17C
kMitsubishiHeavyMaxTemp = 31   # 31C
# Byte[9]
#                               FanMask =       0b00001111  # ~Byte 7 on ZJS.
kMitsubishiHeavy152FanAuto =  0x0  # 0b0000
kMitsubishiHeavy152FanLow =   0x1  # 0b0001
kMitsubishiHeavy152FanMed =   0x2  # 0b0010
kMitsubishiHeavy152FanHigh =  0x3  # 0b0011
kMitsubishiHeavy152FanMax =   0x4  # 0b0100
kMitsubishiHeavy152FanEcono = 0x6  # 0b0110
kMitsubishiHeavy152FanTurbo = 0x8  # 0b1000
# Byte[11]
kMitsubishiHeavy3DMask =        0b00010010
kMitsubishiHeavy152SwingVOffset = 5
kMitsubishiHeavy152SwingVSize = 3  # Bits
kMitsubishiHeavy152SwingVAuto =    0  # 0b000
kMitsubishiHeavy152SwingVHighest = 1  # 0b001
kMitsubishiHeavy152SwingVHigh =    2  # 0b010
kMitsubishiHeavy152SwingVMiddle =  3  # 0b011
kMitsubishiHeavy152SwingVLow =     4  # 0b100
kMitsubishiHeavy152SwingVLowest =  5  # 0b101
kMitsubishiHeavy152SwingVOff =     6  # 0b110
# Byte[13]
kMitsubishiHeavy152SwingHAuto =      0  # 0b0000
kMitsubishiHeavy152SwingHLeftMax =   1  # 0b0001
kMitsubishiHeavy152SwingHLeft =      2  # 0b0010
kMitsubishiHeavy152SwingHMiddle =    3  # 0b0011
kMitsubishiHeavy152SwingHRight =     4  # 0b0100
kMitsubishiHeavy152SwingHRightMax =  5  # 0b0101
kMitsubishiHeavy152SwingHRightLeft = 6  # 0b0110
kMitsubishiHeavy152SwingHLeftRight = 7  # 0b0111
kMitsubishiHeavy152SwingHOff =       8  # 0b1000
# Byte[15]
kMitsubishiHeavyNightOffset = 6
kMitsubishiHeavySilentOffset = 7


# ZJS (88 bit)
kMitsubishiHeavyZjsSig[kMitsubishiHeavySigLength] = {
    0xAD, 0x51, 0x3C, 0xD9, 0x26}
# Byte [5]
kMitsubishiHeavy88CleanOffset = 5
kMitsubishiHeavy88SwingHOffset1 = 2
kMitsubishiHeavy88SwingHOffset2 = 6
kMitsubishiHeavy88SwingHSize = 2  # Bits (per offset)
kMitsubishiHeavy88SwingHOff =       0b0000
kMitsubishiHeavy88SwingHAuto =      0b1000
kMitsubishiHeavy88SwingHLeftMax =   0b0001
kMitsubishiHeavy88SwingHLeft =      0b0101
kMitsubishiHeavy88SwingHMiddle =    0b1001
kMitsubishiHeavy88SwingHRight =     0b1101
kMitsubishiHeavy88SwingHRightMax =  0b0010
kMitsubishiHeavy88SwingHRightLeft = 0b1010
kMitsubishiHeavy88SwingHLeftRight = 0b0110
kMitsubishiHeavy88SwingH3D =        0b1110
# Byte[7]
kMitsubishiHeavy88FanOffset = 5
kMitsubishiHeavy88FanSize = 3  # Bits
kMitsubishiHeavy88FanAuto =  0  # 0b000
kMitsubishiHeavy88FanLow =   2  # 0b010
kMitsubishiHeavy88FanMed =   3  # 0b011
kMitsubishiHeavy88FanHigh =  4  # 0b100
kMitsubishiHeavy88FanTurbo = 6  # 0b110
kMitsubishiHeavy88FanEcono = 7  # 0b111
kMitsubishiHeavy88SwingVByte5Offset = 1
kMitsubishiHeavy88SwingVByte5Size = 1
kMitsubishiHeavy88SwingVByte7Offset = 3
kMitsubishiHeavy88SwingVByte7Size = 2

                                          # Mask 0b111
kMitsubishiHeavy88SwingVOff =       0b000  # 0
kMitsubishiHeavy88SwingVAuto =      0b100  # 4
kMitsubishiHeavy88SwingVHighest =   0b110  # 6
kMitsubishiHeavy88SwingVHigh =      0b001  # 1
kMitsubishiHeavy88SwingVMiddle =    0b011  # 3
kMitsubishiHeavy88SwingVLow =       0b101  # 5
kMitsubishiHeavy88SwingVLowest =    0b111  # 7
# Byte[9] is Power & Mode & Temp.


# Classes
class IRMitsubishiHeavy152Ac {
 public:
  explicit IRMitsubishiHeavy152Ac(pin,
                                  bool inverted = False,
                                  bool use_modulation = True)

  void stateReset(void)
#if SEND_MITSUBISHIHEAVY
  void send(repeat = kMitsubishiHeavy152MinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_MITSUBISHIHEAVY
  void begin(void)
  void on(void)
  void off(void)

  void setPower(bool on)
  bool getPower(void)

  void setTemp(temp)
  getTemp(void)

  void setFan(fan)
  getFan(void)

  void setMode(mode)
  getMode(void)

  void setSwingVertical(pos)
  getSwingVertical(void)
  void setSwingHorizontal(pos)
  getSwingHorizontal(void)

  void setNight(bool on)
  bool getNight(void)

  void set3D(bool on)
  bool get3D(void)

  void setSilent(bool on)
  bool getSilent(void)

  void setFilter(bool on)
  bool getFilter(void)

  void setClean(bool on)
  bool getClean(void)

  void setTurbo(bool on)
  bool getTurbo(void)

  void setEcono(bool on)
  bool getEcono(void)

  uint8_t* getRaw(void)
  void setRaw(uint8_t* data)

  static bool checkZmsSig(*state)
  static bool validChecksum(
      *state,
      length = kMitsubishiHeavy152StateLength)
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
#else  # UNIT_TEST
  IRsendTest _irsend
#endif  # UNIT_TEST
  # The state of the IR remote in IR code form.
  remote_state[kMitsubishiHeavy152StateLength]
  void checksum(void)
}

class IRMitsubishiHeavy88Ac {
 public:
  explicit IRMitsubishiHeavy88Ac(pin,
                                 bool inverted = False,
                                 bool use_modulation = True)

  void stateReset(void)
#if SEND_MITSUBISHIHEAVY
  void send(repeat = kMitsubishiHeavy88MinRepeat)
#endif  # SEND_MITSUBISHIHEAVY
  void begin(void)
  void on(void)
  void off(void)

  void setPower(bool on)
  bool getPower(void)

  void setTemp(temp)
  getTemp(void)

  void setFan(fan)
  getFan(void)

  void setMode(mode)
  getMode(void)

  void setSwingVertical(pos)
  getSwingVertical(void)
  void setSwingHorizontal(pos)
  getSwingHorizontal(void)

  void setTurbo(bool on)
  bool getTurbo(void)

  void setEcono(bool on)
  bool getEcono(void)

  void set3D(bool on)
  bool get3D(void)

  void setClean(bool on)
  bool getClean(void)

  uint8_t* getRaw(void)
  void setRaw(uint8_t* data)

  static bool checkZjsSig(*state)
  static bool validChecksum(
      *state,
      length = kMitsubishiHeavy88StateLength)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static convertSwingV(stdAc.swingv_t position)
  static convertSwingH(stdAc.swingh_t position)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static stdAc.swingv_t toCommonSwingV(pos)
  static stdAc.swingh_t toCommonSwingH(pos)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else  # UNIT_TEST
  IRsendTest _irsend
#endif  # UNIT_TEST
  # The state of the IR remote in IR code form.
  remote_state[kMitsubishiHeavy152StateLength]
  void checksum(void)
}
#endif  # IR_MITSUBISHIHEAVY_H_

"""
# Copyright 2019 David Conran
# Mitsubishi Heavy Industries A/C remote emulation.

# Code to emulate Mitsubishi Heavy Industries A/C IR remote control units,
# which should control at least the following A/C units:
#   Remote Control RLA502A700B:
#     Model SRKxxZM-S
#     Model SRKxxZMXA-S
#   Remote Control RKX502A001C:
#     Model SRKxxZJ-S

# Note: This code was *heavily* influenced by @ToniA's great work & code,
#       but it has been written from scratch.
#       Nothing was copied other than constants and message analysis.

#include "ir_MitsubishiHeavy.h"
#include <algorithm>
#include <cstring>
#include "IRremoteESP8266.h"
#include "IRtext.h"
#include "IRutils.h"
#ifndef ARDUINO
#include <string>
#endif

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/660
#   https:#github.com/ToniA/Raw-IR-decoder-for-Arduino/blob/master/MitsubishiHeavy.cpp
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/MitsubishiHeavyHeatpumpIR.cpp

# Constants
kMitsubishiHeavyHdrMark = 3140
kMitsubishiHeavyHdrSpace = 1630
kMitsubishiHeavyBitMark = 370
kMitsubishiHeavyOneSpace = 420
kMitsubishiHeavyZeroSpace = 1220
kMitsubishiHeavyGap = kDefaultMessageGap  # Just a guess.

using irutils.addBoolToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_MITSUBISHIHEAVY
# Send a MitsubishiHeavy 88 bit A/C message.
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kMitsubishiHeavy88Bits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: BETA / Appears to be working. Needs testing against a real device.
void IRsend.sendMitsubishiHeavy88(unsigned char data[],
                                   nbytes,
                                   repeat) {
  if (nbytes < kMitsubishiHeavy88StateLength)
    return  # Not enough bytes to send a proper message.
  sendGeneric(kMitsubishiHeavyHdrMark, kMitsubishiHeavyHdrSpace,
              kMitsubishiHeavyBitMark, kMitsubishiHeavyOneSpace,
              kMitsubishiHeavyBitMark, kMitsubishiHeavyZeroSpace,
              kMitsubishiHeavyBitMark, kMitsubishiHeavyGap,
              data, nbytes, 38000, False, repeat, kDutyDefault)
}

# Send a MitsubishiHeavy 152 bit A/C message.
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kMitsubishiHeavy152Bits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: BETA / Appears to be working. Needs testing against a real device.
void IRsend.sendMitsubishiHeavy152(unsigned char data[],
                                    nbytes,
                                    repeat) {
  if (nbytes < kMitsubishiHeavy152StateLength)
    return  # Not enough bytes to send a proper message.
  sendMitsubishiHeavy88(data, nbytes, repeat)
}
#endif  # SEND_MITSUBISHIHEAVY

# Class for decoding and constructing MitsubishiHeavy152 AC messages.
IRMitsubishiHeavy152Ac.IRMitsubishiHeavy152Ac(pin,
                                               bool inverted,
                                               bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { stateReset() }

void IRMitsubishiHeavy152Ac.begin(void) { _irsend.begin() }

#if SEND_MITSUBISHIHEAVY
void IRMitsubishiHeavy152Ac.send(repeat) {
  _irsend.sendMitsubishiHeavy152(this->getRaw(), kMitsubishiHeavy152StateLength,
                                 repeat)
}
#endif  # SEND_MITSUBISHIHEAVY

void IRMitsubishiHeavy152Ac.stateReset(void) {
  memcpy(remote_state, kMitsubishiHeavyZmsSig, kMitsubishiHeavySigLength)
  for (i = kMitsubishiHeavySigLength
       i < kMitsubishiHeavy152StateLength - 3 i += 2) remote_state[i] = 0
  remote_state[17] = 0x80
}

*IRMitsubishiHeavy152Ac.getRaw(void) {
  checksum()
  return remote_state
}

void IRMitsubishiHeavy152Ac.setRaw(*data) {
  memcpy(remote_state, data, kMitsubishiHeavy152StateLength)
}

void IRMitsubishiHeavy152Ac.on(void) { setPower(True) }

void IRMitsubishiHeavy152Ac.off(void) { setPower(False) }

void IRMitsubishiHeavy152Ac.setPower(bool on) {
  setBit(&remote_state[5], kMitsubishiHeavyPowerOffset, on)
}

bool IRMitsubishiHeavy152Ac.getPower(void) {
  return GETBIT8(remote_state[5], kMitsubishiHeavyPowerOffset)
}

void IRMitsubishiHeavy152Ac.setTemp(temp) {
  newtemp = temp
  newtemp = std.min(newtemp, kMitsubishiHeavyMaxTemp)
  newtemp = std.max(newtemp, kMitsubishiHeavyMinTemp)
  setBits(&remote_state[7], kLowNibble, kNibbleSize,
          newtemp - kMitsubishiHeavyMinTemp)
}

IRMitsubishiHeavy152Ac.getTemp(void) {
  return GETBITS8(remote_state[7], kLowNibble, kNibbleSize) +
      kMitsubishiHeavyMinTemp
}

# Set the speed of the fan
void IRMitsubishiHeavy152Ac.setFan(speed) {
  newspeed = speed
  switch (speed) {
    case kMitsubishiHeavy152FanLow:
    case kMitsubishiHeavy152FanMed:
    case kMitsubishiHeavy152FanHigh:
    case kMitsubishiHeavy152FanMax:
    case kMitsubishiHeavy152FanEcono:
    case kMitsubishiHeavy152FanTurbo: break
    default: newspeed = kMitsubishiHeavy152FanAuto
  }
  setBits(&remote_state[9], kLowNibble, kNibbleSize, newspeed)
}

IRMitsubishiHeavy152Ac.getFan(void) {
  return GETBITS8(remote_state[9], kLowNibble, kNibbleSize)
}

void IRMitsubishiHeavy152Ac.setMode(mode) {
  newmode = mode
  switch (mode) {
    case kMitsubishiHeavyCool:
    case kMitsubishiHeavyDry:
    case kMitsubishiHeavyFan:
    case kMitsubishiHeavyHeat:
      break
    default:
      newmode = kMitsubishiHeavyAuto
  }
  setBits(&remote_state[5], kMitsubishiHeavyModeOffset, kModeBitsSize, newmode)
}

IRMitsubishiHeavy152Ac.getMode(void) {
  return GETBITS8(remote_state[5], kMitsubishiHeavyModeOffset, kModeBitsSize)
}

void IRMitsubishiHeavy152Ac.setSwingVertical(pos) {
  setBits(&remote_state[11], kMitsubishiHeavy152SwingVOffset,
          kMitsubishiHeavy152SwingVSize,
          std.min(pos, kMitsubishiHeavy152SwingVOff))
}

IRMitsubishiHeavy152Ac.getSwingVertical(void) {
  return GETBITS8(remote_state[11], kMitsubishiHeavy152SwingVOffset,
                  kMitsubishiHeavy152SwingVSize)
}

void IRMitsubishiHeavy152Ac.setSwingHorizontal(pos) {
  setBits(&remote_state[13], kLowNibble, kNibbleSize,
          std.min(pos, kMitsubishiHeavy152SwingHOff))
}

IRMitsubishiHeavy152Ac.getSwingHorizontal(void) {
  return GETBITS8(remote_state[13], kLowNibble, kNibbleSize)
}

void IRMitsubishiHeavy152Ac.setNight(bool on) {
  setBit(&remote_state[15], kMitsubishiHeavyNightOffset, on)
}

bool IRMitsubishiHeavy152Ac.getNight(void) {
  return GETBIT8(remote_state[15], kMitsubishiHeavyNightOffset)
}

void IRMitsubishiHeavy152Ac.set3D(bool on) {
  if (on)
    remote_state[11] |= kMitsubishiHeavy3DMask
  else
    remote_state[11] &= ~kMitsubishiHeavy3DMask
}

bool IRMitsubishiHeavy152Ac.get3D(void) {
  return (remote_state[11] & kMitsubishiHeavy3DMask) == kMitsubishiHeavy3DMask
}

void IRMitsubishiHeavy152Ac.setSilent(bool on) {
  setBit(&remote_state[15], kMitsubishiHeavySilentOffset, on)
}

bool IRMitsubishiHeavy152Ac.getSilent(void) {
  return GETBIT8(remote_state[15], kMitsubishiHeavySilentOffset)
}

void IRMitsubishiHeavy152Ac.setFilter(bool on) {
  setBit(&remote_state[5], kMitsubishiHeavyFilterOffset, on)
}

bool IRMitsubishiHeavy152Ac.getFilter(void) {
  return GETBIT8(remote_state[5], kMitsubishiHeavyFilterOffset)
}

void IRMitsubishiHeavy152Ac.setClean(bool on) {
  this->setFilter(on)
  setBit(&remote_state[5], kMitsubishiHeavyCleanOffset, on)
}

bool IRMitsubishiHeavy152Ac.getClean(void) {
  return GETBIT8(remote_state[5], kMitsubishiHeavyCleanOffset) and getFilter()
}

void IRMitsubishiHeavy152Ac.setTurbo(bool on) {
  if (on)
    this->setFan(kMitsubishiHeavy152FanTurbo)
  else if (this->getTurbo()) this->setFan(kMitsubishiHeavy152FanAuto)
}

bool IRMitsubishiHeavy152Ac.getTurbo(void) {
  return this->getFan() == kMitsubishiHeavy152FanTurbo
}

void IRMitsubishiHeavy152Ac.setEcono(bool on) {
  if (on)
    this->setFan(kMitsubishiHeavy152FanEcono)
  else if (this->getEcono()) this->setFan(kMitsubishiHeavy152FanAuto)
}

bool IRMitsubishiHeavy152Ac.getEcono(void) {
  return this->getFan() == kMitsubishiHeavy152FanEcono
}

# Verify the given state has a ZM-S signature.
bool IRMitsubishiHeavy152Ac.checkZmsSig(*state) {
  for (i = 0 i < kMitsubishiHeavySigLength i++)
    if (state[i] != kMitsubishiHeavyZmsSig[i]) return False
  return True
}

# Protocol technically has no checksum, but does has inverted byte pairs.
void IRMitsubishiHeavy152Ac.checksum(void) {
  for (i = kMitsubishiHeavySigLength - 2
       i < kMitsubishiHeavy152StateLength
       i += 2) {
    remote_state[i + 1] = ~remote_state[i]
  }
}

# Protocol technically has no checksum, but does has inverted byte pairs.
bool IRMitsubishiHeavy152Ac.validChecksum(*state,
                                           length) {
  # Assume anything too short is fine.
  if (length < kMitsubishiHeavySigLength) return True
  # Check all the byte pairs.
  for (i = kMitsubishiHeavySigLength - 2
       i < length
       i += 2) {
    # XOR of a byte and it's self inverted should be 0xFF
    if ((state[i] ^ state[i + 1]) != 0xFF) return False
  }
  return True
}

# Convert a standard A/C mode into its native mode.
IRMitsubishiHeavy152Ac.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kMitsubishiHeavyCool
    case stdAc.opmode_t.kHeat: return kMitsubishiHeavyHeat
    case stdAc.opmode_t.kDry:  return kMitsubishiHeavyDry
    case stdAc.opmode_t.kFan:  return kMitsubishiHeavyFan
    default:                     return kMitsubishiHeavyAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMitsubishiHeavy152Ac.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    # Assumes Econo is slower than Low.
    case stdAc.fanspeed_t.kMin:    return kMitsubishiHeavy152FanEcono
    case stdAc.fanspeed_t.kLow:    return kMitsubishiHeavy152FanLow
    case stdAc.fanspeed_t.kMedium: return kMitsubishiHeavy152FanMed
    case stdAc.fanspeed_t.kHigh:   return kMitsubishiHeavy152FanHigh
    case stdAc.fanspeed_t.kMax:    return kMitsubishiHeavy152FanMax
    default:                         return kMitsubishiHeavy152FanAuto
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishiHeavy152Ac.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kAuto:    return kMitsubishiHeavy152SwingVAuto
    case stdAc.swingv_t.kHighest: return kMitsubishiHeavy152SwingVHighest
    case stdAc.swingv_t.kHigh:    return kMitsubishiHeavy152SwingVHigh
    case stdAc.swingv_t.kMiddle:  return kMitsubishiHeavy152SwingVMiddle
    case stdAc.swingv_t.kLow:     return kMitsubishiHeavy152SwingVLow
    case stdAc.swingv_t.kLowest:  return kMitsubishiHeavy152SwingVLowest
    default:                        return kMitsubishiHeavy152SwingVOff
  }
}

# Convert a standard A/C horizontal swing into its native setting.
IRMitsubishiHeavy152Ac.convertSwingH(stdAc.swingh_t position) {
  switch (position) {
    case stdAc.swingh_t.kAuto:     return kMitsubishiHeavy152SwingHAuto
    case stdAc.swingh_t.kLeftMax:  return kMitsubishiHeavy152SwingHLeftMax
    case stdAc.swingh_t.kLeft:     return kMitsubishiHeavy152SwingHLeft
    case stdAc.swingh_t.kMiddle:   return kMitsubishiHeavy152SwingHMiddle
    case stdAc.swingh_t.kRight:    return kMitsubishiHeavy152SwingHRight
    case stdAc.swingh_t.kRightMax: return kMitsubishiHeavy152SwingHRightMax
    default:                         return kMitsubishiHeavy152SwingHOff
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRMitsubishiHeavy152Ac.toCommonMode(mode) {
  switch (mode) {
    case kMitsubishiHeavyCool: return stdAc.opmode_t.kCool
    case kMitsubishiHeavyHeat: return stdAc.opmode_t.kHeat
    case kMitsubishiHeavyDry:  return stdAc.opmode_t.kDry
    case kMitsubishiHeavyFan:  return stdAc.opmode_t.kFan
    default:                   return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMitsubishiHeavy152Ac.toCommonFanSpeed(spd) {
  switch (spd) {
    case kMitsubishiHeavy152FanMax:   return stdAc.fanspeed_t.kMax
    case kMitsubishiHeavy152FanHigh:  return stdAc.fanspeed_t.kHigh
    case kMitsubishiHeavy152FanMed:   return stdAc.fanspeed_t.kMedium
    case kMitsubishiHeavy152FanLow:   return stdAc.fanspeed_t.kLow
    case kMitsubishiHeavy152FanEcono: return stdAc.fanspeed_t.kMin
    default:                          return stdAc.fanspeed_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingh_t IRMitsubishiHeavy152Ac.toCommonSwingH(pos) {
  switch (pos) {
    case kMitsubishiHeavy152SwingHLeftMax:  return stdAc.swingh_t.kLeftMax
    case kMitsubishiHeavy152SwingHLeft:     return stdAc.swingh_t.kLeft
    case kMitsubishiHeavy152SwingHMiddle:   return stdAc.swingh_t.kMiddle
    case kMitsubishiHeavy152SwingHRight:    return stdAc.swingh_t.kRight
    case kMitsubishiHeavy152SwingHRightMax: return stdAc.swingh_t.kRightMax
    case kMitsubishiHeavy152SwingHOff:      return stdAc.swingh_t.kOff
    default:                                return stdAc.swingh_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRMitsubishiHeavy152Ac.toCommonSwingV(pos) {
  switch (pos) {
    case kMitsubishiHeavy152SwingVHighest: return stdAc.swingv_t.kHighest
    case kMitsubishiHeavy152SwingVHigh:    return stdAc.swingv_t.kHigh
    case kMitsubishiHeavy152SwingVMiddle:  return stdAc.swingv_t.kMiddle
    case kMitsubishiHeavy152SwingVLow:     return stdAc.swingv_t.kLow
    case kMitsubishiHeavy152SwingVLowest:  return stdAc.swingv_t.kLowest
    case kMitsubishiHeavy152SwingVOff:     return stdAc.swingv_t.kOff
    default:                               return stdAc.swingv_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMitsubishiHeavy152Ac.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.MITSUBISHI_HEAVY_152
  result.model = -1  # No models used.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->toCommonSwingV(this->getSwingVertical())
  result.swingh = this->toCommonSwingH(this->getSwingHorizontal())
  result.turbo = this->getTurbo()
  result.econo = this->getEcono()
  result.clean = this->getClean()
  result.quiet = this->getSilent()
  result.filter = this->getFilter()
  result.sleep = this->getNight() ? 0 : -1
  # Not supported.
  result.light = False
  result.beep = False
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRMitsubishiHeavy152Ac.toString(void) {
  String result = ""
  result.reserve(180)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kMitsubishiHeavyAuto,
                            kMitsubishiHeavyCool, kMitsubishiHeavyHeat,
                            kMitsubishiHeavyDry, kMitsubishiHeavyFan)
  result += addTempToString(getTemp())
  result += addIntToString(getFan(), kFanStr)
  result += kSpaceLBraceStr
  switch (this->getFan()) {
    case kMitsubishiHeavy152FanAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy152FanHigh:
      result += kHighStr
      break
    case kMitsubishiHeavy152FanLow:
      result += kLowStr
      break
    case kMitsubishiHeavy152FanMed:
      result += kMedStr
      break
    case kMitsubishiHeavy152FanMax:
      result += kMaxStr
      break
    case kMitsubishiHeavy152FanEcono:
      result += kEconoStr
      break
    case kMitsubishiHeavy152FanTurbo:
      result += kTurboStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addIntToString(getSwingVertical(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (this->getSwingVertical()) {
    case kMitsubishiHeavy152SwingVAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy152SwingVHighest:
      result += kHighestStr
      break
    case kMitsubishiHeavy152SwingVHigh:
      result += kHighStr
      break
    case kMitsubishiHeavy152SwingVMiddle:
      result += kMiddleStr
      break
    case kMitsubishiHeavy152SwingVLow:
      result += kLowStr
      break
    case kMitsubishiHeavy152SwingVLowest:
      result += kLowestStr
      break
    case kMitsubishiHeavy152SwingVOff:
      result += kOffStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addIntToString(getSwingHorizontal(), kSwingHStr)
  result += kSpaceLBraceStr
  switch (this->getSwingHorizontal()) {
    case kMitsubishiHeavy152SwingHAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy152SwingHLeftMax:
      result += kMaxLeftStr
      break
    case kMitsubishiHeavy152SwingHLeft:
      result += kLeftStr
      break
    case kMitsubishiHeavy152SwingHMiddle:
      result += kMiddleStr
      break
    case kMitsubishiHeavy152SwingHRight:
      result += kRightStr
      break
    case kMitsubishiHeavy152SwingHRightMax:
      result += kMaxRightStr
      break
    case kMitsubishiHeavy152SwingHLeftRight:
      result += kLeftStr
      result += ' '
      result += kRightStr
      break
    case kMitsubishiHeavy152SwingHRightLeft:
      result += kRightStr
      result += ' '
      result += kLeftStr
      break
    case kMitsubishiHeavy152SwingHOff:
      result += kOffStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addBoolToString(getSilent(), kSilentStr)
  result += addBoolToString(getTurbo(), kTurboStr)
  result += addBoolToString(getEcono(), kEconoStr)
  result += addBoolToString(getNight(), kNightStr)
  result += addBoolToString(getFilter(), kFilterStr)
  result += addBoolToString(get3D(), k3DStr)
  result += addBoolToString(getClean(), kCleanStr)
  return result
}


# Class for decoding and constructing MitsubishiHeavy88 AC messages.
IRMitsubishiHeavy88Ac.IRMitsubishiHeavy88Ac(pin,
                                             bool inverted,
                                             bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { stateReset() }

void IRMitsubishiHeavy88Ac.begin(void) { _irsend.begin() }

#if SEND_MITSUBISHIHEAVY
void IRMitsubishiHeavy88Ac.send(repeat) {
  _irsend.sendMitsubishiHeavy88(this->getRaw(), kMitsubishiHeavy88StateLength,
                                repeat)
}
#endif  # SEND_MITSUBISHIHEAVY

void IRMitsubishiHeavy88Ac.stateReset(void) {
  memcpy(remote_state, kMitsubishiHeavyZjsSig, kMitsubishiHeavySigLength)
  for (i = kMitsubishiHeavySigLength i < kMitsubishiHeavy88StateLength
       i++) remote_state[i] = 0
}

*IRMitsubishiHeavy88Ac.getRaw(void) {
  checksum()
  return remote_state
}

void IRMitsubishiHeavy88Ac.setRaw(*data) {
  memcpy(remote_state, data, kMitsubishiHeavy88StateLength)
}

void IRMitsubishiHeavy88Ac.on(void) { setPower(True) }

void IRMitsubishiHeavy88Ac.off(void) { setPower(False) }

void IRMitsubishiHeavy88Ac.setPower(bool on) {
  setBit(&remote_state[9], kMitsubishiHeavyPowerOffset, on)
}

bool IRMitsubishiHeavy88Ac.getPower(void) {
  return GETBIT8(remote_state[9], kMitsubishiHeavyPowerOffset)
}

void IRMitsubishiHeavy88Ac.setTemp(temp) {
  newtemp = temp
  newtemp = std.min(newtemp, kMitsubishiHeavyMaxTemp)
  newtemp = std.max(newtemp, kMitsubishiHeavyMinTemp)
  setBits(&remote_state[9], kHighNibble, kNibbleSize,
          newtemp - kMitsubishiHeavyMinTemp)
}

IRMitsubishiHeavy88Ac.getTemp(void) {
  return GETBITS8(remote_state[9], kHighNibble, kNibbleSize) +
      kMitsubishiHeavyMinTemp
}

# Set the speed of the fan
void IRMitsubishiHeavy88Ac.setFan(speed) {
  newspeed = speed
  switch (speed) {
    case kMitsubishiHeavy88FanLow:
    case kMitsubishiHeavy88FanMed:
    case kMitsubishiHeavy88FanHigh:
    case kMitsubishiHeavy88FanTurbo:
    case kMitsubishiHeavy88FanEcono: break
    default: newspeed = kMitsubishiHeavy88FanAuto
  }
  setBits(&remote_state[7], kMitsubishiHeavy88FanOffset,
          kMitsubishiHeavy88FanSize, newspeed)
}

IRMitsubishiHeavy88Ac.getFan(void) {
  return GETBITS8(remote_state[7], kMitsubishiHeavy88FanOffset,
                  kMitsubishiHeavy88FanSize)
}

void IRMitsubishiHeavy88Ac.setMode(mode) {
  newmode = mode
  switch (mode) {
    case kMitsubishiHeavyCool:
    case kMitsubishiHeavyDry:
    case kMitsubishiHeavyFan:
    case kMitsubishiHeavyHeat:
      break
    default:
      newmode = kMitsubishiHeavyAuto
  }
  setBits(&remote_state[9], kMitsubishiHeavyModeOffset, kModeBitsSize, newmode)
}

IRMitsubishiHeavy88Ac.getMode(void) {
  return GETBITS8(remote_state[9], kMitsubishiHeavyModeOffset, kModeBitsSize)
}

void IRMitsubishiHeavy88Ac.setSwingVertical(pos) {
  newpos
  switch (pos) {
    case kMitsubishiHeavy88SwingVAuto:
    case kMitsubishiHeavy88SwingVHighest:
    case kMitsubishiHeavy88SwingVHigh:
    case kMitsubishiHeavy88SwingVMiddle:
    case kMitsubishiHeavy88SwingVLow:
    case kMitsubishiHeavy88SwingVLowest: newpos = pos break
    default: newpos = kMitsubishiHeavy88SwingVOff
  }
  setBit(&remote_state[5], kMitsubishiHeavy88SwingVByte5Offset,
         newpos & 1)
  setBits(&remote_state[7], kMitsubishiHeavy88SwingVByte7Offset,
          kMitsubishiHeavy88SwingVByte7Size,
          newpos >> kMitsubishiHeavy88SwingVByte5Size)
}

IRMitsubishiHeavy88Ac.getSwingVertical(void) {
  return GETBITS8(remote_state[5], kMitsubishiHeavy88SwingVByte5Offset,
                  kMitsubishiHeavy88SwingVByte5Size) |
         (GETBITS8(remote_state[7], kMitsubishiHeavy88SwingVByte7Offset,
                   kMitsubishiHeavy88SwingVByte7Size) <<
          kMitsubishiHeavy88SwingVByte5Size)
}

void IRMitsubishiHeavy88Ac.setSwingHorizontal(pos) {
  newpos
  switch (pos) {
    case kMitsubishiHeavy88SwingHAuto:
    case kMitsubishiHeavy88SwingHLeftMax:
    case kMitsubishiHeavy88SwingHLeft:
    case kMitsubishiHeavy88SwingHMiddle:
    case kMitsubishiHeavy88SwingHRight:
    case kMitsubishiHeavy88SwingHRightMax:
    case kMitsubishiHeavy88SwingHLeftRight:
    case kMitsubishiHeavy88SwingHRightLeft:
    case kMitsubishiHeavy88SwingH3D: newpos = pos break
    default:                         newpos = kMitsubishiHeavy88SwingHOff
  }
  setBits(&remote_state[5], kMitsubishiHeavy88SwingHOffset1,
                  kMitsubishiHeavy88SwingHSize, newpos)
  setBits(&remote_state[5], kMitsubishiHeavy88SwingHOffset2,
                  kMitsubishiHeavy88SwingHSize,
                  newpos >> kMitsubishiHeavy88SwingHSize)
}

IRMitsubishiHeavy88Ac.getSwingHorizontal(void) {
  return GETBITS8(remote_state[5], kMitsubishiHeavy88SwingHOffset1,
                  kMitsubishiHeavy88SwingHSize) |
         (GETBITS8(remote_state[5], kMitsubishiHeavy88SwingHOffset2,
                   kMitsubishiHeavy88SwingHSize) <<
          kMitsubishiHeavy88SwingHSize)
}

void IRMitsubishiHeavy88Ac.setTurbo(bool on) {
  if (on)
    this->setFan(kMitsubishiHeavy88FanTurbo)
  else if (this->getTurbo()) this->setFan(kMitsubishiHeavy88FanAuto)
}

bool IRMitsubishiHeavy88Ac.getTurbo(void) {
  return this->getFan() == kMitsubishiHeavy88FanTurbo
}

void IRMitsubishiHeavy88Ac.setEcono(bool on) {
  if (on)
    this->setFan(kMitsubishiHeavy88FanEcono)
  else if (this->getEcono()) this->setFan(kMitsubishiHeavy88FanAuto)
}

bool IRMitsubishiHeavy88Ac.getEcono(void) {
  return this->getFan() == kMitsubishiHeavy88FanEcono
}

void IRMitsubishiHeavy88Ac.set3D(bool on) {
  if (on)
    this->setSwingHorizontal(kMitsubishiHeavy88SwingH3D)
  else if (this->get3D())
    this->setSwingHorizontal(kMitsubishiHeavy88SwingHOff)
}

bool IRMitsubishiHeavy88Ac.get3D(void) {
  return this->getSwingHorizontal() == kMitsubishiHeavy88SwingH3D
}

void IRMitsubishiHeavy88Ac.setClean(bool on) {
  setBit(&remote_state[5], kMitsubishiHeavy88CleanOffset, on)
}

bool IRMitsubishiHeavy88Ac.getClean(void) {
  return GETBIT8(remote_state[5], kMitsubishiHeavy88CleanOffset)
}

# Verify the given state has a ZJ-S signature.
bool IRMitsubishiHeavy88Ac.checkZjsSig(*state) {
  for (i = 0 i < kMitsubishiHeavySigLength i++)
    if (state[i] != kMitsubishiHeavyZjsSig[i]) return False
  return True
}

# Protocol technically has no checksum, but does has inverted byte pairs.
void IRMitsubishiHeavy88Ac.checksum(void) {
  for (i = kMitsubishiHeavySigLength - 2
       i < kMitsubishiHeavy88StateLength
       i += 2) {
    remote_state[i + 1] = ~remote_state[i]
  }
}

# Protocol technically has no checksum, but does has inverted byte pairs.
bool IRMitsubishiHeavy88Ac.validChecksum(*state,
                                           length) {
  return IRMitsubishiHeavy152Ac.validChecksum(state, length)
}

# Convert a standard A/C mode into its native mode.
IRMitsubishiHeavy88Ac.convertMode(stdAc.opmode_t mode) {
  return IRMitsubishiHeavy152Ac.convertMode(mode)
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMitsubishiHeavy88Ac.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    # Assumes Econo is slower than Low.
    case stdAc.fanspeed_t.kMin:    return kMitsubishiHeavy88FanEcono
    case stdAc.fanspeed_t.kLow:    return kMitsubishiHeavy88FanLow
    case stdAc.fanspeed_t.kMedium: return kMitsubishiHeavy88FanMed
    case stdAc.fanspeed_t.kHigh:   return kMitsubishiHeavy88FanHigh
    case stdAc.fanspeed_t.kMax:    return kMitsubishiHeavy88FanTurbo
    default:                         return kMitsubishiHeavy88FanAuto
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRMitsubishiHeavy88Ac.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kAuto:    return kMitsubishiHeavy88SwingVAuto
    case stdAc.swingv_t.kHighest: return kMitsubishiHeavy88SwingVHighest
    case stdAc.swingv_t.kHigh:    return kMitsubishiHeavy88SwingVHigh
    case stdAc.swingv_t.kMiddle:  return kMitsubishiHeavy88SwingVMiddle
    case stdAc.swingv_t.kLow:     return kMitsubishiHeavy88SwingVLow
    case stdAc.swingv_t.kLowest:  return kMitsubishiHeavy88SwingVLowest
    default:                        return kMitsubishiHeavy88SwingVOff
  }
}

# Convert a standard A/C horizontal swing into its native setting.
IRMitsubishiHeavy88Ac.convertSwingH(stdAc.swingh_t position) {
  switch (position) {
    case stdAc.swingh_t.kAuto:     return kMitsubishiHeavy88SwingHAuto
    case stdAc.swingh_t.kLeftMax:  return kMitsubishiHeavy88SwingHLeftMax
    case stdAc.swingh_t.kLeft:     return kMitsubishiHeavy88SwingHLeft
    case stdAc.swingh_t.kMiddle:   return kMitsubishiHeavy88SwingHMiddle
    case stdAc.swingh_t.kRight:    return kMitsubishiHeavy88SwingHRight
    case stdAc.swingh_t.kRightMax: return kMitsubishiHeavy88SwingHRightMax
    default:                         return kMitsubishiHeavy88SwingHOff
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMitsubishiHeavy88Ac.toCommonFanSpeed(speed) {
  switch (speed) {
    case kMitsubishiHeavy88FanTurbo: return stdAc.fanspeed_t.kMax
    case kMitsubishiHeavy88FanHigh:  return stdAc.fanspeed_t.kHigh
    case kMitsubishiHeavy88FanMed:   return stdAc.fanspeed_t.kMedium
    case kMitsubishiHeavy88FanLow:   return stdAc.fanspeed_t.kLow
    case kMitsubishiHeavy88FanEcono: return stdAc.fanspeed_t.kMin
    default:                         return stdAc.fanspeed_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingh_t IRMitsubishiHeavy88Ac.toCommonSwingH(pos) {
  switch (pos) {
    case kMitsubishiHeavy88SwingHLeftMax:  return stdAc.swingh_t.kLeftMax
    case kMitsubishiHeavy88SwingHLeft:     return stdAc.swingh_t.kLeft
    case kMitsubishiHeavy88SwingHMiddle:   return stdAc.swingh_t.kMiddle
    case kMitsubishiHeavy88SwingHRight:    return stdAc.swingh_t.kRight
    case kMitsubishiHeavy88SwingHRightMax: return stdAc.swingh_t.kRightMax
    case kMitsubishiHeavy88SwingHOff:      return stdAc.swingh_t.kOff
    default:                               return stdAc.swingh_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRMitsubishiHeavy88Ac.toCommonSwingV(pos) {
  switch (pos) {
    case kMitsubishiHeavy88SwingVHighest: return stdAc.swingv_t.kHighest
    case kMitsubishiHeavy88SwingVHigh:    return stdAc.swingv_t.kHigh
    case kMitsubishiHeavy88SwingVMiddle:  return stdAc.swingv_t.kMiddle
    case kMitsubishiHeavy88SwingVLow:     return stdAc.swingv_t.kLow
    case kMitsubishiHeavy88SwingVLowest:  return stdAc.swingv_t.kLowest
    case kMitsubishiHeavy88SwingVOff:     return stdAc.swingv_t.kOff
    default:                              return stdAc.swingv_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMitsubishiHeavy88Ac.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.MITSUBISHI_HEAVY_88
  result.model = -1  # No models used.
  result.power = this->getPower()
  result.mode = IRMitsubishiHeavy152Ac.toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->toCommonSwingV(this->getSwingVertical())
  result.swingh = this->toCommonSwingH(this->getSwingHorizontal())
  result.turbo = this->getTurbo()
  result.econo = this->getEcono()
  result.clean = this->getClean()
  # Not supported.
  result.quiet = False
  result.filter = False
  result.light = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRMitsubishiHeavy88Ac.toString(void) {
  String result = ""
  result.reserve(140)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kMitsubishiHeavyAuto,
                            kMitsubishiHeavyCool, kMitsubishiHeavyHeat,
                            kMitsubishiHeavyDry, kMitsubishiHeavyFan)
  result += addTempToString(getTemp())
  result += addIntToString(getFan(), kFanStr)
  result += kSpaceLBraceStr
  switch (this->getFan()) {
    case kMitsubishiHeavy88FanAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy88FanHigh:
      result += kHighStr
      break
    case kMitsubishiHeavy88FanLow:
      result += kLowStr
      break
    case kMitsubishiHeavy88FanMed:
      result += kMedStr
      break
    case kMitsubishiHeavy88FanEcono:
      result += kEconoStr
      break
    case kMitsubishiHeavy88FanTurbo:
      result += kTurboStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addIntToString(getSwingVertical(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (this->getSwingVertical()) {
    case kMitsubishiHeavy88SwingVAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy88SwingVHighest:
      result += kHighestStr
      break
    case kMitsubishiHeavy88SwingVHigh:
      result += kHighStr
      break
    case kMitsubishiHeavy88SwingVMiddle:
      result += kMiddleStr
      break
    case kMitsubishiHeavy88SwingVLow:
      result += kLowStr
      break
    case kMitsubishiHeavy88SwingVLowest:
      result += kLowestStr
      break
    case kMitsubishiHeavy88SwingVOff:
      result += kOffStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addIntToString(getSwingHorizontal(), kSwingHStr)
  result += kSpaceLBraceStr
  switch (this->getSwingHorizontal()) {
    case kMitsubishiHeavy88SwingHAuto:
      result += kAutoStr
      break
    case kMitsubishiHeavy88SwingHLeftMax:
      result += kMaxLeftStr
      break
    case kMitsubishiHeavy88SwingHLeft:
      result += kLeftStr
      break
    case kMitsubishiHeavy88SwingHMiddle:
      result += kMiddleStr
      break
    case kMitsubishiHeavy88SwingHRight:
      result += kRightStr
      break
    case kMitsubishiHeavy88SwingHRightMax:
      result += kMaxRightStr
      break
    case kMitsubishiHeavy88SwingHLeftRight:
      result += kLeftStr
      result += ' '
      result += kRightStr
      break
    case kMitsubishiHeavy88SwingHRightLeft:
      result += kRightStr
      result += ' '
      result += kLeftStr
      break
    case kMitsubishiHeavy88SwingH3D:
      result += k3DStr
      break
    case kMitsubishiHeavy88SwingHOff:
      result += kOffStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addBoolToString(getTurbo(), kTurboStr)
  result += addBoolToString(getEcono(), kEconoStr)
  result += addBoolToString(get3D(), k3DStr)
  result += addBoolToString(getClean(), kCleanStr)
  return result
}

#if DECODE_MITSUBISHIHEAVY
# Decode the supplied MitsubishiHeavy message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect.
#            Typically kMitsubishiHeavy88Bits or kMitsubishiHeavy152Bits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Appears to be working. Needs testing against a real device.
bool IRrecv.decodeMitsubishiHeavy(decode_results* results,
                                   nbits, bool strict) {
  # Check if can possibly be a valid MitsubishiHeavy message.
  if (results->rawlen < 2 * nbits + kHeader + kFooter - 1) return False
  if (strict) {
    switch (nbits) {
      case kMitsubishiHeavy88Bits:
      case kMitsubishiHeavy152Bits:
        break
      default:
        return False  # Not what is expected
    }
  }

  offset = kStartOffset
  used
  used = matchGeneric(results->rawbuf + offset, results->state,
                      results->rawlen - offset, nbits,
                      kMitsubishiHeavyHdrMark, kMitsubishiHeavyHdrSpace,
                      kMitsubishiHeavyBitMark, kMitsubishiHeavyOneSpace,
                      kMitsubishiHeavyBitMark, kMitsubishiHeavyZeroSpace,
                      kMitsubishiHeavyBitMark, kMitsubishiHeavyGap, True,
                      _tolerance, 0, False)
  if (used == 0) return False
  offset += used
  # Compliance
  switch (nbits) {
    case kMitsubishiHeavy88Bits:
      if (strict and !(IRMitsubishiHeavy88Ac.checkZjsSig(results->state) and
                      IRMitsubishiHeavy88Ac.validChecksum(results->state)))
        return False
      results->decode_type = MITSUBISHI_HEAVY_88
      break
    case kMitsubishiHeavy152Bits:
      if (strict and !(IRMitsubishiHeavy152Ac.checkZmsSig(results->state) and
                      IRMitsubishiHeavy152Ac.validChecksum(results->state)))
        return False
      results->decode_type = MITSUBISHI_HEAVY_152
      break
    default:
      return False
  }

  # Success
  results->bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result->state, we don't record value, address, or command as it
  # is a union data type.
  return True
}
#endif  # DECODE_MITSUBISHIHEAVY
