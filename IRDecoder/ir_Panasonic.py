# -*- coding: utf-8 -*-

# Copyright 2018 David Conran

# Supports:
#   Brand: Panasonic,  Model: TV
#   Brand: Panasonic,  Model: JKE series A/C
#   Brand: Panasonic,  Model: DKE series A/C
#   Brand: Panasonic,  Model: CKP series A/C
#   Brand: Panasonic,  Model: CS-ME10CKPG A/C
#   Brand: Panasonic,  Model: CS-ME12CKPG A/C
#   Brand: Panasonic,  Model: CS-ME14CKPG A/C
#   Brand: Panasonic,  Model: PKR series A/C (Use DKE)
#   Brand: Panasonic,  Model: CS-E7PKR A/C (Use DKE)
#   Brand: Panasonic,  Model: RKR series A/C
#   Brand: Panasonic,  Model: CS-Z9RKR A/C
#   Brand: Panasonic,  Model: NKE series A/C
#   Brand: Panasonic,  Model: CS-YW9MKD A/C
#   Brand: Panasonic,  Model: A75C3747 remote
#   Brand: Panasonic,  Model: A75C3704 remote
#   Brand: Panasonic,  Model: A75C2311 remote (CKP)
#   Brand: Panasonic,  Model: A75C3747 remote
#   Brand: Panasonic,  Model: A75C3747 remote
#   Brand: Panasonic,  Model: A75C3747 remote

# Panasonic A/C support heavily influenced by:
#   https:#github.com/ToniA/ESPEasy/blob/HeatpumpIR/lib/HeatpumpIR/PanasonicHeatpumpIR.cpp

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Constants
kPanasonicFreq = 36700
kPanasonicAcExcess = 0
# Much higher than usual. See issue #540.
kPanasonicAcTolerance = 40

kPanasonicAcAuto = 0  # 0b000
kPanasonicAcDry = 2   # 0b010
kPanasonicAcCool = 3  # 0b011
kPanasonicAcHeat = 4  # 0b010
kPanasonicAcFan = 6   # 0b110
kPanasonicAcFanMin = 0
kPanasonicAcFanMed = 2
kPanasonicAcFanMax = 4
kPanasonicAcFanAuto = 7
kPanasonicAcFanDelta = 3
kPanasonicAcPowerOffset = 0
kPanasonicAcTempOffset = 1  # Bits
kPanasonicAcTempSize = 5  # Bits
kPanasonicAcMinTemp = 16      # Celsius
kPanasonicAcMaxTemp = 30      # Celsius
kPanasonicAcFanModeTemp = 27  # Celsius
kPanasonicAcQuietOffset = 0
kPanasonicAcPowerfulOffset = 5   # 0b100000
# CKP & RKR models have Powerful and Quiet bits swapped.
kPanasonicAcQuietCkpOffset = kPanasonicAcPowerfulOffset
kPanasonicAcPowerfulCkpOffset = kPanasonicAcQuietOffset
kPanasonicAcSwingVHighest = 0x1  # 0b0001
kPanasonicAcSwingVHigh = 0x2     # 0b0010
kPanasonicAcSwingVMiddle = 0x3   # 0b0011
kPanasonicAcSwingVLow = 0x4      # 0b0100
kPanasonicAcSwingVLowest = 0x5   # 0b0101
kPanasonicAcSwingVAuto = 0xF     # 0b1111

kPanasonicAcSwingHMiddle = 0x6     # 0b0110
kPanasonicAcSwingHFullLeft = 0x9   # 0b1001
kPanasonicAcSwingHLeft = 0xA       # 0b1010
kPanasonicAcSwingHRight = 0xB      # 0b1011
kPanasonicAcSwingHFullRight = 0xC  # 0b1100
kPanasonicAcSwingHAuto = 0xD       # 0b1101
kPanasonicAcChecksumInit = 0xF4
kPanasonicAcOnTimerOffset = 1
kPanasonicAcOffTimerOffset = 2
kPanasonicAcTimeSize = 11  # Bits
kPanasonicAcTimeOverflowSize = 3  # Bits
kPanasonicAcTimeMax = 23 * 60 + 59  # Mins since midnight.
kPanasonicAcTimeSpecial = 0x600

kPanasonicKnownGoodState = [
    0x02, 0x20, 0xE0, 0x04, 0x00, 0x00, 0x00, 0x06, 0x02,
    0x20, 0xE0, 0x04, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00,
    0x00, 0x0E, 0xE0, 0x00, 0x00, 0x81, 0x00, 0x00, 0x00]


# Copyright 2015 Kristian Lauszus
# Copyright 2017, 2018 David Conran

# Panasonic devices

# Panasonic protocol originally added by Kristian Lauszus from:
#   https:#github.com/z3t0/Arduino-IRremote
# (Thanks to zenwheel and other people at the original blog post)
#
# Panasonic A/C support add by crankyoldgit but heavily influenced by:
#   https:#github.com/ToniA/ESPEasy/blob/HeatpumpIR/lib/HeatpumpIR/PanasonicHeatpumpIR.cpp
# Panasonic A/C Clock & Timer support:
#   Reverse Engineering by MikkelTb
#   Code by crankyoldgit
# Panasonic A/C models supported:
#   A/C Series/models:
#     JKE, LKE, DKE, CKP, PKR, RKR, & NKE series. (In theory)
#     CS-YW9MKD, CS-Z9RKR, CS-E7PKR (confirmed)
#     CS-ME14CKPG / CS-ME12CKPG / CS-ME10CKPG
#   A/C Remotes:
#     A75C3747 (confirmed)
#     A75C3704
#     A75C2311 (CKP)

# Constants
# Ref:
#   http:#www.remotecentral.com/cgi-bin/mboard/rc-pronto/thread.cgi?26152

kPanasonicTick = 432
kPanasonicHdrMarkTicks = 8
kPanasonicHdrMark = kPanasonicHdrMarkTicks * kPanasonicTick
kPanasonicHdrSpaceTicks = 4
kPanasonicHdrSpace = kPanasonicHdrSpaceTicks * kPanasonicTick
kPanasonicBitMarkTicks = 1
kPanasonicBitMark = kPanasonicBitMarkTicks * kPanasonicTick
kPanasonicOneSpaceTicks = 3
kPanasonicOneSpace = kPanasonicOneSpaceTicks * kPanasonicTick
kPanasonicZeroSpaceTicks = 1
kPanasonicZeroSpace = kPanasonicZeroSpaceTicks * kPanasonicTick
kPanasonicMinCommandLengthTicks = 378
kPanasonicMinCommandLength = kPanasonicMinCommandLengthTicks * kPanasonicTick
kPanasonicEndGap = 5000  # See issue #245
kPanasonicMinGapTicks = (
    kPanasonicMinCommandLengthTicks -
    (kPanasonicHdrMarkTicks + kPanasonicHdrSpaceTicks +
     kPanasonicBits * (kPanasonicBitMarkTicks + kPanasonicOneSpaceTicks) +
     kPanasonicBitMarkTicks)
)
kPanasonicMinGap = kPanasonicMinGapTicks * kPanasonicTick

kPanasonicAcSectionGap = 10000
kPanasonicAcSection1Length = 8
kPanasonicAcMessageGap = kDefaultMessageGap  # Just a guess.


"""



class IRPanasonicAc {
    def __init__(self, pin, inverted=False, use_modulation=True):
        
        self._irsend = IRsend 
  
        self.remote_state = [0] * kPanasonicAcStateLength
        self._swingh = None
        self._temp = None

    def stateReset(self):
    
    def send(self, repeat=kPanasonicAcDefaultRepeat):
    
    def calibrate(self):
        return _irsend.calibrate()
        
    def begin(self):
    
    
    def on(self):
    
    def off(self):
    
    def setPower(self, on):
    
    def getPower(self):
    
    def setTemp(self, temp, remember=True):
    
    def getTemp(self):
    
    def setFan(self, fan):
    
    def getFan(self):
    
    def setMode(self, mode):
    
    def getMode(self):
    
    def setRaw(self, state):
    
    def getRaw(self):
    
    @staticmethod
    def validChecksum(state, length=kPanasonicAcStateLength):
    
    @staticmethod
    def calcChecksum(state, length=kPanasonicAcStateLength):
    
    def setQuiet(self, on):
    
    def getQuiet(self):
    
    def setPowerful(self, on):
    
    def getPowerful(self):
    
    def setModel(self, model):
    
    def getModel(self):
    
    def setSwingVertical(self, elevation):
    
    def getSwingVertical(self):
    
    def setSwingHorizontal(self, direction):
    
    def getSwingHorizontal(self):
    
    @staticmethod
    def encodeTime(self, hours, mins):
    
    def getClock():
    
    def setClock(self, mins_since_midnight):
    
    def getOnTimer(self):
    
    def setOnTimer(self, mins_since_midnight, enable=True):
    
    def cancelOnTimer(self):
    
    def isOnTimerEnabled(self):
    
    def getOffTimer(self):
    
    def setOffTimer(self, mins_since_midnight, enable=True):
    def cancelOffTimer(self):
    
    def isOffTimerEnabled(self):
    
    @staticmethod
    def convertMode(mode):
    
    @staticmethod
    def convertFan(speed):
    
    @staticmethod
    def convertSwingV(position):
    
    @staticmethod
    def convertSwingH(position):
    
    @staticmethod
    def toCommonMode(mode):
    
    @staticmethod
    def toCommonFanSpeed(speed):
  
    @staticmethod
    def toCommonSwingV(pos):
    
    @statethod
    def toCommonSwingH(pos):
  
    def toCommon():
      
    def toString():
  
    def fixChecksum(self, length=kPanasonicAcStateLength):
  
    @staticmethod
    def calcChecksum(state, length=kPanasonicAcStateLength):
  
    @staticmethod
    def _getTime(ptr):
  
    @staticmethod
    def _setTime(ptr, mins_since_midnight, round_down):

"""


addBoolToString = irutils.addBoolToString
addFanToString = irutils.addFanToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addModelToString = irutils.addModelToString
addTempToString = irutils.addTempToString
minsToString = irutils.minsToString
setBit = irutils.setBit
setBits = irutils.setBits

from .protocol_base import *

class Panasonic(ProtocolBase):
    # Send a Panasonic formatted message.
    #
    # Args:
    #   data:   The message to be sent.
    #   nbits:  The number of bits of the message to be sent. (kPanasonicBits).
    #   repeat: The number of times the command is to be repeated.
    #
    # Status: BETA / Should be working.
    #
    # Note:
    #   This protocol is a modified version of Kaseikyo.
    def send_ir(self, address, data, nbits, repeat):
        address <<= 32
        data |= address
        
        self.sendGeneric(
            kPanasonicHdrMark, 
            kPanasonicHdrSpace, 
            kPanasonicBitMark,
            kPanasonicOneSpace, 
            kPanasonicBitMark, 
            kPanasonicZeroSpace,
            kPanasonicBitMark, 
            kPanasonicMinGap, 
            kPanasonicMinCommandLength,
            data, 
            nbits, 
            kPanasonicFreq, 
            True, 
            repeat, 
            50
        )

    # Calculate the raw Panasonic data based on device, subdevice, & function.
    #
    # Args:
    #   manufacturer: A 16-bit manufacturer code. e.g. 0x4004 is Panasonic.
    #   device:       An 8-bit code.
    #   subdevice:    An 8-bit code.
    #   function:     An 8-bit code.
    # Returns:
    #   A raw Panasonic message.
    #
    # Status: BETA / Should be working..
    #
    # Note:
    #   Panasonic 48-bit protocol is a modified version of Kaseikyo.
    # Ref:
    #   http:#www.remotecentral.com/cgi-bin/mboard/rc-pronto/thread.cgi?2615
    @staticmethod
    def encode_ir(manufacturer, device, subdevice, function):
        checksum = device ^ subdevice ^ function
        return (manufacturer << 32) | (device << 24) | (subdevice << 16) | (function << 8) | checksum
    
    # Decode the supplied Panasonic message.
    #
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of data bits to expect.
    #   strict:  Flag indicating if we should perform strict matching.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Status: BETA / Should be working.
    # Note:
    #   Panasonic 48-bit protocol is a modified version of Kaseikyo.
    # Ref:
    #   http:#www.remotecentral.com/cgi-bin/mboard/rc-pronto/thread.cgi?26152
    #   http:#www.hifi-remote.com/wiki/index.php?title=Panasonic
    def decode_ir(self, results, nbits, strict, manufacturer):
        if strict and nbits != kPanasonicBits:
            return False  # Request is out of spec.
    
        data = 0
        offset = kStartOffset
    
        # Match Header + Data + Footer
        if not self.matchGeneric(
            results.rawbuf[:offset],
            data,
            results.rawlen - offset,
            nbits,
            kPanasonicHdrMark,
            kPanasonicHdrSpace,
            kPanasonicBitMark,
            kPanasonicOneSpace,
            kPanasonicBitMark,
            kPanasonicZeroSpace,
            kPanasonicBitMark,
            kPanasonicEndGap,
            True
        ):
            return False

        # Compliance
        address = data >> 32
        command = data

        if strict and address != manufacturer:  # Verify the Manufacturer code.
            return False

        # Verify the checksum.
        checksumOrig = data
        checksumCalc = (data >> 24) ^ (data >> 16) ^ (data >> 8)

        if checksumOrig != checksumCalc:
            return False

        # Success
        results.value = data
        results.address = address
        results.command = command
        results.decode_type = decode_type_t.PANASONIC
        results.bits = nbits
        return True

    #if SEND_PANASONIC_AC
    # Send a Panasonic A/C message.
    #
    # Args:
    #   data:   Contents of the message to be sent. (Guessing MSBF order)
    #   nbits:  Nr. of bits of data to be sent. Typically kPanasonicAcBits.
    #   repeat: Nr. of additional times the message is to be sent.
    #
    # Status: Beta / Appears to work with real device(s).
    #:
    # Panasonic A/C models supported:
    #   A/C Series/models:
    #     JKE, LKE, DKE, CKP, PKR, RKR, & NKE series.
    #     CS-YW9MKD
    #     CS-E7PKR
    #   A/C Remotes:
    #     A75C3747
    #     A75C3704
    #
    def send_ac(self):
        data = self.getRaw()
        nbytes = kPanasonicAcStateLength
        repeat = repeat
        if nbytes < kPanasonicAcSection1Length:
            return

        for _ in range(repeat + 1):
            # First section. (8 bytes)
            self.sendGeneric(
                kPanasonicHdrMark,
                kPanasonicHdrSpace,
                kPanasonicBitMark,
                kPanasonicOneSpace,
                kPanasonicBitMark,
                kPanasonicZeroSpace,
                kPanasonicBitMark,
                kPanasonicAcSectionGap,
                data,
                kPanasonicAcSection1Length,
                kPanasonicFreq,
                False,
                0,
                50
            )
            # First section. (The rest of the data bytes)
            self.sendGeneric(
                kPanasonicHdrMark,
                kPanasonicHdrSpace,
                kPanasonicBitMark,
                kPanasonicOneSpace,
                kPanasonicBitMark,
                kPanasonicZeroSpace,
                kPanasonicBitMark,
                kPanasonicAcMessageGap,
                data[:kPanasonicAcSection1Length],
                nbytes - kPanasonicAcSection1Length,
                kPanasonicFreq,
                False,
                0,
                50
            )

    def stateReset(self):
        self.remote_state = kPanasonicKnownGoodState[:kPanasonicAcStateLength]
        self._temp = 25  # An initial saved desired temp. Completely made up.
        self._swingh = kPanasonicAcSwingHMiddle  # A similar made up value for H Swing.

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        if length < 2:
            return False  # 1 byte of data can't have a checksum.

        return (
            state[length - 1] ==
            sumBytes(state, length - 1, kPanasonicAcChecksumInit)
        )

    @staticmethod
    def calcChecksum(state, length):
        return sumBytes(state, length - 1, kPanasonicAcChecksumInit)

    def fixChecksum(self, length):
        self.remote_state[length - 1] = self.calcChecksum(self.remote_state, length)

    def setModel(self, model):
        if model not in (
            panasonic_ac_remote_model_t.kPanasonicDke,
            panasonic_ac_remote_model_t.kPanasonicJke,
            panasonic_ac_remote_model_t.kPanasonicLke,
            panasonic_ac_remote_model_t.kPanasonicNke,
            panasonic_ac_remote_model_t.kPanasonicCkp,
            panasonic_ac_remote_model_t.kPanasonicRkr
        ):
            return

        # clear & set the various bits and bytes.
        self.remote_state[13] &= 0xF0
        self.remote_state[17] = 0x00
        self.remote_state[21] &= 0b11101111
        self.remote_state[23] = 0x81
        self.remote_state[25] = 0x00

        if model == panasonic_ac_remote_model_t.kPanasonicLke:
            self.remote_state[13] |= 0x02
            self.remote_state[17] = 0x06
        elif model == panasonic_ac_remote_model_t.kPanasonicDke:
            self.remote_state[23] = 0x01
            self.remote_state[25] = 0x06
            # Has to be done last as setSwingHorizontal has model check built-in
            self.setSwingHorizontal(_swingh)
        elif model == panasonic_ac_remote_model_t.kPanasonicNke:
            self.remote_state[17] = 0x06
        elif model == panasonic_ac_remote_model_t.kPanasonicJke:
            self.remote_state[23] = 0x80
        elif model == panasonic_ac_remote_model_t.kPanasonicCkp:
            self.remote_state[21] |= 0x10
            self.remote_state[23] = 0x01
        elif model == panasonic_ac_remote_model_t.kPanasonicRkr:
            self.remote_state[13] |= 0x08
            self.remote_state[23] = 0x89

    def getModel(self):
        if self.remote_state[23] == 0x89:
            return panasonic_ac_remote_model_t.kPanasonicRkr

        if self.remote_state[17] == 0x00:
            if self.remote_state[21] & 0x10 and self.remote_state[23] & 0x01:
                return panasonic_ac_remote_model_t.kPanasonicCkp

            if self.remote_state[23] & 0x80:
                return panasonic_ac_remote_model_t.kPanasonicJke

        if self.remote_state[17] == 0x06 and self.remote_state[13] & 0x0F == 0x02:
            return panasonic_ac_remote_model_t.kPanasonicLke

        if self.remote_state[23] == 0x01:
            return panasonic_ac_remote_model_t.kPanasonicDke

        if self.remote_state[17] == 0x06:
            return panasonic_ac_remote_model_t.kPanasonicNke

        return panasonic_ac_remote_model_t.kPanasonicUnknown  # Default

    def getRaw(self):
      self.fixChecksum()
      return self.remote_state[:]

    def setRaw(self, state):
        self.remote_state = state[:kPanasonicAcStateLength]

    # Control the power state of the A/C unit.
    #
    # For CKP models, the remote has no memory of the power state the A/C unit
    # should be in. For those models setting this on/True will toggle the power
    # state of the Panasonic A/C unit with the next meessage.
    # e.g. If the A/C unit is already on, setPower(True) will turn it off.
    #      If the A/C unit is already off, setPower(True) will turn it on.
    #      setPower(False) will leave the A/C power state as it was.
    #
    # For all other models, setPower(True) should set the internal state to
    # turn it on, and setPower(False) should turn it off.
    def setPower(self, on):
        setBit(self.remote_state[13], kPanasonicAcPowerOffset, on)

    # Return the A/C power state of the remote.
    # Except for CKP models, where it returns if the power state will be toggled
    # on the A/C unit when the next message is sent.
    def getPower(self):
        return GETBIT8(self.remote_state[13], kPanasonicAcPowerOffset)

    def getMode(self):
        return GETBITS8(self.remote_state[13], kHighNibble, kModeBitsSize)

    def setMode(self, desired):
        mode = kPanasonicAcAuto  # Default to Auto mode.
        if desired == kPanasonicAcFan:
            # Allegedly Fan mode has a temperature of 27.
            self.setTemp(kPanasonicAcFanModeTemp, False)
            mode = desired

        if desired in (
            kPanasonicAcAuto,
            kPanasonicAcCool,
            kPanasonicAcHeat,
            kPanasonicAcDry
        ):
            mode = desired

            # Set the temp to the saved temp, just incase our previous mode was Fan.
            self.setTemp(self._temp)
        self.remote_state[13] &= 0x0F  # Clear the previous mode bits.
        setBits(self.remote_state[13], kHighNibble, kModeBitsSize, mode)

    def getTemp(self):
        return GETBITS8(self.remote_state[14], kPanasonicAcTempOffset, kPanasonicAcTempSize)


    # Set the desitred temperature in Celsius.
    # Args:
    #   celsius: The temperature to set the A/C unit to.
    #   remember: A boolean flag for the class to remember the temperature.
    #
    # Automatically safely limits the temp to the operating range supported.
    def setTemp(self, celsius, remember):
        temperature = max(celsius, kPanasonicAcMinTemp)
        temperature = min(temperature, kPanasonicAcMaxTemp)
        if remember:
            self._temp = temperature

        self.remote_state[14] = setBits(
            self.remote_state[14],
            kPanasonicAcTempOffset,
            kPanasonicAcTempSize,
            temperature
        )

    def getSwingVertical(self):
        return GETBITS8(self.remote_state[16], kLowNibble, kNibbleSize)

    def setSwingVertical(self, desired_elevation):
        elevation = desired_elevation
        if elevation != kPanasonicAcSwingVAuto:
            elevation = max(elevation, kPanasonicAcSwingVHighest)
            elevation = min(elevation, kPanasonicAcSwingVLowest)

        self.remote_state[16] = setBits(self.remote_state[16], kLowNibble, kNibbleSize, elevation)

    def getSwingHorizontal(self):
        return GETBITS8(self.remote_state[17], kLowNibble, kNibbleSize)

    def setSwingHorizontal(self, desired_direction):
        if desired_direction not in (
            kPanasonicAcSwingHAuto,
            kPanasonicAcSwingHMiddle,
            kPanasonicAcSwingHFullLeft,
            kPanasonicAcSwingHLeft,
            kPanasonicAcSwingHRight,
            kPanasonicAcSwingHFullRight
        ):
            return
        self._swingh = desired_direction  # Store the direction for later.
        direction = desired_direction


        model = self.getModel()
        if model in (
            kPanasonicNke,
            kPanasonicLke
        ):
            direction = kPanasonicAcSwingHMiddle
        elif model not in (
            kPanasonicDke,
            kPanasonicRkr
        ):
            return

        self.remote_state[17] = setBits(self.remote_state[17], kLowNibble, kNibbleSize, direction)

    def setFan(self, speed):
        if speed in (
            kPanasonicAcFanMin,
            kPanasonicAcFanMed,
            kPanasonicAcFanMax,
            kPanasonicAcFanAuto
        ):
            self.remote_state[16] = setBits(self.remote_state[16], kHighNibble, kNibbleSize, speed + kPanasonicAcFanDelta)
        else:
            self.setFan(kPanasonicAcFanAuto)

    def getFan(self):
        return GETBITS8(self.remote_state[16], kHighNibble, kNibbleSize) - kPanasonicAcFanDelta


    def getQuiet(self):
        model = self.getModel()

        if model in (
            kPanasonicRkr,
            kPanasonicCkp
        ):
            return GETBIT8(self.remote_state[21], kPanasonicAcQuietCkpOffset)

        return GETBIT8(self.remote_state[21], kPanasonicAcQuietOffset)

    def setQuiet(self, on):
        model = self.getModel()
        if model in (
            kPanasonicRkr,
            kPanasonicCkp
        ):
            offset = kPanasonicAcQuietCkpOffset
        else:
            offset = kPanasonicAcQuietOffset

        if on:
            self.setPowerful(False)  # Powerful is mutually exclusive.

        self.remote_state[21] = setBit(self.remote_state[21], offset, on)

    def getPowerful(self):
        model = self.getModel()
        if model in (
            kPanasonicRkr,
            kPanasonicCkp
        ):
            return GETBIT8(self.remote_state[21], kPanasonicAcPowerfulCkpOffset)

        return GETBIT8(self.remote_state[21], kPanasonicAcPowerfulOffset)

    def setPowerful(self, on):
        model = self.getModel()
        if model in (
            kPanasonicRkr,
            kPanasonicCkp
        ):
            offset = kPanasonicAcPowerfulCkpOffset
        else:
            offset = kPanasonicAcPowerfulOffset

        if on:
            self.setQuiet(False)  # Quiet is mutually exclusive.

        self.remote_state[21] = setBit(self.remote_state[21], offset, on)

    # Convert standard (military/24hr) time to nr. of minutes since midnight.
    @staticmethod
    def encodeTime(hours, mins):
        return min(hours, 23) * 60 + min(mins, 59)

    def _getTime(self, ptr):
        result = (
            GETBITS8(ptr[1], kLowNibble, kPanasonicAcTimeOverflowSize) <<
            (kPanasonicAcTimeSize - kPanasonicAcTimeOverflowSize)
        ) + ptr[0]

        if result == kPanasonicAcTimeSpecial:
            return 0
        return result

    def getClock(self):
        return self._getTime(self.remote_state[24])

    def _setTime(self, ptr, mins_since_midnight, round_down):
        corrected = min(mins_since_midnight, kPanasonicAcTimeMax)
        if round_down:
            corrected -= corrected % 10
        if mins_since_midnight == kPanasonicAcTimeSpecial:
            corrected = kPanasonicAcTimeSpecial

        ptr[0] = corrected
        ptr[1] = setBits(
            ptr[1],
            kLowNibble,
            kPanasonicAcTimeOverflowSize,
            corrected >> (kPanasonicAcTimeSize - kPanasonicAcTimeOverflowSize)
        )


void IRPanasonicAc.setClock(mins_since_midnight) {
  _setTime(&remote_state[24], mins_since_midnight, False)
}

IRPanasonicAc.getOnTimer(void) { return _getTime(&remote_state[18]) }

void IRPanasonicAc.setOnTimer(mins_since_midnight,
                               bool enable) {
  # Set the timer flag.
  setBit(&remote_state[13], kPanasonicAcOnTimerOffset, enable)
  # Store the time.
  _setTime(&remote_state[18], mins_since_midnight, True)
}

void IRPanasonicAc.cancelOnTimer(void) { self.setOnTimer(0, False) }

bool IRPanasonicAc.isOnTimerEnabled(void) {
  return GETBIT8(remote_state[13], kPanasonicAcOnTimerOffset)
}

IRPanasonicAc.getOffTimer(void) {
  result = (GETBITS8(remote_state[20], 0, 7) << kNibbleSize) |
      GETBITS8(remote_state[19], kHighNibble, kNibbleSize)
  if (result == kPanasonicAcTimeSpecial) return 0
  return result
}

void IRPanasonicAc.setOffTimer(mins_since_midnight,
                                bool enable) {
  # Ensure its on a 10 minute boundary and no overflow.
  corrected = std.min(mins_since_midnight, kPanasonicAcTimeMax)
  corrected -= corrected % 10
  if (mins_since_midnight == kPanasonicAcTimeSpecial)
    corrected = kPanasonicAcTimeSpecial
  # Set the timer flag.
  setBit(&remote_state[13], kPanasonicAcOffTimerOffset, enable)
  # Store the time.
  setBits(&remote_state[19], kHighNibble, kNibbleSize, corrected)
  setBits(&remote_state[20], 0, 7, corrected >> kNibbleSize)
}

void IRPanasonicAc.cancelOffTimer(void) { self.setOffTimer(0, False) }

bool IRPanasonicAc.isOffTimerEnabled(void) {
  return GETBIT8(remote_state[13], kPanasonicAcOffTimerOffset)
}

# Convert a standard A/C mode into its native mode.
IRPanasonicAc.convertMode(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kCool: return kPanasonicAcCool
    case stdAc.opmode_t.kHeat: return kPanasonicAcHeat
    case stdAc.opmode_t.kDry:  return kPanasonicAcDry
    case stdAc.opmode_t.kFan:  return kPanasonicAcFan
    default:                     return kPanasonicAcAuto
  }
}

# Convert a standard A/C Fan speed into its native fan speed.
IRPanasonicAc.convertFan(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kMin:    return kPanasonicAcFanMin
    case stdAc.fanspeed_t.kLow:    return kPanasonicAcFanMin + 1
    case stdAc.fanspeed_t.kMedium: return kPanasonicAcFanMin + 2
    case stdAc.fanspeed_t.kHigh:   return kPanasonicAcFanMin + 3
    case stdAc.fanspeed_t.kMax:    return kPanasonicAcFanMax
    default:                         return kPanasonicAcFanAuto
  }
}

# Convert a standard A/C vertical swing into its native setting.
IRPanasonicAc.convertSwingV(stdAc.swingv_t position) {
  switch (position) {
    case stdAc.swingv_t.kHighest:
    case stdAc.swingv_t.kHigh:
    case stdAc.swingv_t.kMiddle:
    case stdAc.swingv_t.kLow:
    case stdAc.swingv_t.kLowest: return (uint8_t)position
    default:                       return kPanasonicAcSwingVAuto
  }
}

# Convert a standard A/C horizontal swing into its native setting.
IRPanasonicAc.convertSwingH(stdAc.swingh_t position) {
  switch (position) {
    case stdAc.swingh_t.kLeftMax:  return kPanasonicAcSwingHFullLeft
    case stdAc.swingh_t.kLeft:     return kPanasonicAcSwingHLeft
    case stdAc.swingh_t.kMiddle:   return kPanasonicAcSwingHMiddle
    case stdAc.swingh_t.kRight:    return kPanasonicAcSwingHRight
    case stdAc.swingh_t.kRightMax: return kPanasonicAcSwingHFullRight
    default:                         return kPanasonicAcSwingHAuto
  }
}

# Convert a native mode to it's common equivalent.
stdAc.opmode_t IRPanasonicAc.toCommonMode(mode) {
  switch (mode) {
    case kPanasonicAcCool: return stdAc.opmode_t.kCool
    case kPanasonicAcHeat: return stdAc.opmode_t.kHeat
    case kPanasonicAcDry:  return stdAc.opmode_t.kDry
    case kPanasonicAcFan:  return stdAc.opmode_t.kFan
    default:               return stdAc.opmode_t.kAuto
  }
}

# Convert a native fan speed to it's common equivalent.
stdAc.fanspeed_t IRPanasonicAc.toCommonFanSpeed(spd) {
  switch (spd) {
    case kPanasonicAcFanMax:     return stdAc.fanspeed_t.kMax
    case kPanasonicAcFanMin + 3: return stdAc.fanspeed_t.kHigh
    case kPanasonicAcFanMin + 2: return stdAc.fanspeed_t.kMedium
    case kPanasonicAcFanMin + 1: return stdAc.fanspeed_t.kLow
    case kPanasonicAcFanMin:     return stdAc.fanspeed_t.kMin
    default:                     return stdAc.fanspeed_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingh_t IRPanasonicAc.toCommonSwingH(pos) {
  switch (pos) {
    case kPanasonicAcSwingHFullLeft:  return stdAc.swingh_t.kLeftMax
    case kPanasonicAcSwingHLeft:      return stdAc.swingh_t.kLeft
    case kPanasonicAcSwingHMiddle:    return stdAc.swingh_t.kMiddle
    case kPanasonicAcSwingHRight:     return stdAc.swingh_t.kRight
    case kPanasonicAcSwingHFullRight: return stdAc.swingh_t.kRightMax
    default:                          return stdAc.swingh_t.kAuto
  }
}

# Convert a native vertical swing to it's common equivalent.
stdAc.swingv_t IRPanasonicAc.toCommonSwingV(pos) {
  if (pos >= kPanasonicAcSwingVHighest and pos <= kPanasonicAcSwingVLowest)
    return (stdAc.swingv_t)pos
  else
    return stdAc.swingv_t.kAuto
}

# Convert the A/C state to it's common equivalent.
stdAc.state_t IRPanasonicAc.toCommon(void) {
  stdAc.state_t result
  result.protocol = decode_type_t.PANASONIC_AC
  result.model = self.getModel()
  result.power = self.getPower()
  result.mode = self.toCommonMode(self.getMode())
  result.celsius = True
  result.degrees = self.getTemp()
  result.fanspeed = self.toCommonFanSpeed(self.getFan())
  result.swingv = self.toCommonSwingV(self.getSwingVertical())
  result.swingh = self.toCommonSwingH(self.getSwingHorizontal())
  result.quiet = self.getQuiet()
  result.turbo = self.getPowerful()
  # Not supported.
  result.econo = False
  result.clean = False
  result.filter = False
  result.light = False
  result.beep = False
  result.sleep = -1
  result.clock = -1
  return result
}

# Convert the internal state into a human readable string.
String IRPanasonicAc.toString(void) {
  String result = ""
  result.reserve(180)  # Reserve some heap for the string to reduce fragging.
  result += addModelToString(decode_type_t.PANASONIC_AC, getModel(), False)
  result += addBoolToString(getPower(), kPowerStr)
  result += addModeToString(getMode(), kPanasonicAcAuto, kPanasonicAcCool,
                            kPanasonicAcHeat, kPanasonicAcDry, kPanasonicAcFan)
  result += addTempToString(getTemp())
  result += addFanToString(getFan(), kPanasonicAcFanMax, kPanasonicAcFanMin,
                           kPanasonicAcFanAuto, kPanasonicAcFanAuto,
                           kPanasonicAcFanMed)
  result += addIntToString(getSwingVertical(), kSwingVStr)
  result += kSpaceLBraceStr
  switch (getSwingVertical()) {
    case kPanasonicAcSwingVAuto:
      result += kAutoStr
      break
    case kPanasonicAcSwingVHighest:
      result += kHighestStr
      break
    case kPanasonicAcSwingVHigh:
      result += kHighStr
      break
    case kPanasonicAcSwingVMiddle:
      result += kMiddleStr
      break
    case kPanasonicAcSwingVLow:
      result += kLowStr
      break
    case kPanasonicAcSwingVLowest:
      result += kLowestStr
      break
    default:
      result += kUnknownStr
      break
  }
  result += ')'
  switch (getModel()) {
    case kPanasonicJke:
    case kPanasonicCkp:
      break  # No Horizontal Swing support.
    default:
      result += addIntToString(getSwingHorizontal(), kSwingHStr)
      result += kSpaceLBraceStr
      switch (getSwingHorizontal()) {
        case kPanasonicAcSwingHAuto:
          result += kAutoStr
          break
        case kPanasonicAcSwingHFullLeft:
          result += kMaxLeftStr
          break
        case kPanasonicAcSwingHLeft:
          result += kLeftStr
          break
        case kPanasonicAcSwingHMiddle:
          result += kMiddleStr
          break
        case kPanasonicAcSwingHFullRight:
          result += kMaxRightStr
          break
        case kPanasonicAcSwingHRight:
          result += kRightStr
          break
        default:
          result += kUnknownStr
      }
      result += ')'
  }
  result += addBoolToString(getQuiet(), kQuietStr)
  result += addBoolToString(getPowerful(), kPowerfulStr)
  result += addLabeledString(minsToString(getClock()), kClockStr)
  result += addLabeledString(
      isOnTimerEnabled() ? minsToString(getOnTimer()) : kOffStr,
      kOnTimerStr)
  result += addLabeledString(
      isOffTimerEnabled() ? minsToString(getOffTimer()) : kOffStr,
      kOffTimerStr)
  return result
}

#if DECODE_PANASONIC_AC
# Decode the supplied Panasonic AC message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kPanasonicAcBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Beta / Appears to work with real device(s).
#
# Panasonic A/C models supported:
#   A/C Series/models:
#     JKE, LKE, DKE, PKR, & NKE series.
#     CS-YW9MKD
#     CS-E7PKR
#   A/C Remotes:
#     A75C3747 (Confirmed)
#     A75C3704
bool IRrecv.decodePanasonicAC(decode_results *results, nbits,
                               bool strict) {
  min_nr_of_messages = 1
  if (strict) {
    if (nbits != kPanasonicAcBits and nbits != kPanasonicAcShortBits)
      return False  # Not strictly a PANASONIC_AC message.
  }

  if (results.rawlen <
      min_nr_of_messages * (2 * nbits + kHeader + kFooter) - 1)
    return False  # Can't possibly be a valid PANASONIC_AC message.

  offset = kStartOffset

  # Match Header + Data #1 + Footer
  used
  used = matchGeneric(results.rawbuf + offset, results.state,
                      results.rawlen - offset, kPanasonicAcSection1Length * 8,
                      kPanasonicHdrMark, kPanasonicHdrSpace,
                      kPanasonicBitMark, kPanasonicOneSpace,
                      kPanasonicBitMark, kPanasonicZeroSpace,
                      kPanasonicBitMark, kPanasonicAcSectionGap, False,
                      kPanasonicAcTolerance, kPanasonicAcExcess, False)
  if (!used) return False
  offset += used

  # Match Header + Data #2 + Footer
  if (!matchGeneric(results.rawbuf + offset,
                    results.state + kPanasonicAcSection1Length,
                    results.rawlen - offset,
                    nbits - kPanasonicAcSection1Length * 8,
                    kPanasonicHdrMark, kPanasonicHdrSpace,
                    kPanasonicBitMark, kPanasonicOneSpace,
                    kPanasonicBitMark, kPanasonicZeroSpace,
                    kPanasonicBitMark, kPanasonicAcMessageGap, True,
                    kPanasonicAcTolerance, kPanasonicAcExcess, False))
    return False
  # Compliance
  if (strict) {
    # Check the signatures of the section blocks. They start with 0x02& 0x20.
    if (results.state[0] != 0x02 or results.state[1] != 0x20 or
        results.state[8] != 0x02 or results.state[9] != 0x20)
      return False
    if (!IRPanasonicAc.validChecksum(results.state, nbits / 8)) return False
  }

  # Success
  results.decode_type = decode_type_t.PANASONIC_AC
  results.bits = nbits
  return True
}
#endif  # DECODE_PANASONIC_AC
