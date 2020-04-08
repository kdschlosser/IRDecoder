"""
# Copyright 2017 David Conran

# Toshiba A/C support added by David Conran

# Supports:
#   Brand: Toshiba,  Model: RAS-B13N3KV2
#   Brand: Toshiba,  Model: Akita EVO II
#   Brand: Toshiba,  Model: RAS-B13N3KVP-E
#   Brand: Toshiba,  Model: RAS 18SKP-ES
#   Brand: Toshiba,  Model: WH-TA04NE
#   Brand: Toshiba,  Model: WC-L03SE

#ifndef IR_TOSHIBA_H_
#define IR_TOSHIBA_H_

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

# Constants
kToshibaAcModeOffset = 0
kToshibaAcModeSize = 2  # Nr. of bits
kToshibaAcAuto = 0
kToshibaAcCool = 1
kToshibaAcDry = 2
kToshibaAcHeat = 3
kToshibaAcPowerOffset = 2
kToshibaAcFanOffset = 5
kToshibaAcFanSize = 3  # Nr. of bits
kToshibaAcFanAuto = 0b000
kToshibaAcFanMin =  0b001
kToshibaAcFanMed =  0b011
kToshibaAcFanMax =  0b101
kToshibaAcTempOffset = 4
kToshibaAcTempSize = 4  # Nr. of bits
kToshibaAcMinTemp = 17  # 17C
kToshibaAcMaxTemp = 30  # 30C

# Legacy defines. (Deperecated)
#define TOSHIBA_AC_AUTO kToshibaAcAuto
#define TOSHIBA_AC_COOL kToshibaAcCool
#define TOSHIBA_AC_DRY kToshibaAcDry
#define TOSHIBA_AC_HEAT kToshibaAcHeat
#define TOSHIBA_AC_POWER kToshibaAcPower
#define TOSHIBA_AC_FAN_AUTO kToshibaAcFanAuto
#define TOSHIBA_AC_FAN_MAX kToshibaAcFanMax
#define TOSHIBA_AC_MIN_TEMP kToshibaAcMinTemp
#define TOSHIBA_AC_MAX_TEMP kToshibaAcMaxTemp

class IRToshibaAC {
 public:
  explicit IRToshibaAC(pin, bool inverted = False,
                       bool use_modulation = True)

  void stateReset(void)
#if SEND_TOSHIBA_AC
  void send(repeat = kToshibaACMinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_TOSHIBA_AC
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
  getMode(bool useRaw = False)
  void setRaw(newState[])
  uint8_t* getRaw(void)
  static bool validChecksum(state[],
                            length = kToshibaACStateLength)
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
  remote_state[kToshibaACStateLength]
  void checksum(length = kToshibaACStateLength)
  static calcChecksum(state[],
                              length = kToshibaACStateLength)
  mode_state
}

#endif  # IR_TOSHIBA_H_

"""
# Copyright 2017 David Conran

# Toshiba A/C support added by David Conran


#include "ir_Toshiba.h"
#include <algorithm>
#include <cstring>
#ifndef ARDUINO
#include <string>
#endif
#include "IRrecv.h"
#include "IRsend.h"
#include "IRtext.h"
#include "IRutils.h"

#
# Equipment it seems compatible with:
#  * Toshiba RAS-B13N3KV2 / Akita EVO II
#  * Toshiba RAS-B13N3KVP-E, RAS 18SKP-ES
#  * Toshiba WH-TA04NE, WC-L03SE
#  * <Add models (A/C & remotes) you've gotten it working with here>

# Constants

# Toshiba A/C
# Ref:
#   https:#github.com/r45635/HVAC-IR-Control/blob/master/HVAC_ESP8266/HVAC_ESP8266T.ino#L77
kToshibaAcHdrMark = 4400
kToshibaAcHdrSpace = 4300
kToshibaAcBitMark = 543
kToshibaAcOneSpace = 1623
kToshibaAcZeroSpace = 472
kToshibaAcMinGap = 7048

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_TOSHIBA_AC
# Send a Toshiba A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kToshibaACStateLength)
#   repeat: Nr. of times the message is to be repeated.
#          (Default = kToshibaACMinRepeat).
#
# Status: StABLE / Working.
#
void IRsend.sendToshibaAC(unsigned char data[], nbytes,
                           repeat) {
  if (nbytes < kToshibaACStateLength)
    return  # Not enough bytes to send a proper message.
  sendGeneric(kToshibaAcHdrMark, kToshibaAcHdrSpace, kToshibaAcBitMark,
              kToshibaAcOneSpace, kToshibaAcBitMark, kToshibaAcZeroSpace,
              kToshibaAcBitMark, kToshibaAcMinGap, data, nbytes, 38, True,
              repeat, 50)
}
#endif  # SEND_TOSHIBA_AC

# Code to emulate Toshiba A/C IR remote control unit.
# Inspired and derived from the work done at:
#   https:#github.com/r45635/HVAC-IR-Control
#
# Status:  STABLE / Working.
#
# Initialise the object.
IRToshibaAC.IRToshibaAC(pin, bool inverted,
                         bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRToshibaAC.stateReset(void) {
  # The state of the IR remote in IR code form.
  # Known good state obtained from:
  #   https:#github.com/r45635/HVAC-IR-Control/blob/master/HVAC_ESP8266/HVAC_ESP8266T.ino#L103
  static kReset[kToshibaACStateLength] = {
      0xF2, 0x0D, 0x03, 0xFC, 0x01}
  memcpy(remote_state, kReset, kToshibaACStateLength)
  mode_state = getMode(True)
}

# Configure the pin for output.
void IRToshibaAC.begin(void) { _irsend.begin() }

#if SEND_TOSHIBA_AC
# Send the current desired state to the IR LED.
void IRToshibaAC.send(repeat) {
  _irsend.sendToshibaAC(getRaw(), kToshibaACStateLength, repeat)
}
#endif  # SEND_TOSHIBA_AC

# Return a pointer to the internal state date of the remote.
uint8_t* IRToshibaAC.getRaw(void) {
  this->checksum()
  return remote_state
}

# Override the internal state with the new state.
void IRToshibaAC.setRaw(newState[]) {
  memcpy(remote_state, newState, kToshibaACStateLength)
  mode_state = this->getMode(True)
}

# Calculate the checksum for a given array.
# Args:
#   state:  The array to calculate the checksum over.
#   length: The size of the array.
# Returns:
#   The 8 bit checksum value.
IRToshibaAC.calcChecksum(state[],
                                  length) {
  checksum = 0
  # Only calculate it for valid lengths.
  if (length > 1) {
    # Checksum is simple XOR of all bytes except the last one.
    for (i = 0 i < length - 1 i++) checksum ^= state[i]
  }
  return checksum
}

# Verify the checksum is valid for a given state.
# Args:
#   state:  The array to verify the checksum of.
#   length: The size of the state.
# Returns:
#   A boolean.
bool IRToshibaAC.validChecksum(state[], length) {
  return (length > 1 and state[length - 1] == IRToshibaAC.calcChecksum(state,
                                                                       length))
}

# Calculate & set the checksum for the current internal state of the remote.
void IRToshibaAC.checksum(length) {
  # Stored the checksum value in the last byte.
  if (length > 1) remote_state[length - 1] = this->calcChecksum(remote_state,
                                                                length)
}

# Set the requested power state of the A/C to on.
void IRToshibaAC.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRToshibaAC.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRToshibaAC.setPower(bool on) {
  setBit(&remote_state[6], kToshibaAcPowerOffset, !on)  # Cleared when on.
  if (on)
    setMode(mode_state)
  else
    setBits(&remote_state[6], kToshibaAcModeOffset, kToshibaAcModeSize,
            kToshibaAcHeat)
}

# Return the requested power state of the A/C.
bool IRToshibaAC.getPower(void) {
  return !GETBIT8(remote_state[6], kToshibaAcPowerOffset)
}

# Set the temp. in deg C
void IRToshibaAC.setTemp(degrees) {
  temp = std.max((uint8_t)kToshibaAcMinTemp, degrees)
  temp = std.min((uint8_t)kToshibaAcMaxTemp, temp)
  setBits(&remote_state[5], kToshibaAcTempOffset, kToshibaAcTempSize,
          temp - kToshibaAcMinTemp)
}

# Return the set temp. in deg C
IRToshibaAC.getTemp(void) {
  return GETBITS8(remote_state[5], kToshibaAcTempOffset, kToshibaAcTempSize) +
      kToshibaAcMinTemp
}

# Set the speed of the fan, 0-5.
# 0 is auto, 1-5 is the speed, 5 is Max.
void IRToshibaAC.setFan(speed) {
  fan = speed
  # Bounds check
  if (fan > kToshibaAcFanMax)
    fan = kToshibaAcFanMax  # Set the fan to maximum if out of range.
  if (fan > kToshibaAcFanAuto) fan++
  setBits(&remote_state[6], kToshibaAcFanOffset, kToshibaAcFanSize, fan)
}

# Return the requested state of the unit's fan.
IRToshibaAC.getFan(void) {
  fan = GETBITS8(remote_state[6], kToshibaAcFanOffset,
                         kToshibaAcFanSize)
  if (fan == kToshibaAcFanAuto) return kToshibaAcFanAuto
  return --fan
}

# Get the requested climate operation mode of the a/c unit.
# Args:
#   useRaw:  Indicate to get the mode from the state array. (Default: False)
# Returns:
#   A containing the A/C mode.
IRToshibaAC.getMode(bool useRaw) {
  if (useRaw)
    return GETBITS8(remote_state[6], kToshibaAcModeOffset, kToshibaAcModeSize)
  else
    return mode_state
}

# Set the requested climate operation mode of the a/c unit.
void IRToshibaAC.setMode(mode) {
  # If we get an unexpected mode, default to AUTO.
  switch (mode) {
    case kToshibaAcAuto:
    case kToshibaAcCool:
    case kToshibaAcDry:
    case kToshibaAcHeat:
      mode_state = mode
      # Only adjust the remote_state if we have power set to on.
      if (getPower())
        setBits(&remote_state[6], kToshibaAcModeOffset, kToshibaAcModeSize,
                mode_state)
      return
    default: this->setMode(kToshibaAcAuto)  # There is no Fan mode.
  }
}

# Convert a standard A/C mode into its native mode.
IRToshibaAC.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kToshibaAcCool
    case stdAc.opmode_t.kHeat: return kToshibaAcHeat
    case stdAc.opmode_t.kDry:  return kToshibaAcDry
    # No Fan mode.
    default:                     return kToshibaAcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRToshibaAC.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:    return kToshibaAcFanMax - 4
    case stdAc.fanspeed_t.kLow:    return kToshibaAcFanMax - 3
    case stdAc.fanspeed_t.kMedium: return kToshibaAcFanMax - 2
    case stdAc.fanspeed_t.kHigh:   return kToshibaAcFanMax - 1
    case stdAc.fanspeed_t.kMax:    return kToshibaAcFanMax
    default:                         return kToshibaAcFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRToshibaAC.toCommonMode(mode) {
  switch (mode) {
    case kToshibaAcCool: return stdAc.opmode_t.kCool
    case kToshibaAcHeat: return stdAc.opmode_t.kHeat
    case kToshibaAcDry:  return stdAc.opmode_t.kDry
    default:             return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRToshibaAC.toCommonFanSpeed(spd) {
  switch (spd) {
    case kToshibaAcFanMax:     return stdAc.fanspeed_t.kMax
    case kToshibaAcFanMax - 1: return stdAc.fanspeed_t.kHigh
    case kToshibaAcFanMax - 2: return stdAc.fanspeed_t.kMedium
    case kToshibaAcFanMax - 3: return stdAc.fanspeed_t.kLow
    case kToshibaAcFanMax - 4: return stdAc.fanspeed_t.kMin
    default:                   return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRToshibaAC.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.TOSHIBA_AC
  result.model = -1  # Not supported.
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  # Not supported.
  result.turbo = False
  result.light = False
  result.filter = False
  result.econo = False
  result.swingv = stdAc.swingv_t.kOff
  result.swingh = stdAc.swingh_t.kOff
  result.quiet = False
  result.clean = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRToshibaAC.toString(void) {
  String result = ""
  result.reserve(40)
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kToshibaAcAuto, kToshibaAcCool,
                            kToshibaAcHeat, kToshibaAcDry, kToshibaAcAuto)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kToshibaAcFanMax, kToshibaAcFanMin,
                           kToshibaAcFanAuto, kToshibaAcFanAuto,
                           kToshibaAcFanMed)
  return result
}

#if DECODE_TOSHIBA_AC
# Decode a Toshiba AC IR message if possible.
# Places successful decode information in the results pointer.
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kToshibaACBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status:  STABLE / Working.
#
# Ref:
#
bool IRrecv.decodeToshibaAC(decode_results* results, nbits,
                             bool strict) {
  offset = kStartOffset

  # Compliance
  if (strict and nbits != kToshibaACBits)
    return False  # Must be called with the correct nr. of bytes.

  # Match Header + Data + Footer
  if (!matchGeneric(results->rawbuf + offset, results->state,
                    results->rawlen - offset, nbits,
                    kToshibaAcHdrMark, kToshibaAcHdrSpace,
                    kToshibaAcBitMark, kToshibaAcOneSpace,
                    kToshibaAcBitMark, kToshibaAcZeroSpace,
                    kToshibaAcBitMark, kToshibaAcMinGap, True,
                    _tolerance, kMarkExcess)) return False
  # Compliance
  if (strict) {
    # Check that the checksum of the message is correct.
    if (!IRToshibaAC.validChecksum(results->state)) return False
  }

  # Success
  results->decode_type = TOSHIBA_AC
  results->bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result->state, we don't record value, address, or command as it
  # is a union data type.
  return True
}
#endif  # DECODE_TOSHIBA_AC
