# -*- coding: utf-8 -*-


# Copyright 2017 Ville Skyttä (scop)
# Copyright 2017, 2018 David Conran
#
# Code to emulate Gree protocol compatible HVAC devices.
# Should be compatible with:
# * Heat pumps carrying the "Ultimate" brand name.
# * EKOKAI air conditioners.
#

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *
from .ir_Kelvinator import *
# Constants
# Ref: https:#github.com/ToniA/arduino-heatpumpir/blob/master/GreeHeatpumpIR.h
kGreeHdrMark = 9000
kGreeHdrSpace = 4500  # See #684 and real example in unit tests
kGreeBitMark = 620
kGreeOneSpace = 1600
kGreeZeroSpace = 540
kGreeMsgSpace = 19000
kGreeBlockFooter = 0b010
kGreeBlockFooterBits = 3

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addModelToString = irutils.addModelToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
minsToString = irutils.minsToString
setBit = irutils.setBit
setBits = irutils.setBits

# Gree A/C
#
# Supports:
#   Brand: Ultimate,  Model: Heat Pump
#   Brand: EKOKAI,  Model: A/C
#   Brand: RusClimate,  Model: EACS/I-09HAR_X/N3 A/C
#   Brand: RusClimate,  Model: YAW1F remote
#   Brand: Green,  Model: YBOFB remote
#   Brand: Green,  Model: YBOFB2 remote

# Constants

kGreeAuto = 0
kGreeCool = 1
kGreeDry = 2
kGreeFan = 3
kGreeHeat = 4

# Byte 0
kGreePower1Offset = 3
kGreeFanOffset = 4
kGreeFanSize = 2  # Bits
kGreeFanAuto = 0
kGreeFanMin = 1
kGreeFanMed = 2
kGreeFanMax = 3
kGreeSwingAutoOffset = 6
kGreeSleepOffset = 7
# Byte 1
kGreeTempSize = 4
kGreeMinTemp = 16  # Celsius
kGreeMaxTemp = 30  # Celsius
kGreeTimerHalfHrOffset = 4
kGreeTimerTensHrOffset = 5
kGreeTimerTensHrSize = 2  # Bits
kGreeTimerMax = 24 * 60
kGreeTimerEnabledOffset = 7

# Byte 2
kGreeTimerHoursOffset = 0
kGreeTimerHoursSize = 4  # Bits
kGreeTurboOffset = 4
kGreeLightOffset = 5
# This might not be used. See #814
kGreePower2Offset = 6
kGreeXfanOffset = 7
# Byte 4
kGreeSwingSize = 4  # Bits
kGreeSwingLastPos = 0b0000
kGreeSwingAuto = 0b0001
kGreeSwingUp = 0b0010
kGreeSwingMiddleUp = 0b0011
kGreeSwingMiddle = 0b0100
kGreeSwingMiddleDown = 0b0101
kGreeSwingDown = 0b0110
kGreeSwingDownAuto = 0b0111
kGreeSwingMiddleAuto = 0b1001
kGreeSwingUpAuto = 0b1011
# byte 5
kGreeIFeelOffset = 2
kGreeWiFiOffset = 6

# Legacy defines.
# define GREE_AUTO kGreeAuto
# define GREE_COOL kGreeCool
# define GREE_DRY kGreeDry
# define GREE_FAN kGreeFan
# define GREE_HEAT kGreeHeat
# define GREE_MIN_TEMP kGreeMinTemp
# define GREE_MAX_TEMP kGreeMaxTemp
# define GREE_FAN_MAX kGreeFanMax
# define GREE_SWING_LAST_POS kGreeSwingLastPos
# define GREE_SWING_AUTO kGreeSwingAuto
# define GREE_SWING_UP kGreeSwingUp
# define GREE_SWING_MIDDLE_UP kGreeSwingMiddleUp
# define GREE_SWING_MIDDLE kGreeSwingMiddle
# define GREE_SWING_MIDDLE_DOWN kGreeSwingMiddleDown
# define GREE_SWING_DOWN kGreeSwingDown
# define GREE_SWING_DOWN_AUTO kGreeSwingDownAuto
# define GREE_SWING_MIDDLE_AUTO kGreeSwingMiddleAuto
# define GREE_SWING_UP_AUTO kGreeSwingUpAuto


# Classes
class IRGreeAC(object):

    def __init__(
        self,
        pin,
        model=gree_ac_remote_model_t.YAW1F,
        inverted=False,
        use_modulation=True
    ):

        # The state of the IR remote in IR code form.
        self.remote_state = [0x0] * kGreeStateLength
        self._model = None
        self._irsend = IRsend(pin, inverted, use_modulation)

        self.stateReset()
        self.setModel(model)

    def stateReset(self):
        # This resets to a known-good state to Power Off, Fan Auto, Mode Auto, 25C.
        self.remote_state = [0x0] * kGreeStateLength
        remote_state[1] = 0x09
        remote_state[2] = 0x20
        remote_state[3] = 0x50
        remote_state[5] = 0x20
        remote_state[7] = 0x50

    def send(self, repeat=kGreeDefaultRepeat):
        self.fixup()  # Ensure correct settings before sending.
        self._irsend.sendGree(self.remote_state, kGreeStateLength, repeat)

    def calibrate(self):
        return self._irsend.calibrate()

    def begin(self):
        self._irsend.begin()

    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def setModel(self, model):
        if model in (
            gree_ac_remote_model_t.YAW1F,
            gree_ac_remote_model_t.YBOFB
        ):
            self._model = model
        else:
            self.setModel(gree_ac_remote_model_t.YAW1F)

    def getModel(self):
        return self._model

    def setPower(self, on):
        setBit(self.remote_state[0], kGreePower1Offset, on)
        # May not be needed. See #814
        setBit(
            self.remote_state[2],
            kGreePower2Offset,
            on and _model != gree_ac_remote_model_t.YBOFB
        )

    def getPower(self):
        #  See #814. Not checking/requiring: (remote_state[2] & kGreePower2Mask)
        return GETBIT8(self.remote_state[0], kGreePower1Offset)

    def setTemp(self, temp):
        # Set the temp. in deg C
        new_temp = max(kGreeMinTemp, temp)
        new_temp = min(kGreeMaxTemp, new_temp)

        if self.getMode() == kGreeAuto:
            new_temp = 25

        setBits(
            self.remote_state[1],
            kLowNibble,
            kGreeTempSize,
            new_temp - kGreeMinTemp
        )

    def getTemp(self):
        # Return the set temp. in deg C
        return GETBITS8(self.remote_state[1], kLowNibble, kGreeTempSize) + kGreeMinTemp

    def setFan(self, speed):
        # Set the speed of the fan, 0-3, 0 is auto, 1-3 is the speed

        fan = min(kGreeFanMax, speed)  # Bounds check
        if self.getMode() == kGreeDry:
            fan = 1  # DRY mode is always locked to fan 1.

        # Set the basic fan values.
        setBits(self.remote_state[0], kGreeFanOffset, kGreeFanSize, fan)

    def getFan(self):
        return GETBITS8(self.remote_state[0], kGreeFanOffset, kGreeFanSize)

    def setMode(self, new_mode):
        mode = new_mode

        # AUTO is locked to 25C
        if mode == kGreeAuto:
            self.setTemp(25)
        # DRY always sets the fan to 1.
        elif mode == kGreeDry:
            self.setFan(1)
        elif mode not in (
            kGreeCool,
            kGreeFan,
            kGreeHeat
        ):
            # If we get an unexpected mode, default to AUTO.
            mode = kGreeAuto

        setBits(self.remote_state[0], kLowNibble, kModeBitsSize, mode)

    def getMode(self):
        return GETBITS8(self.remote_state[0], kLowNibble, kModeBitsSize)

    def setLight(self, on):
        setBit(self.remote_state[2], kGreeLightOffset, on)

    def getLight(self):
        return GETBIT8(self.remote_state[2], kGreeLightOffset)

    def setXFan(self, on):
        setBit(self.remote_state[2], kGreeXfanOffset, on)

    def getXFan(self):
        return GETBIT8(self.remote_state[2], kGreeXfanOffset)

    def setSleep(self, on):
        setBit(self.remote_state[0], kGreeSleepOffset, on)

    def getSleep(self):
        return GETBIT8(self.remote_state[0], kGreeSleepOffset)

    def setTurbo(self, on):
        setBit(self.remote_state[2], kGreeTurboOffset, on)

    def getTurbo(self):
        return GETBIT8(self.remote_state[2], kGreeTurboOffset)

    def setIFeel(self, on):
        setBit(self.remote_state[5], kGreeIFeelOffset, on)

    def getIFeel(self):
        return GETBIT8(self.remote_state[5], kGreeIFeelOffset)

    def setWiFi(self, on):
        setBit(self.remote_state[5], kGreeWiFiOffset, on)

    def getWiFi(self):
        return GETBIT8(self.remote_state[5], kGreeWiFiOffset)

    def setSwingVertical(self, automatic, position):
        setBit(self.remote_state[0], kGreeSwingAutoOffset, automatic)
        new_position = position
        if not automatic:
            if position not in (
                kGreeSwingUp,
                kGreeSwingMiddleUp,
                kGreeSwingMiddle,
                kGreeSwingMiddleDown,
                kGreeSwingDown
            ):
                new_position = kGreeSwingLastPos
        else:
            if position not in (
                kGreeSwingAuto,
                kGreeSwingDownAuto,
                kGreeSwingMiddleAuto,
                kGreeSwingUpAuto
            ):
                new_position = kGreeSwingAuto\

        setBits(self.remote_state[4], kLowNibble, kGreeSwingSize, new_position)

    def getSwingVerticalAuto(self):
        return GETBIT8(self.remote_state[0], kGreeSwingAutoOffset)

    def getSwingVerticalPosition(self):
        return GETBITS8(self.remote_state[4], kLowNibble, kGreeSwingSize)

    def getTimer(self):
        # Returns the number of minutes the timer is set for.
        hrs = irutils.bcdToUint8(
            (GETBITS8(self.remote_state[1], kGreeTimerTensHrOffset, kGreeTimerTensHrSize) << kNibbleSize) |
            GETBITS8(self.remote_state[2], kGreeTimerHoursOffset, kGreeTimerHoursSize)
        )
        return hrs * 60 + (30 if GETBIT8(self.remote_state[1], kGreeTimerHalfHrOffset) else 0)

    def setTimer(self, minutes):
        # Set the A/C's timer to turn off in X many minutes.
        # Stores time internally in 30 min units.
        #   e.g. 5 mins means 0 (& Off), 95 mins is  90 mins (& On). Max is 24 hours.
        #
        # Args:
        #   minutes: The number of minutes the timer should be set for.
        mins = min(kGreeTimerMax, minutes)  # Bounds check.
        setTimerEnabled(mins >= 30)  # Timer is enabled when >= 30 mins.
        hours = mins / 60
        # Set the half hour bit.
        setBit(self.remote_state[1], kGreeTimerHalfHrOffset, not ((mins % 60) < 30))
        # Set the "tens" digit of hours.
        setBits(self.remote_state[1], kGreeTimerTensHrOffset, kGreeTimerTensHrSize, hours / 10)
        # Set the "units" digit of hours.
        setBits(self.remote_state[2], kGreeTimerHoursOffset, kGreeTimerHoursSize, hours % 10)

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kGreeCool
        if mode == stdAc.opmode_t.kHeat:
            return kGreeHeat
        if mode == stdAc.opmode_t.kDry:
            return kGreeDry
        if mode == stdAc.opmode_t.kFan:
            return kGreeFan

        return kGreeAuto

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed == stdAc.fanspeed_t.kMin:
            return kGreeFanMin
        if speed in (
            stdAc.fanspeed_t.kLow,
            stdAc.fanspeed_t.kMedium
        ):
            return kGreeFanMax - 1
        if speed in (
            stdAc.fanspeed_t.kHigh,
            stdAc.fanspeed_t.kMax
        ):
            return kGreeFanMax

        return kGreeFanAuto

    @staticmethod
    def convertSwingV(swingv):
        # Convert a standard A/C Vertical Swing into its native version.
        if swingv == stdAc.swingv_t.kHighest:
            return kGreeSwingUp
        if swingv == stdAc.swingv_t.kHigh:
            return kGreeSwingMiddleUp
        if swingv == stdAc.swingv_t.kMiddle:
            return kGreeSwingMiddle
        if swingv == stdAc.swingv_t.kLow:
            return kGreeSwingMiddleDown
        if swingv == stdAc.swingv_t.kLowest:
            return kGreeSwingDown

        return kGreeSwingAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kGreeCool:
            return stdAc.opmode_t.kCool
        if mode == kGreeHeat:
            return stdAc.opmode_t.kHeat
        if mode == kGreeDry:
            return stdAc.opmode_t.kDry
        if mode == kGreeFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kGreeFanMax:
            return stdAc.fanspeed_t.kMax
        if speed == kGreeFanMax - 1:
            return stdAc.fanspeed_t.kMedium
        if speed == kGreeFanMin:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    @staticmethod
    def toCommonSwingV(pos):
        # Convert a native vertical swing to it's common equivalent.
        if pos == kGreeSwingUp:
            return stdAc.swingv_t.kHighest
        if pos == kGreeSwingMiddleUp:
            return stdAc.swingv_t.kHigh
        if pos == kGreeSwingMiddle:
            return stdAc.swingv_t.kMiddle
        if pos == kGreeSwingMiddleDown:
            return stdAc.swingv_t.kLow
        if pos == kGreeSwingDown:
            return stdAc.swingv_t.kLowest

        return stdAc.swingv_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.GREE
        result.model = self.getModel()
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())

        if self.getSwingVerticalAuto():
            result.swingv = stdAc.swingv_t.kAuto
        else:
            result.swingv = self.toCommonSwingV(self.getSwingVerticalPosition())

        result.turbo = self.getTurbo()
        result.light = self.getLight()
        result.clean = self.getXFan()
        result.sleep = 0 if self.getSleep() else -1
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.econo = False
        result.filter = False
        result.beep = False
        result.clock = -1
        return result

    def getRaw(self):
        self.fixup()  # Ensure correct settings before sending.
        return self.remote_state

    def setRaw(self, new_code):
        self.remote_state = new_code
        # We can only detect the difference between models when the power is on.
        if self.getPower():
            if GETBIT8(self.remote_state[2], kGreePower2Offset):
                self._model = gree_ac_remote_model_t.YAW1F
        else:
            self._model = gree_ac_remote_model_t.YBOFB

    @staticmethod
    def validChecksum(state, length=kGreeStateLength):
        # Verify the checksum is valid for a given state.
        # Args:
        #   state:  The array to verify the checksum of.
        #   length: The size of the state.
        # Returns:
        #   A boolean.

        # Top 4 bits of the last byte in the state is the state's checksum.
        return GETBITS8(state[length - 1], kHighNibble, kNibbleSize) == IRKelvinatorAC.calcBlockChecksum(state, length)

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        result += addModelToString(decode_type_t.GREE, self.getModel(), False)
        result += addBoolToString(self.getPower(), kPowerStr)
        result += addModeToString(self.getMode(), kGreeAuto, kGreeCool, kGreeHeat, kGreeDry, kGreeFan)
        result += addTempToString(self.getTemp())
        result += addFanToString(self.getFan(), kGreeFanMax, kGreeFanMin, kGreeFanAuto, kGreeFanAuto, kGreeFanMed)
        result += addBoolToString(self.getTurbo(), kTurboStr)
        result += addBoolToString(self.getIFeel(), kIFeelStr)
        result += addBoolToString(self.getWiFi(), kWifiStr)
        result += addBoolToString(self.getXFan(), kXFanStr)
        result += addBoolToString(self.getLight(), kLightStr)
        result += addBoolToString(self.getSleep(), kSleepStr)
        result += addLabeledString(kAutoStr if self.getSwingVerticalAuto() else kManualStr, kSwingVModeStr)
        result += addIntToString(self.getSwingVerticalPosition(), kSwingVStr)
        result += kSpaceLBraceStr
        pos = self.getSwingVerticalPosition()
        if pos == kGreeSwingLastPos:
            result += kLastStr
        elif pos == kGreeSwingAuto:
            result += kAutoStr
        else:
            result += kUnknownStr

        result += ')'
        result += addLabeledString(minsToString(self.getTimer()) if self.getTimerEnabled() else kOffStr, kTimerStr)
        return result

    def checksum(self, length=kGreeStateLength):
        # Gree uses the same checksum alg. as Kelvinator's block checksum.
        setBits(
            self.remote_state[length - 1],
            kHighNibble,
            kNibbleSize,
            IRKelvinatorAC.calcBlockChecksum(self.remote_state, length)
        )

    def fixup(self):
        self.setPower(self.getPower())  # Redo the power bits as they differ between models.
        self.checksum()  # Calculate the checksums

    def setTimerEnabled(self, on):
        setBit(self.remote_state[1], kGreeTimerEnabledOffset, on)

    def getTimerEnabled(self):
        return GETBIT8(self.remote_state[1], kGreeTimerEnabledOffset)


# Send a Gree Heat Pump message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kGreeStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: ALPHA / Untested.
#
# Ref:
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/GreeHeatpumpIR.cpp
def sendGree(data, nbytes, repeat):
    if nbytes < kGreeStateLength:
        return  # Not enough bytes to send a proper message.

    for _ in range(repeat + 1):
        # Block #1
        sendGeneric(
            kGreeHdrMark,
            kGreeHdrSpace,
            kGreeBitMark,
            kGreeOneSpace,
            kGreeBitMark,
            kGreeZeroSpace,
            0,
            0,  # No Footer.
            data,
            4,
            38,
            False,
            0,
            50
        )

        # Footer #1
        sendGeneric(
            0,
            0,  # No Header
            kGreeBitMark,
            kGreeOneSpace,
            kGreeBitMark,
            kGreeZeroSpace,
            kGreeBitMark,
            kGreeMsgSpace,
            0b010,
            3,
            38,
            False,
            0,
            50
        )

        # Block #2
        sendGeneric(
            0,
            0,  # No Header for Block #2
            kGreeBitMark,
            kGreeOneSpace,
            kGreeBitMark,
            kGreeZeroSpace,
            kGreeBitMark,
            kGreeMsgSpace,
            data + 4,
            nbytes - 4,
            38,
            False,
            0,
            50
        )


# Send a Gree Heat Pump message.
#
# Args:
#   data: The raw message to be sent.
#   nbits: Nr. of bits of data in the message. (Default is kGreeBits)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: ALPHA / Untested.
#
# Ref:
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/GreeHeatpumpIR.cpp
def sendGreeHeatPump(data, nbits, repeat):
    if nbits != kGreeBits:
        return  # Wrong nr. of bits to send a proper message.

    # Set IR carrier frequency
    enableIROut(38)

    for _ in range(repeat + 1):
        # Header
        mark(kGreeHdrMark)
        space(kGreeHdrSpace)

        # Data
        for i in range(0, nbits, 8):
            sendData(
                kGreeBitMark,
                kGreeOneSpace,
                kGreeBitMark,
                kGreeZeroSpace,
                (data >> (nbits - i)) & 0xFF,
                8,
                False
            )
            if i == nbits / 2:
                # Send the mid-message Footer.
                sendData(
                    kGreeBitMark,
                    kGreeOneSpace,
                    kGreeBitMark,
                    kGreeZeroSpace,
                    0b010,
                    3
                )
            mark(kGreeBitMark)
            space(kGreeMsgSpace)

        # Footer
        mark(kGreeBitMark)
        space(kGreeMsgSpace)


# Decode the supplied Gree message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kGreeBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Untested.
def decodeGree(results, nbits, strict):
    if results.rawlen < 2 * (nbits + kGreeBlockFooterBits) + (kHeader + kFooter + 1):
        return False  # Can't possibly be a valid Gree message.

    if strict and nbits != kGreeBits:
        return False  # Not strictly a Gree message.

    offset = kStartOffset

    # There are two blocks back-to-back in a full Gree IR message
    # sequence.

    # Header + Data Block #1 (32 bits)
    used = matchGeneric(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits / 2,
        kGreeHdrMark,
        kGreeHdrSpace,
        kGreeBitMark,
        kGreeOneSpace,
        kGreeBitMark,
        kGreeZeroSpace,
        0,
        0,
        False,
        _tolerance,
        kMarkExcess,
        False
    )
    if used == 0:
        return False
    offset += used

    # Block #1 footer (3 bits, B010)
    data_result = matchData(
        results.rawbuf[offset],
        kGreeBlockFooterBits,
        kGreeBitMark,
        kGreeOneSpace,
        kGreeBitMark,
        kGreeZeroSpace,
        _tolerance,
        kMarkExcess,
        False
    )
    if data_result.success is False:
        return False

    if data_result.data != kGreeBlockFooter:
        return False
    offset += data_result.used

    # Inter-block gap + Data Block #2 (32 bits) + Footer
    if not matchGeneric(
        results.rawbuf + offset,
        results.state + 4,
        results.rawlen - offset,
        nbits / 2,
        kGreeBitMark,
        kGreeMsgSpace,
        kGreeBitMark,
        kGreeOneSpace,
        kGreeBitMark,
        kGreeZeroSpace,
        kGreeBitMark,
        kGreeMsgSpace, True,
        _tolerance,
        kMarkExcess,
        False
    ):
        return False

    # Compliance
    if strict and not IRGreeAC.validChecksum(results.state):
        return False

    # Success
    results.decode_type = GREE
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True
