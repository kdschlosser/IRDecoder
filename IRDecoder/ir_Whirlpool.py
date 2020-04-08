"""
# Whirlpool A/C
#
# Copyright 2018 David Conran

# Supports:
#   Brand: Whirlpool,  Model: DG11J1-3A remote
#   Brand: Whirlpool,  Model: DG11J1-04 remote
#   Brand: Whirlpool,  Model: DG11J1-91 remote
#   Brand: Whirlpool,  Model: SPIS409L A/C
#   Brand: Whirlpool,  Model: SPIS412L A/C
#   Brand: Whirlpool,  Model: SPIW409L A/C
#   Brand: Whirlpool,  Model: SPIW412L A/C
#   Brand: Whirlpool,  Model: SPIW418L A/C

#ifndef IR_WHIRLPOOL_H_
#define IR_WHIRLPOOL_H_

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

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/509

# Constants
kWhirlpoolAcChecksumByte1 = 13
kWhirlpoolAcChecksumByte2 = kWhirlpoolAcStateLength - 1
kWhirlpoolAcHeat = 0
kWhirlpoolAcAuto = 1
kWhirlpoolAcCool = 2
kWhirlpoolAcDry = 3
kWhirlpoolAcFan = 4
kWhirlpoolAcModeOffset = 0
kWhirlpoolAcModePos = 3
kWhirlpoolAcFanOffset = 0  # Mask 0b00000011
kWhirlpoolAcFanSize = 2  # Nr. of bits
kWhirlpoolAcFanAuto = 0
kWhirlpoolAcFanHigh = 1
kWhirlpoolAcFanMedium = 2
kWhirlpoolAcFanLow = 3
kWhirlpoolAcFanPos = 2
kWhirlpoolAcMinTemp = 18     # 18C (DG11J1-3A), 16C (DG11J1-91)
kWhirlpoolAcMaxTemp = 32     # 32C (DG11J1-3A), 30C (DG11J1-91)
kWhirlpoolAcAutoTemp = 23    # 23C
kWhirlpoolAcTempPos = 3
kWhirlpoolAcSwing1Offset = 7
kWhirlpoolAcSwing2Offset = 6
kWhirlpoolAcLightOffset = 5
kWhirlpoolAcPowerToggleOffset = 2  # 0b00000100
kWhirlpoolAcPowerTogglePos = 2
kWhirlpoolAcSleepOffset = 3
kWhirlpoolAcSleepPos = 2
kWhirlpoolAcSuperMask = 0b10010000
kWhirlpoolAcSuperPos = 5
kWhirlpoolAcHourOffset = 0  # Mask 0b00011111
kWhirlpoolAcHourSize = 5  # Nr. of bits
kWhirlpoolAcMinuteOffset = 0  # Mask 0b00111111
kWhirlpoolAcMinuteSize = 6  # Nr. of bits
kWhirlpoolAcTimerEnableOffset = 7  # 0b10000000
kWhirlpoolAcClockPos = 6
kWhirlpoolAcOffTimerPos = 8
kWhirlpoolAcOnTimerPos = 10
kWhirlpoolAcCommandPos = 15
kWhirlpoolAcCommandLight = 0x00
kWhirlpoolAcCommandPower = 0x01
kWhirlpoolAcCommandTemp = 0x02
kWhirlpoolAcCommandSleep = 0x03
kWhirlpoolAcCommandSuper = 0x04
kWhirlpoolAcCommandOnTimer = 0x05
kWhirlpoolAcCommandMode = 0x06
kWhirlpoolAcCommandSwing = 0x07
kWhirlpoolAcCommandIFeel = 0x0D
kWhirlpoolAcCommandFanSpeed = 0x11
kWhirlpoolAcCommand6thSense = 0x17
kWhirlpoolAcCommandOffTimer = 0x1D
kWhirlpoolAcAltTempOffset = 3
kWhirlpoolAcAltTempPos = 18

# Classes
class IRWhirlpoolAc {
 public:
  explicit IRWhirlpoolAc(pin, bool inverted = False,
                         bool use_modulation = True)

  void stateReset(void)
#if SEND_WHIRLPOOL_AC
  void send(repeat = kWhirlpoolAcDefaultRepeat,
            bool calcchecksum = True)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_WHIRLPOOL_AC
  void begin(void)
  void on(void)
  void off(void)
  void setPowerToggle(bool on)
  bool getPowerToggle(void)
  void setSleep(bool on)
  bool getSleep(void)
  void setSuper(bool on)
  bool getSuper(void)
  void setTemp(temp)
  getTemp(void)
  void setFan(speed)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setSwing(bool on)
  bool getSwing(void)
  void setLight(bool on)
  bool getLight(void)
  getClock(void)
  void setClock(minspastmidnight)
  getOnTimer(void)
  void setOnTimer(minspastmidnight)
  void enableOnTimer(bool on)
  bool isOnTimerEnabled(void)
  getOffTimer(void)
  void setOffTimer(minspastmidnight)
  void enableOffTimer(bool on)
  bool isOffTimerEnabled(void)
  void setCommand(code)
  getCommand(void)
  whirlpool_ac_remote_model_t getModel(void)
  void setModel(whirlpool_ac_remote_model_t model)
  uint8_t* getRaw(bool calcchecksum = True)
  void setRaw(new_code[],
              length = kWhirlpoolAcStateLength)
  static bool validChecksum(state[],
                            length = kWhirlpoolAcStateLength)
  convertMode(stdAc.opmode_t mode)
  convertFan(stdAc.fanspeed_t speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # The state of the IR remote in IR code form.
  remote_state[kWhirlpoolAcStateLength]
  _desiredtemp
  void checksum(length = kWhirlpoolAcStateLength)
  getTime(pos)
  void setTime(pos, minspastmidnight)
  bool isTimerEnabled(pos)
  void enableTimer(pos, bool state)
  void _setTemp(temp, bool remember = True)
  void _setMode(mode)
  int8_t getTempOffset(void)
}

#endif  # IR_WHIRLPOOL_H_

"""
# Copyright 2018 David Conran
#
# Code to emulate Whirlpool protocol compatible devices.
# Should be compatible with:
# * SPIS409L, SPIS412L, SPIW409L, SPIW412L, SPIW418L
# Remotes:
# * DG11J1-3A / DG11J1-04
# * DG11J1-91
#
# Note: Smart, iFeel, AroundU, PowerSave, & Silent modes are unsupported.
#       Advanced 6thSense, Dehumidify, & Sleep modes are not supported.
#       FYI:
#         Dim == !Light
#         Jet == Super == Turbo
#

#include "ir_Whirlpool.h"
#include <algorithm>
#include <cstring>
#ifndef ARDUINO
#include <string>
#endif
#include "IRrecv.h"
#include "IRremoteESP8266.h"
#include "IRsend.h"
#include "IRtext.h"
#include "IRutils.h"

# Constants
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/509
kWhirlpoolAcHdrMark = 8950
kWhirlpoolAcHdrSpace = 4484
kWhirlpoolAcBitMark = 597
kWhirlpoolAcOneSpace = 1649
kWhirlpoolAcZeroSpace = 533
kWhirlpoolAcGap = 7920
kWhirlpoolAcMinGap = kDefaultMessageGap  # Just a guess.
kWhirlpoolAcSections = 3

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addModelToString
using irutils.addTempToString
using irutils.minsToString
using irutils.setBit
using irutils.setBits

#if SEND_WHIRLPOOL_AC
# Send a Whirlpool A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kWhirlpoolAcStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: ALPHA / Untested.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/509
void IRsend.sendWhirlpoolAC(unsigned char data[], nbytes,
                             repeat) {
  if (nbytes < kWhirlpoolAcStateLength)
    return  # Not enough bytes to send a proper message.
  for (r = 0 r <= repeat r++) {
    # Section 1
    sendGeneric(kWhirlpoolAcHdrMark, kWhirlpoolAcHdrSpace, kWhirlpoolAcBitMark,
                kWhirlpoolAcOneSpace, kWhirlpoolAcBitMark,
                kWhirlpoolAcZeroSpace, kWhirlpoolAcBitMark, kWhirlpoolAcGap,
                data, 6,  # 6 bytes == 48 bits
                38000,    # Complete guess of the modulation frequency.
                False, 0, 50)
    # Section 2
    sendGeneric(0, 0, kWhirlpoolAcBitMark, kWhirlpoolAcOneSpace,
                kWhirlpoolAcBitMark, kWhirlpoolAcZeroSpace, kWhirlpoolAcBitMark,
                kWhirlpoolAcGap, data + 6, 8,  # 8 bytes == 64 bits
                38000,  # Complete guess of the modulation frequency.
                False, 0, 50)
    # Section 3
    sendGeneric(0, 0, kWhirlpoolAcBitMark, kWhirlpoolAcOneSpace,
                kWhirlpoolAcBitMark, kWhirlpoolAcZeroSpace, kWhirlpoolAcBitMark,
                kWhirlpoolAcMinGap, data + 14, 7,  # 7 bytes == 56 bits
                38000,  # Complete guess of the modulation frequency.
                False, 0, 50)
  }
}
#endif  # SEND_WHIRLPOOL_AC

# Class for emulating a Whirlpool A/C remote.
# Decoding help from:
#   @redmusicxd, @josh929800, @raducostea

IRWhirlpoolAc.IRWhirlpoolAc(pin, bool inverted,
                             bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

void IRWhirlpoolAc.stateReset(void) {
  for (i = 2 i < kWhirlpoolAcStateLength i++) remote_state[i] = 0x0
  remote_state[0] = 0x83
  remote_state[1] = 0x06
  remote_state[6] = 0x80
  this->_setTemp(kWhirlpoolAcAutoTemp)  # Default to a sane value.
}

void IRWhirlpoolAc.begin(void) { _irsend.begin() }

bool IRWhirlpoolAc.validChecksum(state[], length) {
  if (length > kWhirlpoolAcChecksumByte1 and
      state[kWhirlpoolAcChecksumByte1] !=
          xorBytes(state + 2, kWhirlpoolAcChecksumByte1 - 1 - 2)) {
    DPRINTLN("DEBUG: First Whirlpool AC checksum failed.")
    return False
  }
  if (length > kWhirlpoolAcChecksumByte2 and
      state[kWhirlpoolAcChecksumByte2] !=
          xorBytes(state + kWhirlpoolAcChecksumByte1 + 1,
                   kWhirlpoolAcChecksumByte2 - kWhirlpoolAcChecksumByte1 - 1)) {
    DPRINTLN("DEBUG: Second Whirlpool AC checksum failed.")
    return False
  }
  # State is too short to have a checksum or everything checked out.
  return True
}

# Update the checksum for the internal state.
void IRWhirlpoolAc.checksum(length) {
  if (length >= kWhirlpoolAcChecksumByte1)
    remote_state[kWhirlpoolAcChecksumByte1] =
        xorBytes(remote_state + 2, kWhirlpoolAcChecksumByte1 - 1 - 2)
  if (length >= kWhirlpoolAcChecksumByte2)
    remote_state[kWhirlpoolAcChecksumByte2] =
        xorBytes(remote_state + kWhirlpoolAcChecksumByte1 + 1,
                 kWhirlpoolAcChecksumByte2 - kWhirlpoolAcChecksumByte1 - 1)
}

#if SEND_WHIRLPOOL_AC
void IRWhirlpoolAc.send(repeat, bool calcchecksum) {
  if (calcchecksum) this->checksum()
  _irsend.sendWhirlpoolAC(remote_state, kWhirlpoolAcStateLength, repeat)
}
#endif  # SEND_WHIRLPOOL_AC

*IRWhirlpoolAc.getRaw(bool calcchecksum) {
  if (calcchecksum) this->checksum()
  return remote_state
}

void IRWhirlpoolAc.setRaw(new_code[], length) {
  memcpy(remote_state, new_code, std.min(length, kWhirlpoolAcStateLength))
}

whirlpool_ac_remote_model_t IRWhirlpoolAc.getModel(void) {
  if (GETBIT8(remote_state[kWhirlpoolAcAltTempPos], kWhirlpoolAcAltTempOffset))
    return DG11J191
  else
    return DG11J13A
}

void IRWhirlpoolAc.setModel(whirlpool_ac_remote_model_t model) {
  switch (model) {
    case DG11J191:
      setBit(&remote_state[kWhirlpoolAcAltTempPos], kWhirlpoolAcAltTempOffset)
      break
    case DG11J13A:
      # FALL THRU
    default:
      setBit(&remote_state[kWhirlpoolAcAltTempPos], kWhirlpoolAcAltTempOffset,
             False)
  }
  this->_setTemp(_desiredtemp)  # Different models have different temp values.
}

# Return the temp. offset in deg C for the current model.
int8_t IRWhirlpoolAc.getTempOffset(void) {
  switch (this->getModel()) {
    case whirlpool_ac_remote_model_t.DG11J191: return -2
    default:                                    return 0
  }
}

# Set the temp. in deg C
void IRWhirlpoolAc._setTemp(temp, bool remember) {
  if (remember) _desiredtemp = temp
  int8_t offset = this->getTempOffset()  # Cache the min temp for the model.
  newtemp = std.max((uint8_t)(kWhirlpoolAcMinTemp + offset), temp)
  newtemp = std.min((uint8_t)(kWhirlpoolAcMaxTemp + offset), newtemp)
  setBits(&remote_state[kWhirlpoolAcTempPos], kHighNibble, kNibbleSize,
          newtemp - (kWhirlpoolAcMinTemp + offset))
}

# Set the temp. in deg C
void IRWhirlpoolAc.setTemp(temp) {
  this->_setTemp(temp)
  this->setSuper(False)  # Changing temp cancels Super/Jet mode.
  this->setCommand(kWhirlpoolAcCommandTemp)
}

# Return the set temp. in deg C
IRWhirlpoolAc.getTemp(void) {
  return GETBITS8(remote_state[kWhirlpoolAcTempPos], kHighNibble, kNibbleSize) +
      kWhirlpoolAcMinTemp + this->getTempOffset()
}

void IRWhirlpoolAc._setMode(mode) {
  switch (mode) {
    case kWhirlpoolAcAuto:
      this->setFan(kWhirlpoolAcFanAuto)
      this->_setTemp(kWhirlpoolAcAutoTemp, False)
      this->setSleep(False)  # Cancel sleep mode when in auto/6thsense mode.
      # FALL THRU
    case kWhirlpoolAcHeat:
    case kWhirlpoolAcCool:
    case kWhirlpoolAcDry:
    case kWhirlpoolAcFan:
      setBits(&remote_state[kWhirlpoolAcModePos], kWhirlpoolAcModeOffset,
              kModeBitsSize, mode)
      this->setCommand(kWhirlpoolAcCommandMode)
      break
    default:
      return
  }
  if (mode == kWhirlpoolAcAuto) this->setCommand(kWhirlpoolAcCommand6thSense)
}

void IRWhirlpoolAc.setMode(mode) {
    this->setSuper(False)  # Changing mode cancels Super/Jet mode.
    this->_setMode(mode)
}

IRWhirlpoolAc.getMode(void) {
  return GETBITS8(remote_state[kWhirlpoolAcModePos], kWhirlpoolAcModeOffset,
                  kModeBitsSize)
}

void IRWhirlpoolAc.setFan(speed) {
  switch (speed) {
    case kWhirlpoolAcFanAuto:
    case kWhirlpoolAcFanLow:
    case kWhirlpoolAcFanMedium:
    case kWhirlpoolAcFanHigh:
      setBits(&remote_state[kWhirlpoolAcFanPos], kWhirlpoolAcFanOffset,
              kWhirlpoolAcFanSize, speed)
      this->setSuper(False)  # Changing fan speed cancels Super/Jet mode.
      this->setCommand(kWhirlpoolAcCommandFanSpeed)
      break
  }
}

IRWhirlpoolAc.getFan(void) {
  return GETBITS8(remote_state[kWhirlpoolAcFanPos], kWhirlpoolAcFanOffset,
                  kWhirlpoolAcFanSize)
}

void IRWhirlpoolAc.setSwing(bool on) {
  setBit(&remote_state[kWhirlpoolAcFanPos], kWhirlpoolAcSwing1Offset, on)
  setBit(&remote_state[kWhirlpoolAcOffTimerPos], kWhirlpoolAcSwing2Offset, on)
  setCommand(kWhirlpoolAcCommandSwing)
}

bool IRWhirlpoolAc.getSwing(void) {
  return GETBIT8(remote_state[kWhirlpoolAcFanPos], kWhirlpoolAcSwing1Offset) and
         GETBIT8(remote_state[kWhirlpoolAcOffTimerPos],
                 kWhirlpoolAcSwing2Offset)
}

void IRWhirlpoolAc.setLight(bool on) {
  # Cleared when on.
  setBit(&remote_state[kWhirlpoolAcClockPos], kWhirlpoolAcLightOffset, !on)
}

bool IRWhirlpoolAc.getLight(void) {
  return !GETBIT8(remote_state[kWhirlpoolAcClockPos], kWhirlpoolAcLightOffset)
}

void IRWhirlpoolAc.setTime(pos,
                            minspastmidnight) {
  # Hours
  setBits(&remote_state[pos], kWhirlpoolAcHourOffset, kWhirlpoolAcHourSize,
          (minspastmidnight / 60) % 24)
  # Minutes
  setBits(&remote_state[pos + 1], kWhirlpoolAcMinuteOffset,
          kWhirlpoolAcMinuteSize, minspastmidnight % 60)
}

IRWhirlpoolAc.getTime(pos) {
  return GETBITS8(remote_state[pos], kWhirlpoolAcHourOffset,
                  kWhirlpoolAcHourSize) * 60 +
         GETBITS8(remote_state[pos + 1], kWhirlpoolAcMinuteOffset,
                  kWhirlpoolAcMinuteSize)
}

bool IRWhirlpoolAc.isTimerEnabled(pos) {
  return GETBIT8(remote_state[pos - 1], kWhirlpoolAcTimerEnableOffset)
}

void IRWhirlpoolAc.enableTimer(pos, bool on) {
  setBit(&remote_state[pos - 1], kWhirlpoolAcTimerEnableOffset, on)
}

void IRWhirlpoolAc.setClock(minspastmidnight) {
  this->setTime(kWhirlpoolAcClockPos, minspastmidnight)
}

IRWhirlpoolAc.getClock(void) {
  return this->getTime(kWhirlpoolAcClockPos)
}

void IRWhirlpoolAc.setOffTimer(minspastmidnight) {
  this->setTime(kWhirlpoolAcOffTimerPos, minspastmidnight)
}

IRWhirlpoolAc.getOffTimer(void) {
  return this->getTime(kWhirlpoolAcOffTimerPos)
}

bool IRWhirlpoolAc.isOffTimerEnabled(void) {
  return this->isTimerEnabled(kWhirlpoolAcOffTimerPos)
}

void IRWhirlpoolAc.enableOffTimer(bool on) {
  this->enableTimer(kWhirlpoolAcOffTimerPos, on)
  this->setCommand(kWhirlpoolAcCommandOffTimer)
}

void IRWhirlpoolAc.setOnTimer(minspastmidnight) {
  this->setTime(kWhirlpoolAcOnTimerPos, minspastmidnight)
}

IRWhirlpoolAc.getOnTimer(void) {
  return this->getTime(kWhirlpoolAcOnTimerPos)
}

bool IRWhirlpoolAc.isOnTimerEnabled(void) {
  return this->isTimerEnabled(kWhirlpoolAcOnTimerPos)
}

void IRWhirlpoolAc.enableOnTimer(bool on) {
  this->enableTimer(kWhirlpoolAcOnTimerPos, on)
  this->setCommand(kWhirlpoolAcCommandOnTimer)
}

void IRWhirlpoolAc.setPowerToggle(bool on) {
  setBit(&remote_state[kWhirlpoolAcPowerTogglePos],
         kWhirlpoolAcPowerToggleOffset, on)
  this->setSuper(False)  # Changing power cancels Super/Jet mode.
  this->setCommand(kWhirlpoolAcCommandPower)
}

bool IRWhirlpoolAc.getPowerToggle(void) {
  return GETBIT8(remote_state[kWhirlpoolAcPowerTogglePos],
                 kWhirlpoolAcPowerToggleOffset)
}

IRWhirlpoolAc.getCommand(void) {
  return remote_state[kWhirlpoolAcCommandPos]
}

void IRWhirlpoolAc.setSleep(bool on) {
  setBit(&remote_state[kWhirlpoolAcSleepPos],
         kWhirlpoolAcSleepOffset, on)
  if (on) this->setFan(kWhirlpoolAcFanLow)
  this->setCommand(kWhirlpoolAcCommandSleep)
}

bool IRWhirlpoolAc.getSleep(void) {
  return GETBIT8(remote_state[kWhirlpoolAcSleepPos], kWhirlpoolAcSleepOffset)
}

# AKA Jet/Turbo mode.
void IRWhirlpoolAc.setSuper(bool on) {
  if (on) {
    this->setFan(kWhirlpoolAcFanHigh)
    switch (this->getMode()) {
      case kWhirlpoolAcHeat:
        this->setTemp(kWhirlpoolAcMaxTemp + this->getTempOffset())
        break
      case kWhirlpoolAcCool:
      default:
        this->setTemp(kWhirlpoolAcMinTemp + this->getTempOffset())
        this->setMode(kWhirlpoolAcCool)
        break
    }
    remote_state[kWhirlpoolAcSuperPos] |= kWhirlpoolAcSuperMask
  } else {
    remote_state[kWhirlpoolAcSuperPos] &= ~kWhirlpoolAcSuperMask
  }
  this->setCommand(kWhirlpoolAcCommandSuper)
}

bool IRWhirlpoolAc.getSuper(void) {
  return remote_state[kWhirlpoolAcSuperPos] & kWhirlpoolAcSuperMask
}

void IRWhirlpoolAc.setCommand(code) {
  remote_state[kWhirlpoolAcCommandPos] = code
}

# Convert a standard A/C mode into its native mode.
IRWhirlpoolAc.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kWhirlpoolAcCool
    case stdAc.opmode_t.kHeat: return kWhirlpoolAcHeat
    case stdAc.opmode_t.kDry:  return kWhirlpoolAcDry
    case stdAc.opmode_t.kFan:  return kWhirlpoolAcFan
    default:                     return kWhirlpoolAcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRWhirlpoolAc.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kWhirlpoolAcFanLow
    case stdAc.fanspeed_t.kMedium: return kWhirlpoolAcFanMedium
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kWhirlpoolAcFanHigh
    default:                         return kWhirlpoolAcFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRWhirlpoolAc.toCommonMode(mode) {
  switch (mode) {
    case kWhirlpoolAcCool: return stdAc.opmode_t.kCool
    case kWhirlpoolAcHeat: return stdAc.opmode_t.kHeat
    case kWhirlpoolAcDry:  return stdAc.opmode_t.kDry
    case kWhirlpoolAcFan:  return stdAc.opmode_t.kFan
    default:               return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRWhirlpoolAc.toCommonFanSpeed(speed) {
  switch (speed) {
    case kWhirlpoolAcFanHigh:   return stdAc.fanspeed_t.kMax
    case kWhirlpoolAcFanMedium: return stdAc.fanspeed_t.kMedium
    case kWhirlpoolAcFanLow:    return stdAc.fanspeed_t.kMin
    default:                    return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRWhirlpoolAc.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.WHIRLPOOL_AC
  result.model = this->getModel()
  result.power = this->getPowerToggle()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->getSwing() ? stdAc.swingv_t.kAuto :
                                     stdAc.swingv_t.kOff
  result.turbo = this->getSuper()
  result.light = this->getLight()
  result.sleep = this->getSleep() ? 0 : -1
  # Not supported.
  result.swingh = stdAc.swingh_t.kOff
  result.quiet = False
  result.filter = False
  result.econo = False
  result.clean = False
  result.beep = False
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRWhirlpoolAc.toString(void) {
  String result = ""
  result.reserve(200)  # Reserve some heap for the string to reduce fragging.
  result += addModelToString(decode_type_t.WHIRLPOOL_AC, getModel(), False)
  result += addBoolToString(getPowerToggle(), kPowerToggleStr)
  result += addModeToString(getMode(), kWhirlpoolAcAuto, kWhirlpoolAcCool,
                            kWhirlpoolAcHeat, kWhirlpoolAcDry, kWhirlpoolAcFan)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kWhirlpoolAcFanHigh, kWhirlpoolAcFanLow,
                           kWhirlpoolAcFanAuto, kWhirlpoolAcFanAuto,
                           kWhirlpoolAcFanMedium)
  result += addBoolToString(getSwing(), kSwingStr)
  result += addBoolToString(getLight(), kLightStr)
  result += addLabeledString(minsToString(getClock()), kClockStr)
  result += addLabeledString(
      isOnTimerEnabled() ? minsToString(getOnTimer()) : kOffStr,
      kOnTimerStr)
  result += addLabeledString(
      isOffTimerEnabled() ? minsToString(getOffTimer()) : kOffStr,
      kOffTimerStr)
  result += addBoolToString(getSleep(), kSleepStr)
  result += addBoolToString(getSuper(), kSuperStr)
  result += addIntToString(getCommand(), kCommandStr)
  result += kSpaceLBraceStr
  switch (this->getCommand()) {
    case kWhirlpoolAcCommandLight:
      result += kLightStr
      break
    case kWhirlpoolAcCommandPower:
      result += kPowerStr
      break
    case kWhirlpoolAcCommandTemp:
      result += kTempStr
      break
    case kWhirlpoolAcCommandSleep:
      result += kSleepStr
      break
    case kWhirlpoolAcCommandSuper:
      result += kSuperStr
      break
    case kWhirlpoolAcCommandOnTimer:
      result += kOnTimerStr
      break
    case kWhirlpoolAcCommandMode:
      result += kModeStr
      break
    case kWhirlpoolAcCommandSwing:
      result += kSwingStr
      break
    case kWhirlpoolAcCommandIFeel:
      result += kIFeelStr
      break
    case kWhirlpoolAcCommandFanSpeed:
      result += kFanStr
      break
    case kWhirlpoolAcCommand6thSense:
      result += k6thSenseStr
      break
    case kWhirlpoolAcCommandOffTimer:
      result += kOffTimerStr
      break
    default:
      result += kUnknownStr
      break
  }
  result += ')'
  return result
}

#if DECODE_WHIRLPOOL_AC
# Decode the supplied Whirlpool A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kWhirlpoolAcBits
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Working as intended.
#
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/509
bool IRrecv.decodeWhirlpoolAC(decode_results *results, nbits,
                               bool strict) {
  if (results->rawlen < 2 * nbits + 4 + kHeader + kFooter - 1)
    return False  # Can't possibly be a valid Whirlpool A/C message.
  if (strict) {
    if (nbits != kWhirlpoolAcBits) return False
  }

  offset = kStartOffset
  sectionSize[kWhirlpoolAcSections] = {6, 8, 7}

  # Header
  if (!matchMark(results->rawbuf[offset++], kWhirlpoolAcHdrMark)) return False
  if (!matchSpace(results->rawbuf[offset++], kWhirlpoolAcHdrSpace))
    return False

  # Data Sections
  pos = 0
  for (section = 0 section < kWhirlpoolAcSections
       section++) {
    used
    # Section Data
    used = matchGeneric(results->rawbuf + offset, results->state + pos,
                        results->rawlen - offset, sectionSize[section] * 8,
                        0, 0,
                        kWhirlpoolAcBitMark, kWhirlpoolAcOneSpace,
                        kWhirlpoolAcBitMark, kWhirlpoolAcZeroSpace,
                        kWhirlpoolAcBitMark, kWhirlpoolAcGap,
                        section >= kWhirlpoolAcSections - 1,
                        _tolerance, kMarkExcess, False)
    if (used == 0) return False
    offset += used
    pos += sectionSize[section]
  }

  # Compliance
  if (strict) {
    # Re-check we got the correct size/length due to the way we read the data.
    if (pos * 8 != nbits) return False
    if (!IRWhirlpoolAc.validChecksum(results->state, nbits / 8))
      return False
  }

  # Success
  results->decode_type = WHIRLPOOL_AC
  results->bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result->state, we don't record value, address, or command as it
  # is a union data type.
  return True
}
#endif  # WHIRLPOOL_AC
