# -*- coding: utf-8 -*-

# Copyright 2018 crankyoldgit
# The specifics of reverse engineering the protocol details by kuzin2006

# Supports:
#   Brand: Haier,  Model: HSU07-HEA03 remote
#   Brand: Haier,  Model: YR-W02 remote
#   Brand: Haier,  Model: HSU-09HMC203 A/C


from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/404
#   https:#www.dropbox.com/s/mecyib3lhdxc8c6/IR%20data%20reverse%20engineering.xlsx?dl=0
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/485
#   https:#www.dropbox.com/sh/w0bt7egp0fjger5/AADRFV6Wg4wZskJVdFvzb8Z0a?dl=0&preview=haer2.ods

# Constants

# Haier HSU07-HEA03 remote
# Byte 0
kHaierAcPrefix = 0b10100101

# Byte 1
kHaierAcMinTemp = 16
kHaierAcDefTemp = 25
kHaierAcMaxTemp = 30
kHaierAcCmdOff = 0b0000
kHaierAcCmdOn = 0b0001
kHaierAcCmdMode = 0b0010
kHaierAcCmdFan = 0b0011
kHaierAcCmdTempUp = 0b0110
kHaierAcCmdTempDown = 0b0111
kHaierAcCmdSleep = 0b1000
kHaierAcCmdTimerSet = 0b1001
kHaierAcCmdTimerCancel = 0b1010
kHaierAcCmdHealth = 0b1100
kHaierAcCmdSwing = 0b1101

# Byte 2 (Clock Hours)

# Byte 3 (Timer Flags & Clock Minutes)
kHaierAcOffTimerOffset = 6
kHaierAcOnTimerOffset = 7

# Byte 4 (Health & Off Time Hours)
kHaierAcHealthBitOffset = 5

# Byte 5 (Swing & Off Time Mins)
kHaierAcSwingOffset = 6
kHaierAcSwingSize = 2  # Bits
kHaierAcSwingOff = 0b00
kHaierAcSwingUp = 0b01
kHaierAcSwingDown = 0b10
kHaierAcSwingChg = 0b11

# Byte 6 (Mode & On Time Hours)
kHaierAcModeOffset = 5
kHaierAcAuto = 0
kHaierAcCool = 1
kHaierAcDry = 2
kHaierAcHeat = 3
kHaierAcFan = 4

kHaierAcFanAuto = 0
kHaierAcFanLow = 1
kHaierAcFanMed = 2
kHaierAcFanHigh = 3

# Byte 7 (On Time Minutes)

# Time
kHaierAcTimeOffset = 0  # Bits
kHaierAcHoursSize = 5  # Bits
kHaierAcMinsSize = 6  # Bits

kHaierAcMaxTime = (23 * 60) + 59

# Byte 7
kHaierAcSleepBitOffset = 6
kHaierAcSleepBit = 0b01000000

# Legacy Haier AC defines.
# define HAIER_AC_MIN_TEMP kHaierAcMinTemp
# define HAIER_AC_DEF_TEMP kHaierAcDefTemp
# define HAIER_AC_MAX_TEMP kHaierAcMaxTemp
# define HAIER_AC_CMD_OFF kHaierAcCmdOff
# define HAIER_AC_CMD_ON kHaierAcCmdOn
# define HAIER_AC_CMD_MODE kHaierAcCmdMode
# define HAIER_AC_CMD_FAN kHaierAcCmdFan
# define HAIER_AC_CMD_TEMP_UP kHaierAcCmdTempUp
# define HAIER_AC_CMD_TEMP_DOWN kHaierAcCmdTempDown
# define HAIER_AC_CMD_SLEEP kHaierAcCmdSleep
# define HAIER_AC_CMD_TIMER_SET kHaierAcCmdTimerSet
# define HAIER_AC_CMD_TIMER_CANCEL kHaierAcCmdTimerCancel
# define HAIER_AC_CMD_HEALTH kHaierAcCmdHealth
# define HAIER_AC_CMD_SWING kHaierAcCmdSwing
# define HAIER_AC_SWING_OFF kHaierAcSwingOff
# define HAIER_AC_SWING_UP kHaierAcSwingUp
# define HAIER_AC_SWING_DOWN kHaierAcSwingDown
# define HAIER_AC_SWING_CHG kHaierAcSwingChg
# define HAIER_AC_AUTO kHaierAcAuto
# define HAIER_AC_COOL kHaierAcCool
# define HAIER_AC_DRY kHaierAcDry
# define HAIER_AC_HEAT kHaierAcHeat
# define HAIER_AC_FAN kHaierAcFan
# define HAIER_AC_FAN_AUTO kHaierAcFanAuto
# define HAIER_AC_FAN_LOW kHaierAcFanLow
# define HAIER_AC_FAN_MED kHaierAcFanMed
# define HAIER_AC_FAN_HIGH kHaierAcFanHigh

# Haier YRW02 remote
# Byte 0
kHaierAcYrw02Prefix = 0xA6

# Byte 1
# High Nibble - Temperature
# 0x0 = 16DegC, ... 0xE = 30DegC
# Low Nibble - Swing
kHaierAcYrw02SwingOff = 0x0
kHaierAcYrw02SwingTop = 0x1
kHaierAcYrw02SwingMiddle = 0x2  # Not available in heat mode.
kHaierAcYrw02SwingBottom = 0x3  # Only available in heat mode.
kHaierAcYrw02SwingDown = 0xA
kHaierAcYrw02SwingAuto = 0xC  # Airflow

# Byte 3
kHaierAcYrw02HealthOffset = 1

# Byte 4
kHaierAcYrw02PowerOffset = 6
kHaierAcYrw02Power = 0b01000000

# Byte 5
# Bits 0-3
kHaierAcYrw02FanOffset = 5
kHaierAcYrw02FanSize = 3
kHaierAcYrw02FanHigh = 0b001
kHaierAcYrw02FanMed = 0b010
kHaierAcYrw02FanLow = 0b011
kHaierAcYrw02FanAuto = 0b101

# Byte 6
kHaierAcYrw02TurboOffset = 6
kHaierAcYrw02TurboSize = 2
kHaierAcYrw02TurboOff = 0x0
kHaierAcYrw02TurboHigh = 0x1
kHaierAcYrw02TurboLow = 0x2

# Byte 7
#                      Mode mask 0b11100000
kHaierAcYrw02ModeOffset = 5
kHaierAcYrw02Auto = 0b000  # 0
kHaierAcYrw02Cool = 0b001  # 1
kHaierAcYrw02Dry = 0b010  # 2
kHaierAcYrw02Heat = 0b100  # 4
kHaierAcYrw02Fan = 0b110  # 5

# Byte 8
kHaierAcYrw02SleepOffset = 7
kHaierAcYrw02Sleep = 0b10000000

# Byte 12
# Bits 4-7
kHaierAcYrw02ButtonTempUp = 0x0
kHaierAcYrw02ButtonTempDown = 0x1
kHaierAcYrw02ButtonSwing = 0x2
kHaierAcYrw02ButtonFan = 0x4
kHaierAcYrw02ButtonPower = 0x5
kHaierAcYrw02ButtonMode = 0x6
kHaierAcYrw02ButtonHealth = 0x7
kHaierAcYrw02ButtonTurbo = 0x8
kHaierAcYrw02ButtonSleep = 0xB

# Legacy Haier YRW02 remote defines.
# define HAIER_AC_YRW02_SWING_OFF kHaierAcYrw02SwingOff
# define HAIER_AC_YRW02_SWING_TOP kHaierAcYrw02SwingTop
# define HAIER_AC_YRW02_SWING_MIDDLE kHaierAcYrw02SwingMiddle
# define HAIER_AC_YRW02_SWING_BOTTOM kHaierAcYrw02SwingBottom
# define HAIER_AC_YRW02_SWING_DOWN kHaierAcYrw02SwingDown
# define HAIER_AC_YRW02_SWING_AUTO kHaierAcYrw02SwingAuto
# define HAIER_AC_YRW02_FAN_HIGH kHaierAcYrw02FanHigh
# define HAIER_AC_YRW02_FAN_MED kHaierAcYrw02FanMed
# define HAIER_AC_YRW02_FAN_LOW kHaierAcYrw02FanLow
# define HAIER_AC_YRW02_FAN_AUTO kHaierAcYrw02FanAuto
# define HAIER_AC_YRW02_TURBO_OFF kHaierAcYrw02TurboOff
# define HAIER_AC_YRW02_TURBO_HIGH kHaierAcYrw02TurboHigh
# define HAIER_AC_YRW02_TURBO_LOW kHaierAcYrw02TurboLow
# define HAIER_AC_YRW02_AUTO kHaierAcYrw02Auto
# define HAIER_AC_YRW02_COOL kHaierAcYrw02Cool
# define HAIER_AC_YRW02_DRY kHaierAcYrw02Dry
# define HAIER_AC_YRW02_HEAT kHaierAcYrw02Heat
# define HAIER_AC_YRW02_FAN kHaierAcYrw02Fan
# define HAIER_AC_YRW02_BUTTON_TEMP_UP kHaierAcYrw02ButtonTempUp
# define HAIER_AC_YRW02_BUTTON_TEMP_DOWN kHaierAcYrw02ButtonTempDown
# define HAIER_AC_YRW02_BUTTON_SWING kHaierAcYrw02ButtonSwing
# define HAIER_AC_YRW02_BUTTON_FAN kHaierAcYrw02ButtonFan
# define HAIER_AC_YRW02_BUTTON_POWER kHaierAcYrw02ButtonPower
# define HAIER_AC_YRW02_BUTTON_MODE kHaierAcYrw02ButtonMode
# define HAIER_AC_YRW02_BUTTON_HEALTH kHaierAcYrw02ButtonHealth
# define HAIER_AC_YRW02_BUTTON_TURBO kHaierAcYrw02ButtonTurbo
# define HAIER_AC_YRW02_BUTTON_SLEEP kHaierAcYrw02ButtonSleep


class IRHaierAC(object):
    # Class for emulating a Haier HSU07-HEA03 remote

    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kHaierACStateLength
        self._irsend = IRSend(pin, inverted, use_modulation)
        self.stateReset()

    def send(self, repeat=kHaierAcDefaultRepeat):
        self._irsend.sendHaierAC(self.getRaw(), kHaierACStateLength, repeat)

    def calibrate(self):
        return self._irsend.calibrate()

    def begin(self):
        self._irsend.begin()

    def setCommand(self, command):
        if command in (
            kHaierAcCmdOff,
            kHaierAcCmdOn,
            kHaierAcCmdMode,
            kHaierAcCmdFan,
            kHaierAcCmdTempUp,
            kHaierAcCmdTempDown,
            kHaierAcCmdSleep,
            kHaierAcCmdTimerSet,
            kHaierAcCmdTimerCancel,
            kHaierAcCmdHealth,
            kHaierAcCmdSwing
        ):
            setBits(self.remote_state[1], kLowNibble, kNibbleSize, command)

    def getCommand(self):
        return GETBITS8(self.remote_state[1], kLowNibble, kNibbleSize)

    def setTemp(self, degrees):
        temp = degrees
        if temp < kHaierAcMinTemp:
            temp = kHaierAcMinTemp
        elif temp > kHaierAcMaxTemp:
            temp = kHaierAcMaxTemp

        old_temp = self.getTemp()
        if old_temp == temp:
            return
        if old_temp > temp:
            self.setCommand(kHaierAcCmdTempDown)
        else:
            self.setCommand(kHaierAcCmdTempUp)

        setBits(self.remote_state[1], kHighNibble, kNibbleSize, temp - kHaierAcMinTemp)

    def getTemp(self):
        return GETBITS8(self.remote_state[1], kHighNibble, kNibbleSize) + kHaierAcMinTemp

    def setFan(self, speed):
        if speed == kHaierAcFanLow:
            new_speed = 3
        elif sped == kHaierAcFanMed:
            new_speed = 1
        elif speed == kHaierAcFanHigh:
            new_speed = 2
        else:
            # Default to auto for anything else.
            new_speed = kHaierAcFanAuto

        if speed != self.getFan():
            self.setCommand(kHaierAcCmdFan)

        setBits(self.remote_state[5], kLowNibble, kHaierAcSwingSize, new_speed)

    def getFan(self):
        speed = GETBITS8(self.remote_state[5], kLowNibble, kHaierAcSwingSize)
        if speed == 1:
            return kHaierAcFanMed
        if speed == 2:
            return kHaierAcFanHigh
        if speed == 3:
            return kHaierAcFanLow
        return kHaierAcFanAuto

    def getMode(self):
        return GETBITS8(self.remote_state[6], kHaierAcModeOffset, kModeBitsSize)

    def setMode(self, mode):
        new_mode = mode
        self.setCommand(kHaierAcCmdMode)
        # If out of range, default to auto mode.
        if mode > kHaierAcFan:
            new_mode = kHaierAcAuto

        setBits(self.remote_state[6], kHaierAcModeOffset, kModeBitsSize, new_mode)

    def getSleep(self):
        return GETBIT8(self.remote_state[7], kHaierAcSleepBitOffset)

    def setSleep(self, on):
        self.setCommand(kHaierAcCmdSleep)
        setBit(self.remote_state[7], kHaierAcSleepBitOffset, on)

    def getHealth(self):
        return GETBIT8(self.remote_state[4], kHaierAcHealthBitOffset)

    def setHealth(self, on):
        self.setCommand(kHaierAcCmdHealth)
        setBit(self.remote_state[4], kHaierAcHealthBitOffset, on)

    def getOnTimer(self):
        # Check if the timer is turned on.
        if GETBIT8(self.remote_state[3], kHaierAcOnTimerOffset):
            return self.getTime(self.remote_state + 6)
        else:
            return -1

    def setOnTimer(self, mins):
        self.setCommand(kHaierAcCmdTimerSet)
        setBit(self.remote_state[3], kHaierAcOnTimerOffset)
        self.setTime(self.remote_state + 6, mins)

    def getOffTimer(self):
        # Check if the timer is turned on.
        if GETBIT8(self.remote_state[3], kHaierAcOffTimerOffset):
            return self.getTime(self.remote_state + 4)
        else:
            return -1

    def setOffTimer(self, mins):
        self.setCommand(kHaierAcCmdTimerSet)
        setBit(self.remote_state[3], kHaierAcOffTimerOffset)
        self.setTime(self.remote_state + 4, mins)

    def cancelTimers(self):
        self.setCommand(kHaierAcCmdTimerCancel)
        setBits(self.remote_state[3], kHaierAcOffTimerOffset, 2, 0)

    def getCurrTime(self):
        return getTime(self.remote_state + 2)

    def setCurrTime(self, mins):
        self.setTime(self.remote_state + 2, mins)

    def getSwing(self):
        return GETBITS8(self.remote_state[2], kHaierAcSwingOffset, kHaierAcSwingSize)

    def setSwing(self, cmd):
        if cmd == self.getSwing():
            return  # Nothing to do.
        if cmd in (
            kHaierAcSwingOff,
            kHaierAcSwingUp,
            kHaierAcSwingDown,
            kHaierAcSwingChg
        ):
            self.setCommand(kHaierAcCmdSwing)
            setBits(self.remote_state[2], kHaierAcSwingOffset, kHaierAcSwingSize, cmd)

    def getRaw(self):
        self.checksum()
        return self.remote_state

    def setRaw(self, new_code):
        self.remote_state = new_code[:]

    @staticmethod
    def validChecksum(state, length=kHaierACStateLength):
        if length < 2:
            return False  # 1 byte of data can't have a checksum.

        return state[length - 1] == sumBytes(state, length - 1)

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        cmd = self.getCommand()
        result += addIntToString(cmd, kCommandStr, False)
        result += kSpaceLBraceStr
        if cmd == kHaierAcCmdOff:
            result += kOffStr
        elif cmd == kHaierAcCmdOn:
            result += kOnStr
        elif cmd == kHaierAcCmdMode:
            result += kModeStr
        elif cmd == kHaierAcCmdFan:
            result += kFanStr
        elif cmd == kHaierAcCmdTempUp:
            result += kTempUpStr
        elif cmd == kHaierAcCmdTempDown:
            result += kTempDownStr
        elif cmd == kHaierAcCmdSleep:
            result += kSleepStr
        elif cmd == kHaierAcCmdTimerSet:
            result += kTimerStr
            result += ' '
            result += kSetStr
        elif cmd == kHaierAcCmdTimerCancel:
            result += kTimerStr
            result += ' '
            result += kCancelStr
        elif cmd == kHaierAcCmdHealth:
            result += kHealthStr
        elif cmd == kHaierAcCmdSwing:
            result += kSwingStr
        else:
            result += kUnknownStr

        result += ')'
        result += addModeToString(
            self.getMode(),
            kHaierAcAuto,
            kHaierAcCool,
            kHaierAcHeat,
            kHaierAcDry,
            kHaierAcFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kHaierAcFanHigh,
            kHaierAcFanLow,
            kHaierAcFanAuto,
            kHaierAcFanAuto,
            kHaierAcFanMed
        )
        result += addIntToString(
            self.getSwing(),
            kSwingStr
        )
        result += kSpaceLBraceStr

        swing = getSwing()

        if swing == kHaierAcSwingOff:
            result += kOffStr
        elif swing == kHaierAcSwingUp:
            result += kUpStr
        elif swing == kHaierAcSwingDown:
            result += kDownStr
        elif swing == kHaierAcSwingChg:
            result += kChangeStr
        else:
            result += kUnknownStr

        result += ')'
        result += addBoolToString(getSleep(), kSleepStr)
        result += addBoolToString(getHealth(), kHealthStr)
        result += addLabeledString(minsToString(getCurrTime()), kClockStr)
        result += addLabeledString(
            minsToString(self.getOnTimer()) if self.getOnTimer() >= 0 else kOffStr,
            kOnTimerStr
        )
        result += addLabeledString(
            minsToString(self.getOffTimer()) if self.getOffTimer() >= 0 else kOffStr,
            kOffTimerStr
        )
        return result

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kHaierAcCool
        if mode == stdAc.opmode_t.kHeat:
            return kHaierAcHeat
        if mode == stdAc.opmode_t.kDry:
            return kHaierAcDry
        if mode == stdAc.opmode_t.kFan:
            return kHaierAcFan

        return kHaierAcAuto

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):
            return kHaierAcFanLow
        if speed == stdAc.fanspeed_t.kMedium:
            return kHaierAcFanMed
        if speed in (
            stdAc.fanspeed_t.kHigh,
            stdAc.fanspeed_t.kMax
        ):
            return kHaierAcFanHigh

        return kHaierAcFanAuto

    @staticmethod
    def convertSwingV(position):
        # Convert a standard A/C vertical swing into its native setting.
        if position in (
            stdAc.swingv_t.kHighest,
            stdAc.swingv_t.kHigh,
            stdAc.swingv_t.kMiddle
        ):
            return kHaierAcSwingUp

        if position in (
            stdAc.swingv_t.kLow,
            stdAc.swingv_t.kLowest
        ):
            return kHaierAcSwingDown

        if position == stdAc.swingv_t.kOff:
            return kHaierAcSwingOff

        return kHaierAcSwingChg

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kHaierAcCool:
            return stdAc.opmode_t.kCool
        if mode == kHaierAcHeat:
            return stdAc.opmode_t.kHeat
        if mode == kHaierAcDry:
            return stdAc.opmode_t.kDry
        if mode == kHaierAcFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kHaierAcFanHigh:
            return stdAc.fanspeed_t.kMax
        if speed == kHaierAcFanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kHaierAcFanLow:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    @staticmethod
    def toCommonSwingV(pos):
        # Convert a native vertical swing to it's common equivalent.
        if pos == kHaierAcSwingUp:
            return stdAc.swingv_t.kHighest
        if pos == kHaierAcSwingDown:
            return stdAc.swingv_t.kLowest
        if pos == kHaierAcSwingOff:
            return stdAc.swingv_t.kOff

        return stdAc.swingv_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.HAIER_AC
        result.model = -1  # No models used.
        result.power = True
        if self.getCommand() == kHaierAcCmdOff:
            result.power = False

        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = self.toCommonSwingV(self.getSwing())
        result.filter = self.getHealth()
        result.sleep = 0 if self.getSleep() else -1
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.turbo = False
        result.econo = False
        result.light = False
        result.clean = False
        result.beep = False
        result.clock = -1
        return result

    def stateReset(self):
        self.remote_state = [0x0] * kHaierACStateLength
        self.remote_state[0] = kHaierAcPrefix
        self.remote_state[2] = 0x20
        self.remote_state[4] = 0x0C
        self.remote_state[5] = 0xC0

        self.setTemp(kHaierAcDefTemp)
        self.setFan(kHaierAcFanAuto)
        self.setMode(kHaierAcAuto)
        self.setCommand(kHaierAcCmdOn)

    def checksum(self):
        self.remote_state[8] = sumBytes(self.remote_state, kHaierACStateLength - 1)

    @staticmethod
    def getTime(ptr):
        return (
            GETBITS8(ptr[0], kHaierAcTimeOffset, kHaierAcHoursSize) * 60 +
            GETBITS8(ptr[1], kHaierAcTimeOffset, kHaierAcMinsSize)
        )

    @staticmethod
    def setTime(ptr, nr_mins):
        mins = nr_mins
        if nr_mins > kHaierAcMaxTime:
            mins = kHaierAcMaxTime
        setBits(ptr, kHaierAcTimeOffset, kHaierAcHoursSize, mins / 60)  # Hours
        setBits(ptr + 1, kHaierAcTimeOffset, kHaierAcMinsSize, mins % 60)  # Minutes


class IRHaierACYRW02(object):
    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kHaierACYRW02StateLength
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.stateReset()

    def send(self, repeat=kHaierAcYrw02DefaultRepeat):
        self._irsend.sendHaierACYRW02(self.getRaw(), kHaierACYRW02StateLength, repeat)

    def begin(self):
        self._irsend.begin()

    def setButton(self, button):
        if buton in (
            kHaierAcYrw02ButtonTempUp,
            kHaierAcYrw02ButtonTempDown,
            kHaierAcYrw02ButtonSwing,
            kHaierAcYrw02ButtonFan,
            kHaierAcYrw02ButtonPower,
            kHaierAcYrw02ButtonMode,
            kHaierAcYrw02ButtonHealth,
            kHaierAcYrw02ButtonTurbo,
            kHaierAcYrw02ButtonSleep
        ):
            setBits(self.remote_state[12], kLowNibble, kNibbleSize, button)

    def getButton(self):
        return GETBITS8(self.remote_state[12], kLowNibble, kNibbleSize)

    def setTemp(self, celsius):
        temp = celsius
        if temp < kHaierAcMinTemp:
            temp = kHaierAcMinTemp
        elif temp > kHaierAcMaxTemp:
            temp = kHaierAcMaxTemp

        old_temp = self.getTemp()
        if old_temp == temp:
            return

        if old_temp > temp:
            self.setButton(kHaierAcYrw02ButtonTempDown)
        else:
            self.setButton(kHaierAcYrw02ButtonTempUp)

        setBits(self.remote_state[1], kHighNibble, kNibbleSize, temp - kHaierAcMinTemp)

    def getTemp(self):
        return GETBITS8(self.remote_state[1], kHighNibble, kNibbleSize) + kHaierAcMinTemp

    def setFan(self, speed):
        if speed in (
            kHaierAcYrw02FanLow,
            kHaierAcYrw02FanMed,
            kHaierAcYrw02FanHigh,
            kHaierAcYrw02FanAuto
        ):
            setBits(self.remote_state[5], kHaierAcYrw02FanOffset, kHaierAcYrw02FanSize, speed)

        self.setButton(kHaierAcYrw02ButtonFan)

    def getFan(self):
        return GETBITS8(self.remote_state[5], kHaierAcYrw02FanOffset, kHaierAcYrw02FanSize)

    def getMode(self):
        return GETBITS8(self.remote_state[7], kHaierAcYrw02ModeOffset, kModeBitsSize)

    def setMode(self, mode):
        new_mode = mode
        self.setButton(kHaierAcYrw02ButtonMode)
        if mode not in (
            kHaierAcYrw02Auto,
            kHaierAcYrw02Cool,
            kHaierAcYrw02Dry,
            kHaierAcYrw02Heat,
            kHaierAcYrw02Fan
        ):
            new_mode = kHaierAcYrw02Auto  # Unexpected, default to auto mode.

        setBits(self.remote_state[7], kHaierAcYrw02ModeOffset, kModeBitsSize, new_mode)

    def getPower(self):
        return GETBIT8(self.remote_state[4], kHaierAcYrw02PowerOffset)

    def setPower(self, on):
        self.setButton(kHaierAcYrw02ButtonPower)
        setBit(self.remote_state[4], kHaierAcYrw02PowerOffset, on)

    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def getSleep(self):
        return GETBIT8(self.remote_state[8], kHaierAcYrw02SleepOffset)

    def setSleep(self, on):
        self.setButton(kHaierAcYrw02ButtonSleep)
        setBit(self.remote_state[8], kHaierAcYrw02SleepOffset, on)

    def getHealth(self):
        return GETBIT8(self.remote_state[3], kHaierAcYrw02HealthOffset)

    def setHealth(self, on):
        self.setButton(kHaierAcYrw02ButtonHealth)
        setBit(self.remote_state[3], kHaierAcYrw02HealthOffset, on)

    def getTurbo(self):
        return GETBITS8(self.remote_state[6], kHaierAcYrw02TurboOffset, kHaierAcYrw02TurboSize)

    def setTurbo(self, speed):
        if speed in (
            kHaierAcYrw02TurboOff,
            kHaierAcYrw02TurboLow,
            kHaierAcYrw02TurboHigh
        ):
            setBits(self.remote_state[6], kHaierAcYrw02TurboOffset, kHaierAcYrw02TurboSize, speed)
            self.setButton(kHaierAcYrw02ButtonTurbo)

    def getSwing(self):
        return GETBITS8(self.remote_state[1], kLowNibble, kNibbleSize)

    def setSwing(self, pos):
        newpos = pos

        if pos in (
            kHaierAcYrw02SwingOff,
            kHaierAcYrw02SwingAuto,
            kHaierAcYrw02SwingTop,
            kHaierAcYrw02SwingMiddle,
            kHaierAcYrw02SwingBottom,
            kHaierAcYrw02SwingDown
        ):
            self.setButton(kHaierAcYrw02ButtonSwing)
        else:
            return  # Unexpected value so don't do anything.

        # Heat mode has no MIDDLE setting, use BOTTOM instead.
        if pos == kHaierAcYrw02SwingMiddle and self.getMode() == kHaierAcYrw02Heat:
            newpos = kHaierAcYrw02SwingBottom

        # BOTTOM is only allowed if we are in Heat mode, otherwise MIDDLE.
        if pos == kHaierAcYrw02SwingBottom and self.getMode() != kHaierAcYrw02Heat:
            newpos = kHaierAcYrw02SwingMiddle

        setBits(self.remote_state[1], kLowNibble, kNibbleSize, newpos)

    def getRaw(self):
        self.checksum()
        return remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kHaierACYRW02StateLength]

    @staticmethod
    def validChecksum(state, length=kHaierACYRW02StateLength):
        if length < 2:
            return False  # 1 byte of data can't have a checksum.

        return state[length - 1] == sumBytes(state, length - 1)

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kHaierAcYrw02Cool
        if mode == stdAc.opmode_t.kHeat:
            return kHaierAcYrw02Heat
        if mode == stdAc.opmode_t.kDry:
            return kHaierAcYrw02Dry
        if mode == stdAc.opmode_t.kFan:
            return kHaierAcYrw02Fan

        return kHaierAcYrw02Auto

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):
            return kHaierAcYrw02FanLow

        if speed == stdAc.fanspeed_t.kMedium:
            return kHaierAcYrw02FanMed

        if speed in (
            stdAc.fanspeed_t.kHigh,
            stdAc.fanspeed_t.kMax
        ):
            return kHaierAcYrw02FanHigh

        return kHaierAcYrw02FanAuto

    @staticmethod
    def convertSwingV(position):
        # Convert a standard A/C vertical swing into its native setting.
        if position in (
            stdAc.swingv_t.kHighest,
            stdAc.swingv_t.kHigh
        ):
            return kHaierAcYrw02SwingTop

        if position == stdAc.swingv_t.kMiddle:
            return kHaierAcYrw02SwingMiddle
        if position == stdAc.swingv_t.kLow:
            return kHaierAcYrw02SwingDown
        if position == stdAc.swingv_t.kLowest:
            return kHaierAcYrw02SwingBottom
        if position == stdAc.swingv_t.kOff:
            return kHaierAcYrw02SwingOff

        return kHaierAcYrw02SwingAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kHaierAcYrw02Cool:
            return stdAc.opmode_t.kCool
        if mode == kHaierAcYrw02Heat:
            return stdAc.opmode_t.kHeat
        if mode == kHaierAcYrw02Dry:
            return stdAc.opmode_t.kDry
        if mode == kHaierAcYrw02Fan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kHaierAcYrw02FanHigh:
            return stdAc.fanspeed_t.kMax
        if speed == kHaierAcYrw02FanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kHaierAcYrw02FanLow:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    @staticmethod
    def toCommonSwingV(pos):
        # Convert a native vertical swing to it's common equivalent.
        if pos == kHaierAcYrw02SwingTop:
            return stdAc.swingv_t.kHighest
        if pos == kHaierAcYrw02SwingMiddle:
            return stdAc.swingv_t.kMiddle
        if pos == kHaierAcYrw02SwingDown:
            return stdAc.swingv_t.kLow
        if pos == kHaierAcYrw02SwingBottom:
            return stdAc.swingv_t.kLowest
        if pos == kHaierAcYrw02SwingOff:
            return stdAc.swingv_t.kOff

        return stdAc.swingv_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.HAIER_AC_YRW02
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = self.toCommonSwingV(self.getSwing())
        result.filter = self.getHealth()
        result.sleep = 0 if self.getSleep() else -1
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.turbo = False
        result.econo = False
        result.light = False
        result.clean = False
        result.beep = False
        result.clock = -1
        return result

    def toString(self):
        # Convert the internal state into a human readable string.

        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        cmd = self.getButton()
        result += addIntToString(cmd, kButtonStr)
        result += kSpaceLBraceStr
        if cmd == kHaierAcYrw02ButtonPower:
            result += kPowerStr
        elif cmd == kHaierAcYrw02ButtonMode:
            result += kModeStr
        elif cmd == kHaierAcYrw02ButtonFan:
            result += kFanStr
        elif cmd == kHaierAcYrw02ButtonTempUp:
            result += kTempUpStr
        elif cmd == kHaierAcYrw02ButtonTempDown:
            result += kTempDownStr
        elif cmd == kHaierAcYrw02ButtonSleep:
            result += kSleepStr
        elif cmd == kHaierAcYrw02ButtonHealth:
            result += kHealthStr
        elif cmd == kHaierAcYrw02ButtonSwing:
            result += kSwingStr
        elif cmd == kHaierAcYrw02ButtonTurbo:
            result += kTurboStr
        else:
            result += kUnknownStr

        result += ')'
        result += addModeToString(
            self.getMode(),
            kHaierAcYrw02Auto,
            kHaierAcYrw02Cool,
            kHaierAcYrw02Heat,
            kHaierAcYrw02Dry,
            kHaierAcYrw02Fan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kHaierAcYrw02FanHigh,
            kHaierAcYrw02FanLow,
            kHaierAcYrw02FanAuto,
            kHaierAcYrw02FanAuto,
            kHaierAcYrw02FanMed
        )
        result += addIntToString(self.getTurbo(), kTurboStr)
        result += kSpaceLBraceStr
        turbo = self.getTurbo()

        if turbo == kHaierAcYrw02TurboOff:
            result += kOffStr
        elif turbo == kHaierAcYrw02TurboLow:
            result += kLowStr
        elif turbo == kHaierAcYrw02TurboHigh:
            result += kHighStr
        else:
            result += kUnknownStr

        result += ')'
        result += addIntToString(self.getSwing(), kSwingStr)
        result += kSpaceLBraceStr

        swing = self.getSwing()
        if swing == kHaierAcYrw02SwingOff:
            result += kOffStr
        elif swing == kHaierAcYrw02SwingAuto:
            result += kAutoStr
        elif swing == kHaierAcYrw02SwingBottom:
            result += kLowestStr
        elif swing == kHaierAcYrw02SwingDown:
            result += kLowStr
        elif swing == kHaierAcYrw02SwingTop:
            result += kHighestStr
        elif swing == kHaierAcYrw02SwingMiddle:
            result += kMiddleStr
        else:
            result += kUnknownStr

        result += ')'
        result += addBoolToString(self.getSleep(), kSleepStr)
        result += addBoolToString(self.getHealth(), kHealthStr)
        return result

    def stateReset(self):
        self.remote_state = [0x0] * kHaierACYRW02StateLength
        self.remote_state[0] = kHaierAcYrw02Prefix

        self.setTemp(kHaierAcDefTemp)
        self.setHealth(True)
        self.setTurbo(kHaierAcYrw02TurboOff)
        self.setSleep(False)
        self.setFan(kHaierAcYrw02FanAuto)
        self.setSwing(kHaierAcYrw02SwingOff)
        self.setMode(kHaierAcYrw02Auto)
        self.setPower(True)

    def checksum(self):
        self.remote_state[kHaierACYRW02StateLength - 1] = sumBytes(self.remote_state, kHaierACYRW02StateLength - 1)


# Supported devices:
#   * Haier HSU07-HEA03 Remote control.
#   * Haier YR-W02 Remote control
#   * Haier HSU-09HMC203 A/C unit.

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/404
#   https:#www.dropbox.com/s/mecyib3lhdxc8c6/IR%20data%20reverse%20engineering.xlsx?dl=0
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/485
#   https:#www.dropbox.com/sh/w0bt7egp0fjger5/AADRFV6Wg4wZskJVdFvzb8Z0a?dl=0&preview=haer2.ods

# Constants
kHaierAcHdr = 3000
kHaierAcHdrGap = 4300
kHaierAcBitMark = 520
kHaierAcOneSpace = 1650
kHaierAcZeroSpace = 650
kHaierAcMinGap = 150000  # Completely made up value.

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
minsToString = irutils.minsToString
setBit = irutils.setBit
setBits = irutils.setBits


# Send a Haier A/C message. (HSU07-HEA03 remote)
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kHaierACStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: STABLE / Known to be working.
#
def sendHaierAC(data, nbytes, repeat):
    if nbytes < kHaierACStateLength:
        return

    for _ in tange(repeat + 1):
        enableIROut(38000)
        mark(kHaierAcHdr)
        space(kHaierAcHdr)
        sendGeneric(
            kHaierAcHdr,
            kHaierAcHdrGap,
            kHaierAcBitMark,
            kHaierAcOneSpace,
            kHaierAcBitMark,
            kHaierAcZeroSpace,
            kHaierAcBitMark,
            kHaierAcMinGap,
            data,
            nbytes,
            38,
            True,
            0,  # Repeats handled elsewhere
            50
        )


# Send a Haier YR-W02 remote A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kHaierACYRW02StateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: Alpha / Untested on a real device.
#
def sendHaierACYRW02(data, nbytes, repeat):
    if nbytes >= kHaierACYRW02StateLength:
        sendHaierAC(data, nbytes, repeat)


# End of IRHaierACYRW02 class.

# Decode the supplied Haier HSU07-HEA03 remote message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kHaierACBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Known to be working.
#
def decodeHaierAC(results, nbits, strict):
    if strict and nbits != kHaierACBits:
        return False  # Not strictly a HAIER_AC message.

    if results.rawlen < (2 * nbits + kHeader) + kFooter - 1:
        return False  # Can't possibly be a valid HAIER_AC message.

    offset = kStartOffset

    # Pre-Header
    offset += 1
    if not matchMark(results.rawbuf[offset], kHaierAcHdr):
        return False

    offset += 1
    if not matchSpace(results.rawbuf[offset], kHaierAcHdr):
        return False

    # Match Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        kHaierAcHdr,
        kHaierAcHdrGap,
        kHaierAcBitMark,
        kHaierAcOneSpace,
        kHaierAcBitMark,
        kHaierAcZeroSpace,
        kHaierAcBitMark,
        kHaierAcMinGap,
        True,
        _tolerance,
        kMarkExcess
    ):
        return False

    # Compliance
    if strict:
        if results.state[0] != kHaierAcPrefix:
            return False
        if not IRHaierAC.validChecksum(results.state, nbits / 8):
            return False

    # Success
    results.decode_type = HAIER_AC
    results.bits = nbits
    return True


# Decode the supplied Haier YR-W02 remote A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kHaierACYRW02Bits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Appears to be working.
#
def decodeHaierACYRW02(results, nbits, strict):
    if strict and nbits != kHaierACYRW02Bits:
        return False  # Not strictly a HAIER_AC_YRW02 message.

    # The protocol is almost exactly the same as HAIER_AC
    if not decodeHaierAC(results, nbits, False):
        return False

    # Compliance
    if strict and results.state[0] != kHaierAcYrw02Prefix:
        return False

    if not IRHaierACYRW02.validChecksum(results.state, nbits / 8):
        return False

    # Success
    # It looks correct, but we haven't check the checksum etc.
    results.decode_type = HAIER_AC_YRW02
    return True
