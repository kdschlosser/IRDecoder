# -*- coding: utf-8 -*-
# Copyright 2009 Ken Shirriff
# Copyright 2017, 2018, 2019 David Conran

# Samsung remote emulation

# Samsung originally added from https:#github.com/shirriff/Arduino-IRremote/

# Constants
# Ref:
#   http:#elektrolab.wz.cz/katalog/samsung_protocol.pdf
# Samsung A/C
#
# Copyright 2018 David Conran

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Supports:
#   Brand: Samsung,  Model: UA55H6300 TV
#   Brand: Samsung,  Model: IEC-R03 remote
#   Brand: Samsung,  Model: AR12KSFPEWQNET A/C
#   Brand: Samsung,  Model: AR12HSSDBWKNEU A/C

# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/505

# Constants
kSamsungAcAuto = 0
kSamsungAcCool = 1
kSamsungAcDry = 2
kSamsungAcFan = 3
kSamsungAcHeat = 4
kSamsungAcModeOffset = 4  # Mask 0b01110000
kSamsungAcFanOffest = 1  # Mask 0b00001110
kSamsungAcFanSize = 3  # Bits
kSamsungAcFanAuto = 0
kSamsungAcFanLow = 2
kSamsungAcFanMed = 4
kSamsungAcFanHigh = 5
kSamsungAcFanAuto2 = 6
kSamsungAcFanTurbo = 7
kSamsungAcMinTemp = 16   # 16C
kSamsungAcMaxTemp = 30   # 30C
kSamsungAcAutoTemp = 25  # 25C
kSamsungAcPower1Offset = 5
kSamsungAcPower6Offset = 4  # Mask 0b00110000
kSamsungAcPower6Size = 2  # Bits
kSamsungAcSwingOffset = 4  # Mask 0b01110000
kSamsungAcSwingSize = 3  # Bits
kSamsungAcSwingMove = 0b010
kSamsungAcSwingStop = 0b111
kSamsungAcBeepOffset = 1
kSamsungAcClean10Offset = 7
kSamsungAcClean11Offset = 1     # 0b00000010
kSamsungAcQuiet1Offset = 4
kSamsungAcQuiet5Offset = 5
kSamsungAcPowerfulMask8 = 0b01010000
kSamsungAcPowerful10Offset = 1  # Mask 0b00000110
kSamsungAcPowerful10Size = 1  # Mask 0b00000110

kSamsungACSectionLength = 7
kSamsungAcPowerSection = 0x1D20F00000000

kSamsungTick = 560
kSamsungHdrMarkTicks = 8
kSamsungHdrMark = kSamsungHdrMarkTicks * kSamsungTick
kSamsungHdrSpaceTicks = 8
kSamsungHdrSpace = kSamsungHdrSpaceTicks * kSamsungTick
kSamsungBitMarkTicks = 1
kSamsungBitMark = kSamsungBitMarkTicks * kSamsungTick
kSamsungOneSpaceTicks = 3
kSamsungOneSpace = kSamsungOneSpaceTicks * kSamsungTick
kSamsungZeroSpaceTicks = 1
kSamsungZeroSpace = kSamsungZeroSpaceTicks * kSamsungTick
kSamsungRptSpaceTicks = 4
kSamsungRptSpace = kSamsungRptSpaceTicks * kSamsungTick
kSamsungMinMessageLengthTicks = 193
kSamsungMinMessageLength = kSamsungMinMessageLengthTicks * kSamsungTick
kSamsungMinGapTicks = (
    kSamsungMinMessageLengthTicks -
    (kSamsungHdrMarkTicks + kSamsungHdrSpaceTicks +
     kSamsungBits * (kSamsungBitMarkTicks + kSamsungOneSpaceTicks) +
     kSamsungBitMarkTicks)
)
kSamsungMinGap = kSamsungMinGapTicks * kSamsungTick

kSamsungAcHdrMark = 690
kSamsungAcHdrSpace = 17844
kSamsungAcSections = 2
kSamsungAcSectionMark = 3086
kSamsungAcSectionSpace = 8864
kSamsungAcSectionGap = 2886
kSamsungAcBitMark = 586
kSamsungAcOneSpace = 1432
kSamsungAcZeroSpace = 436


# Classes
class IRSamsungAc(object):
    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kSamsungAcExtendedStateLength
        self._forcepower = False  # Hack to know when we need to send a special power mesg.
        self._lastsentpowerstate = False
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.stateReset() 

    def stateReset(self, forcepower=True, initialPower=True):
        # Reset the internal state of the emulation.
        # Args:
        #   forcepower: A flag indicating if force sending a special power message
        #              with the first `send()` call. Default: True
        kReset[kSamsungAcExtendedStateLength] = [
            0x02,
            0x92,
            0x0F,
            0x00,
            0x00,
            0x00,
            0xF0,
            0x01,
            0x02,
            0xAE,
            0x71,
            0x00,
            0x15,
            0xF0
        ]
        self.remote_state = kReset[:kSamsungAcExtendedStateLength]
        self._forcepower = forcepower
        self._lastsentpowerstate = initialPower
        self.setPower(initialPower)
    
    def send(self, repeat=kSamsungAcDefaultRepeat, calcchecksum=True):
        # Use for most function/mode/settings changes to the unit.
        # i.e. When the device is already running.

        if calcchecksum:
            self.checksum()

        # Do we need to send a the special power on/off message?
        if self.getPower() != _lastsentpowerstate or self._forcepower:
            self._forcepower = False  # It will now been sent, so clear the flag if set.

        if self.getPower():
            self.sendOn(repeat)
        else:
            self.sendOff(repeat)
            return  # No point sending anything else if we are turning the unit off.

        self._irsend.sendSamsungAC(self.remote_state, kSamsungAcStateLength, repeat)

    def sendExtended(self, repeat=kSamsungAcDefaultRepeat, calcchecksum=True):
        # Use this for when you need to power on/off the device.
        # Samsung A/C requires an extended length message when you want to
        # change the power operating mode of the A/C unit.

        if calcchecksum:
            self.checksum()

        extended_state = [0x00] * kSamsungAcExtendedStateLength
        extended_state[7] = 0x01
        extended_state[8] = 0xD2
        extended_state[9] = 0x0F

        # Copy/convert the internal state to an extended state.
        for i in range(kSamsungACSectionLength):
            extended_state[i] = self.remote_state[i]

        for i in range(kSamsungACSectionLength, kSamsungAcStateLength):
            extended_state[i + kSamsungACSectionLength] = self.remote_state[i]

        # extended_state[8] seems special. This is a guess on how to calculate it.
        extended_state[8] = (extended_state[1] & 0x9F) | 0x40
        # Send it.
        self._irsend.sendSamsungAC(extended_state, kSamsungAcExtendedStateLength, repeat)

    def sendOn(self, repeat=kSamsungAcDefaultRepeat):
        # Send the special extended "On" message as the library can't seem to reproduce
        # this message automatically.
        # See: https:#github.com/crankyoldgit/IRremoteESP8266/issues/604#issuecomment-475020036
        extended_state = [
            0x02, 0x92, 0x0F, 0x00, 0x00, 0x00, 0xF0,
            0x01, 0xD2, 0x0F, 0x00, 0x00, 0x00, 0x00,
            0x01, 0xE2, 0xFE, 0x71, 0x80, 0x11, 0xF0
        ]
        self._irsend.sendSamsungAC(extended_state, kSamsungAcExtendedStateLength, repeat)
        self._lastsentpowerstate = True  # On

    def sendOff(self, repeat=kSamsungAcDefaultRepeat):
        # Send the special extended "Off" message as the library can't seem to
        # reproduce this message automatically.
        # See: https:#github.com/crankyoldgit/IRremoteESP8266/issues/604#issuecomment-475020036
        extended_state = [
            0x02, 0xB2, 0x0F, 0x00, 0x00, 0x00, 0xC0,
            0x01, 0xD2, 0x0F, 0x00, 0x00, 0x00, 0x00,
            0x01, 0x02, 0xFF, 0x71, 0x80, 0x11, 0xC0
        ]
        self._irsend.sendSamsungAC(extended_state, kSamsungAcExtendedStateLength, repeat)
        self._lastsentpowerstate = False  # Off
    
    def calibrate(self):
        return self._irsend.calibrate()
    
    def begin(self):
        self._irsend.begin()
        
    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def setPower(self, on):
        setBit(self.remote_state[1], kSamsungAcPower1Offset, not on)  # Cleared when on.
        setBits(
            self.remote_state[6],
            kSamsungAcPower6Offset,
            kSamsungAcPower6Size,
            0b11 if on else 0b00
        )
    
    def getPower(self):
        return (
            GETBITS8(self.remote_state[6], kSamsungAcPower6Offset, kSamsungAcPower6Size) == 0b11 and
            not GETBIT8(self.remote_state[1], kSamsungAcPower1Offset)
        )

    def setTemp(self, temp):
        # Set the temp. in deg C
        newtemp = max(kSamsungAcMinTemp, temp)
        newtemp = min(kSamsungAcMaxTemp, newtemp)
        setBits(
            self.remote_state[11],
            kHighNibble,
            kNibbleSize,
            newtemp - kSamsungAcMinTemp
        )

    def getTemp(self):
        # Return the set temp. in deg C
        return GETBITS8(self.remote_state[11], kHighNibble, kNibbleSize) + kSamsungAcMinTemp
    
    def setFan(self, speed):
        if speed in (
            kSamsungAcFanAuto,
            kSamsungAcFanLow,
            kSamsungAcFanMed,
            kSamsungAcFanHigh,
            kSamsungAcFanTurbo
        ):
            if self.getMode() == kSamsungAcAuto:
                return  # Not valid in Auto mode.

        elif speed == kSamsungAcFanAuto2:  # Special fan setting for when in Auto mode.
            if self.getMode() != kSamsungAcAuto:
                return

        else:
            return

        setBits(self.remote_state[12], kSamsungAcFanOffest, kSamsungAcFanSize, speed)

    def getFan(self):
        return GETBITS8(self.remote_state[12], kSamsungAcFanOffest, kSamsungAcFanSize)

    def setMode(self, mode):
        # If we get an unexpected mode, default to AUTO.
        newmode = mode
        if newmode > kSamsungAcHeat:
            newmode = kSamsungAcAuto

        setBits(self.remote_state[12], kSamsungAcModeOffset, kModeBitsSize, newmode)

        # Auto mode has a special fan setting valid only in auto mode.
        if newmode == kSamsungAcAuto:
            self.setFan(kSamsungAcFanAuto2)
        else:
            # Non-Auto can't have this fan setting
            if self.getFan() == kSamsungAcFanAuto2:
                self.setFan(kSamsungAcFanAuto)  # Default to something safe.

    def getMode(self):
        return GETBITS8(self.remote_state[12], kSamsungAcModeOffset, kModeBitsSize)

    def setSwing(self, on):
        # TODO(Hollako): Explain why sometimes the LSB of remote_state[9] is a 1.
        # e.g. 0xAE or 0XAF for swing move.
        setBits(
            self.remote_state[9],
            kSamsungAcSwingOffset,
            kSamsungAcSwingSize,
            kSamsungAcSwingMove if on else kSamsungAcSwingStop
        )
    
    def getSwing(self):
        # TODO(Hollako): Explain why sometimes the LSB of remote_state[9] is a 1.
        # e.g. 0xAE or 0XAF for swing move.
        return GETBITS8(
            self.remote_state[9],
            kSamsungAcSwingOffset,
            kSamsungAcSwingSize
        ) == kSamsungAcSwingMove

    def setBeep(self, on):
        setBit(self.remote_state[13], kSamsungAcBeepOffset, on)
    
    def getBeep(self):
        return GETBIT8(self.remote_state[13], kSamsungAcBeepOffset)
    
    def setClean(self, on):
        setBit(self.remote_state[10], kSamsungAcClean10Offset, on)
        setBit(self.remote_state[11], kSamsungAcClean11Offset, on)

    def getClean(self):
        return (
            GETBIT8(self.remote_state[10], kSamsungAcClean10Offset) and
            GETBIT8(self.remote_state[11], kSamsungAcClean11Offset)
        )

    def setQuiet(self, on):
        setBit(self.remote_state[1], kSamsungAcQuiet1Offset, not on)  # Cleared when on.
        setBit(self.remote_state[5], kSamsungAcQuiet5Offset, on)
        if on:
            # Quiet mode seems to set fan speed to auto.
            self.setFan(kSamsungAcFanAuto)
            self.setPowerful(False)  # Quiet 'on' is mutually exclusive to Powerful.
    
    def getQuiet(self):
        return (
            not GETBIT8(self.remote_state[1], kSamsungAcQuiet1Offset) and
            GETBIT8(self.remote_state[5], kSamsungAcQuiet5Offset)
        )

    def setPowerful(self, on):
        setBits(
            self.remote_state[10],
            kSamsungAcPowerful10Offset,
            kSamsungAcPowerful10Offset,
            0b11 if on else 0b00
        )
        if on:
            self.remote_state[8] &= ~kSamsungAcPowerfulMask8  # Bit needs to be cleared.
            # Powerful mode sets fan speed to Turbo.
            self.setFan(kSamsungAcFanTurbo)
            self.setQuiet(False)  # Powerful 'on' is mutually exclusive to Quiet.
        else:
            self.remote_state[8] |= kSamsungAcPowerfulMask8  # Bit needs to be set.
            # Turning off Powerful mode sets fan speed to Auto if we were in Turbo mode
            if self.getFan() == kSamsungAcFanTurbo:
                self.setFan(kSamsungAcFanAuto)

    def getPowerful(self):
        return (
            not (self.remote_state[8] & kSamsungAcPowerfulMask8) and
            GETBITS8(
                self.remote_state[10],
                kSamsungAcPowerful10Offset,
                kSamsungAcPowerful10Offset
            ) and
            (self.getFan() == kSamsungAcFanTurbo)
        )
    
    def getRaw(self):
        self.checksum()
        return self.remote_state

    def setRaw(self, new_code, length=kSamsungAcStateLength):
        self.remote_state = new_code[:min(length, kSamsungAcExtendedStateLength)]

        # Shrink the extended state into a normal state.
        if length > kSamsungAcStateLength:
            for i in range(kSamsungAcStateLength, length):
                self.remote_state[i - kSamsungACSectionLength] = self.remote_state[i]

    @staticmethod
    def validChecksum(state, length=kSamsungAcStateLength):
        if length < kSamsungAcStateLength:
            return True  # No checksum to compare with. Assume okay.

        offset = 0
        if length >= kSamsungAcExtendedStateLength:
            offset = 7

        return (
            (
                GETBITS8(state[length - 6], kHighNibble, kNibbleSize) ==
                IRSamsungAc.calcChecksum(state, length)
            ) and
            (
                GETBITS8(state[length - (13 + offset)], kHighNibble, kNibbleSize) ==
                IRSamsungAc.calcChecksum(state, length - (7 + offset))
            )
        )
    
    @staticmethod
    def calcChecksum(state, length=kSamsungAcStateLength):
        sm = 0
        # Safety check so we don't go outside the array.
        if length < 7:
            return 255
        # Shamelessly inspired by:
        #   https:#github.com/adafruit/Raw-IR-decoder-for-Arduino/pull/3/files
        # Count most of the '1' bits after the checksum location.
        sm += countBits(state[length - 7], 8)
        sm -= countBits(GETBITS8(state[length - 6], kLowNibble, kNibbleSize), 8)
        sm += countBits(GETBITS8(state[length - 5], 1, 7), 8)
        sm += countBits(state + length - 4, 3)
        return GETBITS8(28 - sm, kLowNibble, kNibbleSize)
    
    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kSamsungAcCool
        if mode == stdAc.opmode_t.kHeat:
            return kSamsungAcHeat
        if mode == stdAc.opmode_t.kDry:
            return kSamsungAcDry
        if mode == stdAc.opmode_t.kFan:
            return kSamsungAcFan
        return kSamsungAcAuto

    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):
            return kSamsungAcFanLow

        if speed == stdAc.fanspeed_t.kMedium:
            return kSamsungAcFanMed
        if pseed == stdAc.fanspeed_t.kHigh:
            return kSamsungAcFanHigh
        if speed == stdAc.fanspeed_t.kMax:
            return kSamsungAcFanTurbo

        return kSamsungAcFanAuto
    
    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kSamsungAcCool:
            return stdAc.opmode_t.kCool
        if mode == kSamsungAcHeat:
            return stdAc.opmode_t.kHeat
        if mode == kSamsungAcDry:
            return stdAc.opmode_t.kDry
        if mode == kSamsungAcFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kSamsungAcFanTurbo:
            return stdAc.fanspeed_t.kMax
        if speed == kSamsungAcFanHigh:
            return stdAc.fanspeed_t.kHigh
        if speed == kSamsungAcFanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kSamsungAcFanLow:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.SAMSUNG_AC
        result.model = -1  # Not supported.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwing() else stdAc.swingv_t.kOff
        result.quiet = self.getQuiet()
        result.turbo = self.getPowerful()
        result.clean = self.getClean()
        result.beep = self.getBeep()
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.econo = False
        result.filter = False
        result.light = False
        result.sleep = -1
        result.clock = -1
        return result

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kSamsungAcAuto,
            kSamsungAcCool,
            kSamsungAcHeat,
            kSamsungAcDry,
            kSamsungAcFan
        )
        result += addTempToString(self.getTemp())
        result += addIntToString(self.getFan(), kFanStr)
        result += kSpaceLBraceStr

        speed = self.getFan()
        if speed in (
            kSamsungAcFanAuto,
            kSamsungAcFanAuto2
        ):
            result += kAutoStr

        elif speed == kSamsungAcFanLow:
            result += kLowStr
        elif speed == kSamsungAcFanMed:
            result += kMedStr
        elif speed == kSamsungAcFanHigh:
            result += kHighStr
        elif speed == kSamsungAcFanTurbo:
            result += kTurboStr
        else:
            result += kUnknownStr

        result += ')'

        result += addBoolToString(self.getSwing(), kSwingStr)
        result += addBoolToString(self.getBeep(), kBeepStr)
        result += addBoolToString(self.getClean(), kCleanStr)
        result += addBoolToString(self.getQuiet(), kQuietStr)
        result += addBoolToString(self.getPowerful(), kPowerfulStr)
        return result

    def checksum(self, length=kSamsungAcStateLength):
        # Update the checksum for the internal state.
        if length < 13:
            return
        setBits(
            self.remote_state[length - 6],
            kHighNibble,
            kNibbleSize,
            self.calcChecksum(self.remote_state, length)
        )
        setBits(
            self.remote_state[length - 13],
            kHighNibble,
            kNibbleSize,
            self.calcChecksum(remote_state, length - 7)
        )


addBoolToString = irutils.addBoolToString
addFanToString = irutils.addFanToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits


# Send a Samsung formatted message.
# Samsung has a separate message to indicate a repeat, like NEC does.
# TODO(crankyoldgit): Confirm that is actually how Samsung sends a repeat.
#                     The refdoc doesn't indicate it is True.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The bit size of the message being sent. typically kSamsungBits.
#   repeat: The number of times the message is to be repeated.
#
# Status: BETA / Should be working.
#
# Ref: http:#elektrolab.wz.cz/katalog/samsung_protocol.pdf
def sendSAMSUNG(data, nbits, repeat):
    sendGeneric(
        kSamsungHdrMark, 
        kSamsungHdrSpace, 
        kSamsungBitMark,
        kSamsungOneSpace, 
        kSamsungBitMark, 
        kSamsungZeroSpace,
        kSamsungBitMark, 
        kSamsungMinGap, 
        kSamsungMinMessageLength, 
        data,
        nbits, 
        38, 
        True, 
        repeat, 
        33
    )


# Construct a raw Samsung message from the supplied customer(address) &
# command.
#
# Args:
#   customer: The customer code. (aka. Address)
#   command:  The command code.
# Returns:
#   A raw 32-bit Samsung message suitable for sendSAMSUNG().
#
# Status: BETA / Should be working.
def encodeSAMSUNG(customer, command):
    revcustomer = reverseBits(customer, len(customer) * 8)
    revcommand = reverseBits(command, len(command) * 8)
    return (
        (revcommand ^ 0xFF) | 
        (revcommand << 8) | 
        (revcustomer << 16) |
        (revcustomer << 24)
    )


# Decode the supplied Samsung message.
# Samsung messages whilst 32 bits in size, only contain 16 bits of distinct
# data. e.g. In transmition order:
#   customer_byte + customer_byte(same) + address_byte + invert(address_byte)
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion. Typically kSamsungBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE
#
# Note:
#   LG 32bit protocol appears near identical to the Samsung protocol.
#   They differ on their compliance criteria and how they repeat.
# Ref:
#  http:#elektrolab.wz.cz/katalog/samsung_protocol.pdf
def decodeSAMSUNG(results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader + kFooter - 1:
        return False  # Can't possibly be a valid Samsung message.
    
    if strict and nbits != kSamsungBits:
        return False  # We expect Samsung to be 32 bits of message.

    data = 0
    offset = kStartOffset
    
    # Match Header + Data + Footer
    if not matchGeneric(
        results,
        rawbuf + offset,
        data,
        results.None - offset, 
        nbits,
        kSamsungHdrMark, 
        kSamsungHdrSpace,
        kSamsungBitMark, 
        kSamsungOneSpace,
        kSamsungBitMark, 
        kSamsungZeroSpace,
        kSamsungBitMark, 
        kSamsungMinGap, 
        True
    ):
        return False
    # Compliance
    # According to the spec, the customer (address) code is the first 8
    # transmitted bits. It's then repeated. Check for that.
    address = data >> 24
    
    if strict and address != ((data >> 16) & 0xFF):
        return False
    # Spec says the command code is the 3rd block of transmitted 8-bits,
    # followed by the inverted command code.
    command = (data & 0xFF00) >> 8
    
    if strict and command != ((data & 0xFF) ^ 0xFF):
        return False
    
    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = SAMSUNG
    # command & address need to be reversed as they are transmitted LSB first,
    results.command = reverseBits(command, sizeof(command) * 8)
    results.address = reverseBits(address, sizeof(address) * 8)
    return True


# Send a Samsung 36-bit formatted message.
#
# Args:
#   data:   The message to be sent.
#   nbits:  The bit size of the message being sent. typically kSamsung36Bits.
#   repeat: The number of times the message is to be repeated.
#
# Status: Alpha / Experimental.
#
# Note:
#   Protocol is used by Samsung Bluray Remote: ak59-00167a
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/621
def sendSamsung36(data, nbits, repeat):
    if nbits < 16:
        return  # To small to send.
  
    for _ in range(repeat + 1):
        # Block #1 (16 bits)
        sendGeneric(
            kSamsungHdrMark, 
            kSamsungHdrSpace,
            kSamsungBitMark, 
            kSamsungOneSpace,
            kSamsungBitMark, 
            kSamsungZeroSpace,
            kSamsungBitMark, 
            kSamsungHdrSpace,
            data >> (nbits - 16), 
            16, 
            38, 
            True, 
            0, 
            kDutyDefault
        )
        
        # Block #2 (The rest, typically 20 bits)
        sendGeneric(
            0, 
            0,  # No header
            kSamsungBitMark, 
            kSamsungOneSpace,
            kSamsungBitMark, 
            kSamsungZeroSpace,
            kSamsungBitMark, 
            kSamsungMinGap,  # Gap is just a guess.
            # Mask off the rest of the bits.
            data & ((1 << (nbits - 16)) - 1),
            nbits - 16, 
            38, 
            True, 
            0, 
            kDutyDefault
        )


# Decode the supplied Samsung36 message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kSamsung36Bits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Experimental
#
# Note:
#   Protocol is used by Samsung Bluray Remote: ak59-00167a
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/621
def decodeSamsung36(results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader + kFooter * 2 - 1:
        return False  # Can't possibly be a valid Samsung message.
    # We need to be looking for > 16 bits to make sense.
    if nbits <= 16:
        return False
    if strict and nbits != kSamsung36Bits:
        return False  # We expect nbits to be 36 bits of message.

    data = 0
    offset = kStartOffset

    # Match Header + Data + Footer

    used = matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        16,
        kSamsungHdrMark,
        kSamsungHdrSpace,
        kSamsungBitMark,
        kSamsungOneSpace,
        kSamsungBitMark,
        kSamsungZeroSpace,
        kSamsungBitMark,
        kSamsungHdrSpace,
        False
    )

    if not used:
        return False

    offset += used
    # Data (Block #2)
    data2 = 0
    if not matchGeneric(
        results.rawbuf + offset,
        data2,
        results.rawlen - offset,
        nbits - 16,
        0,
        0,
        kSamsungBitMark,
        kSamsungOneSpace,
        kSamsungBitMark,
        kSamsungZeroSpace,
        kSamsungBitMark,
        kSamsungMinGap,
        True
    ):
        return False

    data <<= (nbits - 16)
    data += data2

    # Success
    results.bits = nbits
    results.value = data
    results.decode_type = SAMSUNG36
    results.command = data & ((1 << (nbits - 16)) - 1)
    results.address = data >> (nbits - 16)
    return True


# Send a Samsung A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kSamsungAcStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: Stable / Known working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/505
def sendSamsungAC(data, nbytes, repeat):
    if nbytes < kSamsungAcStateLength and nbytes % kSamsungACSectionLength:
        return  # Not an appropriate number of bytes to send a proper message.

    enableIROut(38)
    for r in range(repeat + 1):
        # Header
        mark(kSamsungAcHdrMark)
        space(kSamsungAcHdrSpace)
        # Send in 7 byte sections.
        for offset in range(0, nbytes, kSamsungACSectionLength):
            sendGeneric(
                kSamsungAcSectionMark,
                kSamsungAcSectionSpace,
                kSamsungAcBitMark,
                kSamsungAcOneSpace,
                kSamsungAcBitMark,
                kSamsungAcZeroSpace,
                kSamsungAcBitMark,
                kSamsungAcSectionGap,
                data + offset,
                kSamsungACSectionLength,  # 7 bytes == 56 bits
                38000,
                False,
                0,
                50
            )                    # Send in LSBF order

        # Complete made up guess at inter-message gap.
        space(kDefaultMessageGap - kSamsungAcSectionGap)


# Decode the supplied Samsung A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kSamsungAcBits
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Stable / Known to be working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/505
def decodeSamsungAC(results, nbits, strict):
    if results.rawlen < 2 * nbits + kHeader * 3 + kFooter * 2 - 1:
        return False  # Can't possibly be a valid Samsung A/C message.

    if nbits != kSamsungAcBits and nbits != kSamsungAcExtendedBits:
        return False

    offset = kStartOffset

    # Message Header
    offset += 1
    if not matchMark(results.rawbuf[offset], kSamsungAcBitMark):
        return False

    offset += 1
    if not matchSpace(results.rawbuf[offset], kSamsungAcHdrSpace):
        return False

    # Section(s)
    for pos in range(0, (nbits / 8) - kSamsungACSectionLength, kSamsungACSectionLength):

        # Section Header + Section Data (7 bytes) + Section Footer
        used = matchGeneric(
            results.rawbuf + offset,
            results.state + pos,
            results.rawlen - offset,
            kSamsungACSectionLength * 8,
            kSamsungAcSectionMark,
            kSamsungAcSectionSpace,
            kSamsungAcBitMark,
            kSamsungAcOneSpace,
            kSamsungAcBitMark,
            kSamsungAcZeroSpace,
            kSamsungAcBitMark,
            kSamsungAcSectionGap,
            pos + kSamsungACSectionLength >= nbits / 8,
            _tolerance,
            0,
            False
        )

        if used == 0:
            return False

        offset += used

    # Compliance
    # Is the signature correct?

    if results.state[0] != 0x02 or results.state[2] != 0x0F:
        return False

    if strict and not IRSamsungAc.validChecksum(results.state, nbits / 8):
        return False

    # Success
    results.decode_type = SAMSUNG_AC
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True
