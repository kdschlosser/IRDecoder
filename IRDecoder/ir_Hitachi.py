# -*- coding: utf-8 -*-

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Hitachi A/C
#
# Copyright 2018-2019 David Conran

# Supports:
#   Brand: Hitachi,  Model: RAS-35THA6 remote
#   Brand: Hitachi,  Model: LT0541-HTA remote
#   Brand: Hitachi,  Model: Series VI A/C (Circa 2007)
#   Brand: Hitachi,  Model: RAR-8P2 remote
#   Brand: Hitachi,  Model: RAS-AJ25H A/C


# Constants
kHitachiAcFreq = 38000  # Hz.
kHitachiAcAuto = 2
kHitachiAcHeat = 3
kHitachiAcCool = 4
kHitachiAcDry = 5
kHitachiAcFan = 0xC
kHitachiAcFanAuto = 1
kHitachiAcFanLow = 2
kHitachiAcFanMed = 3
kHitachiAcFanHigh = 5
kHitachiAcMinTemp = 16   # 16C
kHitachiAcMaxTemp = 32   # 32C
kHitachiAcAutoTemp = 23  # 23C
kHitachiAcPowerOffset = 0
kHitachiAcSwingOffset = 7

# HitachiAc424
# Byte[11]
kHitachiAc424ButtonByte = 11
kHitachiAc424ButtonPowerMode = 0x13
kHitachiAc424ButtonFan = 0x42
kHitachiAc424ButtonTempDown = 0x43
kHitachiAc424ButtonTempUp = 0x44
kHitachiAc424ButtonSwingV = 0x81

# Byte[13]
kHitachiAc424TempByte = 13
kHitachiAc424TempOffset = 2
kHitachiAc424TempSize = 6
kHitachiAc424MinTemp = 16   # 16C
kHitachiAc424MaxTemp = 32   # 32C
kHitachiAc424FanTemp = 27   # 27C

# Byte[25]
kHitachiAc424ModeByte = 25
kHitachiAc424Fan = 1
kHitachiAc424Cool = 3
kHitachiAc424Dry = 5
kHitachiAc424Heat = 6
kHitachiAc424FanByte = kHitachiAc424ModeByte
kHitachiAc424FanMin = 1
kHitachiAc424FanLow = 2
kHitachiAc424FanMedium = 3
kHitachiAc424FanHigh = 4
kHitachiAc424FanAuto = 5
kHitachiAc424FanMax = 6
kHitachiAc424FanMaxDry = 2
# Byte[27]
kHitachiAc424PowerByte = 27
kHitachiAc424PowerOn = 0xF1
kHitachiAc424PowerOff = 0xE1


# Copyright 2018-2019 David Conran
#
# Code to emulate Hitachi protocol compatible devices.
# Should be compatible with:
# * Hitachi RAS-35THA6 remote
#

# Constants
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/417
kHitachiAcHdrMark = 3300
kHitachiAcHdrSpace = 1700
kHitachiAc1HdrMark = 3400
kHitachiAc1HdrSpace = 3400
kHitachiAcBitMark = 400
kHitachiAcOneSpace = 1250
kHitachiAcZeroSpace = 500
kHitachiAcMinGap = kDefaultMessageGap  # Just a guess.
# Support for HitachiAc424 protocol
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/973
kHitachiAc424LdrMark = 29784   # Leader
kHitachiAc424LdrSpace = 49290  # Leader
kHitachiAc424HdrMark = 3416    # Header
kHitachiAc424HdrSpace = 1604   # Header
kHitachiAc424BitMark = 463
kHitachiAc424OneSpace = 1208
kHitachiAc424ZeroSpace = 372

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits


# Classes
class IRHitachiAc(object):

    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kHitachiAcStateLength
        self._previoustemp = 0
        self._irsend = IRSend(pin, inverted, use_modulation)
        self.stateReset()

    def stateReset(self):
        self.remote_state = [0x0] * kHitachiAcStateLength
        self.remote_state[0] = 0x80
        self.remote_state[1] = 0x08
        self.remote_state[2] = 0x0C
        self.remote_state[3] = 0x02
        self.remote_state[4] = 0xFD
        self.remote_state[5] = 0x80
        self.remote_state[6] = 0x7F
        self.remote_state[7] = 0x88
        self.remote_state[8] = 0x48
        self.remote_state[9] = 0x10
        self.remote_state[14] = 0x60
        self.remote_state[15] = 0x60
        self.remote_state[24] = 0x80
        self.setTemp(23)

    def send(self, repeat=kHitachiAcDefaultRepeat):
        self._irsend.sendHitachiAC(getRaw(), kHitachiAcStateLength, repeat)

    def calibrate(self):
        return self._irsend.calibrate()

    def begin(self):
        self._irsend.begin()

    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def setPower(self, on):
        setBit(self.remote_state[17], kHitachiAcPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote_state[17], kHitachiAcPowerOffset)

    def setTemp(self, temp):
        if temp != 64:
            self._previoustemp = temp
            temp = min(temp, kHitachiAcMaxTemp)
            temp = max(temp, kHitachiAcMinTemp)

        self.remote_state[11] = reverseBits(temp << 1, 8)
        if temp == kHitachiAcMinTemp:
            self.remote_state[9] = 0x90
        else:
            self.remote_state[9] = 0x10

    def getTemp(self):
        return reverseBits(self.remote_state[11], 8) >> 1

    def setFan(self, speed):
        fanmin = kHitachiAcFanAuto
        fanmax = kHitachiAcFanHigh
        mode = self.getMode()
        if mode == kHitachiAcDry:
            # Only 2 x low speeds in Dry mode.
            fanmin = kHitachiAcFanLow
            fanmax = kHitachiAcFanLow + 1
        elif mode == kHitachiAcFan:
            fanmin = kHitachiAcFanLow  # No Auto in Fan mode.

        newspeed = max(speed, fanmin)
        newspeed = min(newspeed, fanmax)
        self.remote_state[13] = reverseBits(newspeed, 8)

    def getFan(self):
        return reverseBits(self.remote_state[13], 8)

    def setMode(self, mode):
        newmode = mode
        # Fan mode sets a special temp.
        if mode == kHitachiAcFan:
            self.setTemp(64)
        elif mode not in (
            kHitachiAcAuto,
            kHitachiAcHeat,
            kHitachiAcCool,
            kHitachiAcDry
        ):
            newmode = kHitachiAcAuto

        self.remote_state[10] = reverseBits(newmode, 8)
        if mode != kHitachiAcFan:
            self.setTemp(self._previoustemp)

        self.setFan(self.getFan())  # Reset the fan speed after the mode change.

    def getMode(self):
        return reverseBits(self.remote_state[10], 8)

    def setSwingVertical(self, on):
        setBit(self.remote_state[14], kHitachiAcSwingOffset, on)

    def getSwingVertical(self):
        return GETBIT8(self.remote_state[14], kHitachiAcSwingOffset)

    def setSwingHorizontal(self, on):
        setBit(self.remote_state[15], kHitachiAcSwingOffset, on)

    def getSwingHorizontal(self):
        return GETBIT8(self.remote_state[15], kHitachiAcSwingOffset)

    def getRaw(self):
        self.checksum()
        return self.remote_state[:]

    def setRaw(self, new_code, length=kHitachiAcStateLength):
        self.remote_state = new_code[:min(length, kHitachiAcStateLength)]

    @staticmethod
    def validChecksum(state, length=kHitachiAcStateLength):
        if length < 2:
            return True  # Assume True for lengths that are too short.

        return state[length - 1] == calcChecksum(state, length)

    @staticmethod
    def calcChecksum(state, length=kHitachiAcStateLength):
        sm = 62
        for i in range(length - 1):
            sm -= reverseBits(state[i], 8)

        return reverseBits(sm, 8)

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode
        if mode == stdAc.opmode_t.kCool:
            return kHitachiAcCool
        if mode == stdAc.opmode_t.kHeat:
            return kHitachiAcHeat
        if mode == stdAc.opmode_t.kDry:
            return kHitachiAcDry
        if mode == stdAc.opmode_t.kFan:
            return kHitachiAcFan

        return kHitachiAcAuto

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):
            return kHitachiAcFanLow

        if speed == stdAc.fanspeed_t.kMedium:
            return kHitachiAcFanLow + 1
        if speed == stdAc.fanspeed_t.kHigh:
            return kHitachiAcFanHigh - 1
        if speed == stdAc.fanspeed_t.kMax:
            return kHitachiAcFanHigh

        return kHitachiAcFanAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kHitachiAcCool:
            return stdAc.opmode_t.kCool
        if mode == kHitachiAcHeat:
            return stdAc.opmode_t.kHeat
        if mode == kHitachiAcDry:
            return stdAc.opmode_t.kDry
        if mode == kHitachiAcFan:
            return stdAc.opmode_t.kFan
        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kHitachiAcFanHigh:
            return stdAc.fanspeed_t.kMax
        if speed == kHitachiAcFanHigh - 1:
            return stdAc.fanspeed_t.kHigh
        if speed == kHitachiAcFanLow + 1:
            return stdAc.fanspeed_t.kMedium
        if speed == kHitachiAcFanLow:
            return stdAc.fanspeed_t.kLow

        return stdAc.fanspeed_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.HITACHI_AC
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwingVertical() else stdAc.swingv_t.kOff
        result.swingh = stdAc.swingh_t.kAuto if self.getSwingHorizontal() else stdAc.swingh_t.kOff
        # Not supported.
        result.quiet = False
        result.turbo = False
        result.clean = False
        result.econo = False
        result.filter = False
        result.light = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kHitachiAcAuto,
            kHitachiAcCool,
            kHitachiAcHeat,
            kHitachiAcDry,
            kHitachiAcFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kHitachiAcFanHigh,
            kHitachiAcFanLow,
            kHitachiAcFanAuto,
            kHitachiAcFanAuto,
            kHitachiAcFanMed
        )
        result += addBoolToString(self.getSwingVertical(), kSwingVStr)
        result += addBoolToString(self.getSwingHorizontal(), kSwingHStr)
        return result

    def checksum(self, length=kHitachiAcStateLength):
        self.remote_state[length - 1] = calcChecksum(self.remote_state, length)


class IRHitachiAc424(object):

    def __init__(self, pin, inverted=False, use_modulation=True):
        # The state of the IR remote in IR code form.
        self.remote_state = [0x0] * kHitachiAc424StateLength
        self._previoustemp = 0
        
        self._irsend = IRSend(pin, inverted, use_modulation)
        self.stateReset()

    def stateReset(self):
        # Reset to auto fan, cooling, 23° Celcius
        self.remote_state = [0x0] * kHitachiAc424StateLength

        self.remote_state[0] = 0x01
        self.remote_state[1] = 0x10
        self.remote_state[3] = 0x40
        self.remote_state[5] = 0xFF
        self.remote_state[7] = 0xCC
        self.remote_state[33] = 0x80
        self.remote_state[35] = 0x03
        self.remote_state[37] = 0x01
        self.remote_state[39] = 0x88
        self.remote_state[45] = 0xFF
        self.remote_state[47] = 0xFF
        self.remote_state[49] = 0xFF
        self.remote_state[51] = 0xFF

        self.setTemp(23)
        self.setPower(True)
        self.setMode(kHitachiAc424Cool)
        self.setFan(kHitachiAc424FanAuto)

    def setInvertedStates(self):
        for i in range(3, kHitachiAc424StateLength - 1, 2):
            self.remote_state[i + 1] = ~self.remote_state[i]

    def send(self, repeat=kHitachiAcDefaultRepeat):
        self._irsend.sendHitachiAc424(self.getRaw(), kHitachiAc424StateLength, repeat)
    
    def calibrate(self):
        return self._irsend.calibrate()
        
    def begin(self):
        self._irsend.begin()
        
    def on(self):
        self.setPower(True)
        
    def off(self):
        self.setPower(False)
    
    def setPower(self, on):
        self.setButton(kHitachiAc424ButtonPowerMode)
        remote_state[kHitachiAc424PowerByte] = kHitachiAc424PowerOn if on else kHitachiAc424PowerOff

    def getPower(self):
        return self.remote_state[kHitachiAc424PowerByte] == kHitachiAc424PowerOn

    def setTemp(self, temp, setPrevious=True):
        temp = min(temp, kHitachiAc424MaxTemp)
        temp = max(temp, kHitachiAc424MinTemp)
        setBits(self.remote_state[kHitachiAc424TempByte], kHitachiAc424TempOffset, kHitachiAc424TempSize, temp)

        if self._previoustemp > temp:
            self.setButton(kHitachiAc424ButtonTempDown)
        elif self._previoustemp < temp:
            self.setButton(kHitachiAc424ButtonTempUp)

        if setPrevious:
            self._previoustemp = temp

    def getTemp(self):
        return GETBITS8(self.remote_state[kHitachiAc424TempByte], kHitachiAc424TempOffset, kHitachiAc424TempSize)

    def setFan(self, speed):
        newSpeed = max(speed, kHitachiAc424FanMin)
        fanMax = kHitachiAc424FanMax

        # Only 2 x low speeds in Dry mode or Auto
        if self.getMode() == kHitachiAc424Dry and speed == kHitachiAc424FanAuto:
            fanMax = kHitachiAc424FanAuto
        elif self.getMode() == kHitachiAc424Dry:
            fanMax = kHitachiAc424FanMaxDry
        elif self.getMode() == kHitachiAc424Fan and speed == kHitachiAc424FanAuto:
            # Fan Mode does not have auto. Set to safe low
            newSpeed = kHitachiAc424FanMin

        newSpeed = min(newSpeed, fanMax)

        # Handle the setting the button value if we are going to change the value.
        if newSpeed != self.getFan():
            self.setButton(kHitachiAc424ButtonFan)

        # Set the values
        setBits(self.remote_state[kHitachiAc424FanByte], kHighNibble, kNibbleSize, newSpeed)
        self.remote_state[9] = 0x92
        self.remote_state[29] = 0x00

        # When fan is at min/max, additional bytes seem to be set
        if newSpeed == kHitachiAc424FanMin:
            self.remote_state[9] = 0x98
        if newSpeed == kHitachiAc424FanMax:
            self.remote_state[9] = 0xA9
            self.remote_state[29] = 0x30
    
    def getFan(self):
        return GETBITS8(self.remote_state[kHitachiAc424FanByte], kHighNibble, kNibbleSize)

    def setMode(self, mode):
        newMode = mode
        # Fan mode sets a special temp.
        if mode == kHitachiAc424Fan:
            setTemp(kHitachiAc424FanTemp, False)
        elif mode not in (
            kHitachiAc424Heat,
            kHitachiAc424Cool,
            kHitachiAc424Dry
        ):
            newMode = kHitachiAc424Cool

        setBits(self.remote_state[kHitachiAc424ModeByte], kLowNibble, kNibbleSize, newMode)
        if newMode != kHitachiAc424Fan:
            self.setTemp(self._previoustemp)

        self.setFan(self.getFan())  # Reset the fan speed after the mode change.
        self.setButton(kHitachiAc424ButtonPowerMode)

    def getMode(self):
        return GETBITS8(self.remote_state[kHitachiAc424ModeByte], kLowNibble, kNibbleSize)

    def getButton(self):
        return self.remote_state[kHitachiAc424ButtonByte]

    def setButton(self, button):
        # The remote sends the type of button pressed on send
        self.remote_state[kHitachiAc424ButtonByte] = button

    def setSwingVToggle(self, on):
        # The remote does not keep state of the vertical swing.
        # A byte is sent indicating the swing button is pressed on the remote
        button = self.getButton()  # Get the current button value.
        if on:
            button = kHitachiAc424ButtonSwingV  # Set the button to SwingV.
        elif button == kHitachiAc424ButtonSwingV:
            # Asked to unset it
            # It was set previous, so use Power as a default
            button = kHitachiAc424ButtonPowerMode
        else:
            return

        self.setButton(button)

    def getSwingVToggle(self):
        return self.getButton() == kHitachiAc424ButtonSwingV

    def getRaw(self):
        self.setInvertedStates()
        return self.remote_state[:]

    def setRaw(self, new_code, length=kHitachiAc424StateLength):
        self.remote_state = new_code[:min(length, kHitachiAc424StateLength)]

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kHitachiAc424Cool
        if mode == stdAc.opmode_t.kHeat:
            return kHitachiAc424Heat
        if mode == stdAc.opmode_t.kDry:
            return kHitachiAc424Dry
        if mode == stdAc.opmode_t.kFan:
            return kHitachiAc424Fan

        return kHitachiAc424Cool

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed == stdAc.fanspeed_t.kMin:
            return kHitachiAc424FanMin
        if speed == stdAc.fanspeed_t.kLow:
            return kHitachiAc424FanLow
        if speed == stdAc.fanspeed_t.kMedium:
            return kHitachiAc424FanMedium
        if speed == stdAc.fanspeed_t.kHigh:
            return kHitachiAc424FanHigh
        if speed == stdAc.fanspeed_t.kMax:
            return kHitachiAc424FanMax

        return kHitachiAc424FanAuto
    
    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kHitachiAc424Cool:
            return stdAc.opmode_t.kCool
        if mode == kHitachiAc424Heat:
            return stdAc.opmode_t.kHeat
        if mode == kHitachiAc424Dry:
            return stdAc.opmode_t.kDry
        if mode == kHitachiAc424Fan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kCool
    
    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kHitachiAc424FanMax:
            return stdAc.fanspeed_t.kMax
        if speed == kHitachiAc424FanHigh:
            return stdAc.fanspeed_t.kHigh
        if speed == kHitachiAc424FanMedium:
            return stdAc.fanspeed_t.kMedium
        if speed == kHitachiAc424FanLow:
            return stdAc.fanspeed_t.kLow
        if speed == kHitachiAc424FanMin:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()

        result.protocol = decode_type_t.HITACHI_AC424
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwingVToggle() else stdAc.swingv_t.kOff
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.turbo = False
        result.clean = False
        result.econo = False
        result.filter = False
        result.light = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            0,
            kHitachiAc424Cool,
            kHitachiAc424Heat,
            kHitachiAc424Dry,
            kHitachiAc424Fan
        )
        result += addTempToString(self.getTemp())
        result += addIntToString(self.getFan(), kFanStr)
        result += kSpaceLBraceStr

        speed = self.getFan()
        if speed == kHitachiAc424FanAuto:
            result += kAutoStr
        elif speed == kHitachiAc424FanMax:
            result += kMaxStr
        elif speed == kHitachiAc424FanHigh:
            result += kHighStr
        elif speed == kHitachiAc424FanMedium:
            result += kMedStr
        elif speed == kHitachiAc424FanLow:
            result += kLowStr
        elif speed == kHitachiAc424FanMin:
            result += kMinStr
        else:
            result += kUnknownStr

        result += ')'
        result += addBoolToString(self.getSwingVToggle(), kSwingVToggleStr)
        result += addIntToString(self.getButton(), kButtonStr)
        result += kSpaceLBraceStr
        button = self.getButton()
        if button == kHitachiAc424ButtonPowerMode:
            result += kPowerStr
            result += '/'
            result += kModeStr
        elif button == kHitachiAc424ButtonFan:
            result += kFanStr
        elif button == kHitachiAc424ButtonSwingV:
            result += kSwingVStr
        elif button == kHitachiAc424ButtonTempDown:
            result += kTempDownStr
        elif button == kHitachiAc424ButtonTempUp:
            result += kTempUpStr
        else:
            result += kUnknownStr

        result += ')'
        return result


# Send a Hitachi A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kHitachiAcStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: ALPHA / Untested.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/417
def sendHitachiAC(data, nbytes, repeat):
    if nbytes < kHitachiAcStateLength:
        return  # Not enough bytes to send a proper message.

    sendGeneric(
        kHitachiAcHdrMark,
        kHitachiAcHdrSpace,
        kHitachiAcBitMark,
        kHitachiAcOneSpace,
        kHitachiAcBitMark,
        kHitachiAcZeroSpace,
        kHitachiAcBitMark,
        kHitachiAcMinGap,
        data,
        nbytes,
        38,
        True,
        repeat,
        50
    )


# Send a Hitachi A/C 13-byte message.
#
# For devices:
#  Hitachi A/C Series VI (Circa 2007) / Remote: LT0541-HTA
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kHitachiAc1StateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: BETA / Appears to work.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/453
#   Basically the same as sendHitatchiAC() except different size and header.
def sendHitachiAC1(data, nbytes, repeat):
    if nbytes < kHitachiAc1StateLength:
        return  # Not enough bytes to send a proper message.

    sendGeneric(
        kHitachiAc1HdrMark,
        kHitachiAc1HdrSpace,
        kHitachiAcBitMark,
        kHitachiAcOneSpace,
        kHitachiAcBitMark,
        kHitachiAcZeroSpace,
        kHitachiAcBitMark,
        kHitachiAcMinGap,
        data,
        nbytes,
        kHitachiAcFreq,
        True,
        repeat,
        kDutyDefault
    )


# Send a Hitachi A/C 53-byte message.
#
# For devices:
#  Hitachi A/C Series VI (Circa 2007) / Remote: LT0541-HTA
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kHitachiAc2StateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: BETA / Appears to work.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/417
#   Basically the same as sendHitatchiAC() except different size.
def sendHitachiAC2(data, nbytes, repeat):
    if nbytes < kHitachiAc2StateLength:
        return  # Not enough bytes to send a proper message.

    sendHitachiAC(data, nbytes, repeat)


# Decode the supplied Hitachi A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect.
#            Typically kHitachiAcBits, kHitachiAc1Bits, kHitachiAc2Bits
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Untested.
#
# Supported devices:
#  Hitachi A/C Series VI (Circa 2007) / Remote: LT0541-HTA
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/417
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/453
def decodeHitachiAC(results, nbits, strict):
    k_tolerance = _tolerance + 5
    if results.rawlen < 2 * nbits + kHeader + kFooter - 1:
        return False  # Can't possibly be a valid HitachiAC message.

    if strict and nbits not in (
        kHitachiAcBits,
        kHitachiAc1Bits,
        kHitachiAc2Bits
    ):
        return False  # Not strictly a Hitachi message.

    offset = kStartOffset

    if nbits == kHitachiAc1Bits:
        hmark = kHitachiAc1HdrMark
        hspace = kHitachiAc1HdrSpace
    else:
        hmark = kHitachiAcHdrMark
        hspace = kHitachiAcHdrSpace

    # Match Header + Data + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        hmark,
        hspace,
        kHitachiAcBitMark,
        kHitachiAcOneSpace,
        kHitachiAcBitMark,
        kHitachiAcZeroSpace,
        kHitachiAcBitMark,
        kHitachiAcMinGap,
        True,
        k_tolerance
    ):
        return False

    # Compliance
    if (
        strict and
        nbits / 8 == kHitachiAcStateLength and
        not IRHitachiAc.validChecksum(results.state, kHitachiAcStateLength)
    ):
        return False

    # Success
    if nbits == kHitachiAc1Bits:
        results.decode_type = HITACHI_AC1

    elif nbits == kHitachiAc2Bits:
        results.decode_type = HITACHI_AC2

    else:
        results.decode_type = HITACHI_AC

    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True


# Send HITACHI_AC424 messages
#
# Note: This protocol is almost exactly the same as HitachiAC2 except this
#       variant has a leader section as well, and subtle timing differences.
#       It is also in LSBF order (per byte), rather than MSBF order.
#
# Args:
#   data: An array of bytes containing the IR command.
#         It is assumed to be in LSBF order for this code.
#   nbytes: Nr. of bytes of data in the array. (>=kHitachiAc424StateLength)
#   repeat: Nr. of times the message is to be repeated.
#
# Status: STABLE / Reported as working.
def sendHitachiAc424(data, nbytes, repeat):
    enableIROut(kHitachiAcFreq)
    for _ in range(repeat + 1):
        # Leader
        mark(kHitachiAc424LdrMark)
        space(kHitachiAc424LdrSpace)
        # Header + Data + Footer
        sendGeneric(
            kHitachiAc424HdrMark,
            kHitachiAc424HdrSpace,
            kHitachiAc424BitMark,
            kHitachiAc424OneSpace,
            kHitachiAc424BitMark,
            kHitachiAc424ZeroSpace,
            kHitachiAc424BitMark,
            kHitachiAcMinGap,
            data,
            nbytes,  # Bytes
            kHitachiAcFreq,
            False,
            kNoRepeat,
            kDutyDefault
        )


# Decode the supplied Hitachi 424 bit A/C message.
#
# Note: This protocol is almost exactly the same as HitachiAC2 except this
#       variant has a leader section as well, and subtle timing differences.
#       It is also in LSBF order (per byte), rather than MSBF order.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kHitachiAc424Bits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Reported as working.
#
# Supported devices:
#  Hitachi Shirokumakun / AC Model: RAS-AJ25H / AC Remote Model: RAR-8P2
#  Manual (Japanese):
#    https:#kadenfan.hitachi.co.jp/support/raj/item/docs/ras_aj22h_a_tori.pdf
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/973
def decodeHitachiAc424(results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader + kHeader + kFooter - 1:
        return False  # Too short a message to match.

    if strict and nbits != kHitachiAc424Bits:
        return False

    offset = kStartOffset

    # Leader
    offset += 1

    if not matchMark(results.rawbuf[offset], kHitachiAc424LdrMark):
        return False

    offset += 1
    if not matchSpace(results.rawbuf[offset], kHitachiAc424LdrSpace):
        return False

    # Header + Data + Footer
    used = matchGeneric(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        kHitachiAc424HdrMark,
        kHitachiAc424HdrSpace,
        kHitachiAc424BitMark,
        kHitachiAc424OneSpace,
        kHitachiAc424BitMark,
        kHitachiAc424ZeroSpace,
        kHitachiAc424BitMark,
        kHitachiAcMinGap,
        True,
        kUseDefTol,
        0,
        False
    )

    if used == 0:
        return False  # We failed to find any data.

    # Success
    results.decode_type = decode_type_t.HITACHI_AC424
    results.bits = nbits
    return True
