"""
# Copyright 2018 Erdem U. Altinyurt
# Copyright 2019 David Conran

# Supports:
#   Brand: Vestel,  Model: BIOX CXP-9 A/C (9K BTU)

#ifndef IR_VESTEL_H_
#define IR_VESTEL_H_

#define __STDC_LIMIT_MACROS
#include <stdint.h>
#ifdef ARDUINO
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Vestel added by Erdem U. Altinyurt

# Structure of a Command message (56 bits)
#   Signature: 12 bits. e.g. 0x201
#   Checksum: 8 bits
#   Swing: 4 bits. (auto 0xA, stop 0xF)
#   turbo_sleep_normal: 4bits. (normal 0x1, sleep 0x3, turbo 0x7)
#   Unused: 8 bits. (0x00)
#   Temperature: 4 bits. (Celsius, but offset by -16 degrees. e.g. 0x0 = 16C)
#   Fan Speed: 4 bits (auto 0x1, low 0x5, mid 0x9, high 0xB, 0xD auto hot,
#                    0xC auto cool)
#   Mode: 3 bits. (auto 0x0, cold 0x1, dry 0x2, fan 0x3, hot 0x4)
#   unknown/unused: 6 bits.
#   Ion flag: 1 bit.
#   unknown/unused: 1 bit.
#   Power/message type: 4 bits. (on 0xF, off 0xC, 0x0 == Timer mesage)
#
# Structure of a Time(r) message (56 bits)
#   Signature: 12 bits. e.g. 0x201
#   Checksum: 8 bits
#   Off Minutes: 3 bits. (Stored in 10 min increments. eg. xx:20 is 0x2)
#   Off Hours: 5 bits. (0x17 == 11PM / 23:00)
#   On Minutes: 3 bits. (Stored in 10 min increments. eg. xx:20 is 0x2)
#   On Hours: 5 bits. (0x9 == 9AM / 09:00)
#   Clock Hours: 5 bits.
#   On Timer flag: 1 bit.
#   Off Timer flag: 1 bit.
#   Timer mode flag: 1 bit. (Off after X many hours/mins, not at clock time.)
#   Clock Minutes: 8 bits. (0-59)
#   Power/message type: 4 bits. (0x0 == Timer mesage, else see Comman message)

# Constants
kVestelAcHdrMark = 3110
kVestelAcHdrSpace = 9066
kVestelAcBitMark = 520
kVestelAcOneSpace = 1535
kVestelAcZeroSpace = 480
kVestelAcTolerance = 30

kVestelAcMinTempH = 16
kVestelAcMinTempC = 18
kVestelAcMaxTemp = 30

kVestelAcAuto = 0
kVestelAcCool = 1
kVestelAcDry = 2
kVestelAcFan = 3
kVestelAcHeat = 4

kVestelAcFanAuto = 1
kVestelAcFanLow = 5
kVestelAcFanMed = 9
kVestelAcFanHigh = 0xB
kVestelAcFanAutoCool = 0xC
kVestelAcFanAutoHot = 0xD

kVestelAcNormal = 1
kVestelAcSleep = 3
kVestelAcTurbo = 7
kVestelAcIon = 4
kVestelAcSwing = 0xA

kVestelAcChecksumOffset = 12
kVestelAcChecksumSize = 8  # Nr. of bits
kVestelAcSwingOffset = 20
kVestelAcTurboSleepOffset = 24
kVestelAcTempOffset = 36
kVestelAcFanOffset = 40
kVestelAcFanSize = 4  # Nr. of bits
kVestelAcModeOffset = 44
kVestelAcIonOffset = 50
kVestelAcPowerOffset = 52
kVestelAcPowerSize = 2  # Nr. of bits
kVestelAcOffTimeOffset = 20
kVestelAcOnTimeOffset = 28
kVestelAcTimerHourSize = 5  # Nr. of bits
kVestelAcTimerMinsSize = 3  # Nr. of bits
kVestelAcTimerSize = kVestelAcTimerHourSize +
    kVestelAcTimerMinsSize  # Nr. of bits
kVestelAcHourOffset = 36  # 5 bits
kVestelAcHourSize = 5  # Nr. of bits
kVestelAcOnTimerFlagOffset = kVestelAcHourOffset + 5
kVestelAcOffTimerFlagOffset = kVestelAcHourOffset + 6
kVestelAcTimerFlagOffset = kVestelAcHourOffset + 7
kVestelAcMinuteOffset = 44
kVestelAcMinuteSize = 8  # Nr. of bits
# Default states
kVestelAcStateDefault = 0x0F00D9001FEF201ULL
kVestelAcTimeStateDefault = 0x201ULL

class IRVestelAc {
 public:
  explicit IRVestelAc(pin, bool inverted = False,
                      bool use_modulation = True)

  void stateReset(void)
#if SEND_VESTEL_AC
  void send(void)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_VESTEL_AC
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setAuto(int8_t autoLevel)
  void setTimer(minutes)
  getTimer(void)
  void setTime(minutes)
  getTime(void)
  void setOnTimer(minutes)
  getOnTimer(void)
  void setOffTimer(minutes)
  getOffTimer(void)
  void setTemp(temp)
  getTemp(void)
  void setFan(fan)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setRaw(uint8_t* newState)
  void setRaw(newState)
  getRaw(void)
  static bool validChecksum(state)
  void setSwing(bool on)
  bool getSwing(void)
  void setSleep(bool on)
  bool getSleep(void)
  void setTurbo(bool on)
  bool getTurbo(void)
  void setIon(bool on)
  bool getIon(void)
  bool isTimeCommand(void)
  bool isOnTimerActive(void)
  void setOnTimerActive(bool on)
  bool isOffTimerActive(void)
  void setOffTimerActive(bool on)
  bool isTimerActive(void)
  void setTimerActive(bool on)
  static calcChecksum(state)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
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
  remote_state
  remote_time_state
  bool use_time_state
  void checksum(void)
  void _setTimer(minutes, offset)
  _getTimer(offset)
}

#endif  # IR_VESTEL_H_

"""
# Copyright 2018 Erdem U. Altinyurt
# Copyright 2019 David Conran

# Vestel added by Erdem U. Altinyurt

#include "ir_Vestel.h"
#include <algorithm>
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRrecv.h"
#include "IRremoteESP8266.h"
#include "IRsend.h"
#include "IRtext.h"
#include "IRutils.h"
#include "ir_Haier.h"

# Equipment it seems compatible with:
#  * Vestel AC Model BIOX CXP-9 (9K BTU)
#  * <Add models (A/C & remotes) you've gotten it working with here>

# Ref:
#   None. Totally reverse engineered.

using irutils.addBoolToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.minsToString
using irutils.setBit
using irutils.setBits

#if SEND_VESTEL_AC
# Send a Vestel message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kVestelBits.
#
# Status: STABLE / Working.
#
void IRsend.sendVestelAc(data, nbits,
                          repeat) {
  if (nbits % 8 != 0) return  # nbits is required to be a multiple of 8.

  sendGeneric(kVestelAcHdrMark, kVestelAcHdrSpace,   # Header
              kVestelAcBitMark, kVestelAcOneSpace,   # Data
              kVestelAcBitMark, kVestelAcZeroSpace,  # Data
              kVestelAcBitMark, 100000,              # Footer + repeat gap
              data, nbits, 38, False, repeat, 50)
}
#endif

# Code to emulate Vestel A/C IR remote control unit.

# Initialise the object.
IRVestelAc.IRVestelAc(pin, bool inverted,
                       bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRVestelAc.stateReset(void) {
  # Power On, Mode Auto, Fan Auto, Temp = 25C/77F
  remote_state = kVestelAcStateDefault
  remote_time_state = kVestelAcTimeStateDefault
  use_time_state = False
}

# Configure the pin for output.
void IRVestelAc.begin(void) {
  _irsend.begin()
}

#if SEND_VESTEL_AC
# Send the current desired state to the IR LED.
void IRVestelAc.send(void) { _irsend.sendVestelAc(getRaw()) }
#endif  # SEND_VESTEL_AC

# Return the internal state date of the remote.
IRVestelAc.getRaw(void) {
  this->checksum()
  if (use_time_state) return remote_time_state
  return remote_state
}

# Override the internal state with the new state.
void IRVestelAc.setRaw(uint8_t* newState) {
  upState = 0
  for (int i = 0 i < 7 i++)
    upState |= static_cast<uint64_t>(newState[i]) << (i * 8)
  this->setRaw(upState)
}

void IRVestelAc.setRaw(newState) {
  use_time_state = False
  remote_state = newState
  remote_time_state = newState
  if (this->isTimeCommand()) {
    use_time_state = True
    remote_state = kVestelAcStateDefault
  } else {
    remote_time_state = kVestelAcTimeStateDefault
  }
}

# Set the requested power state of the A/C to on.
void IRVestelAc.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRVestelAc.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRVestelAc.setPower(bool on) {
  setBits(&remote_state, kVestelAcPowerOffset, kVestelAcPowerSize,
          on ? 0b11 : 0b00)
  use_time_state = False
}

# Return the requested power state of the A/C.
bool IRVestelAc.getPower(void) {
  return GETBITS64(remote_state, kVestelAcPowerOffset, kVestelAcPowerSize)
}

# Set the temperature in Celsius degrees.
void IRVestelAc.setTemp(temp) {
  new_temp = std.max(kVestelAcMinTempC, temp)
  new_temp = std.min(kVestelAcMaxTemp, new_temp)
  setBits(&remote_state, kVestelAcTempOffset, kNibbleSize,
          new_temp - kVestelAcMinTempH)
  use_time_state = False
}

# Return the set temperature.
IRVestelAc.getTemp(void) {
  return GETBITS64(remote_state, kVestelAcTempOffset, kNibbleSize) +
      kVestelAcMinTempH
}

# Set the speed of the fan,
void IRVestelAc.setFan(fan) {
  switch (fan) {
    case kVestelAcFanLow:
    case kVestelAcFanMed:
    case kVestelAcFanHigh:
    case kVestelAcFanAutoCool:
    case kVestelAcFanAutoHot:
    case kVestelAcFanAuto:
      setBits(&remote_state, kVestelAcFanOffset, kVestelAcFanSize, fan)
      break
    default:
      setFan(kVestelAcFanAuto)
  }
  use_time_state = False
}

# Return the requested state of the unit's fan.
IRVestelAc.getFan(void) {
  return GETBITS64(remote_state, kVestelAcFanOffset, kVestelAcFanSize)
}

# Get the requested climate operation mode of the a/c unit.
# Returns:
#   A containing the A/C mode.
IRVestelAc.getMode(void) {
  return GETBITS64(remote_state, kVestelAcModeOffset, kModeBitsSize)
}

# Set the requested climate operation mode of the a/c unit.
void IRVestelAc.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    case kVestelAcAuto:
    case kVestelAcCool:
    case kVestelAcHeat:
    case kVestelAcDry:
    case kVestelAcFan:
      setBits(&remote_state, kVestelAcModeOffset, kModeBitsSize, mode)
      break
    default:
      setMode(kVestelAcAuto)
  }
  use_time_state = False
}

# Set Auto mode of AC.
void IRVestelAc.setAuto(int8_t autoLevel) {
  if (autoLevel < -2 or autoLevel > 2) return
  setMode(kVestelAcAuto)
  setFan((autoLevel < 0 ? kVestelAcFanAutoCool : kVestelAcFanAutoHot))
  if (autoLevel == 2)
    setTemp(30)
  else if (autoLevel == 1)
    setTemp(31)
  else if (autoLevel == 0)
    setTemp(25)
  else if (autoLevel == -1)
    setTemp(16)
  else if (autoLevel == -2)
    setTemp(17)
}

void IRVestelAc.setTimerActive(bool on) {
  setBit(&remote_time_state, kVestelAcTimerFlagOffset, on)
  use_time_state = True
}

bool IRVestelAc.isTimerActive(void) {
  return GETBIT64(remote_time_state, kVestelAcTimerFlagOffset)
}

# Set Timer option of AC.
# Valid time arguments are 0, 0.5, 1, 2, 3 and 5 hours (in min). 0 disables the
# timer.
void IRVestelAc.setTimer(minutes) {
  # Clear both On & Off timers.
  remote_time_state &= ~((uint64_t)0xFFFF << kVestelAcOffTimeOffset)
  # Set the "Off" time with the nr of minutes before we turn off.
  remote_time_state |= (uint64_t)(((minutes / 60) << 3) + (minutes % 60) / 10)
                       << kVestelAcOffTimeOffset
  setOffTimerActive(False)
  # Yes. On Timer instead of Off timer active.
  setOnTimerActive(minutes != 0)
  setTimerActive(minutes != 0)
  use_time_state = True
}

IRVestelAc.getTimer(void) { return getOffTimer() }

# Set the AC's internal clock
void IRVestelAc.setTime(minutes) {
  setBits(&remote_time_state, kVestelAcHourOffset, kVestelAcHourSize,
          minutes / 60)
  setBits(&remote_time_state, kVestelAcMinuteOffset, kVestelAcMinuteSize,
          minutes % 60)
  use_time_state = True
}

IRVestelAc.getTime(void) {
  return GETBITS64(remote_time_state, kVestelAcHourOffset, kVestelAcHourSize) *
      60 + GETBITS64(remote_time_state, kVestelAcMinuteOffset,
                     kVestelAcMinuteSize)
}

void IRVestelAc.setOnTimerActive(bool on) {
  setBit(&remote_time_state, kVestelAcOnTimerFlagOffset, on)
  use_time_state = True
}

bool IRVestelAc.isOnTimerActive(void) {
  return GETBIT64(remote_time_state, kVestelAcOnTimerFlagOffset)
}

# Set a given timer (via offset). Takes time in nr. of minutes.
void IRVestelAc._setTimer(minutes, offset) {
  setBits(&remote_time_state, offset, kVestelAcTimerSize,
          ((minutes / 60) << 3) + (minutes % 60) / 10)
  setTimerActive(False)
  use_time_state = True
}

# Get the number of mins a timer is set for.
IRVestelAc._getTimer(offset) {
  return GETBITS64(remote_time_state, offset + kVestelAcTimerMinsSize,
                   kVestelAcTimerHourSize) * 60 +  # Hrs
      GETBITS64(remote_time_state, offset, kVestelAcTimerMinsSize) * 10  # Min
}
# Set AC's wake up time. Takes time in minute.
void IRVestelAc.setOnTimer(minutes) {
  setOnTimerActive(minutes)
  _setTimer(minutes, kVestelAcOnTimeOffset)
}

IRVestelAc.getOnTimer(void) {
  return _getTimer(kVestelAcOnTimeOffset)
}

void IRVestelAc.setOffTimerActive(bool on) {
  setBit(&remote_time_state, kVestelAcOffTimerFlagOffset, on)
  use_time_state = True
}

bool IRVestelAc.isOffTimerActive(void) {
  return GETBIT64(remote_time_state, kVestelAcOffTimerFlagOffset)
}

# Set AC's turn off time. Takes time in minute.
void IRVestelAc.setOffTimer(minutes) {
  setOffTimerActive(minutes)
  _setTimer(minutes, kVestelAcOffTimeOffset)
}

IRVestelAc.getOffTimer(void) {
  return _getTimer(kVestelAcOffTimeOffset)
}

# Set the Sleep state of the A/C.
void IRVestelAc.setSleep(bool on) {
  setBits(&remote_state, kVestelAcTurboSleepOffset, kNibbleSize,
          on ? kVestelAcSleep : kVestelAcNormal)
  use_time_state = False
}

# Return the Sleep state of the A/C.
bool IRVestelAc.getSleep(void) {
  return GETBITS64(remote_state, kVestelAcTurboSleepOffset, kNibbleSize) ==
      kVestelAcSleep
}

# Set the Turbo state of the A/C.
void IRVestelAc.setTurbo(bool on) {
  setBits(&remote_state, kVestelAcTurboSleepOffset, kNibbleSize,
          on ? kVestelAcTurbo : kVestelAcNormal)
  use_time_state = False
}

# Return the Turbo state of the A/C.
bool IRVestelAc.getTurbo(void) {
  return GETBITS64(remote_state, kVestelAcTurboSleepOffset, kNibbleSize) ==
      kVestelAcTurbo
}

# Set the Ion state of the A/C.
void IRVestelAc.setIon(bool on) {
  setBit(&remote_state, kVestelAcIonOffset, on)
  use_time_state = False
}

# Return the Ion state of the A/C.
bool IRVestelAc.getIon(void) {
  return GETBIT64(remote_state, kVestelAcIonOffset)
}

# Set the Swing Roaming state of the A/C.
void IRVestelAc.setSwing(bool on) {
  setBits(&remote_state, kVestelAcSwingOffset, kNibbleSize,
          on ? kVestelAcSwing : 0xF)
  use_time_state = False
}

# Return the Swing Roaming state of the A/C.
bool IRVestelAc.getSwing(void) {
  return GETBITS64(remote_state, kVestelAcSwingOffset, kNibbleSize) ==
      kVestelAcSwing
}

# Calculate the checksum for a given array.
# Args:
#   state:  The state to calculate the checksum over.
# Returns:
#   The 8 bit checksum value.
IRVestelAc.calcChecksum(state) {
  # Just counts the set bits +1 on stream and take inverse after mask
  return 0xFF - countBits(GETBITS64(state, 20, 44), 44, True, 2)
}

# Verify the checksum is valid for a given state.
# Args:
#   state:  The state to verify the checksum of.
# Returns:
#   A boolean.
bool IRVestelAc.validChecksum(state) {
  return GETBITS64(state, kVestelAcChecksumOffset, kVestelAcChecksumSize) ==
      IRVestelAc.calcChecksum(state)
}

# Calculate & set the checksum for the current internal state of the remote.
void IRVestelAc.checksum(void) {
  # Stored the checksum value in the last byte.
  setBits(&remote_state, kVestelAcChecksumOffset, kVestelAcChecksumSize,
          this->calcChecksum(remote_state))
  setBits(&remote_time_state, kVestelAcChecksumOffset, kVestelAcChecksumSize,
          this->calcChecksum(remote_time_state))
}

bool IRVestelAc.isTimeCommand(void) {
  return !GETBITS64(remote_state, kVestelAcPowerOffset, kNibbleSize) or
      use_time_state
}

# Convert a standard A/C mode into its native mode.
IRVestelAc.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kVestelAcCool
    case stdAc.opmode_t.kHeat: return kVestelAcHeat
    case stdAc.opmode_t.kDry:  return kVestelAcDry
    case stdAc.opmode_t.kFan:  return kVestelAcFan
    default:                     return kVestelAcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRVestelAc.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kVestelAcFanLow
    case stdAc.fanspeed_t.kMedium: return kVestelAcFanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kVestelAcFanHigh
    default:                         return kVestelAcFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRVestelAc.toCommonMode(mode) {
  switch (mode) {
    case kVestelAcCool: return stdAc.opmode_t.kCool
    case kVestelAcHeat: return stdAc.opmode_t.kHeat
    case kVestelAcDry:  return stdAc.opmode_t.kDry
    case kVestelAcFan:  return stdAc.opmode_t.kFan
    default:            return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRVestelAc.toCommonFanSpeed(spd) {
  switch (spd) {
    case kVestelAcFanHigh: return stdAc.fanspeed_t.kMax
    case kVestelAcFanMed:  return stdAc.fanspeed_t.kMedium
    case kVestelAcFanLow:  return stdAc.fanspeed_t.kMin
    default:               return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRVestelAc.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.VESTEL_AC
  result.model = -1  # Not supported.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->getSwing() ? stdAc.swingv_t.kAuto :
                                     stdAc.swingv_t.kOff
  result.turbo = this->getTurbo()
  result.filter = this->getIon()
  result.sleep = this->getSleep() ? 0 : -1
  # Not supported.
  result.swingh = stdAc.swingh_t.kOff
  result.light = False
  result.econo = False
  result.quiet = False
  result.clean = False
  result.beep = False
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRVestelAc.toString(void) {
  String result = ""
  result.reserve(100)  # Reserve some heap for the string to reduce fragging.
  if (this->isTimeCommand()) {
    result += addLabeledString(minsToString(getTime()), kClockStr, False)
    result += addLabeledString(
        isTimerActive() ? minsToString(getTimer()) : kOffStr,
        kTimerStr)
    result += addLabeledString(
        (isOnTimerActive() and !isTimerActive()) ?
          minsToString(this->getOnTimer()) : kOffStr,
        kOnTimerStr)
    result += addLabeledString(
        isOffTimerActive() ? minsToString(getOffTimer()) : kOffStr,
        kOffTimerStr)
    return result
  }
  # Not a time command, it's a normal command.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kVestelAcAuto, kVestelAcCool,
                            kVestelAcHeat, kVestelAcDry, kVestelAcFan)
  result += addTempToString(getTemp())
  result += addIntToString(getFan(), kFanStr)
  result += kSpaceLBraceStr
  switch (this->getFan()) {
    case kVestelAcFanAuto:
      result += kAutoStr
      break
    case kVestelAcFanLow:
      result += kLowStr
      break
    case kVestelAcFanMed:
      result += kMedStr
      break
    case kVestelAcFanHigh:
      result += kHighStr
      break
    case kVestelAcFanAutoCool:
      result += kAutoStr
      result += ' '
      result += kCoolStr
      break
    case kVestelAcFanAutoHot:
      result += kAutoStr
      result += ' '
      result += kHeatStr
      break
    default:
      result += kUnknownStr
  }
  result += ')'
  result += addBoolToString(getSleep(), kSleepStr)
  result += addBoolToString(getTurbo(), kTurboStr)
  result += addBoolToString(getIon(), kIonStr)
  result += addBoolToString(getSwing(), kSwingStr)
  return result
}

#if DECODE_VESTEL_AC
# Decode the supplied Vestel message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kVestelBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Needs testing against a real device.
#
bool IRrecv.decodeVestelAc(decode_results* results, nbits,
                            bool strict) {
  if (nbits % 8 != 0)  # nbits has to be a multiple of nr. of bits in a byte.
    return False

  if (strict)
    if (nbits != kVestelAcBits)
      return False  # Not strictly a Vestel AC message.

  data = 0
  offset = kStartOffset

  if (nbits > sizeof(data) * 8)
    return False  # We can't possibly capture a Vestel packet that big.

  # Match Header + Data + Footer
  if (!matchGeneric(results->rawbuf + offset, &data,
                    results->rawlen - offset, nbits,
                    kVestelAcHdrMark, kVestelAcHdrSpace,
                    kVestelAcBitMark, kVestelAcOneSpace,
                    kVestelAcBitMark, kVestelAcZeroSpace,
                    kVestelAcBitMark, 0, False,
                    kVestelAcTolerance, kMarkExcess, False)) return False
  # Compliance
  if (strict)
    if (!IRVestelAc.validChecksum(data)) return False

  # Success
  results->decode_type = VESTEL_AC
  results->bits = nbits
  results->value = data
  results->address = 0
  results->command = 0

  return True
}
#endif  # DECODE_VESTEL_AC
