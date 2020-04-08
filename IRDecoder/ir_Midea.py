"""
# Copyright 2017 David Conran
# Midea

# Supports:
#   Brand: Pioneer System,  Model: RYBO12GMFILCAD A/C (12K BTU)
#   Brand: Pioneer System,  Model: RUBO18GMFILCAD A/C (18K BTU)
#   Brand: Comfee, Model: MPD1-12CRN7 A/C
#   Brand: Keystone, Model: RG57H4(B)BGEF remote

#ifndef IR_MIDEA_H_
#define IR_MIDEA_H_

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

# Midea added by crankyoldgit & bwze
# Ref:
#   https:#docs.google.com/spreadsheets/d/1TZh4jWrx4h9zzpYUI9aYXMl1fYOiqu-xVuOOMqagxrs/edit?usp=sharing

# Constants
kMideaACTempOffset = 24
kMideaACTempSize = 5  # Bits
kMideaACMinTempF = 62  # Fahrenheit
kMideaACMaxTempF = 86  # Fahrenheit
kMideaACMinTempC = 17  # Celsius
kMideaACMaxTempC = 30  # Celsius
kMideaACCelsiusOffset = 29
kMideaACModeOffset = 32
kMideaACCool = 0     # 0b000
kMideaACDry = 1      # 0b001
kMideaACAuto = 2     # 0b010
kMideaACHeat = 3     # 0b011
kMideaACFan = 4      # 0b100
kMideaACFanOffset = 35
kMideaACFanSize = 2  # Bits
kMideaACFanAuto = 0  # 0b00
kMideaACFanLow = 1   # 0b01
kMideaACFanMed = 2   # 0b10
kMideaACFanHigh = 3  # 0b11
kMideaACSleepOffset = 38
kMideaACPowerOffset = 39
kMideaACToggleSwingV = 0x0000A201FFFFFF7C

# Legacy defines. (Deprecated)
#define MIDEA_AC_COOL kMideaACCool
#define MIDEA_AC_DRY kMideaACDry
#define MIDEA_AC_AUTO kMideaACAuto
#define MIDEA_AC_HEAT kMideaACHeat
#define MIDEA_AC_FAN kMideaACFan
#define MIDEA_AC_FAN_AUTO kMideaACFanAuto
#define MIDEA_AC_FAN_LOW kMideaACFanLow
#define MIDEA_AC_FAN_MED kMideaACFanMed
#define MIDEA_AC_FAN_HI kMideaACFanHigh
#define MIDEA_AC_POWER kMideaACPower
#define MIDEA_AC_SLEEP kMideaACSleep
#define MIDEA_AC_MIN_TEMP_F kMideaACMinTempF
#define MIDEA_AC_MAX_TEMP_F kMideaACMaxTempF
#define MIDEA_AC_MIN_TEMP_C kMideaACMinTempC
#define MIDEA_AC_MAX_TEMP_C kMideaACMaxTempC

class IRMideaAC {
 public:
  explicit IRMideaAC(pin, bool inverted = False,
                     bool use_modulation = True)

  void stateReset(void)
#if SEND_MIDEA
  void send(repeat = kMideaMinRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_MIDEA
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  bool getUseCelsius(void)
  void setUseCelsius(bool celsius)
  void setTemp(temp, bool useCelsius = False)
  getTemp(bool useCelsius = False)
  void setFan(fan)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setRaw(newState)
  getRaw(void)
  static bool validChecksum(state)
  void setSleep(bool on)
  bool getSleep(void)
  bool isSwingVToggle(void)
  void setSwingVToggle(bool on)
  bool getSwingVToggle(void)
  convertMode(stdAc.opmode_t mode)
  convertFan(stdAc.fanspeed_t speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  stdAc.state_t toCommon(stdAc.state_t *prev = NULL)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  remote_state
  bool _SwingVToggle
  void checksum(void)
  static calcChecksum(state)
}

#endif  # IR_MIDEA_H_

"""
# Copyright 2017 bwze, crankyoldgit
# Midea

#include "ir_Midea.h"
#include <algorithm>
#ifndef ARDUINO
#include <string>
#endif
#include "IRrecv.h"
#include "IRsend.h"
#include "IRtext.h"
#include "IRutils.h"

# Midea A/C added by (send) bwze/crankyoldgit & (decode) crankyoldgit
#
# Equipment it seems compatible with:
#  * Pioneer System Model RYBO12GMFILCAD (12K BTU)
#  * Pioneer System Model RUBO18GMFILCAD (18K BTU)
#  * <Add models (A/C & remotes) you've gotten it working with here>

# Ref:
#   https:#docs.google.com/spreadsheets/d/1TZh4jWrx4h9zzpYUI9aYXMl1fYOiqu-xVuOOMqagxrs/edit?usp=sharing

# Constants
kMideaTick = 80
kMideaBitMarkTicks = 7
kMideaBitMark = kMideaBitMarkTicks * kMideaTick
kMideaOneSpaceTicks = 21
kMideaOneSpace = kMideaOneSpaceTicks * kMideaTick
kMideaZeroSpaceTicks = 7
kMideaZeroSpace = kMideaZeroSpaceTicks * kMideaTick
kMideaHdrMarkTicks = 56
kMideaHdrMark = kMideaHdrMarkTicks * kMideaTick
kMideaHdrSpaceTicks = 56
kMideaHdrSpace = kMideaHdrSpaceTicks * kMideaTick
kMideaMinGapTicks =
    kMideaHdrMarkTicks + kMideaZeroSpaceTicks + kMideaBitMarkTicks
kMideaMinGap = kMideaMinGapTicks * kMideaTick
kMideaTolerance = 30  # Percent

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_MIDEA
# Send a Midea message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kMideaBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: Alpha / Needs testing against a real device.
#
void IRsend.sendMidea(data, nbits, repeat) {
  if (nbits % 8 != 0) return  # nbits is required to be a multiple of 8.

  # Set IR carrier frequency
  enableIROut(38)

  for (r = 0 r <= repeat r++) {
    # The protcol sends the message, then follows up with an entirely
    # inverted payload.
    for (size_t inner_loop = 0 inner_loop < 2 inner_loop++) {
      # Header
      mark(kMideaHdrMark)
      space(kMideaHdrSpace)
      # Data
      #   Break data into byte segments, starting at the Most Significant
      #   Byte. Each byte then being sent normal, then followed inverted.
      for (i = 8 i <= nbits i += 8) {
        # Grab a bytes worth of data.
        segment = (data >> (nbits - i)) & 0xFF
        sendData(kMideaBitMark, kMideaOneSpace, kMideaBitMark, kMideaZeroSpace,
                 segment, 8, True)
      }
      # Footer
      mark(kMideaBitMark)
      space(kMideaMinGap)  # Pause before repeating

      # Invert the data for the 2nd phase of the message.
      # As we get called twice in the inner loop, we will always revert
      # to the original 'data' state.
      data = ~data
    }
  }
}
#endif

# Code to emulate Midea A/C IR remote control unit.
# Warning: Consider this very alpha code.

# Initialise the object.
IRMideaAC.IRMideaAC(pin, bool inverted,
                     bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

# Reset the state of the remote to a known good state/sequence.
void IRMideaAC.stateReset(void) {
  # Power On, Mode Auto, Fan Auto, Temp = 25C/77F
  remote_state = 0xA1826FFFFF62
  _SwingVToggle = False
}

# Configure the pin for output.
void IRMideaAC.begin(void) { _irsend.begin() }

#if SEND_MIDEA
# Send the current desired state to the IR LED.
void IRMideaAC.send(repeat) {
  this->checksum()  # Ensure correct checksum before sending.
  _irsend.sendMidea(remote_state, kMideaBits, repeat)
  # Handle toggling the swing if we need to.
  if (_SwingVToggle and !isSwingVToggle()) {
    _irsend.sendMidea(kMideaACToggleSwingV, kMideaBits, repeat)
  }
  _SwingVToggle = False  # The toggle message has been sent, so reset.
}
#endif  # SEND_MIDEA

# Return a pointer to the internal state date of the remote.
IRMideaAC.getRaw(void) {
  this->checksum()
  return GETBITS64(remote_state, 0, kMideaBits)
}

# Override the internal state with the new state.
void IRMideaAC.setRaw(newState) { remote_state = newState }

# Set the requested power state of the A/C to on.
void IRMideaAC.on(void) { setPower(True) }

# Set the requested power state of the A/C to off.
void IRMideaAC.off(void) { setPower(False) }

# Set the requested power state of the A/C.
void IRMideaAC.setPower(bool on) {
  setBit(&remote_state, kMideaACPowerOffset, on)
}

# Return the requested power state of the A/C.
bool IRMideaAC.getPower(void) {
  return GETBIT64(remote_state, kMideaACPowerOffset)
}

# Returns True if we want the A/C unit to work natively in Celsius.
bool IRMideaAC.getUseCelsius(void) {
  return !GETBIT64(remote_state, kMideaACCelsiusOffset)
}

# Set the A/C unit to use Celsius natively.
void IRMideaAC.setUseCelsius(bool on) {
  if (on != getUseCelsius()) {  # We need to change.
    native_temp = getTemp(!on)  # Get the old native temp.
    setBit(&remote_state, kMideaACCelsiusOffset, !on)  # Cleared is on.
    setTemp(native_temp, !on)  # Reset temp using the old native temp.
  }
}

# Set the temperature.
# Args:
#   temp:       Temp. in degrees.
#   useCelsius: Degree type to use. Celsius (True) or Fahrenheit (False)
void IRMideaAC.setTemp(temp, bool useCelsius) {
  max_temp = kMideaACMaxTempF
  min_temp = kMideaACMinTempF
  if (useCelsius) {
    max_temp = kMideaACMaxTempC
    min_temp = kMideaACMinTempC
  }
  new_temp = std.min(max_temp, std.max(min_temp, temp))
  if (getUseCelsius() and !useCelsius)  # Native is in C, new_temp is in F
    new_temp = fahrenheitToCelsius(new_temp) - kMideaACMinTempC
  else if (!getUseCelsius() and useCelsius)  # Native is in F, new_temp is in C
    new_temp = celsiusToFahrenheit(new_temp) - kMideaACMinTempF
  else  # Native and desired are the same units.
    new_temp -= min_temp
  # Set the actual data.
  setBits(&remote_state, kMideaACTempOffset, kMideaACTempSize, new_temp)
}

# Return the set temp.
# Args:
#   celsius: Flag indicating if the results are in Celsius or Fahrenheit.
# Returns:
#   A containing the temperature.
IRMideaAC.getTemp(bool celsius) {
  temp = GETBITS64(remote_state, kMideaACTempOffset, kMideaACTempSize)
  if (getUseCelsius())
    temp += kMideaACMinTempC
  else
    temp += kMideaACMinTempF
  if (celsius and !getUseCelsius()) temp = fahrenheitToCelsius(temp) + 0.5
  if (!celsius and getUseCelsius()) temp = celsiusToFahrenheit(temp)
  return temp
}

# Set the speed of the fan,
# 1-3 set the speed, 0 or anything else set it to auto.
void IRMideaAC.setFan(fan) {
  setBits(&remote_state, kMideaACFanOffset, kMideaACFanSize,
          (fan > kMideaACFanHigh) ? kMideaACFanAuto : fan)
}

# Return the requested state of the unit's fan.
IRMideaAC.getFan(void) {
  return GETBITS64(remote_state, kMideaACFanOffset, kMideaACFanSize)
}

# Get the requested climate operation mode of the a/c unit.
# Returns:
#   A containing the A/C mode.
IRMideaAC.getMode(void) {
  return GETBITS64(remote_state, kMideaACModeOffset, kModeBitsSize)
}

# Set the requested climate operation mode of the a/c unit.
void IRMideaAC.setMode(mode) {
  switch (mode) {
    case kMideaACAuto:
    case kMideaACCool:
    case kMideaACHeat:
    case kMideaACDry:
    case kMideaACFan:
      setBits(&remote_state, kMideaACModeOffset, kModeBitsSize, mode)
      break
    default:
      this->setMode(kMideaACAuto)
  }
}

# Set the Sleep state of the A/C.
void IRMideaAC.setSleep(bool on) {
  setBit(&remote_state, kMideaACSleepOffset, on)
}

# Return the Sleep state of the A/C.
bool IRMideaAC.getSleep(void) {
  return GETBIT64(remote_state, kMideaACSleepOffset)
}

# Set the A/C to toggle the vertical swing toggle for the next send.
void IRMideaAC.setSwingVToggle(bool on) { _SwingVToggle = on }

# Return if the message/state is just a Swing V toggle message/command.
bool IRMideaAC.isSwingVToggle(void) {
  return remote_state == kMideaACToggleSwingV
}

# Return the Swing V toggle state of the A/C.
bool IRMideaAC.getSwingVToggle(void) {
  _SwingVToggle |= isSwingVToggle()
  return _SwingVToggle
}

# Calculate the checksum for a given array.
# Args:
#   state:  The state to calculate the checksum over.
# Returns:
#   The 8 bit checksum value.
IRMideaAC.calcChecksum(state) {
  sum = 0
  temp_state = state

  for (i = 0 i < 5 i++) {
    temp_state >>= 8
    sum += reverseBits((temp_state & 0xFF), 8)
  }
  sum = 256 - sum
  return reverseBits(sum, 8)
}

# Verify the checksum is valid for a given state.
# Args:
#   state:  The state to verify the checksum of.
# Returns:
#   A boolean.
bool IRMideaAC.validChecksum(state) {
  return GETBITS64(state, 0, 8) == calcChecksum(state)
}

# Calculate & set the checksum for the current internal state of the remote.
void IRMideaAC.checksum(void) {
  # Stored the checksum value in the last byte.
  setBits(&remote_state, 0, 8, calcChecksum(remote_state))
}


# Convert a standard A/C mode into its native mode.
IRMideaAC.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kMideaACCool
    case stdAc.opmode_t.kHeat: return kMideaACHeat
    case stdAc.opmode_t.kDry:  return kMideaACDry
    case stdAc.opmode_t.kFan:  return kMideaACFan
    default:                     return kMideaACAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRMideaAC.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kMideaACFanLow
    case stdAc.fanspeed_t.kMedium: return kMideaACFanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kMideaACFanHigh
    default:                         return kMideaACFanAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRMideaAC.toCommonMode(mode) {
  switch (mode) {
    case kMideaACCool: return stdAc.opmode_t.kCool
    case kMideaACHeat: return stdAc.opmode_t.kHeat
    case kMideaACDry:  return stdAc.opmode_t.kDry
    case kMideaACFan:  return stdAc.opmode_t.kFan
    default:           return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRMideaAC.toCommonFanSpeed(speed) {
  switch (speed) {
    case kMideaACFanHigh: return stdAc.fanspeed_t.kMax
    case kMideaACFanMed:  return stdAc.fanspeed_t.kMedium
    case kMideaACFanLow:  return stdAc.fanspeed_t.kMin
    default:              return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRMideaAC.toCommon(stdAc.state_t *prev) {
  stdAc.state_t result
  if (prev != NULL) {
    result = *prev
  } else {
  # Fixed/Not supported/Non-zero defaults.
  result.protocol = decode_type_t.MIDEA
  result.model = -1  # No models used.
  result.swingh = stdAc.swingh_t.kOff
  result.swingv = stdAc.swingv_t.kOff
  result.quiet = False
  result.turbo = False
  result.clean = False
  result.econo = False
  result.filter = False
  result.light = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  }
  if (this->isSwingVToggle()) {
    result.swingv = result.swingv != stdAc.swingv_t.kOff ?
        stdAc.swingv_t.kAuto : stdAc.swingv_t.kOff
    return result
  }
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = this->getUseCelsius()
  result.degrees = this->getTemp(result.celsius)
  result.fanspeed = this->toCommonFanSpeed(this->getFan())
  result.sleep = this->getSleep() ? 0 : -1
  return result
}

# Convert the internal state into a human readable string.
String IRMideaAC.toString(void) {
  String result = ""
  result.reserve(100)  # Reserve some heap for the string to reduce fragging.
  if (!isSwingVToggle()) {
    result += addBoolToString(getPower(), kPowerStr, False)
    result += addModeToString(getMode(), kMideaACAuto, kMideaACCool,
                              kMideaACHeat, kMideaACDry, kMideaACFan)
    result += addBoolToString(getUseCelsius(), kCelsiusStr)
    result += addTempToString(getTemp(True))
    result += '/'
    result += uint64ToString(getTemp(False))
    result += 'F'
    result += addFanToString(getFan(), kMideaACFanHigh, kMideaACFanLow,
                             kMideaACFanAuto, kMideaACFanAuto, kMideaACFanMed)
    result += addBoolToString(getSleep(), kSleepStr)
  }
  result += addBoolToString(getSwingVToggle(), kSwingVToggleStr,
                            !isSwingVToggle())
  return result
}

#if DECODE_MIDEA
# Decode the supplied Midea message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kMideaBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Needs testing against a real device.
#
bool IRrecv.decodeMidea(decode_results *results, nbits, bool strict) {
  min_nr_of_messages = 1
  if (strict) {
    if (nbits != kMideaBits) return False  # Not strictly a MIDEA message.
    min_nr_of_messages = 2
  }

  # The protocol sends the data normal + inverted, alternating on
  # each byte. Hence twice the number of expected data bits.
  if (results->rawlen <
      min_nr_of_messages * (2 * nbits + kHeader + kFooter) - 1)
    return False  # Can't possibly be a valid MIDEA message.

  data = 0
  inverted = 0
  offset = kStartOffset

  if (nbits > sizeof(data) * 8)
    return False  # We can't possibly capture a Midea packet that big.

  for (i = 0 i < min_nr_of_messages i++) {
    # Match Header + Data + Footer
    used
    used = matchGeneric(results->rawbuf + offset, i % 2 ? &inverted : &data,
                        results->rawlen - offset, nbits,
                        kMideaHdrMark, kMideaHdrSpace,
                        kMideaBitMark, kMideaOneSpace,
                        kMideaBitMark, kMideaZeroSpace,
                        kMideaBitMark, kMideaMinGap, False, kMideaTolerance)
    if (!used) return False
    offset += used
  }

  # Compliance
  if (strict) {
    # Protocol requires a second message with all the data bits inverted.
    # We should have checked we got a second message in the previous loop.
    # Just need to check it's value is an inverted copy of the first message.
    mask = (1ULL << kMideaBits) - 1
    if ((data & mask) != ((inverted ^ mask) & mask)) return False
    if (!IRMideaAC.validChecksum(data)) return False
  }

  # Success
  results->decode_type = MIDEA
  results->bits = nbits
  results->value = data
  results->address = 0
  results->command = 0
  return True
}
#endif  # DECODE_MIDEA
