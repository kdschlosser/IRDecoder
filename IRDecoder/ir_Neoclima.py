# -*- coding: utf-8 -*-
# Neoclima A/C
#
# Copyright 2019 David Conran

# Analysis by crankyoldgit & AndreyShpilevoy

from .IRrecv import *
from .IRutils import *
from .IRsend import *
from .IRtext import *
from .protocol_base import ACProtocolBase

# Supports:
#   Brand: Neoclima,  Model: NS-09AHTI A/C
#   Brand: Neoclima,  Model: ZH/TY-01 remote

# Ref:
#  https:#github.com/crankyoldgit/IRremoteESP8266/issues/764
#  https:#drive.google.com/file/d/1kjYk4zS9NQcMQhFkak-L4mp4UuaAIesW/view


class SetBit(SetParam):

    @classmethod
    def set(cls, remote_state, bit_state):
        if cls.num_bits is None:
            remote_state[cls.byte_num] = irutils.setBit(
                remote_state[cls.byte_num],
                cls.bit_num,
                bit_state
            )
        else:
            remote_state[cls.byte_num] = irutils.setBits(
                remote_state[cls.byte_num],
                cls.bit_num,
                cls.num_bits,
                bit_state
            )

        if hasattr(cls, 'button'):
            Button.set(remote_state, getattr(cls, 'button'))


# Constants
# state[1]
class AntiFreeze(AntiFreezeBase, SetBit):
    byte_num = 1
    bit_num = 1
    button = 0x1D


class Filter(FilterBase, SetBit):
    byte_num = 1
    bit_num = 2
    button = 0x14


# state[3]
class Light(LightBase, SetBit):
    byte_num = 3
    bit_num = 0
    button = 0x0B


class Hold(HoldBase, SetBit):
    byte_num = 3
    bit_num = 2
    button = 0x08


class Turbo(TurboBase, SetBit):
    byte_num = 3
    bit_num = 1
    button = 0x0A


class Eye(SetBit):
    byte_num = 3
    bit_num = 6
    on = 0b1
    off = 0b0
    button = 0x0E


# state[5]
class Vent(VentBase, SetBit):
    byte_num = 5
    bit_num = 7
    button = 0x15


class Button(SetBit):
    byte_num = 5
    bit_num = 0
    num_bits = 5
    temp_up = 0x02
    temp_down = 0x03


# state[7]
class Sleep(SleepBase, SetBit):
    byte_num = 7
    bit_num = 0
    button = 0x09


class Power(PowerBase, SetBit):
    byte_num = 7
    bit_num = 1
    button = 0x00


class SwingVert(SwingVertBase, SetBit):
    byte_num = 7
    bit_num = 1
    num_bits = 2
    auto = 0b01
    off = 0b10
    button = 0x04


class SwingHorz(SwingHorzBase, SetBit):
    byte_num = 7
    bit_num = 4
    auto = 0b1
    off = 0b0
    button = 0x07


class FanSpeed(FanSpeedBase, SetBit):
    byte_num = 7
    bit_num = 5
    num_bits = 2
    auto = 0b00
    high = 0b01
    medium = 0b10
    low = 0b11
    min = low
    max = high
    button = 0x05


# state[8]
class Follow(SetBit):
    byte_num = 8
    follow = 0x5D  # Also 0x5F
    button = 0x13


# state[9]
class Temperature(TemperatureBase, SetBit):
    byte_num = 9
    bit_num = 0
    num_bits = 5
    min = 16  # 16C
    max = 32  # 32C


class Mode(ModeBase, SetBit):
    byte_num = 9
    bit_num = 6
    auto = 0b000
    cool = 0b001
    dry = 0b010
    fan = 0b011
    heat = 0b100
    button = 0x01


# Constants

kNeoclimaHdrMark = 6112
kNeoclimaHdrSpace = 7391
kNeoclimaBitMark = 537
kNeoclimaOneSpace = 1651
kNeoclimaZeroSpace = 571
kNeoclimaMinGap = kDefaultMessageGap


# Send a Neoclima message.
#
# Args:
#   data: message to be sent.
#   nbytes: Nr. of bytes of the message to be sent.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: Beta / Known to be working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/764
def sendNeoclima(self, data, nbytes, repeat):
    # Set IR carrier frequency
    self.enable_ir_out(38)

    for ii in range(repeat):
        self.send_generic(
            kNeoclimaHdrMark, kNeoclimaHdrSpace,
            kNeoclimaBitMark, kNeoclimaOneSpace,
            kNeoclimaBitMark, kNeoclimaZeroSpace,
            kNeoclimaBitMark, kNeoclimaHdrSpace,
            data, nbytes, 38000, False, 0, 50
        )
    # Extra footer.
    self.mark(kNeoclimaBitMark)
    self.space(kNeoclimaMinGap)


IRsend.sendNeoclima = sendNeoclima


class IRNeoclimaAc(ACProtocolBase):
    _anti_freeze = AntiFreeze
    _filter = Filter
    _light = Light
    _hold = Hold
    _turbo = Turbo
    _eye = Eye
    _vent = Vent
    _button = Button
    _sleep = Sleep
    _power = Power
    _swing_vert = SwingVert
    _swing_horz = SwingHorz
    _fan_speed = FanSpeed
    _follow = Follow
    _temperature = Temperature
    _mode = Mode
    _packet_len = kNeoclimaStateLength
    _reset = [
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x6A, 0x00, 0x2A, 0xA5
    ]
    _reset += [0x00] * (_packet_len - len(_reset))
    _protocol = decode_type_t.NEOCLIMA

    def send(self, repeat=kNeoclimaMinRepeat):
        self._irsend.sendNeoclima(self.get_raw(), self._packet_len, repeat)

    @property
    def button(self):
        return Button.get(self.remote_state)

    # Return the set temp. in deg C
    @property
    def temperature(self):
        return Temperature.get(self.remote_state) + Temperature.min

    # Set the temp. in deg C
    @temperature.setter
    def temperature(self, temp):
        old_temp = self.temperature
        new_temp = max(Temperature.min, temp)
        new_temp = min(Temperature.max, new_temp)

        if old_temp > new_temp:
            Button.set(self.remote_state, Button.temp_down)
        elif new_temp > old_temp:
            Button.set(self.remote_state, Button.temp_up)

        Temperature.set(self.remote_state, new_temp - Temperature.min)

    @property
    def eye(self):
        return Eye.get(self.remote_state)

    @eye.setter
    def eye(self, state):
        Eye.set(self.remote_state, state)

    @property
    def follow(self):
        state = Follow.get(self.remote_state)
        return state & Follow.follow == Follow.follow

    @follow.setter
    def follow(self, value):
        # TODO
        # Work out why "on" is either 0x5D or 0x5F
        pass

    # Convert the internal state into a human readable string.
    def to_string(self):
        result = ACProtocolBase.to_string(self)
        result += irutils.addBoolToString(self.eye, kEyeStr)
        result += irutils.addBoolToString(self.follow, kFollowStr)
        result += irutils.addIntToString(self.button, kButtonStr)
        result += kSpaceLBraceStr
        button = self.button

        if button == self._power.button:
            result += kPowerStr
        elif button == self._mode.button:
            result += kModeStr
        elif button == self._button.temp_up:
            result += kTempUpStr
        elif button == self._button.temp_down:
            result += kTempDownStr
        elif button == self._swing_vert.button:
            result += kSwingStr
        elif button == self._fan_speed.button:
            result += kFanStr
        elif button == self._swing_horz.button:
            result += kAirFlowStr
        elif button == self._hold.button:
            result += kHoldStr
        elif button == self._sleep.button:
            result += kSleepStr
        elif button == self._light.button:
            result += kLightStr
        elif button == self._eye.button:
            result += kEyeStr
        elif button == self._follow.button:
            result += kFollowStr
        elif button == self._filter.button:
            result += kIonStr
        elif button == self._vent.button:
            result += kFreshStr
        elif button == self._anti_freeze.button:
            result += k8CHeatStr
        elif button == self._turbo.button:
            result += kTurboStr
        else:
            result += kUnknownStr

        result += ')'
        return result


# Decode the supplied Neoclima message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of data bits to expect. Typically kNeoclimaBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Known working
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/764
def decodeNeoclima(self, results, nbits, strict):
    # Compliance
    if strict and nbits != kNeoclimaBits:
        return False  # Incorrect nr. of bits per spec.

    offset = kStartOffset
    # Match Main Header + Data + Footer
    used = self.match_generic(
        results.rawbuf + offset, results.state,
        results.rawlen - offset, nbits,
        kNeoclimaHdrMark, kNeoclimaHdrSpace,
        kNeoclimaBitMark, kNeoclimaOneSpace,
        kNeoclimaBitMark, kNeoclimaZeroSpace,
        kNeoclimaBitMark, kNeoclimaHdrSpace,
        False, self._tolerance, 0, False
    )
    if not used:
        return False

    offset += used
    # Extra footer.

    unused = []
    if not self.match_generic(
        results.rawbuf + offset, unused,
        results.rawlen - offset,
        0, 0, 0, 0, 0, 0, 0,
        kNeoclimaBitMark, kNeoclimaHdrSpace,
        True
    ):
        return False

    # Compliance
    if strict and not IRNeoclimaAc.valid_checksum(results.state, nbits / 8):
        return False

    # Success
    results.decode_type = decode_type_t.NEOCLIMA
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True


IRrecv.decodeNeoclima = decodeNeoclima