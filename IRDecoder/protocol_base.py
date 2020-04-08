# -*- coding: utf-8 -*-
# Copyright 2020 Kevin Schlosser


from .IRutils import *
from .IRsend import IRsend


class ACProtocolBase(object):
    _anti_freeze = None
    _filter = None
    _light = None
    _hold = None
    _turbo = None
    _vent = None
    _sleep = None
    _power = None
    _swing_vert = None
    _swing_horz = None
    _fan_speed = None
    _follow = None
    _temperature = None
    _mode = None
    _packet_len = 0
    _reset = []
    _min_repeat = 0
    _protocol = None
    _clock = None
    _quiet = None
    _econo = None
    _clean = None
    _beep = None
    _model = None

    def __init__(self, pin, inverted=False, use_modulation=True):
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.remote_state = [0x00] * self._packet_len
        self.state_reset()

    def state_reset(self):
        if self._reset:
            for ii in range(self._packet_len):
                self.remote_state[ii] = self._reset[ii]

    def calibrate(self):
        return self._irsend.calibrate()

    def begin(self):
        self._irsend.begin()

    @classmethod
    def calc_checksum(cls, state, length=None):
        if length is None:
            length = cls._packet_len

        if length == 0:
            return state[0]

        return sumBytes(state, length - 1)

    @classmethod
    def valid_checksum(cls, state, length=None):
        if length is None:
            length = cls._packet_len

        if length < 2:
            return True  # No checksum to compare with. Assume okay.
        return state[length - 1] == cls.calc_checksum(state, length)

    # Update the checksum for the internal state.
    def checksum(self, length=None):
        if length is None:
            length = self._packet_len

        if length < 2:
            return

        self.remote_state[length - 1] = self.calc_checksum(self.remote_state, length)

    def send(self, repeat=None):
        raise NotImplementedError

    def get_raw(self):
        self.checksum()
        return self.remote_state

    def set_raw(self, new_code, length=None):
        if length is None:
            length = self._packet_len

        self.remote_state = new_code[:min(length, self._packet_len)]

    def on(self):
        self.power = True

    def off(self):
        self.power = False

    @property
    def power(self):
        if self._power is not None:
            res = self._power.get(self.remote_state)

            if res == self._power.on:
                return True
            if res == self._power.off:
                return False

    @power.setter
    def power(self, state):
        if self._power is not None:
            if state:
                state = self._power.on
            else:
                state = self._power.off

            self._power.set(self.remote_state, state)

    @property
    def model(self):
        if self._model is not None:
            return self._model.get(self.remote_state)

    @property
    def mode(self):
        if self._mode is not None:
            return self.to_common_mode(self._mode.get(self.remote_state))

    @mode.setter
    def mode(self, mode):
        if self._mode is not None:
            mode = self.from_common_mode(mode)

            if mode == self._mode.dry:
                # In this mode fan speed always LOW
                self.fan_speed = stdAc.fanspeed_t.kLow

            self._mode.set(self.remote_state, mode)

    @classmethod
    # Convert a standard A/C mode into its native mode.
    def from_common_mode(cls, mode):
        if mode == stdAc.opmode_t.kCool:
            return cls._mode.cool
        if mode == stdAc.opmode_t.kHeat:
            return cls._mode.heat
        if mode == stdAc.opmode_t.kDry:
            return cls._mode.dry
        if mode == stdAc.opmode_t.kFan:
            return cls._mode.fan

        return cls._mode.auto

    # Convert a native mode to it's common equivalent.
    @classmethod
    def to_common_mode(cls, mode):
        if mode == cls._mode.cool:
            return stdAc.opmode_t.kCool
        if mode == cls._mode.heat:
            return stdAc.opmode_t.kHeat
        if mode == cls._mode.dry:
            return stdAc.opmode_t.kDry
        if mode == cls._mode.fan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    # Return the set temp. in deg C
    @property
    def temperature(self):
        if self._temperature is not None:
            temp = self._temperature.get(self.remote_state)
            if self._temperature.delta is None:
                return temp

            return temp + self._temperature.delta

    # Set the temp. in deg C
    @temperature.setter
    def temperature(self, temp):
        if self._temperature is not None:
            new_temp = max(self._temperature.min, temp)
            new_temp = min(self._temperature.max, new_temp)

            if self._temperature.delta is not None:
                new_temp -= self._temperature.delta

            self._temperature.set(self.remote_state, new_temp)

    @property
    def fan_speed(self):
        if self._fan_speed is not None:
            return self.to_common_fan_speed(self._fan_speed.get(self.remote_state))

    @fan_speed.setter
    def fan_speed(self, speed):
        if self._fan_speed is not None:
            speed = self.from_common_fan_speed(speed)

            if self.mode == stdAc.opmode_t.kDry:
                # Dry mode only allows low speed.
                self._fan_speed.set(self.remote_state, self._fan_speed.low)
            else:
                self._fan_speed.set(self.remote_state, speed)

    # Convert a standard A/C Fan speed into its native fan speed.
    @classmethod
    def from_common_fan_speed(cls, speed):
        if speed == stdAc.fanspeed_t.kLow:
            return cls._fan_speed.low
        if speed == stdAc.fanspeed_t.kMedium:
            return cls._fan_speed.medium
        if speed == stdAc.fanspeed_t.kHigh:
            return cls._fan_speed.high
        if speed == stdAc.fanspeed_t.kMin:
            return cls._fan_speed.min
        if speed == stdAc.fanspeed_t.kMax:
            return cls._fan_speed.max

        return cls._fan_speed.auto

    # Convert a native fan speed to it's common equivalent.
    @classmethod
    def to_common_fan_speed(cls, speed):
        if speed == cls._fan_speed.high:
            return stdAc.fanspeed_t.kMax
        if speed == cls._fan_speed.medium:
            return stdAc.fanspeed_t.kMedium
        if speed == cls._fan_speed.low:
            return stdAc.fanspeed_t.kMin
        if speed == cls._fan_speed.min:
            return stdAc.fanspeed_t.kMin
        if speed == cls._fan_speed.max:
            return stdAc.fanspeed_t.kMax

        return stdAc.fanspeed_t.kAuto

    @property
    def sleep(self):
        if self._sleep is not None:
            res = self._sleep.get(self.remote_state)
            if res == self._sleep.on:
                return True
            if res == self._sleep.off:
                return False

    @sleep.setter
    def sleep(self, state):
        if self._sleep is not None:
            if state:
                state = self._sleep.on
            else:
                state = self._sleep.off

            self._sleep.set(self.remote_state, state)

    @property
    def swing_vert(self):
        if self._swing_vert is not None:
            return self.to_common_swing_vert(self._swing_vert.get(self.remote_state))

    @swing_vert.setter
    def swing_vert(self, state):
        if self._swing_vert is not None:
            state = self.from_common_swing_vert(state)
            self._swing_vert.set(self.remote_state, state)

    @classmethod
    def from_common_swing_vert(cls, state):
        if state == stdAc.swingv_t.kOff:
            return cls._swing_vert.off
        if state == stdAc.swingv_t.kAuto:
            return cls._swing_vert.auto
        if state == stdAc.swingv_t.kHighest:
            return cls._swing_vert.highest
        if state == stdAc.swingv_t.kHigh:
            return cls._swing_vert.high
        if state == stdAc.swingv_t.kMiddleHigh:
            return cls._swing_vert.middle_high
        if state == stdAc.swingv_t.kMiddle:
            return cls._swing_vert.middle
        if state == stdAc.swingv_t.kMiddleLow:
            return cls._swing_vert.middle_low
        if state == stdAc.swingv_t.kLow:
            return cls._swing_vert.low
        if state == stdAc.swingv_t.kLowest:
            return cls._swing_vert.lowest

    @classmethod
    def to_common_swing_vert(cls, state):
        if state == cls._swing_vert.off:
            return stdAc.swingv_t.kOff
        if state == cls._swing_vert.auto:
            return stdAc.swingv_t.kAuto
        if state == cls._swing_vert.highest:
            return stdAc.swingv_t.kHighest
        if state == cls._swing_vert.high:
            return stdAc.swingv_t.kHigh
        if state == cls._swing_vert.middle_high:
            return stdAc.swingv_t.kMiddleHigh
        if state == cls._swing_vert.middle:
            return stdAc.swingv_t.kMiddle
        if state == cls._swing_vert.middle_low:
            return stdAc.swingv_t.kMiddleLow
        if state == cls._swing_vert.low:
            return stdAc.swingv_t.kLow
        if state == cls._swing_vert.lowest:
            return stdAc.swingv_t.kLowest

    @property
    def swing_horz(self):
        if self._swing_horz is not None:
            return self.to_common_swing_horz(self._swing_horz.get(self.remote_state))

    @swing_horz.setter
    def swing_horz(self, state):
        if self._swing_horz is not None:
            state = self.from_common_swing_horz(state)
            self._swing_horz.set(self.remote_state, state)

    @classmethod
    def from_common_swing_horz(cls, state):
        if state == stdAc.swingh_t.kOff:
            return cls._swing_horz.off
        if state == stdAc.swingh_t.kAuto:
            return cls._swing_horz.auto
        if state == stdAc.swingh_t.kLeftMax:
            return cls._swing_horz.left_max
        if state == stdAc.swingh_t.kLeft:
            return cls._swing_horz.left
        if state == stdAc.swingh_t.kMiddle:
            return cls._swing_horz.middle
        if state == stdAc.swingh_t.kRight:
            return cls._swing_horz.right
        if state == stdAc.swingh_t.kRightMax:
            return cls._swing_horz.right_max
        if state == stdAc.swingh_t.kWide:
            return cls._swing_horz.wide

    @classmethod
    def to_common_swing_horz(cls, state):
        if state == cls._swing_horz.off:
            return stdAc.swingh_t.kOff
        if state == cls._swing_horz.auto:
            return stdAc.swingh_t.kAuto
        if state == cls._swing_horz.left_max:
            return stdAc.swingh_t.kLeftMax
        if state == cls._swing_horz.left:
            return stdAc.swingh_t.kLeft
        if state == cls._swing_horz.middle:
            return stdAc.swingh_t.kMiddle
        if state == cls._swing_horz.right:
            return stdAc.swingh_t.kRight
        if state == cls._swing_horz.right_max:
            return stdAc.swingh_t.kRightMax
        if state == cls._swing_horz.wide:
            return stdAc.swingh_t.kWide

    @property
    def turbo(self):
        if self._turbo is not None:
            res = self._turbo.get(self.remote_state)

            if res == self._turbo.on:
                return True
            if res == self._turbo.off:
                return False

    @turbo.setter
    def turbo(self, state):
        if self._turbo is not None:
            if state:
                state = self._turbo.on
            else:
                state = self._turbo.off

            self._turbo.set(self.remote_state, state)

    @property
    def vent(self):
        if self._vent is not None:
            res = self._vent.get(self.remote_state)
            if res == self._vent.on:
                return True

            if res == self._vent.off:
                return False

    @vent.setter
    def vent(self, state):
        if self._vent is not None:
            if state:
                state = self._vent.on
            else:
                state = self._vent.off

            self._vent.set(self.remote_state, state)

    @property
    def hold(self):
        if self._hold is not None:
            res = self._hold.get(self.remote_state)

            if res == self._hold.on:
                return True
            if res == self._hold.off:
                return False

    @hold.setter
    def hold(self, state):
        if self._hold is not None:
            if state:
                state = self._hold.on
            else:
                state = self._hold.off

            self._hold.set(self.remote_state, state)

    @property
    def filter(self):
        if self._filter is not None:
            res = self._filter.get(self.remote_state)
            if res == self._filter.on:
                return True

            if res == self._filter.off:
                return False

    @filter.setter
    def filter(self, state):
        if self._filter is not None:
            if state:
                state = self._filter.on
            else:
                state = self._filter.off

            self._filter.set(self.remote_state, state)

    @property
    def light(self):
        if self._light is not None:
            res = self._light.get(self.remote_state)

            if res == self._light.on:
                return True
            if res == self._light.off:
                return False

    @light.setter
    def light(self, state):
        if self._light is not None:
            if state:
                state = self._light.on
            else:
                state = self._light.off

            self._light.set(self.remote_state, state)

    # This feature maintains the room temperature steadily at 8 C and prevents the
    # room from freezing by activating the heating operation automatically when
    # nobody is at home over a longer period during severe winter.
    @property
    def anti_freeze(self):
        if self._anti_freeze is not None:
            res = self._anti_freeze.get(self.remote_state)
            if res == self._anti_freeze.on:
                return True
            if res == self._anti_freeze.off:
                return False

    @anti_freeze.setter
    def anti_freeze(self, state):
        if self._anti_freeze is not None:
            if state:
                state = self._anti_freeze.on
            else:
                state = self._anti_freeze.off

            self._anti_freeze.set(self.remote_state, state)

    @property
    def clock(self):
        if self._clock is not None:
            return self._clock.get(self.remote_state)

    @clock.setter
    def clock(self, value):
        if self._clock is not None:
            self._clock.set(self.remote_state, value)

    @property
    def scale(self):
        return 'C'

    @property
    def quiet(self):
        if self._quiet is not None:
            return self._quiet.get(self.remote_state)

    @quiet.setter
    def quiet(self, value):
        if self._quiet is not None:
            self._quiet.set(self.remote_state, value)

    @property
    def econo(self):
        if self._econo is not None:
            return self._econo.get(self.remote_state)

    @econo.setter
    def econo(self, value):
        if self._econo is not None:
            self._econo.set(self.remote_state, value)

    @property
    def clean(self):
        if self._clean is not None:
            return self._clean.get(self.remote_state)

    @clean.setter
    def clean(self, value):
        if self._clean is not None:
            self._clean.set(self.remote_state, value)

    @property
    def beep(self):
        if self._beep is not None:
            return self._beep.get(self.remote_state)

    @beep.setter
    def beep(self, value):
        if self._beep is not None:
            self._beep.set(self.remote_state, value)

    @property
    def follow(self):
        if self._follow is not None:
            return self._follow.get(self.remote_state)

    @follow.setter
    def follow(self, value):
        if self._follow is not None:
            self._follow.set(self.remote_state, value)

    # Convert the A/C state to it's common equivalent.
    def to_common(self):
        result = stdAc.state_t()
        result.protocol = self._protocol
        result.model = self.model
        result.power = self.power
        result.mode = self.mode
        result.scale = self.scale
        result.degrees = self.temperature
        result.fanspeed = self.fan_speed
        result.swingv = self.swing_vert
        result.swingh = self.swing_horz
        result.turbo = self.turbo
        result.light = self.light
        result.filter = self.filter
        result.sleep = self.sleep
        result.quiet = self.quiet
        result.econo = self.econo
        result.clean = self.clean
        result.beep = self.beep
        result.clock = self.clock
        return result

    # Convert the internal state into a human readable string.
    def to_string(self):
        result = ""
        result += irutils.addBoolToString(self.power, kPowerStr, False)
        result += irutils.addModeToString(self.mode)
        result += irutils.addTempToString(self.temperature)
        result += irutils.addFanToString(self.fan_speed)
        result += irutils.addSwingVToString(self.swing_vert)
        result += irutils.addSwingHToString(self.swing_horz)
        result += irutils.addBoolToString(self.sleep, kSleepStr)
        result += irutils.addBoolToString(self.turbo, kTurboStr)
        result += irutils.addBoolToString(self.hold, kHoldStr)
        result += irutils.addBoolToString(self.filter, kFilterStr)
        result += irutils.addBoolToString(self.light, kLightStr)
        result += irutils.addBoolToString(self.anti_freeze, k8CHeatStr)
        result += irutils.addBoolToString(self.vent, kVentStr)
        result += irutils.addBoolToString(self.follow, kFollowStr)
        return result


class ProtocolBase(object):

    def __init__(self, pin, inverted, use_modulation):
        self.remote_state = []
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.stateReset()

    def stateReset(self):
        raise NotImplementedError

    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def setPower(self, on):
        raise NotImplementedError

    def begin(self):
        self._irsend.begin()

    def decode(self, *_, **__):
        raise NotImplementedError

    def send(self, *_, **__):
        raise NotImplementedError

    def send_ac(self, *_, **__):
        raise NotImplementedError

    def decode_ac(self, *_, **__):
        raise NotImplementedError

    def sendGeneric(self, *_, **__):
        pass

    def matchData(self, *_, **__):
        return True

    def matchMark(self, *_, **__):
        return True

    def matchSpace(self, *_, **__):
        return True

    def matchGeneric(self, *_, **__):
        return True

    def matchAtLeast(self, *_, **__):
        return True
