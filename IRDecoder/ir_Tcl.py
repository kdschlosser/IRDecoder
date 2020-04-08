"""
# Copyright 2019 David Conran

# Supports:
#   Brand: Leberg,  Model: LBS-TOR07 A/C

#ifndef IR_TCL_H_
#define IR_TCL_H_

#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#include "IRrecv.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Constants
kTcl112AcHdrMark = 3000
kTcl112AcHdrSpace = 1650
kTcl112AcBitMark = 500
kTcl112AcOneSpace = 1050
kTcl112AcZeroSpace = 325
kTcl112AcGap = kDefaultMessageGap  # Just a guess.
# Total tolerance percentage to use for matching the header mark.
kTcl112AcHdrMarkTolerance = 6
kTcl112AcTolerance = 5  # Extra Percentage for the rest.

kTcl112AcHeat = 1
kTcl112AcDry =  2
kTcl112AcCool = 3
kTcl112AcFan =  7
kTcl112AcAuto = 8
kTcl112AcModeSize = 4  # Nr. of Bits

kTcl112AcFanSize = 3  # Nr. of Bits. Mask = 0b00000111
kTcl112AcFanAuto = 0b000
kTcl112AcFanLow  = 0b010
kTcl112AcFanMed  = 0b011
kTcl112AcFanHigh = 0b101

kTcl112AcHalfDegreeOffset = 5
float   kTcl112AcTempMax    = 31.0
float   kTcl112AcTempMin    = 16.0

kTcl112AcPowerOffset = 2
kTcl112AcBitEconoOffset = 7
kTcl112AcBitLightOffset = 6
kTcl112AcBitHealthOffset = 4
kTcl112AcBitSwingHOffset = 3
kTcl112AcSwingVOffset = 3  # Mask 0b00111000
kTcl112AcSwingVSize = 3  # Nr. of bits.
kTcl112AcSwingVOn =    0b111
kTcl112AcSwingVOff =   0b000
kTcl112AcBitTurboOffset = 6


class IRTcl112Ac {
 public:
  explicit IRTcl112Ac(pin, bool inverted = False,
                      bool use_modulation = True)

#if SEND_TCL112AC
  void send(repeat = kTcl112AcDefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_TCL
  void begin(void)
  uint8_t* getRaw(void)
  void setRaw(new_code[],
              length = kTcl112AcStateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(float celsius)  # Celsius in 0.5 increments
  float getTemp(void)
  void setMode(mode)
  getMode(void)
  static calcChecksum(state[],
                              length = kTcl112AcStateLength)
  static bool validChecksum(state[],
                            length = kTcl112AcStateLength)
  void setFan(speed)
  getFan(void)
  void setEcono(bool on)
  bool getEcono(void)
  void setHealth(bool on)
  bool getHealth(void)
  void setLight(bool on)
  bool getLight(void)
  void setSwingHorizontal(bool on)
  bool getSwingHorizontal(void)
  void setSwingVertical(bool on)
  bool getSwingVertical(void)
  void setTurbo(bool on)
  bool getTurbo(void)
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
  remote_state[kTcl112AcStateLength]
  void stateReset(void)
  void checksum(length = kTcl112AcStateLength)
}

#endif  # IR_TCL_H_

"""
# Copyright 2019 David Conran

#include "ir_Tcl.h"
#include <algorithm>
#include <cstring>
#ifndef ARDUINO
#include <string>
#endif
#include "IRremoteESP8266.h"
#include "IRtext.h"
#include "IRutils.h"

# Constants

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_TCL112AC
void IRsend.sendTcl112Ac(unsigned char data[], nbytes,
                          repeat) {
  sendGeneric(kTcl112AcHdrMark, kTcl112AcHdrSpace,
              kTcl112AcBitMark, kTcl112AcOneSpace,
              kTcl112AcBitMark, kTcl112AcZeroSpace,
              kTcl112AcBitMark, kTcl112AcGap,
              data, nbytes, 38000, False, repeat, 50)
}
#endif  # SEND_TCL112AC

IRTcl112Ac.IRTcl112Ac(pin, bool inverted,
                       bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { stateReset() }

void IRTcl112Ac.begin(void) { this->_irsend.begin() }

#if SEND_TCL112AC
void IRTcl112Ac.send(repeat) {
  this->_irsend.sendTcl112Ac(getRaw(), kTcl112AcStateLength, repeat)
}
#endif  # SEND_TCL112AC

# Calculate the checksum for a given array.
# Args:
#   state:  The array to calculate the checksum over.
#   length: The size of the array.
# Returns:
#   The 8 bit checksum value.
IRTcl112Ac.calcChecksum(state[], length) {
  if (length)
    return sumBytes(state, length - 1)
  else
    return 0
}

# Calculate & set the checksum for the current internal state of the remote.
void IRTcl112Ac.checksum(length) {
  # Stored the checksum value in the last byte.
  if (length > 1)
    remote_state[length - 1] = calcChecksum(remote_state, length)
}

# Verify the checksum is valid for a given state.
# Args:
#   state:  The array to verify the checksum of.
#   length: The size of the state.
# Returns:
#   A boolean.
bool IRTcl112Ac.validChecksum(state[], length) {
  return (length > 1 and state[length - 1] == calcChecksum(state, length))
}

void IRTcl112Ac.stateReset(void) {
  # A known good state. (On, Cool, 24C)
  static reset[kTcl112AcStateLength] = {
      0x23, 0xCB, 0x26, 0x01, 0x00, 0x24, 0x03, 0x07, 0x40, 0x00, 0x00, 0x00,
      0x00, 0x03}
  memcpy(remote_state, reset, kTcl112AcStateLength)
}

uint8_t* IRTcl112Ac.getRaw(void) {
  this->checksum()
  return remote_state
}

void IRTcl112Ac.setRaw(new_code[], length) {
  memcpy(remote_state, new_code, std.min(length, kTcl112AcStateLength))
}

# Set the requested power state of the A/C to on.
void IRTcl112Ac.on(void) { this->setPower(True) }

# Set the requested power state of the A/C to off.
void IRTcl112Ac.off(void) { this->setPower(False) }

# Set the requested power state of the A/C.
void IRTcl112Ac.setPower(bool on) {
  setBit(&remote_state[5], kTcl112AcPowerOffset, on)
}

# Return the requested power state of the A/C.
bool IRTcl112Ac.getPower(void) {
  return GETBIT8(remote_state[5], kTcl112AcPowerOffset)
}

# Get the requested climate operation mode of the a/c unit.
# Returns:
#   A containing the A/C mode.
IRTcl112Ac.getMode(void) {
  return remote_state[6] & 0xF
}

# Set the requested climate operation mode of the a/c unit.
# Note: Fan/Ventilation mode sets the fan speed to high.
#       Unknown values default to Auto.
void IRTcl112Ac.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    case kTcl112AcFan:
      this->setFan(kTcl112AcFanHigh)
      # FALLTHRU
    case kTcl112AcAuto:
    case kTcl112AcCool:
    case kTcl112AcHeat:
    case kTcl112AcDry:
      setBits(&remote_state[6], kLowNibble, kTcl112AcModeSize, mode)
      break
    default:
      setMode(kTcl112AcAuto)
  }
}

void IRTcl112Ac.setTemp(float celsius) {
  # Make sure we have desired temp in the correct range.
  float safecelsius = std.max(celsius, kTcl112AcTempMin)
  safecelsius = std.min(safecelsius, kTcl112AcTempMax)
  # Convert to integer nr. of half degrees.
  nrHalfDegrees = safecelsius * 2
  # Do we have a half degree celsius?
  setBit(&remote_state[12], kTcl112AcHalfDegreeOffset, nrHalfDegrees & 1)
  setBits(&remote_state[7], kLowNibble, kNibbleSize,
          (uint8_t)kTcl112AcTempMax - nrHalfDegrees / 2)
}

float IRTcl112Ac.getTemp(void) {
  float result = kTcl112AcTempMax - GETBITS8(remote_state[7], kLowNibble,
                                             kNibbleSize)
  if (GETBIT8(remote_state[12], kTcl112AcHalfDegreeOffset)) result += 0.5
  return result
}

# Set the speed of the fan.
# Unknown speeds will default to Auto.
void IRTcl112Ac.setFan(speed) {
  switch (speed) {
    case kTcl112AcFanAuto:
    case kTcl112AcFanLow:
    case kTcl112AcFanMed:
    case kTcl112AcFanHigh:
      setBits(&remote_state[8], kLowNibble, kTcl112AcFanSize, speed)
      break
    default:
      this->setFan(kTcl112AcFanAuto)
  }
}

# Return the currect fan speed.
IRTcl112Ac.getFan(void) {
  return GETBITS8(remote_state[8], kLowNibble, kTcl112AcFanSize)
}

# Control economy mode.
void IRTcl112Ac.setEcono(bool on) {
  setBit(&remote_state[5], kTcl112AcBitEconoOffset, on)
}

# Return the economy state of the A/C.
bool IRTcl112Ac.getEcono(void) {
  return GETBIT8(remote_state[5],  kTcl112AcBitEconoOffset)
}

# Control Health mode.
void IRTcl112Ac.setHealth(bool on) {
  setBit(&remote_state[6], kTcl112AcBitHealthOffset, on)
}

# Return the Health mode state of the A/C.
bool IRTcl112Ac.getHealth(void) {
  return GETBIT8(remote_state[6], kTcl112AcBitHealthOffset)
}

# Control Light/Display mode.
void IRTcl112Ac.setLight(bool on) {
  setBit(&remote_state[5], kTcl112AcBitLightOffset, !on)  # Cleared when on.
}

# Return the Light/Display mode state of the A/C.
bool IRTcl112Ac.getLight(void) {
  return !GETBIT8(remote_state[5],  kTcl112AcBitLightOffset)
}

# Control Horizontal Swing.
void IRTcl112Ac.setSwingHorizontal(bool on) {
  setBit(&remote_state[12], kTcl112AcBitSwingHOffset, on)
}

# Return the Horizontal Swing state of the A/C.
bool IRTcl112Ac.getSwingHorizontal(void) {
  return GETBIT8(remote_state[12], kTcl112AcBitSwingHOffset)
}

# Control Vertical Swing.
void IRTcl112Ac.setSwingVertical(bool on) {
  setBits(&remote_state[8], kTcl112AcSwingVOffset, kTcl112AcSwingVSize,
          on ? kTcl112AcSwingVOn : kTcl112AcSwingVOff)
}

# Return the Vertical Swing state of the A/C.
bool IRTcl112Ac.getSwingVertical(void) {
  return GETBITS8(remote_state[8], kTcl112AcSwingVOffset, kTcl112AcSwingVSize)
}

# Control the Turbo setting.
void IRTcl112Ac.setTurbo(bool on) {
  setBit(&remote_state[6], kTcl112AcBitTurboOffset, on)
  if (on) {
    this->setFan(kTcl112AcFanHigh)
    this->setSwingVertical(True)
  }
}

# Return the Turbo setting state of the A/C.
bool IRTcl112Ac.getTurbo(void) {
  return GETBIT8(remote_state[6], kTcl112AcBitTurboOffset)
}

# Convert a standard A/C mode into its native mode.
IRTcl112Ac.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kTcl112AcCool
    case stdAc.opmode_t.kHeat: return kTcl112AcHeat
    case stdAc.opmode_t.kDry:  return kTcl112AcDry
    case stdAc.opmode_t.kFan:  return kTcl112AcFan
    default:                     return kTcl112AcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRTcl112Ac.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kTcl112AcFanLow
    case stdAc.fanspeed_t.kMedium: return kTcl112AcFanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kTcl112AcFanHigh
    default:                         return kTcl112AcFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRTcl112Ac.toCommonMode(mode) {
  switch (mode) {
    case kTcl112AcCool: return stdAc.opmode_t.kCool
    case kTcl112AcHeat: return stdAc.opmode_t.kHeat
    case kTcl112AcDry:  return stdAc.opmode_t.kDry
    case kTcl112AcFan:  return stdAc.opmode_t.kFan
    default:            return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRTcl112Ac.toCommonFanSpeed(spd) {
  switch (spd) {
    case kTcl112AcFanHigh: return stdAc.fanspeed_t.kMax
    case kTcl112AcFanMed:  return stdAc.fanspeed_t.kMedium
    case kTcl112AcFanLow:  return stdAc.fanspeed_t.kMin
    default:               return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRTcl112Ac.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.TCL112AC
  result.model = -1  # Not supported.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.swingv = this->getSwingVertical() ? stdAc.swingv_t.kAuto :
                                             stdAc.swingv_t.kOff
  result.swingh = this->getSwingHorizontal() ? stdAc.swingh_t.kAuto :
                                               stdAc.swingh_t.kOff
  result.turbo = this->getTurbo()
  result.light = this->getLight()
  result.filter = this->getHealth()
  result.econo = this->getEcono()
  # Not supported.
  result.quiet = False
  result.clean = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRTcl112Ac.toString(void) {
  String result = ""
  result.reserve(140)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kTcl112AcAuto, kTcl112AcCool,
                            kTcl112AcHeat, kTcl112AcDry, kTcl112AcFan)
  nrHalfDegrees = this->getTemp() * 2
  result += addIntToString(nrHalfDegrees / 2, kTempStr)
  if (nrHalfDegrees & 1) result += F(".5")
  result += 'C'
  result += addFanToString(getFan(), kTcl112AcFanHigh, kTcl112AcFanLow,
                           kTcl112AcFanAuto, kTcl112AcFanAuto, kTcl112AcFanMed)
  result += addBoolToString(getEcono(), kEconoStr)
  result += addBoolToString(getHealth(), kHealthStr)
  result += addBoolToString(getLight(), kLightStr)
  result += addBoolToString(getTurbo(), kTurboStr)
  result += addBoolToString(getSwingHorizontal(), kSwingHStr)
  result += addBoolToString(getSwingVertical(), kSwingVStr)
  return result
}

#if DECODE_TCL112AC
# NOTE: There is no `decodedecodeTcl112Ac()`.
#       It's the same as `decodeMitsubishi112()`. A shared routine is used.
#       You can find it in: ir_Mitsubishi.cpp
#endif  # DECODE_TCL112AC
