# -*- coding: utf-8 -*-

# Copyright bakrus
# Copyright 2017,2019 David Conran

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRutils import *
from .IRsend import *
from .IRtext import *
from .protocol_base import ACProtocolBase

# Coolix A/C / heatpump added by (send) bakrus & (decode) crankyoldgit
#
# Supports:
#   Brand: Beko, Model: RG57K7(B)/BGEF Remote
#   Brand: Beko, Model: BINR 070/071 split-type A/C
#   Brand: Midea, Model: RG52D/BGE Remote
#   Brand: Midea, Model: MS12FU-10HRDN1-QRD0GW(B) A/C
#   Brand: Midea, Model: MSABAU-07HRFN1-QRD0GW A/C (circa 2016)
#   Brand: Tokio, Model: AATOEMF17-12CHR1SW split-type RG51|50/BGE Remote
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/484

# Constants
# Pulse parms are *50-100 for the Mark and *50+100 for the space
# First MARK is the one after the long gap
# pulse parameters in usec
kCoolixTick = 560  # Approximately 21 cycles at 38kHz
kCoolixBitMarkTicks = 1
kCoolixBitMark = kCoolixBitMarkTicks * kCoolixTick
kCoolixOneSpaceTicks = 3
kCoolixOneSpace = kCoolixOneSpaceTicks * kCoolixTick
kCoolixZeroSpaceTicks = 1
kCoolixZeroSpace = kCoolixZeroSpaceTicks * kCoolixTick
kCoolixHdrMarkTicks = 8
kCoolixHdrMark = kCoolixHdrMarkTicks * kCoolixTick
kCoolixHdrSpaceTicks = 8
kCoolixHdrSpace = kCoolixHdrSpaceTicks * kCoolixTick
kCoolixMinGapTicks = kCoolixHdrMarkTicks + kCoolixZeroSpaceTicks
kCoolixMinGap = kCoolixMinGapTicks * kCoolixTick

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits

# Supports:
#   Brand: Beko, Model: RG57K7(B)/BGEF Remote
#   Brand: Beko, Model: BINR 070/071 split-type A/C
#   Brand: Midea, Model: RG52D/BGE Remote
#   Brand: Midea, Model: MS12FU-10HRDN1-QRD0GW(B) A/C
#   Brand: Midea, Model: MSABAU-07HRFN1-QRD0GW A/C (circa 2016)
#   Brand: Tokio, Model: AATOEMF17-12CHR1SW split-type RG51|50/BGE Remote
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/484
# Kudos:
#   Hamper: For the breakdown and mapping of the bit values.


class Param(SetParam):
    _get = SetParam.get
    _set = SetParam.set

    @classmethod
    def get(cls, remote_state):
        if remote_state in (
            SwingHorz.cmd,
            SwingVert.cmd,
            Swing.cmd,
            Sleep.cmd,
            Turbo.cmd,
            Light.cmd,
            Clean.cmd,
            Power.cmd
        ):
            for ii in range(3):
                remote_state[ii] = Command.saved_state[ii]

        return cls._get(remote_state)

    @classmethod
    def set(cls, remote_state, bit_state):
        if remote_state in (
            SwingHorz.cmd,
            SwingVert.cmd,
            Swing.cmd,
            Sleep.cmd,
            Turbo.cmd,
            Light.cmd,
            Clean.cmd,
            Power.cmd
        ):
            for ii in range(3):
                remote_state[ii] = Command.saved_state[ii]

        cls._set(remote_state, bit_state)


# Constants
# Modes
# const uint32_t kCoolixModeMask = 0b00000000 00000000 00001100  # 0xC
class Mode(ModeBase, Param):
    byte_num = 2
    bit_num = 2
    num_bits = 3
    cool = 0b000
    dry = 0b001
    auto = 0b010
    heat = 0b011
    fan = 0b100


# const uint32_t kCoolixZoneFollowMask = 0b00001000 00000000 00000000  0x80000
class Follow(FollowBase, Param):
    byte_num = 0
    bit_num = 3


# Fan Control
# const uint32_t kCoolixFanMask = 0b00000000 11100000 00000000  # 0x00E000
class FanSpeed(FanSpeedBase, Param):
    byte_num = 1
    bit_num = 5
    num_bits = 3
    min = 0b100
    medium = 0b010
    max = 0b001
    auto = 0b101
    auto_0 = 0b000
    follow = 0b110
    fixed = 0b111


# Temperature
# const uint32_t kCoolixTempMask = 0b11110000
class Temperature(TemperatureBase, Param):
    byte_num = 2
    bit_num = 4
    num_bits = 4
    min = 17
    max = 30

    @classmethod
    def get_temp(cls, temp):
        if temp < cls.min:
            temp = cls.min
        elif temp > cls.max:
            temp = cls.max

        temp -= cls.min
        return cls.mapping[temp]

    fan_temp = 0b1110  # Part of Fan Mode.

    mapping = [
        0b0000,  # 17C
        0b0001,  # 18C
        0b0011,  # 19C
        0b0010,  # 20C
        0b0110,  # 21C
        0b0111,  # 22C
        0b0101,  # 23C
        0b0100,  # 24C
        0b1100,  # 25C
        0b1101,  # 26C
        0b1001,  # 27C
        0b1000,  # 28C
        0b1010,  # 29C
        0b1011  # 30C
    ]


# kCoolixSensorTempMask = 0b00000000 00001111 00000000  # 0xF00
class SensorTemperature(Temperature, Param):
    byte_num = 2
    bit_num = 0
    num_bits = 4
    min = 16
    max = 30
    ignore = 0b1111

    @classmethod
    def get_temp(cls, temp):
        if temp < cls.min:
            temp = cls.min
        elif temp > cls.max:
            temp = cls.max

        temp -= cls.min
        return cls.mapping[temp]


class Command(SetParam):
    _state = False
    on = 0b1
    off = 0b0
    saved_state = [0xB2, 0x1F, 0xC8]
    cmd = []

    @classmethod
    def get(cls, _):
        return cls._state

    @classmethod
    def set(cls, remote_state, value):
        if value == cls._state:
            return

        cls._state = value

        if remote_state not in (
            SwingHorz.cmd,
            SwingVert.cmd,
            Swing.cmd,
            Sleep.cmd,
            Turbo.cmd,
            Light.cmd,
            Clean.cmd,
            Power.cmd
        ):

            Command.saved_state = remote_state[:]

        for ii in range(3):
            remote_state[ii] = cls.cmd[ii]


class SwingHorz(SwingHorzBase, Command):
    _state = False
    cmd = [0xB2, 0xF5, 0xA2]


class SwingVert(SwingVertBase, Command):
    _state = False
    cmd = [0xB2, 0x0F, 0xE0]


class Swing(SetParam, Command):
    _state = False
    cmd = [0xB2, 0x6B, 0xE0]


class Sleep(SleepBase, Command):
    _state = False
    cmd = [0xB2, 0xE0, 0x03]


class Turbo(TurboBase, Command):
    _state = False
    cmd = [0xB5, 0xF5, 0xA2]


class Power(PowerBase, Command):
    _state = False
    cmd = [0xB2, 0x7B, 0xE0]


class Light(LightBase, Command):
    _state = False
    cmd = [0xB5, 0xF5, 0xA5]


class Clean(CleanBase):
    _state = False
    cmd = [0xB5, 0xF5, 0xAA]


kCoolixCmdFan = [0xB2, 0xBF, 0xE4]


# IRCoolixAC class
# Supports:
#   RG57K7(B)/BGEF remote control for Beko BINR 070/071 split-type aircon.
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/484
class IRCoolixAC(ACProtocolBase):
    _temperature = Temperature
    _sensor_temperature = SensorTemperature
    _fan_speed = FanSpeed
    _mode = Mode
    _follow = Follow
    _clean = Clean
    _light = Light
    _power = Power
    _swing_vert = SwingVert
    _swing_horz = SwingHorz
    _turbo = Turbo
    _sleep = Sleep
    _swing = Swing
    _reset = [0xB2, 0x1F, 0xC8]
    _packet_len = 3

    def state_reset(self):
        ACProtocolBase.state_reset(self)
        self.sensor_temperature = 0

    def send(self, repeat=kCoolixDefaultRepeat):
        data = (
            self.remote_state[0] << 16 |
            self.remote_state[1] << 8 |
            self.remote_state[2]
        )

        self._irsend.sendCOOLIX(data, kCoolixBits, repeat)

    def set_raw(self, new_code, length=_packet_len):
        # it isn`t special so might affect Temp|mode|Fan
        if new_code == kCoolixCmdFan:
            self.mode = stdAc.opmode_t.kFan
            return
        # must be a command changing Temp|Mode|Fan
        # it is safe to just copy to remote var
        self.remote_state = new_code[:]

    # Return True if the current state is a special state.
    @property
    def swing(self):
        res = self._swing.get(self.remote_state)
        if res == self._swing.on:
            return True
        if res == self._swing.off:
            return False

    @swing.setter
    def swing(self, value):
        if value:
            value = self._swing.on
        else:
            value = self._swing.off

        self._swing.set(self.remote_state, value)

    @property
    def temperature(self):
        temp = ACProtocolBase.temperature.fget(self)
        for ii, item in enumerate(self._temperature.mapping):
            if item == temp:
                break
        else:
            return

        return ii + self._temperature.min

    @temperature.setter
    def temperature(self, temp):
        temp = self._temperature.get_temp(temp)
        ACProtocolBase.temperature.fset(self, temp)

    @property
    def sensor_temperature(self):
        temp = self._sensor_temperature.get(self.remote_state)

        for ii, item in enumerate(self._sensor_temperature.mapping):
            if item == temp:
                break
        else:
            return 0

        return ii + self._sensor_temperature.min

    @sensor_temperature.setter
    def sensor_temperature(self, temp):
        if temp == 0:
            temp = self._sensor_temperature.ignore
            self.follow = False
        else:
            temp = self._sensor_temperature.get_temp(temp)
            self.follow = True  # Setting a Sensor temp means you want to Zone Follow.

        self._sensor_temperature.set(self.remote_state, temp)

    @property
    def mode(self):
        mode = ACProtocolBase.mode.fget(self)
        if mode == stdAc.opmode_t.kDry:
            if self._temperature.get(self.remote_state) == self._temperature.fan_temp:
                return stdAc.opmode_t.kFan

        return mode

    @mode.setter
    def mode(self, mode):
        actualmode = mode
        if mode in (stdAc.opmode_t.kAuto, stdAc.opmode_t.kDry):
            self._fan_speed.set(self.remote_state, self._fan_speed.auto_0)
        elif mode in (stdAc.opmode_t.kCool, stdAc.opmode_t.kHeat, stdAc.opmode_t.kFan):
            self._fan_speed.set(self.remote_state, self._fan_speed.auto)
        else:
            self.mode = stdAc.opmode_t.kAuto
            self._fan_speed.set(self.remote_state, self._fan_speed.auto_0)
            return

        self.temperature = self.temperature

        # Fan mode is a special case of Dry.
        if mode == stdAc.opmode_t.kFan:
            actualmode = stdAc.opmode_t.kDry
            self._temperature.set(self.remote_state, self._temperature.fan_temp)

        ACProtocolBase.mode.fset(self, actualmode)

    @property
    def fan_speed(self):
        return self.to_common_fan_speed(self._fan_speed.get(self.remote_state))

    @fan_speed.setter
    def fan_speed(self, speed):
        if speed == stdAc.fanspeed_t.kAuto:  # Dry & Auto mode can't have this speed.
            mode = self.mode

            if mode in (stdAc.opmode_t.kAuto, stdAc.opmode_t.kDry):
                newspeed = self._fan_speed.auto_0
            else:
                newspeed = self.from_common_fan_speed(speed)

        elif speed == stdAc.fanspeed_t.kMin:  # Only Dry & Auto mode can have this speed.
            mode = self.mode

            if mode in (stdAc.opmode_t.kAuto, stdAc.opmode_t.kDry):
                newspeed = self.from_common_fan_speed(speed)
            else:
                newspeed = self.from_common_fan_speed(stdAc.fanspeed_t.kAuto)
        else:
            newspeed = self.from_common_fan_speed(speed)

        self._fan_speed.set(self.remote_state, newspeed)


# Send a Coolix message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kCoolixBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: BETA / Probably works.
#
# Ref:
#   https:#github.com/z3t0/Arduino-IRremote/blob/master/ir_COOLIX.cpp
# TODO(anyone): Verify repeat functionality against a real unit.
def sendCOOLIX(self, data, nbits, repeat):
    if nbits % 8 != 0:
        return  # nbits is required to be a multiple of 8.

    # Set IR carrier frequency
    self.enable_ir_out(38)

    for r in range(repeat + 1):
        # Header
        self.mark(kCoolixHdrMark)
        self.space(kCoolixHdrSpace)

        # Data
        #   Break data into byte segments, starting at the Most Significant
        #   Byte. Each byte then being sent normal, then followed inverted.

        for ii in range(8, nbits + 1, 8):
            # Grab a bytes worth of data.
            segment = data >> (nbits - ii) & 0xFF
            # Normal
            self.send_data(
                kCoolixBitMark,
                kCoolixOneSpace,
                kCoolixBitMark,
                kCoolixZeroSpace,
                segment,
                8,
                True
            )
            # Inverted.
            self.send_data(
                kCoolixBitMark,
                kCoolixOneSpace,
                kCoolixBitMark,
                kCoolixZeroSpace,
                segment ^ 0xFF,
                8,
                True
            )

        # Footer
        self.mark(kCoolixBitMark)
        self.space(kCoolixMinGap)  # Pause before repeating

    self.space(kDefaultMessageGap)


IRsend.sendCOOLIX = sendCOOLIX


# Decode the supplied Coolix message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kCoolixBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Probably working.
def decodeCOOLIX(self, results, nbits, strict):
    # The protocol sends the data normal + inverted, alternating on
    # each byte. Hence twice the number of expected data bits.
    if results.rawlen < 2 * 2 * nbits + kHeader + kFooter - 1:
        return False  # Can't possibly be a valid COOLIX message.

    if strict and nbits != kCoolixBits:
        return False      # Not strictly a COOLIX message.

    if nbits % 8 != 0:  # nbits has to be a multiple of nr. of bits in a byte.
        return False

    data = 0
    inverted = 0
    offset = kStartOffset

    if nbits > 64:
        return False  # We can't possibly capture a Coolix packet that big.

    # Header
    if not self.match_mark(results.rawbuf[offset], kCoolixHdrMark):
        return False

    # Calculate how long the common tick time is based on the header mark.
    offset += 1
    m_tick = results.rawbuf[offset] * kRawTick / kCoolixHdrMarkTicks

    if not self.match_space(results.rawbuf[offset], kCoolixHdrSpace):
        return False

    offset += 1
    # Calculate how long the common tick time is based on the header space.
    s_tick = results.rawbuf[offset] * kRawTick / kCoolixHdrSpaceTicks

    # Data
    # Twice as many bits as there are normal plus inverted bits.
    for ii in range(nbits * 2):
        flip = (ii / 8) % 2

        offset += 1
        if not self.match_mark(results.rawbuf[offset], kCoolixBitMarkTicks * m_tick):
            return False
        if self.match_space(results.rawbuf[offset], kCoolixOneSpaceTicks * s_tick):
            if flip:
                inverted = (inverted << 1) | 1
            else:
                data = (data << 1) | 1
        elif self.match_space(results.rawbuf[offset], kCoolixZeroSpaceTicks * s_tick):
            if flip:
                inverted <<= 1
            else:
                data <<= 1
        else:
            return False

        offset += 1

    # Footer
    offset += 1
    if not self.match_mark(results.rawbuf[offset], kCoolixBitMarkTicks * m_tick):
        return False

    if (
        offset < results.rawlen and
        not self.match_at_least(results.rawbuf[offset], kCoolixMinGapTicks * s_tick)
    ):
        return False

    # Compliance
    orig = data  # Save a copy of the data.
    if strict:
        for _ in range(0, nbits, 8):
            if (data & 0xFF) != ((inverted & 0xFF) ^ 0xFF):
                return False

            data >>= 8
            inverted >>= 8

    # Success
    results.decode_type = COOLIX
    results.bits = nbits
    results.value = orig
    results.address = 0
    results.command = 0
    return True


IRrecv.decodeCOOLIX = decodeCOOLIX
