"""
# Copyright 2019 Fabien Valthier

#ifndef IR_TECO_H_
#define IR_TECO_H_

#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Supports:
#   Brand: Alaska,  Model: SAC9010QC A/C
#   Brand: Alaska,  Model: SAC9010QC remote

# Constants.
kTecoAuto = 0
kTecoCool = 1
kTecoDry = 2
kTecoFan = 3
kTecoHeat = 4
kTecoFanAuto = 0  # 0b00
kTecoFanLow = 1   # 0b01
kTecoFanMed = 2   # 0b10
kTecoFanHigh = 3  # 0b11
kTecoMinTemp = 16   # 16C
kTecoMaxTemp = 30   # 30C

kTecoModeOffset = 0
kTecoPowerOffset = 3
kTecoFanOffset = 4
kTecoFanSize = 2  # Nr. of bits
kTecoSwingOffset = 6
kTecoSleepOffset = 7
kTecoTempOffset = 8
kTecoTempSize = 4  # Nr. of bits
kTecoTimerHalfHourOffset = 12
kTecoTimerTensHoursOffset = 13
kTecoTimerTensHoursSize = 2  # Nr. of bits
kTecoTimerOnOffset = 15
kTecoTimerUnitHoursOffset = 16
kTecoTimerUnitHoursSize = 4  # Nr. of bits
kTecoHumidOffset = 20
kTecoLightOffset = 21
kTecoSaveOffset = 23
kTecoReset =      0b01001010000000000000010000000000000
/*
  (header mark and space)
        Teco AC map read and to be sent in LSB with number of bits

  byte 0 = Cst 0x02
  byte 1 = Cst 0x50
    b6-7 = "AIR" 0, 1, 2 (Not Implemented)
  byte 2:
    b0 = Save
    b1 = "Tree with bubbles" / Filter?? (Not Implemented)
    b2 = Light/LED.
    b3 = Humid
    b4-7 = Timer hours (unit, not thenth)
      hours:
        0000 (0) = +0 hour
        0001 (1) = +1 hour
        ...
        1001 (9) = +9 hours
  byte 3: = timer and Temperature
    b0 = Timer (1 = On, 0 = Off)
    b1-2 = Timer - number of 10hours
      10Hours:
        00 = 0 * 10hours of timer
        01 = 1 * 10 hours of timer
        10 = 2 * 10hours of timer
    b3 = Timer - half hour (1=half hour on, 0 = round hour)
    b4-7: Degrees C.
      0000 (0) = 16C
      0001 (1) = 17C
      0010 (2) = 18C
      ...
      1101 (13) = 29C
      1110 (14) = 30C
  byte 4: Basics
    b0 = Sleep Mode (1 = On, 0 = Off)
    b1 = Vent swing (1 = On, 0 = Off)
    b2-3 = Fan
      Fan:
        00 = Auto
        01 = Fan 1
        10 = Fan 2
        11 = Fan 3 or higher
    b4 = Power Status (1 = On, 0 = Off)
    b5-7 = Modes LSB first
      Modes:
        000 = Auto (temp = 25C)
        001 = Cool
        010 = Dry (temp = 25C, but not shown)
        011 = Fan
        100 = Heat
*/

# Classes
class IRTecoAc {
 public:
  explicit IRTecoAc(pin, bool inverted = False,
                    bool use_modulation = True)

  void stateReset(void)
#if SEND_TECO
  void send(repeat = kTecoDefaultRepeat)
#endif  # SEND_TECO
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

  void setSwing(bool on)
  bool getSwing(void)

  void setSleep(bool on)
  bool getSleep(void)

  void setLight(bool on)
  bool getLight(void)

  void setHumid(bool on)
  bool getHumid(void)

  void setSave(bool on)
  bool getSave(void)

  getTimer(void)
  void setTimer(mins)

  getRaw(void)
  void setRaw(new_code)

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
  remote_state
  bool getTimerEnabled(void)
}

#endif  # IR_TECO_H_

"""
# Copyright 2019 Fabien Valthier
/*
Node MCU/ESP8266 Sketch to emulate Teco
*/

#include "ir_Teco.h"
#include <algorithm>
#include "IRremoteESP8266.h"
#include "IRtext.h"
#include "IRutils.h"
#ifndef ARDUINO
#include <string>
#endif

# Constants
# using SPACE modulation.
kTecoHdrMark = 9000
kTecoHdrSpace = 4440
kTecoBitMark = 620
kTecoOneSpace = 1650
kTecoZeroSpace = 580
kTecoGap = kDefaultMessageGap  # Made-up value. Just a guess.

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_TECO
# Send a Teco A/C message.
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kTecoBits.
#   repeat: Nr. of additional times the message is to be sent.
void IRsend.sendTeco(data, nbits,
                      repeat) {
  sendGeneric(kTecoHdrMark, kTecoHdrSpace, kTecoBitMark, kTecoOneSpace,
              kTecoBitMark, kTecoZeroSpace, kTecoBitMark, kTecoGap,
              data, nbits, 38000, False, repeat, kDutyDefault)
}
#endif  # SEND_TECO

# Class for decoding and constructing Teco AC messages.
IRTecoAc.IRTecoAc(pin, bool inverted,
                   bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

void IRTecoAc.begin(void) { _irsend.begin() }

#if SEND_TECO
void IRTecoAc.send(repeat) {
  _irsend.sendTeco(remote_state, kTecoBits, repeat)
}
#endif  # SEND_TECO

void IRTecoAc.stateReset(void) {
  # Mode:auto, Power:Off, fan:auto, temp:16, swing:off, sleep:off
  remote_state = kTecoReset
}

IRTecoAc.getRaw(void) { return remote_state }

void IRTecoAc.setRaw(new_code) { remote_state = new_code }

void IRTecoAc.on(void) { setPower(True) }

void IRTecoAc.off(void) { setPower(False) }

void IRTecoAc.setPower(bool on) {
  setBit(&remote_state, kTecoPowerOffset, on)
}

bool IRTecoAc.getPower(void) {
  return GETBIT64(remote_state, kTecoPowerOffset)
}

void IRTecoAc.setTemp(temp) {
  newtemp = temp
  newtemp = std.min(newtemp, kTecoMaxTemp)
  newtemp = std.max(newtemp, kTecoMinTemp)
  setBits(&remote_state, kTecoTempOffset, kTecoTempSize,
          newtemp - kTecoMinTemp)
}

IRTecoAc.getTemp(void) {
  return GETBITS64(remote_state, kTecoTempOffset, kTecoTempSize) + kTecoMinTemp
}

# Set the speed of the fan
void IRTecoAc.setFan(speed) {
  newspeed = speed
  switch (speed) {
    case kTecoFanAuto:
    case kTecoFanHigh:
    case kTecoFanMed:
    case kTecoFanLow: break
    default: newspeed = kTecoFanAuto
  }
  setBits(&remote_state, kTecoFanOffset, kTecoFanSize, newspeed)
}

IRTecoAc.getFan(void) {
  return GETBITS64(remote_state, kTecoFanOffset, kTecoFanSize)
}

void IRTecoAc.setMode(mode) {
  newmode = mode
  switch (mode) {
    case kTecoAuto:
    case kTecoCool:
    case kTecoDry:
    case kTecoFan:
    case kTecoHeat: break
    default: newmode = kTecoAuto
  }
  setBits(&remote_state, kTecoModeOffset, kModeBitsSize, newmode)
}

IRTecoAc.getMode(void) {
  return GETBITS64(remote_state, kTecoModeOffset, kModeBitsSize)
}

void IRTecoAc.setSwing(bool on) {
  setBit(&remote_state, kTecoSwingOffset, on)
}

bool IRTecoAc.getSwing(void) {
  return GETBIT64(remote_state, kTecoSwingOffset)
}

void IRTecoAc.setSleep(bool on) {
  setBit(&remote_state, kTecoSleepOffset, on)
}

bool IRTecoAc.getSleep(void) {
  return GETBIT64(remote_state, kTecoSleepOffset)
}

void IRTecoAc.setLight(bool on) {
  setBit(&remote_state, kTecoLightOffset, on)
}

bool IRTecoAc.getLight(void) {
  return GETBIT64(remote_state,  kTecoLightOffset)
}

void IRTecoAc.setHumid(bool on) {
  setBit(&remote_state, kTecoHumidOffset, on)
}

bool IRTecoAc.getHumid(void) {
  return GETBIT64(remote_state, kTecoHumidOffset)
}

void IRTecoAc.setSave(bool on) {
  setBit(&remote_state, kTecoSaveOffset, on)
}

bool IRTecoAc.getSave(void) {
  return GETBIT64(remote_state, kTecoSaveOffset)
}

bool IRTecoAc.getTimerEnabled(void) {
  return GETBIT64(remote_state, kTecoTimerOnOffset)
}

IRTecoAc.getTimer(void) {
  mins = 0
  if (getTimerEnabled()) {
    mins = GETBITS64(remote_state, kTecoTimerTensHoursOffset,
                     kTecoTimerTensHoursSize) * 60 * 10 +
        GETBITS64(remote_state, kTecoTimerUnitHoursOffset,
                  kTecoTimerUnitHoursSize) * 60
    if (GETBIT64(remote_state, kTecoTimerHalfHourOffset)) mins += 30
  }
  return mins
}

# Set the timer for when the A/C unit will switch power state.
# Args:
#   nr_mins: Number of minutes before power state change.
#            `0` will clear the timer. Max is 24 hrs.
#            Time is stored internaly in increments of 30 mins.
void IRTecoAc.setTimer(nr_mins) {
  mins = std.min(nr_mins, (uint16_t)(24 * 60))  # Limit to 24 hrs.
  hours = mins / 60
  setBit(&remote_state, kTecoTimerOnOffset, mins)  # Set the timer flag.
  # Set the half hour bit.
  setBit(&remote_state, kTecoTimerHalfHourOffset, (mins % 60) >= 30)
  # Set the unit hours.
  setBits(&remote_state, kTecoTimerUnitHoursOffset, kTecoTimerUnitHoursSize,
          hours % 10)
  # Set the tens of hours.
  setBits(&remote_state, kTecoTimerTensHoursOffset, kTecoTimerTensHoursSize,
          hours / 10)
}

# Convert a standard A/C mode into its native mode.
IRTecoAc.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kTecoCool
    case stdAc.opmode_t.kHeat: return kTecoHeat
    case stdAc.opmode_t.kDry:  return kTecoDry
    case stdAc.opmode_t.kFan:  return kTecoFan
    default:                     return kTecoAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRTecoAc.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kTecoFanLow
    case stdAc.fanspeed_t.kMedium: return kTecoFanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kTecoFanHigh
    default:                         return kTecoFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRTecoAc.toCommonMode(mode) {
  switch (mode) {
    case kTecoCool: return stdAc.opmode_t.kCool
    case kTecoHeat: return stdAc.opmode_t.kHeat
    case kTecoDry:  return stdAc.opmode_t.kDry
    case kTecoFan:  return stdAc.opmode_t.kFan
    default:        return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRTecoAc.toCommonFanSpeed(speed) {
  switch (speed) {
    case kTecoFanHigh: return stdAc.fanspeed_t.kMax
    case kTecoFanMed:  return stdAc.fanspeed_t.kMedium
    case kTecoFanLow:  return stdAc.fanspeed_t.kMin
    default:           return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRTecoAc.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.TECO
  result.model = -1  # Not supported.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->getSwing() ? stdAc.swingv_t.kAuto :
                                     stdAc.swingv_t.kOff
  result.sleep = this->getSleep() ? 0 : -1
  result.light = this->getLight()
  # Not supported.
  result.swingh = stdAc.swingh_t.kOff
  result.turbo = False
  result.filter = False
  result.econo = False
  result.quiet = False
  result.clean = False
  result.beep = False
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRTecoAc.toString(void) {
  String result = ""
  result.reserve(100)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kTecoAuto, kTecoCool, kTecoHeat,
                            kTecoDry, kTecoFan)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kTecoFanHigh, kTecoFanLow,
                           kTecoFanAuto, kTecoFanAuto, kTecoFanMed)
  result += addBoolToString(getSleep(), kSleepStr)
  result += addBoolToString(getSwing(), kSwingStr)
  result += addBoolToString(getLight(), kLightStr)
  result += addBoolToString(getHumid(), kHumidStr)
  result += addBoolToString(getSave(), kSaveStr)
  if (getTimerEnabled())
    result += addLabeledString(irutils.minsToString(getTimer()),
                               kTimerStr)
  else
    result += addBoolToString(False, kTimerStr)
  return result
}

#if DECODE_TECO
# Decode the supplied Teco message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kTecoBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Tested.
bool IRrecv.decodeTeco(decode_results* results,
                        nbits, bool strict) {
  if (strict and nbits != kTecoBits) return False  # Not what is expected

  data = 0
  offset = kStartOffset
  # Match Header + Data + Footer
  if (!matchGeneric(results->rawbuf + offset, &data,
                    results->rawlen - offset, nbits,
                    kTecoHdrMark, kTecoHdrSpace,
                    kTecoBitMark, kTecoOneSpace,
                    kTecoBitMark, kTecoZeroSpace,
                    kTecoBitMark, kTecoGap, True,
                    _tolerance, kMarkExcess, False)) return False

  # Success
  results->decode_type = TECO
  results->bits = nbits
  results->value = data
  results->address = 0
  results->command = 0
  return True
}
#endif  # DECODE_TECO
