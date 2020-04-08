# -*- coding: utf-8 -*-

# /*
# Node MCU/ESP8266 Sketch to emulate Argo Ulisse 13 DCI remote
# Controls Argo Ulisse 13 DCI A/C
# Copyright 2017 Schmolders
# Copyright 2019 crankyoldgit
# */

# Supports:
#   Brand: Argo,  Model: Ulisse 13 DCI Mobile Split A/C

from .IRtext import *
from . IRutils import *
from . IRsend import *
from .IRremoteESP8266 import *
from .protocol_base import ACProtocolBase

#  ARGO Ulisse DCI

# /*
# 	Protocol Description:
#   All in LSB first as it is sent. argo message array will be stored MSB first!
#   do LSB-MSB conversion in sendData
#   Byte 0: const 0	0	1	1	0	1	0	1
#   Byte 1: const 1	0	1	0	1	1	1	1
#   Byte 2: 0 0 0, 3bit Cool/Heat Mode, 2bit start SetTemp LSB first
#   Byte 3: 3bit End SetTemp, 2bit Fan Mode, 3bit RoomTemp LSB first
#   Byte 4: 2bit RoomTemp, 3bit Flap Mode, 3bit OnTimer
#   Byte 5: 8bit OnTimer
#   Byte 6: 8Bit OffTimer
#   Byte 7: 3bit OffTimer, 5bit Time
#   Byte 8: 6bit Time, 1bit Timer On/Off, 1bit Timer Program
#   Byte 9: 1bit Timer Program, 1bit Timer 1h, 1 bit Night Mode, 1bit Max Mode,
#           1bit Filter, 1bit on/off, 1bit const 0, 1bit iFeel
#   Byte 10: 2bit const 0 1, 6bit Checksum
#   Byte 11: 2bit Checksum
# */


# Constants
# using SPACE modulation. MARK is always const 400u
kArgoHdrMark = 6400
kArgoHdrSpace = 3300
kArgoBitMark = 400
kArgoOneSpace = 2200
kArgoZeroSpace = 900
kArgoGap = kDefaultMessageGap  # Made up value. Complete guess.

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits


# Constants. Store MSB left.

class Temperature(TemperatureBase):
    low_byte_num = 2
    low_bit_num = 5
    low_num_bits = 2

    high_byte_num = 3
    high_bit_num = 0
    high_num_bits = 3

    min = 10  # Celsius delta +4
    max = 32  # Celsius
    delta = 4

    @classmethod
    def set(cls, remote_state, bit_state):
        bit_state -= cls.delta
        # mask out bits
        # argo[13] & 0x00000100  # mask out ON/OFF Bit
        irutils.setBits(
            remote_state[cls.low_byte_num],
            cls.low_bit_num,
            cls.low_num_bits,
            bit_state
        )
        irutils.setBits(
            remote_state[cls.high_byte_num],
            cls.high_bit_num,
            cls.high_num_bits,
            bit_state >> cls.low_num_bits
        )

    @classmethod
    def get(cls, remote_state):
        return (
            GETBITS8(
                remote_state[cls.high_byte_num],
                cls.high_bit_num,
                cls.high_num_bits
            ) << cls.low_num_bits |
            GETBITS8(
                remote_state[cls.low_byte_num],
                cls.low_bit_num,
                cls.low_num_bits
            )
        ) + cls.delta


# byte[2]
class Mode(ModeBase):
    byte_num = 2
    bit_num = 3
    num_bits = 3
    cool = 0b000
    heat = 0b100
    dry = 0b001
    auto = 0b010
    off = 0b011
    heat_auto = 0b101
    heat_blink = 0b110


# byte[3]
class FanSpeed(FanSpeedBase):
    byte_num = 3
    bit_num = 3
    num_bits = 2
    low = 0b01
    medium = 0b10
    high = 0b11
    auto = 0b00


class RoomTemperature(Temperature):
    low_byte_num = 3
    low_bit_num = 5
    low_num_bits = 3

    high_byte_num = 4
    high_bit_num = 0
    high_num_bits = 2

    max = (
        ((1 << (high_num_bits + low_num_bits)) - 1) +
        Temperature.delta  # 35C
    )
    min = Temperature.delta  # Celsius delta +4


# byte[9]
class Sleep(SleepBase):
    byte_num = 9
    bit_num = 2

    on = 0b1
    off = 0b0


class Turbo(TurboBase):
    byte_num = 9
    bit_num = 3
    on = 0b1
    off = 0b0


class Power(PowerBase):
    byte_num = 9
    bit_num = 5
    on = 0b1
    off = 0b0


class Feel(PowerBase):
    byte_num = 9
    bit_num = 7
    on = 0b1
    off = 0b0


class SwingVert(SwingVertBase):
    # TODO:
    # possible bit numbers are 6, 4, 1, 0

    byte_num = 9
    highest = 0b111
    high = 0b110
    middle_high = 0b101
    middle_low = 0b100
    low = 0b011
    lowest = 0b010
    off = 0b001
    auto = 0b000


class IRArgoAC(ACProtocolBase):
    _power = Power
    _fan_speed = FanSpeed
    _mode = Mode
    _sleep = Sleep
    _turbo = Turbo
    _feel = Feel
    _swing_vert = SwingVert
    _temperatte = Temperature
    _room_temperature = RoomTemperature
    _clock = None

    _packet_len = kArgoStateLength
    _reset = [0x0] * kArgoStateLength

    # Argo Message. Store MSB left.
    # Default message:
    _reset[0] = 0b10101100  # LSB first (as sent) 0b00110101 #const preamble
    _reset[1] = 0b11110101  # LSB first: 0b10101111 #const preamble
    # Keep payload 2-9 at zero
    _reset[10] = 0b00000010  # Const 01, checksum 6bit
    _reset[11] = 0b00000000  # Checksum 2bit

    _min_repeat = kArgoDefaultRepeat
    _protocol = decode_type_t.ARGO

    def send(self, repeat=_min_repeat):
        self._irsend.sendArgo(self.get_raw(), kArgoStateLength, repeat)

    @classmethod
    def calc_checksum(cls, state, length=None):
        if length is None:
            length = cls._packet_len

        # Corresponds to byte 11 being constant 0b01
        # Only add up bytes to 9. byte 10 is 0b01 constant anyway.
        # Assume that argo array is MSB first (left)
        return sumBytes(state, length - 2, 2)

    @classmethod
    def valid_checksum(cls, state, length=None):
        if length is None:
            length = cls._packet_len

        return ((state[length - 2] >> 2) + (state[length - 1] << 6)) == cls.calc_checksum(state, length)

    def checksum(self, length=None):
        if length is None:
            length = self._packet_len

        sm = self.calc_checksum(self.remote_state, length)
        # Append sum to end of array
        # Set const part of checksum bit 10
        self.remote_state[10] = 0b00000010
        self.remote_state[10] += sm << 2  # Shift up 2 bits and append to byte 10
        self.remote_state[11] = sm >> 6   # Shift down 6 bits and add in two LSBs of bit 11

    def state_reset(self):
        ACProtocolBase.state_reset(self)

        self.power = False
        self.temperature = 20
        self.room_temperature = 25
        self.mode = stdAc.opmode_t.kAuto
        self.fan_speed = stdAc.fanspeed_t.kAuto

    @property
    def room_temperature(self):
        return self._room_temperature.get(self.remote_state)

    @room_temperature.setter
    def room_temperature(self, temp):
        new_temp = max(self._room_temperature.min, temp)
        new_temp = min(self._room_temperature.max, new_temp)

        self._temperature.set(self.remote_state, new_temp)

    @property
    def feel(self):
        res = self._feel.get(self.remote_state)
        return res == self._feel.on

    @feel.setter
    def feel(self, state):
        if state:
            state = self._feel.on
        else:
            state = self._feel.off

        self._feel.set(self.remote_state, state)

    @property
    def swing_vert(self):
        # TODO
        return None

    @swing_vert.setter
    def swing_vert(self, state):
        # TODO
        pass

    @property
    def clock(self):
        # TODO
        return None

    @clock.setter
    def clock(self, value):
        # TODO
        pass

    # Convert the internal state into a human readable string.
    def to_string(self):
        result = ACProtocolBase.to_string(self)
        result += kCommaSpaceStr
        result += kRoomStr
        result += ' '
        result += addTempToString(self.room_temperature, True, False)
        result += addBoolToString(self.feel, kIFeelStr)
        return result


# Send an Argo A/C message.
#
# Args:
#   data: An array of kArgoStateLength bytes containing the IR command.
#
# Status: ALPHA / Untested.

def sendArgo(self, data, nbytes, repeat):
    # Check if we have enough bytes to send a proper message.
    if nbytes < kArgoStateLength:
        return
    # TODO(kaschmo): validate

    self.send_generic(
        kArgoHdrMark,
        kArgoHdrSpace,
        kArgoBitMark,
        kArgoOneSpace,
        kArgoBitMark,
        kArgoZeroSpace,
        0,
        0,  # No Footer.
        data,
        nbytes,
        38,
        False,
        repeat,
        kDutyDefault
    )


IRsend.sendArgo = sendArgo

# Decode the supplied Argo message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kArgoBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Probably doesn't work.
#
# Note:
#   This decoder is based soley off sendArgo(). We have no actual captures
#   to test this against. If you have one of these units, please let us know.
def decodeArgo(self, results, nbits, strict):
    if strict and nbits != kArgoBits:
        return False

    offset = kStartOffset

    # Match Header + Data
    if not self.match_generic(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        kArgoHdrMark,
        kArgoHdrSpace,
        kArgoBitMark,
        kArgoOneSpace,
        kArgoBitMark,
        kArgoZeroSpace,
        0,
        0,  # Footer (None, allegedly. This seems very wrong.)
        True,
        self._tolerance,
        0,
        False
    ):
        return False

    # Compliance
    # Verify we got a valid checksum.
    if strict and not IRArgoAC.valid_checksum(results.state):
        return False

    # Success
    results.decode_type = decode_type_t.ARGO
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True


IRrecv.decodeArgo = decodeArgo
