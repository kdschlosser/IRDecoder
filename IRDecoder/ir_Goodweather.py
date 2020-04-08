# -*- coding: utf-8 -*-

# Copyright 2019 ribeirodanielf
# Copyright 2019 David Conran
#
# Code to emulate Goodweather protocol compatible HVAC devices.
# Should be compatible with:
# * ZH/JT-03 remote control
#

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits

# Supports:
#   Brand: Goodweather,  Model: ZH/JT-03 remote

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/697

# Constants

# Timing
kGoodweatherBitMark = 580
kGoodweatherOneSpace = 580
kGoodweatherZeroSpace = 1860
kGoodweatherHdrMark = 6820
kGoodweatherHdrSpace = 6820
kGoodweatherExtraTolerance = 12  # +12% extra

# Masks
kGoodweatherBitLight = 8
kGoodweatherBitTurbo = kGoodweatherBitLight + 3  # 11
kGoodweatherBitCommand = kGoodweatherBitTurbo + 5  # 16
kGoodweatherCommandSize = 4  # Bits
kGoodweatherBitSleep = kGoodweatherBitCommand + 8  # 24
kGoodweatherBitPower = kGoodweatherBitSleep + 1  # 25
kGoodweatherBitSwing = kGoodweatherBitPower + 1  # 26
kGoodweatherSwingSize = 2  # Bits
kGoodweatherBitAirFlow = kGoodweatherBitSwing + 2  # 28
kGoodweatherBitFan = kGoodweatherBitAirFlow + 1  # 29
kGoodweatherFanSize = 2  # Bits
kGoodweatherBitTemp = kGoodweatherBitFan + 3  # 32
kGoodweatherTempSize = 4  # Bits
kGoodweatherBitMode = kGoodweatherBitTemp + 5  # 37
kGoodweatherBitEOF = kGoodweatherBitMode + 3  # 40
kGoodweatherEOFMask = 0xFF << kGoodweatherBitEOF

# Modes
kGoodweatherAuto = 0b000
kGoodweatherCool = 0b001
kGoodweatherDry = 0b010
kGoodweatherFan = 0b011
kGoodweatherHeat = 0b100
# Swing
kGoodweatherSwingFast = 0b00
kGoodweatherSwingSlow = 0b01
kGoodweatherSwingOff = 0b10
# Fan Control
kGoodweatherFanAuto = 0b00
kGoodweatherFanHigh = 0b01
kGoodweatherFanMed = 0b10
kGoodweatherFanLow = 0b11
# Temperature
kGoodweatherTempMin = 16  # Celsius
kGoodweatherTempMax = 31  # Celsius
# Commands
kGoodweatherCmdPower = 0x00
kGoodweatherCmdMode = 0x01
kGoodweatherCmdUpTemp = 0x02
kGoodweatherCmdDownTemp = 0x03
kGoodweatherCmdSwing = 0x04
kGoodweatherCmdFan = 0x05
kGoodweatherCmdTimer = 0x06
kGoodweatherCmdAirFlow = 0x07
kGoodweatherCmdHold = 0x08
kGoodweatherCmdSleep = 0x09
kGoodweatherCmdTurbo = 0x0A
kGoodweatherCmdLight = 0x0B
# PAD EOF
kGoodweatherStateInit = 0xD50000000000


# Classes
class IRGoodweatherAc(object):
    def __init__(self, pin, inverted=False, use_modulation=True):
        # The state of the IR remote in IR code form.
        self.remote = 0
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.stateReset()
        
    def stateReset(self):
        self.remote = kGoodweatherStateInit
  
    def send(self, repeat=kGoodweatherMinRepeat):
        self._irsend.sendGoodweather(self.remote, kGoodweatherBits, repeat)
  
    def calibrate(self):
        return self._irsend.calibrate()
  
    def begin(self):
        self._irsend.begin()
        
    def on(self):
        self.setPower(True)
    
    def off(self):
        self.setPower(False)
        
    def setPower(self, on):
        self.setCommand(kGoodweatherCmdPower)
        setBit(self.remote, kGoodweatherBitPower, on)
    
    def getPower(self):
        return GETBIT64(self.remote, kGoodweatherBitPower)
    
    def setTemp(self, temp):
        # Set the temp. in deg C
        new_temp = max(kGoodweatherTempMin, temp)
        new_temp = min(kGoodweatherTempMax, new_temp)
        if new_temp > self.getTemp():
            self.setCommand(kGoodweatherCmdUpTemp)
        elif new_temp < self.getTemp():
            self.setCommand(kGoodweatherCmdDownTemp)
          
        setBits(
            self.remote, 
            kGoodweatherBitTemp, 
            kGoodweatherTempSize, 
            new_temp - kGoodweatherTempMin
        )
        
    def getTemp(self):
        # Return the set temp. in deg C
        return GETBITS64(
            self.remote, 
            kGoodweatherBitTemp, 
            kGoodweatherTempSize
        ) + kGoodweatherTempMin
    
    def setFan(self, speed):
        # Set the speed of the fan
        if speed in (
            kGoodweatherFanAuto,
            kGoodweatherFanLow,
            kGoodweatherFanMed,
            kGoodweatherFanHigh
        ):
            self.setCommand(kGoodweatherCmdFan)
            setBits(self.remote, kGoodweatherBitFan, kGoodweatherFanSize, speed)
        else:
            self.setFan(kGoodweatherFanAuto)
    
    def getFan(self):
        return GETBITS64(self.remote, kGoodweatherBitFan, kGoodweatherFanSize)
  
    def setMode(self, mode):
        if mode in (
            kGoodweatherAuto,
            kGoodweatherDry,
            kGoodweatherCool,
            kGoodweatherFan,
            kGoodweatherHeat
        ):
            self.setCommand(kGoodweatherCmdMode)
            setBits(self.remote, kGoodweatherBitMode, kModeBitsSize, mode)
        else:
            # If we get an unexpected mode, default to AUTO.
            self.setMode(kGoodweatherAuto)
  
    def getMode(self):
        return GETBITS64(self.remote, kGoodweatherBitMode, kModeBitsSize)
  
    def setSwing(self, speed):
        if speed in (
            kGoodweatherSwingOff,
            kGoodweatherSwingSlow,
            kGoodweatherSwingFast
        ):
            self.setCommand(kGoodweatherCmdSwing)
            setBits(self.remote, kGoodweatherBitSwing, kGoodweatherSwingSize, speed)
            
        else:
            self.setSwing(kGoodweatherSwingOff)
    
    def getSwing(self):
        return GETBITS64(self.remote, kGoodweatherBitSwing, kGoodweatherSwingSize)
        
    def setSleep(self, toggle):
        self.setCommand(kGoodweatherCmdSleep)
        setBit(self.remote, kGoodweatherBitSleep, toggle)
  
    def getSleep(self):
        return GETBIT64(self.remote, kGoodweatherBitSleep)

    def setTurbo(self, toggle):
        self.setCommand(kGoodweatherCmdTurbo)
        setBit(self.remote, kGoodweatherBitTurbo, toggle)
  
    def getTurbo(self):
        return GETBIT64(self.remote, kGoodweatherBitTurbo)

    def setLight(self, toggle):
        self.setCommand(kGoodweatherCmdLight)
        setBit(self.remote, kGoodweatherBitLight, toggle)
  
    def getLight(self):
        return GETBIT64(self.remote, kGoodweatherBitLight)
        
    def setCommand(self, cmd):
        if cmd <= kGoodweatherCmdLight:
            setBits(self.remote, kGoodweatherBitCommand, kGoodweatherCommandSize, cmd)
      
    def getCommand(self):
        return GETBITS64(self.remote, kGoodweatherBitCommand, kGoodweatherCommandSize)

    def getRaw(self):
        return self.remote
    
    def setRaw(self, state):
        self.remote = state

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool: 
            return kGoodweatherCool
        if mode == stdAc.opmode_t.kHeat: 
            return kGoodweatherHeat
        if mode == stdAc.opmode_t.kDry: 
            return kGoodweatherDry
        if mode == stdAc.opmode_t.kFan:  
            return kGoodweatherFan
            
        return kGoodweatherAuto
    
    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):   
            return kGoodweatherFanLow    
        if speed == stdAc.fanspeed_t.kMedium: 
            return kGoodweatherFanMed
        if speed in (
            stdAc.fanspeed_t.kHigh,
            stdAc.fanspeed_t.kMax
        ):
            return kGoodweatherFanHigh
            
        return kGoodweatherFanAuto
  
    @staticmethod
    def convertSwingV(swingv):
        # Convert a standard A/C Vertical Swing into its native version.
        if swingv in (
            stdAc.swingv_t.kHighest,
            stdAc.swingv_t.kHigh,
            stdAc.swingv_t.kMiddle
        ): 
            return kGoodweatherSwingFast
        if swingv in (
            stdAc.swingv_t.kLow,
            stdAc.swingv_t.kLowest,
            stdAc.swingv_t.kAuto
        ):
            return kGoodweatherSwingSlow
            
        return kGoodweatherSwingOff

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kGoodweatherCool: 
            return stdAc.opmode_t.kCool
        if mode == kGoodweatherHeat:
            return stdAc.opmode_t.kHeat
        if mode == kGoodweatherDry:  
            return stdAc.opmode_t.kDry
        if mode == kGoodweatherFan:  
            return stdAc.opmode_t.kFan
            
        return stdAc.opmode_t.kAuto
    
    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kGoodweatherFanHigh: 
            return stdAc.fanspeed_t.kMax
        if speed == kGoodweatherFanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kGoodweatherFanLow:  
            return stdAc.fanspeed_t.kMin
            
        return stdAc.fanspeed_t.kAuto
  
    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.GOODWEATHER
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kOff if self.getSwing() == kGoodweatherSwingOff else stdAc.swingv_t.kAuto
        result.turbo = self.getTurbo()
        result.light = self.getLight()
        result.sleep = 0 if self.getSleep() else -1
        # Not supported.
        result.model = -1
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.econo = False
        result.filter = False
        result.clean = False
        result.beep = False
        result.clock = -1
        return result
  
    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(), 
            kGoodweatherAuto, 
            kGoodweatherCool,
            kGoodweatherHeat, 
            kGoodweatherDry, 
            kGoodweatherFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(), 
            kGoodweatherFanHigh, 
            kGoodweatherFanLow,
            kGoodweatherFanAuto, 
            kGoodweatherFanAuto,
            kGoodweatherFanMed
        )
        result += addLabeledString(kToggleStr if self.getTurbo() else "-", kTurboStr)
        result += addLabeledString(kToggleStr if self.getLight() else "-", kLightStr)
        result += addLabeledString(kToggleStr if self.getSleep() else "-", kSleepStr)
        result += addIntToString(self.getSwing(), kSwingStr)
        result += kSpaceLBraceStr
        swing = self.getSwing()
        
        if swing == kGoodweatherSwingFast:
            result += kFastStr
        elif swing == kGoodweatherSwingSlow:
            result += kSlowStr
        elif swing == kGoodweatherSwingOff:
            result += kOffStr
        else:
            result += kUnknownStr
            
        result += ')'
        result += addIntToString(self.getCommand(), kCommandStr)
        result += kSpaceLBraceStr
        
        cmd = self.getCommand()
        if cmd == kGoodweatherCmdPower:
            result += kPowerStr
        elif cmd == kGoodweatherCmdMode:
            result += kModeStr
        elif cmd == kGoodweatherCmdUpTemp:
            result += kTempUpStr
        elif cmd == kGoodweatherCmdDownTemp:
            result += kTempDownStr
        elif cmd == kGoodweatherCmdSwing:
            result += kSwingStr
        elif cmd == kGoodweatherCmdFan:
            result += kFanStr
        elif cmd == kGoodweatherCmdTimer:
            result += kTimerStr
        elif cmd == kGoodweatherCmdAirFlow:
            result += kAirFlowStr
        elif cmd == kGoodweatherCmdHold:
            result += kHoldStr
        elif cmd == kGoodweatherCmdSleep:
            result += kSleepStr
        elif cmd == kGoodweatherCmdTurbo:
            result += kTurboStr
        elif cmd == kGoodweatherCmdLight:
            result += kLightStr
        else:
            result += kUnknownStr
            
        result += ')'
        return result


# Send a Goodweather message.
#
# Args:
#   data: The raw message to be sent.
#   nbits: Nr. of bits of data in the message. (Default is kGoodweatherBits)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: ALPHA / Untested.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/697
def sendGoodweather(data, nbits, repeat):
    if nbits != kGoodweatherBits:
        return  # Wrong nr. of bits to send a proper message.
    # Set IR carrier frequency
    enableIROut(38)

    for _ in range(repeat + 1):
        # Header
        mark(kGoodweatherHdrMark)
        space(kGoodweatherHdrSpace)

        # Data
        for i in range(0, nbits, 8):
            chunk = (data >> i) & 0xFF  # Grab a byte at a time.
            chunk |= ~chunk << 8  # Prepend a inverted copy of the byte.
            
            sendData(
                kGoodweatherBitMark, 
                kGoodweatherOneSpace, 
                kGoodweatherBitMark, 
                kGoodweatherZeroSpace, 
                chunk, 
                16, 
                False
            )
    
        # Footer
        mark(kGoodweatherBitMark)
        space(kGoodweatherHdrSpace)
        mark(kGoodweatherBitMark)
        space(kDefaultMessageGap)


# Decode the supplied Goodweather message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kGoodweatherBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: ALPHA / Untested.
def decodeGoodweather(results, nbits, strict):
    if results.rawlen < 2 * (2 * nbits) + kHeader + 2 * kFooter - 1:
        return False  # Can't possibly be a valid Goodweather message.

    if strict and nbits != kGoodweatherBits:
        return False  # Not strictly a Goodweather message.

    dataSoFar = 0
    dataBitsSoFar = 0
    offset = kStartOffset

    # Header
    offset += 1
    if not matchMark(results.rawbuf[offset], kGoodweatherHdrMark):
        return False

    offset += 1
    if not matchSpace(results.rawbuf[offset], kGoodweatherHdrSpace):
        return False

    # Data
    while offset <= results.rawlen - 32 and dataBitsSoFar < nbits:
        dataBitsSoFar += 8

        # Read in a byte at a time.
        # Normal first.
        data_result = matchData(
            results.rawbuf[offset],
            8,
            kGoodweatherBitMark,
            kGoodweatherOneSpace,
            kGoodweatherBitMark,
            kGoodweatherZeroSpace,
            _tolerance + kGoodweatherExtraTolerance,
            kMarkExcess,
            False
        )
        if data_result.success is False:
            return False

        offset += data_result.used
        data = data_result.data
        # Then inverted.
        data_result = matchData(
            results.rawbuf[offset],
            8,
            kGoodweatherBitMark,
            kGoodweatherOneSpace,
            kGoodweatherBitMark,
            kGoodweatherZeroSpace,
            _tolerance + kGoodweatherExtraTolerance,
            kMarkExcess,
            False
        )
        if data_result.success is False:
            return False

        offset += data_result.used
        inverted = data_result.data

        if data != (inverted ^ 0xFF):
            return False  # Data integrity failed.

        dataSoFar |= data << dataBitsSoFar

    # Footer.
    offset += 1
    if not matchMark(
        results.rawbuf[offset],
        kGoodweatherBitMark,
        _tolerance + kGoodweatherExtraTolerance
    ):
        return False

    offset += 1
    if not matchSpace(results.rawbuf[offset], kGoodweatherHdrSpace):
        return False

    offset += 1
    if not matchMark(
        results.rawbuf[offset],
        kGoodweatherBitMark,
        _tolerance + kGoodweatherExtraTolerance
    ):
        return False

    if offset <= results.rawlen and not matchAtLeast(results.rawbuf[offset], kGoodweatherHdrSpace):
        return False

    # Compliance
    if strict and dataBitsSoFar != kGoodweatherBits:
        return False

    # Success
    results.decode_type = decode_type_t.GOODWEATHER
    results.bits = dataBitsSoFar
    results.value = dataSoFar
    results.address = 0
    results.command = 0
    return True
