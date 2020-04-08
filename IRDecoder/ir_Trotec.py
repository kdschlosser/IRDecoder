"""
# Copyright 2017 stufisher
# Copyright 2019 crankyoldgit

#ifndef IR_TROTEC_H_
#define IR_TROTEC_H_

#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRsend.h"
#ifdef UNIT_TEST
#include "IRsend_test.h"
#endif

# Constants
# Byte 0
kTrotecIntro1 = 0x12

# Byte 1
kTrotecIntro2 = 0x34

# Byte 2
kTrotecModeOffset = 0
kTrotecModeSize = 2  # Nr. of bits
kTrotecAuto = 0
kTrotecCool = 1
kTrotecDry = 2
kTrotecFan = 3

kTrotecPowerBitOffset = 3

kTrotecFanOffset = 4
kTrotecFanSize = 2  # Nr. of bits
kTrotecFanLow = 1
kTrotecFanMed = 2
kTrotecFanHigh = 3

# Byte 3
kTrotecTempOffset = 0
kTrotecTempSize = 4  # Nr. of bits
kTrotecMinTemp = 18
kTrotecDefTemp = 25
kTrotecMaxTemp = 32
kTrotecSleepBitOffset = 7

# Byte 5
kTrotecTimerBitOffset = 6

# Byte 6
kTrotecMaxTimer = 23

# Legacy defines. (Deperecated)
#define TROTEC_AUTO kTrotecAuto
#define TROTEC_COOL kTrotecCool
#define TROTEC_DRY kTrotecDry
#define TROTEC_FAN kTrotecFan
#define TROTEC_FAN_LOW kTrotecFanLow
#define TROTEC_FAN_MED kTrotecFanMed
#define TROTEC_FAN_HIGH kTrotecFanHigh
#define TROTEC_MIN_TEMP kTrotecMinTemp
#define TROTEC_MAX_TEMP kTrotecMaxTemp
#define TROTEC_MAX_TIMER kTrotecMaxTimer

class IRTrotecESP {
 public:
  explicit IRTrotecESP(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_TROTEC
  void send(repeat = kTrotecDefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_TROTEC
  void begin(void)

  void setPower(bool state)
  bool getPower(void)

  void setTemp(celsius)
  getTemp(void)

  void setSpeed(fan)
  getSpeed(void)

  getMode(void)
  void setMode(mode)

  bool getSleep(void)
  void setSleep(bool on)

  getTimer(void)
  void setTimer(timer)

  uint8_t* getRaw(void)
  void setRaw(state[])
  static bool validChecksum(state[],
                            length = kTrotecStateLength)
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
  remote_state[kTrotecStateLength]
  static calcChecksum(state[],
                              length = kTrotecStateLength)
  void stateReset(void)
  void checksum(void)
}

#endif  # IR_TROTEC_H_

"""
# Copyright 2017 stufisher
# Copyright 2019 crankyoldgit

#include "ir_Trotec.h"
#include <algorithm>
#include <cstring>
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include "IRremoteESP8266.h"
#include "IRtext.h"
#include "IRutils.h"

# Constants
kTrotecHdrMark = 5952
kTrotecHdrSpace = 7364
kTrotecBitMark = 592
kTrotecOneSpace = 1560
kTrotecZeroSpace = 592
kTrotecGap = 6184
kTrotecGapEnd = 1500  # made up value

using irutils.addBoolToString
using irutils.addFanToString
using irutils.addIntToString
using irutils.addLabeledString
using irutils.addModeToString
using irutils.addTempToString
using irutils.setBit
using irutils.setBits

#if SEND_TROTEC

void IRsend.sendTrotec(unsigned char data[], nbytes,
                        repeat) {
  if (nbytes < kTrotecStateLength) return

  enableIROut(36)
  for (r = 0 r <= repeat r++) {
    sendGeneric(kTrotecHdrMark, kTrotecHdrSpace, kTrotecBitMark,
                kTrotecOneSpace, kTrotecBitMark, kTrotecZeroSpace,
                kTrotecBitMark, kTrotecGap, data, nbytes, 36, False,
                0,  # Repeats handled elsewhere
                50)
    # More footer
    mark(kTrotecBitMark)
    space(kTrotecGapEnd)
  }
}
#endif  # SEND_TROTEC

IRTrotecESP.IRTrotecESP(pin, bool inverted,
                         bool use_modulation)
    : _irsend(pin, inverted, use_modulation) { this->stateReset() }

void IRTrotecESP.begin(void) { _irsend.begin() }

#if SEND_TROTEC
void IRTrotecESP.send(repeat) {
  this->checksum()
  _irsend.sendTrotec(remote_state, kTrotecStateLength, repeat)
}
#endif  # SEND_TROTEC

IRTrotecESP.calcChecksum(state[],
                                  length) {
  return sumBytes(state + 2, length - 3)
}

bool IRTrotecESP.validChecksum(state[], length) {
  return state[length - 1] == calcChecksum(state, length)
}

void IRTrotecESP.checksum(void) {
  remote_state[kTrotecStateLength - 1] = sumBytes(remote_state + 2,
                                                  kTrotecStateLength - 3)
}

void IRTrotecESP.stateReset(void) {
  for (i = 2 i < kTrotecStateLength i++) remote_state[i] = 0x0

  remote_state[0] = kTrotecIntro1
  remote_state[1] = kTrotecIntro2

  this->setPower(False)
  this->setTemp(kTrotecDefTemp)
  this->setSpeed(kTrotecFanMed)
  this->setMode(kTrotecAuto)
}

uint8_t* IRTrotecESP.getRaw(void) {
  this->checksum()
  return remote_state
}

void IRTrotecESP.setRaw(state[]) {
  memcpy(remote_state, state, kTrotecStateLength)
}

void IRTrotecESP.setPower(bool on) {
  setBit(&remote_state[2], kTrotecPowerBitOffset, on)
}

bool IRTrotecESP.getPower(void) {
  return GETBIT8(remote_state[2], kTrotecPowerBitOffset)
}

void IRTrotecESP.setSpeed(fan) {
  speed = std.min(fan, kTrotecFanHigh)
  setBits(&remote_state[2], kTrotecFanOffset, kTrotecFanSize, speed)
}

IRTrotecESP.getSpeed(void) {
  return GETBITS8(remote_state[2], kTrotecFanOffset, kTrotecFanSize)
}

void IRTrotecESP.setMode(mode) {
  setBits(&remote_state[2], kTrotecModeOffset, kTrotecModeSize,
          (mode > kTrotecFan) ? kTrotecAuto : mode)
}

IRTrotecESP.getMode(void) {
  return GETBITS8(remote_state[2], kTrotecModeOffset, kTrotecModeSize)
}

void IRTrotecESP.setTemp(celsius) {
  temp = std.max(celsius, kTrotecMinTemp)
  temp = std.min(temp, kTrotecMaxTemp)
  setBits(&remote_state[3], kTrotecTempOffset, kTrotecTempSize,
          temp - kTrotecMinTemp)
}

IRTrotecESP.getTemp(void) {
  return GETBITS8(remote_state[3], kTrotecTempOffset, kTrotecTempSize) +
      kTrotecMinTemp
}

void IRTrotecESP.setSleep(bool on) {
  setBit(&remote_state[3], kTrotecSleepBitOffset, on)
}

bool IRTrotecESP.getSleep(void) {
  return GETBIT8(remote_state[3], kTrotecSleepBitOffset)
}

void IRTrotecESP.setTimer(timer) {
  setBit(&remote_state[5], kTrotecTimerBitOffset, timer)
  remote_state[6] = (timer > kTrotecMaxTimer) ? kTrotecMaxTimer : timer
}

IRTrotecESP.getTimer(void) { return remote_state[6] }

# Convert a standard A/C mode into its native mode.
IRTrotecESP.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kTrotecCool
    case stdAc.opmode_t.kDry:  return kTrotecDry
    case stdAc.opmode_t.kFan:  return kTrotecFan
    # Note: No Heat mode.
    default:                     return kTrotecAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRTrotecESP.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:
    case stdAc.fanspeed_t.kLow:    return kTrotecFanLow
    case stdAc.fanspeed_t.kMedium: return kTrotecFanMed
    case stdAc.fanspeed_t.kHigh:
    case stdAc.fanspeed_t.kMax:    return kTrotecFanHigh
    default:                         return kTrotecFanMed
  }
}


# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRTrotecESP.toCommonMode(mode) {
  switch (mode) {
    case kTrotecCool: return stdAc.opmode_t.kCool
    case kTrotecDry:  return stdAc.opmode_t.kDry
    case kTrotecFan:  return stdAc.opmode_t.kFan
    default:          return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRTrotecESP.toCommonFanSpeed(spd) {
  switch (spd) {
    case kTrotecFanHigh: return stdAc.fanspeed_t.kMax
    case kTrotecFanMed:  return stdAc.fanspeed_t.kMedium
    case kTrotecFanLow:  return stdAc.fanspeed_t.kMin
    default:             return stdAc.fanspeed_t.kAuto
  }
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRTrotecESP.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.TROTEC
  result.power = this->getPower()
  result.mode = this->toCommonMode(this->getMode())
  result.celsius = True
  result.degrees = this->getTemp()
  result.fanspeed = this->toCommonFanSpeed(this->getSpeed())
  result.sleep = this->getSleep() ? 0 : -1
  # Not supported.
  result.model = -1  # Not supported.
  result.swingv = stdAc.swingv_t.kOff
  result.swingh = stdAc.swingh_t.kOff
  result.turbo = False
  result.light = False
  result.filter = False
  result.econo = False
  result.quiet = False
  result.clean = False
  result.beep = False
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRTrotecESP.toString(void) {
  String result = ""
  result.reserve(100)  # Reserve some heap for the string to reduce fragging.
  result += addBoolToString(getPower(), kPowerStr, False)
  result += addModeToString(getMode(), kTrotecAuto, kTrotecCool, kTrotecAuto,
                            kTrotecDry, kTrotecFan)
  result += addTempToString(getTemp())
  result += addFanToString(getSpeed(), kTrotecFanHigh, kTrotecFanLow,
                           kTrotecFanHigh, kTrotecFanHigh, kTrotecFanMed)
  result += addBoolToString(getSleep(), kSleepStr)
  return result
}

#if DECODE_TROTEC
# Decode the supplied Trotec message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kTrotecBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Probably works. Untested on real devices.
#
# Ref:
bool IRrecv.decodeTrotec(decode_results *results, nbits,
                          bool strict) {
  if (results->rawlen < 2 * nbits + kHeader + 2 * kFooter - 1)
    return False  # Can't possibly be a valid Samsung A/C message.
  if (strict and nbits != kTrotecBits) return False

  offset = kStartOffset
  used
  # Header + Data + Footer #1
  used = matchGeneric(results->rawbuf + offset, results->state,
                      results->rawlen - offset, nbits,
                      kTrotecHdrMark, kTrotecHdrSpace,
                      kTrotecBitMark, kTrotecOneSpace,
                      kTrotecBitMark, kTrotecZeroSpace,
                      kTrotecBitMark, kTrotecGap, True,
                      _tolerance, 0, False)
  if (used == 0) return False
  offset += used

  # Footer #2
  if (!matchMark(results->rawbuf[offset++], kTrotecBitMark)) return False
  if (offset <= results->rawlen and
      !matchAtLeast(results->rawbuf[offset++], kTrotecGapEnd)) return False
  # Compliance
  # Verify we got a valid checksum.
  if (strict and !IRTrotecESP.validChecksum(results->state)) return False
  # Success
  results->decode_type = TROTEC
  results->bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result->state, we don't record value, address, or command as it
  # is a union data type.
  return True
}
#endif  # DECODE_TROTEC
