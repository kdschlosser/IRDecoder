# -*- coding: utf-8 -*-

# Copyright 2019 David Conran
# Copyright 2020 Kevin Schlosser

# Supports:
#   Brand: Amcor,  Model: ADR-853H A/C
#   Brand: Amcor,  Model: TAC-495 remote
#   Brand: Amcor,  Model: TAC-444 remote
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/834
# Kudos:
#   ldellus: For the breakdown and mapping of the bit values.

from .IRrecv import *
from .IRutils import *
from .IRsend import *
from .protocol_base import ACProtocolBase
from .IRremoteESP8266 import *


# Constants
# state[1]
class FanSpeed(FanSpeedBase):
    byte_num = 1
    bit_num = 4
    num_bits = 3
    auto = 0b100
    high = 0b011
    medium = 0b010
    low = 0b001
    min = low
    max = high


class Mode(ModeBase):
    byte_num = 1
    bit_num = 0
    num_bits = 3
    off = 0b000
    auto = 0b101
    cool = 0b001
    dry = 0b100
    fan = 0b011
    heat = 0b010


# state[2]
class Temperature(TemperatureBase):
    byte_num = 2
    bit_num = 1
    num_bits = 6
    min = 12  # 16C
    max = 32  # 32C


# state[5]
class Power(PowerBase):
    byte_num = 5
    bit_num = 4
    num_bits = 4
    on = 0b0011
    off = 0b1100


# state[6]
class Turbo(TurboBase):
    byte_num = 6
    bit_num = 0
    num_bits = 2
    on = 0b11
    off = 0b00


# "Vent" Mode
class Vent(VentBase):
    byte_num = 6
    bit_num = 6
    num_bits = 2
    on = 0b11
    off = 0b00


# state[7]
# Checksum byte.
kAmcorChecksumByte = kAmcorStateLength - 1


# Constants
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/385
kAmcorHdrMark = 8200
kAmcorHdrSpace = 4200
kAmcorOneMark = 1500
kAmcorZeroMark = 600
kAmcorOneSpace = kAmcorZeroMark
kAmcorZeroSpace = kAmcorOneMark
kAmcorFooterMark = 1900
kAmcorGap = 34300
kAmcorTolerance = 40


addBoolToString = irutils.addBoolToString
addModeToString = irutils.addModeToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBits = irutils.setBits


# Classes
class IRAmcorAc(ACProtocolBase):
    _fanspeed = FanSpeed
    _mode = Mode
    _temperature = Temperature
    _power = Power
    _turbo = Turbo
    _vent = Vent

    _reset = [0x0] * kAmcorStateLength
    _reset[0] = 0x01
    _packet_len = kAmcorStateLength

    _protocol = decode_type_t.AMCOR

    def state_reset(self):
        ACProtocolBase.state_reset(self)

        self.fan_speed = stdAc.fanspeed_t.kAuto
        self.mode = stdAc.opmode_t.kAuto
        self.temperature = 25  # 25C

    def send(self, repeat=kAmcorDefaultRepeat):
        self._irsend.sendAmcor(self.get_raw(), kAmcorStateLength, repeat)

    @classmethod
    def calc_checksum(cls, state, length=kAmcorStateLength):
        return irutils.sumNibbles(state, length - 1)

    @property
    def mode(self):
        return ACProtocolBase.mode.fget(self)

    @mode.setter
    def mode(self, mode):
        if mode in (
            stdAc.opmode_t.kFan,
            stdAc.opmode_t.kCool,
            stdAc.opmode_t.kHeat,
            stdAc.opmode_t.kDry,
            stdAc.opmode_t.kAuto
        ):
            if mode == stdAc.opmode_t.kFan:
                self.vent = True
            else:
                self.vent = False

            ACProtocolBase.mode.fset(self, mode)

    def checksum(self, length=kAmcorStateLength):
        self.remote_state[kAmcorChecksumByte] = self.calc_checksum(self.remote_state, length)


# Send a Amcor HVAC formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbytes: The byte size of the array being sent. typically kAmcorStateLength.
#   repeat: The number of times the message is to be repeated.
#
# Status: STABLE / Reported as working.
#
def sendAmcor(self, data, nbytes, repeat):
    # Check if we have enough bytes to send a proper message.
    if nbytes < kAmcorStateLength:
        return

    self.send_generic(
        kAmcorHdrMark,
        kAmcorHdrSpace,
        kAmcorOneMark,
        kAmcorOneSpace,
        kAmcorZeroMark,
        kAmcorZeroSpace,
        kAmcorFooterMark,
        kAmcorGap,
        data,
        nbytes,
        38,
        False,
        repeat,
        kDutyDefault
    )


IRsend.sendAmcor = sendAmcor


# Decode the supplied Amcor HVAC message.
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kAmcorBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, false if it can't.
#
# Status: STABLE / Reported as working.
#
def decodeAmcor(self, results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader - 1:
        return False  # Can't possibly be a valid Amcor message.

    if strict and nbits != kAmcorBits:
        return False  # We expect Amcor to be 64 bits of message.

    offset = kStartOffset

    # Header + Data Block (64 bits) + Footer
    used = self.match_generic(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        64,
        kAmcorHdrMark,
        kAmcorHdrSpace,
        kAmcorOneMark,
        kAmcorOneSpace,
        kAmcorZeroMark,
        kAmcorZeroSpace,
        kAmcorFooterMark,
        kAmcorGap,
        True,
        kAmcorTolerance,
        0,
        False
    )
    if not used:
        return False

    offset += used

    if strict and not IRAmcorAc.valid_checksum(results.state):
        return False

    # Success
    results.bits = nbits
    results.decode_type = AMCOR
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True


IRrecv.decodeAmcor = decodeAmcor
