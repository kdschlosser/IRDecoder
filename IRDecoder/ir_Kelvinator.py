# -*- coding: utf-8 -*-

# Kelvinator A/C
#
# Copyright 2016 David Conran

# Supports:
#   Brand: Kelvinator,  Model: YALIF Remote
#   Brand: Kelvinator,  Model: KSV26CRC A/C
#   Brand: Kelvinator,  Model: KSV26HRC A/C
#   Brand: Kelvinator,  Model: KSV35CRC A/C
#   Brand: Kelvinator,  Model: KSV35HRC A/C
#   Brand: Kelvinator,  Model: KSV53HRC A/C
#   Brand: Kelvinator,  Model: KSV62HRC A/C
#   Brand: Kelvinator,  Model: KSV70CRC A/C
#   Brand: Kelvinator,  Model: KSV70HRC A/C
#   Brand: Kelvinator,  Model: KSV80HRC A/C
#   Brand: Green,  Model: YAPOF3 remote

# Copyright 2016 David Conran
#
# Code to emulate IR Kelvinator YALIF remote control unit, which should control
# at least the following Kelvinator A/C units:
# KSV26CRC, KSV26HRC, KSV35CRC, KSV35HRC, KSV53HRC, KSV62HRC, KSV70CRC,
# KSV70HRC, KSV80HRC.
#
# Note:
# * Unsupported:
#    - All Sleep modes.
#    - All Timer modes.
#    - "I Feel" button & mode.
#    - Energy Saving mode.
#    - Low Heat mode.
#    - Fahrenheit.


from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *
from .IRac import *


# Constants
kKelvinatorAuto = 0
kKelvinatorCool = 1
kKelvinatorDry = 2
kKelvinatorFan = 3
kKelvinatorHeat = 4
kKelvinatorBasicFanMax = 3
kKelvinatorFanAuto = 0
kKelvinatorFanMin = 1
kKelvinatorFanMax = 5
kKelvinatorMinTemp = 16   # 16C
kKelvinatorMaxTemp = 30   # 30C
kKelvinatorAutoTemp = 25  # 25C

kKelvinatorTick = 85
kKelvinatorHdrMarkTicks = 106
kKelvinatorHdrMark = kKelvinatorHdrMarkTicks * kKelvinatorTick
kKelvinatorHdrSpaceTicks = 53
kKelvinatorHdrSpace = kKelvinatorHdrSpaceTicks * kKelvinatorTick
kKelvinatorBitMarkTicks = 8
kKelvinatorBitMark = kKelvinatorBitMarkTicks * kKelvinatorTick
kKelvinatorOneSpaceTicks = 18
kKelvinatorOneSpace = kKelvinatorOneSpaceTicks * kKelvinatorTick
kKelvinatorZeroSpaceTicks = 6
kKelvinatorZeroSpace = kKelvinatorZeroSpaceTicks * kKelvinatorTick
kKelvinatorGapSpaceTicks = 235
kKelvinatorGapSpace = kKelvinatorGapSpaceTicks * kKelvinatorTick

kKelvinatorCmdFooter = 2
kKelvinatorCmdFooterBits = 3

kKelvinatorModeOffset = 0  # Mask 0b111
kKelvinatorPowerOffset = 3
kKelvinatorFanOffset = 4  # Mask 0b111
kKelvinatorFanSize = 3  # Bits
kKelvinatorBasicFanSize = 2  # Bits, Mask 0b011
kKelvinatorChecksumStart = 10
kKelvinatorVentSwingOffset = 6
kKelvinatorVentSwingVOffset = 0
kKelvinatorVentSwingHOffset = 4
kKelvinatorQuietOffset = 7
kKelvinatorIonFilterOffset = 6
kKelvinatorLightOffset = 5
kKelvinatorXfanOffset = 7
kKelvinatorTurboOffset = 4

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits

# Legacy defines (Deprecated)
KELVINATOR_MIN_TEMP = kKelvinatorMinTemp
KELVINATOR_MAX_TEMP = kKelvinatorMaxTemp
KELVINATOR_HEAT = kKelvinatorHeat
KELVINATOR_FAN_MAX = kKelvinatorFanMax
KELVINATOR_FAN_AUTO = kKelvinatorFanAuto
KELVINATOR_FAN = kKelvinatorFan
KELVINATOR_DRY = kKelvinatorDry
KELVINATOR_COOL = kKelvinatorCool
KELVINATOR_BASIC_FAN_MAX = kKelvinatorBasicFanMax
KELVINATOR_AUTO_TEMP = kKelvinatorAutoTemp
KELVINATOR_AUTO = kKelvinatorAuto


#       Kelvinator AC map
# 
# (header mark and space)
# byte 0 = Basic Modes
#   b2-0 = Modes
#     Modes:
#       000 = Auto (temp = 25C)
#       001 = Cool
#       010 = Dry (temp = 25C, but not shown)
#       011 = Fan
#       100 = Heat
#   b3 = Power Status (1 = On, 0 = Off)
#   b5-4 = Fan (Basic modes)
#     Fan:
#       00 = Auto
#       01 = Fan 1
#       10 = Fan 2
#       11 = Fan 3 or higher (See byte 14)
#   b6 = Vent swing (1 = On, 0 = Off) (See byte 4)
#   b7 = Sleep Modes 1 & 3 (1 = On, 0 = Off)
# byte 1 = Temperature
#   b3-0: Degrees C.
#     0000 (0) = 16C
#     0001 (1) = 17C
#     0010 (2) = 18C
#     ...
#     1101 (13) = 29C
#     1110 (14) = 30C
# byte 2 = Extras
#   b3-0 = UNKNOWN, typically 0.
#   b4 = Turbo Fan (1 = On, 0 = Off)
#   b5 = Light (Display) (1 = On, 0 = Off)
#   b6 = Ion Filter (1 = On, 0 = Off)
#   b7 = X-Fan (Fan runs for a while after power off) (1 = On, 0 = Off)
# byte 3 = Section Indicator
#   b3-0 = Unused (Typically 0)
#   b5-4 = Unknown (possibly timer related) (Typically 0b01)
#   b7-6 = End of command block (B01)
# (B010 marker and a gap of 20ms)
# byte 4 = Extended options
#   b0 = Swing Vent Vertical (1 = On, 0 = Off)
#   b4 = Swing Vent Horizontal (1 = On, 0 = Off)
# byte 5-6 = Timer related. Typically 0 except when timer in use.
# byte 7 = checksum
#   b3-0 = Unknown (Used in Timer mode)
#   b7-4 = checksum of the previous bytes (0-6)
# (gap of 40ms)
# (header mark and space)
# byte 8 = Repeat of byte 0
# byte 9 = Repeat of byte 1
# byte 10 = Repeat of byte 2
# byte 11 = Section Indicator
#   b3-0 = Unused (Typically 0)
#   b5-4 = Unknown (possibly timer related) (Typically 0b11)
#   b7-6 = End of command block (B01)
# (B010 marker and a gap of 20ms)
# byte 12 = Extended options
#   b0 = Sleep mode 2 (1 = On, 0=Off)
#   b6-1 = Unknown (Used in Sleep Mode 3, Typically 0b000000)
#   b7 = Quiet Mode (1 = On, 0=Off)
# byte 13 = Unknown (Sleep Mode 3 related, Typically 0x00)
# byte 14 = Fan control
#   b3-0 = Unknown (Sleep Mode 3 related, Typically 0b0000)
#   b6-4 = Fan speed
#      0b000 (0) = Automatic
#      0b001 (1) = Fan 1
#      0b010 (2) = Fan 2
#      0b011 (3) = Fan 3
#      0b100 (4) = Fan 4
#      0b101 (5) = Fan 5
# byte 15 = checksum
#   b3-0 = Unknown (Typically 0b0000)
#   b7-4 = checksum of the previous bytes (8-14)
 
 
# Classes
class IRKelvinatorAC(object):
    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kKelvinatorStateLength
        self._irsend = IRSend(pin, inverted, use_modulation)

        self.stateReset()

    def stateReset(self):
        self.remote_state = [0x0] * kKelvinatorStateLength
        self.remote_state[3] = 0x50
        self.remote_state[11] = 0x70
    
    def send(self, repeat=kKelvinatorDefaultRepeat):
        self.fixup()  # Ensure correct settings before sending.
        self._irsend.sendKelvinator(self.remote_state, kKelvinatorStateLength, repeat)
    
    def calibrate(self):
        return self._irsend.calibrate()
        
    def begin(self):
        self._irsend.begin()
        
    def on(self):
        self.setPower(True)
        
    def off(self):
        self.setPower(False)

    def setPower(self, on):
        setBit(self.remote_state[0], kKelvinatorPowerOffset, on)
        self.remote_state[8] = self.remote_state[0]  # Duplicate to the 2nd command chunk.
    
    def getPower(self):
        return GETBIT8(self.remote_state[0], kKelvinatorPowerOffset)

    def setTemp(self, degrees):
        # Set the temp. in deg C
        temp = max(kKelvinatorMinTemp, degrees)
        temp = min(kKelvinatorMaxTemp, temp)
        setBits(self.remote_state[1], kLowNibble, kNibbleSize, temp - kKelvinatorMinTemp)
        self.remote_state[9] = self.remote_state[1]  # Duplicate to the 2nd command chunk.

    def getTemp(self):
        # Return the set temp. in deg C
        return GETBITS8(self.remote_state[1], kLowNibble, kNibbleSize) + kKelvinatorMinTemp
    
    def setFan(self, speed):
        # Set the speed of the fan, 0-5, 0 is auto, 1-5 is the speed
        fan = min(kKelvinatorFanMax, speed)  # Bounds check

        # Only change things if we need to.
        if fan != self.getFan():
            # Set the basic fan values.
            setBits(
                self.remote_state[0],
                kKelvinatorFanOffset,
                kKelvinatorBasicFanSize,
                min(kKelvinatorBasicFanMax, fan)
            )
            self.remote_state[8] = self.remote_state[0]  # Duplicate to the 2nd command chunk.
            # Set the advanced(?) fan value.
            setBits(self.remote_state[14], kKelvinatorFanOffset, kKelvinatorFanSize, fan)
            # Turbo mode is turned off if we change the fan settings.
            self.setTurbo(False)
    
    def getFan(self):
        return GETBITS8(self.remote_state[14], kKelvinatorFanOffset, kKelvinatorFanSize)

    def setMode(self, mode):
        if mode in (
            kKelvinatorAuto,
            kKelvinatorDry,
            kKelvinatorHeat,
            kKelvinatorCool,
            kKelvinatorFan
        ):

            if mode in (
                kKelvinatorAuto,
                kKelvinatorDry
            ):
                # When the remote is set to Auto or Dry, it defaults to 25C and doesn't
                # show it.
                self.setTemp(kKelvinatorAutoTemp)
                # FALL-THRU

            setBits(self.remote_state[0], kKelvinatorModeOffset, kModeBitsSize, mode)
            self.remote_state[8] = self.remote_state[0]  # Duplicate to the 2nd command chunk.

        else:  # If we get an unexpected mode, default to AUTO.
            self.setMode(kKelvinatorAuto)

    def getMode(self):
        return GETBITS8(self.remote_state[0], kKelvinatorModeOffset, kModeBitsSize)
    
    def setSwingVertical(self, on):
        setBit(self.remote_state[4], kKelvinatorVentSwingVOffset, on)
        setBit(self.remote_state[0], kKelvinatorVentSwingOffset, on or self.getSwingHorizontal())
        self.remote_state[8] = self.remote_state[0]  # Duplicate to the 2nd command chunk.
    
    def getSwingVertical(self):
        return GETBIT8(self.remote_state[4], kKelvinatorVentSwingVOffset)

    def setSwingHorizontal(self, on):
        setBit(self.remote_state[4], kKelvinatorVentSwingHOffset, on)
        setBit(self.remote_state[0], kKelvinatorVentSwingOffset, on or self.getSwingVertical())
        self.remote_state[8] = self.remote_state[0]  # Duplicate to the 2nd command chunk.
    
    def getSwingHorizontal(self):
        return GETBIT8(self.remote_state[4], kKelvinatorVentSwingHOffset)

    def setQuiet(self, on):
        setBit(self.remote_state[12], kKelvinatorQuietOffset, on)

    def getQuiet(self):
        return GETBIT8(self.remote_state[12], kKelvinatorQuietOffset)
    
    def setIonFilter(self, on):
        setBit(self.remote_state[2], kKelvinatorIonFilterOffset, on)
        self.remote_state[10] = self.remote_state[2]  # Duplicate to the 2nd command chunk.
    
    def getIonFilter(self):
        return GETBIT8(self.remote_state[2], kKelvinatorIonFilterOffset)

    def setLight(self, on):
        setBit(self.remote_state[2], kKelvinatorLightOffset, on)
        self.remote_state[10] = self.remote_state[2]  # Duplicate to the 2nd command chunk.
    
    def getLight(self):
        return GETBIT8(self.remote_state[2], kKelvinatorLightOffset)
    
    def setXFan(self, on):
        # Note: XFan mode is only valid in Cool or Dry mode.
        setBit(self.remote_state[2], kKelvinatorXfanOffset, on)
        self.remote_state[10] = self.remote_state[2]  # Duplicate to the 2nd command chunk.
    
    def getXFan(self):
        return GETBIT8(self.remote_state[2], kKelvinatorXfanOffset)

    def setTurbo(self, on):
        # Note: Turbo mode is turned off if the fan speed is changed.
        setBit(self.remote_state[2], kKelvinatorTurboOffset, on)
        self.remote_state[10] = self.remote_state[2]  # Duplicate to the 2nd command chunk.
    
    def getTurbo(self):
        return GETBIT8(self.remote_state[2], kKelvinatorTurboOffset)

    def getRaw(self):
        self.fixup()  # Ensure correct settings before sending.
        return self.remote_state[:]
    
    def setRaw(self, new_code):
        self.remote_state = new_code[:kKelvinatorStateLength]
    
    @staticmethod
    def calcBlockChecksum(block, length=kKelvinatorStateLength / 2):
        sm = kKelvinatorChecksumStart
        # Sum the lower half of the first 4 bytes of this block.
        i = 0

        while i < 4 and i < length - 1:
            sm += block & 0b1111
            i += 1
            block += 1

        # then sum the upper half of the next 3 bytes.
        i = 4

        while i < length - 1:
            sm += block >> 4
            i += 1
            block += 1

        # Trim it down to fit into the 4 bits allowed. i.e. Mod 16.
        return sm & 0b1111

    @staticmethod
    def validChecksum(state, length=kKelvinatorStateLength):
        # Verify the checksum is valid for a given state.
        # Args:
        #   state:  The array to verify the checksum of.
        #   length: The size of the state.
        # Returns:
        #   A boolean.
        offset = 0
        while offset + 7 < length:
            # Top 4 bits of the last byte in the block is the block's checksum.
            if GETBITS8(state[offset + 7], kHighNibble, kNibbleSize) != self.calcBlockChecksum(state + offset):
                return False
            offset += 8

        return True
    
    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kKelvinatorCool
        if mode == stdAc.opmode_t.kHeat:
            return kKelvinatorHeat
        if mode == stdAc.opmode_t.kDry:
            return kKelvinatorDry
        if mode == stdAc.opmode_t.kFan:
            return kKelvinatorFan

        return kKelvinatorAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kKelvinatorCool:
            return stdAc.opmode_t.kCool
        if mode == kKelvinatorHeat:
            return stdAc.opmode_t.kHeat
        if mode == kKelvinatorDry:
            return stdAc.opmode_t.kDry
        if mode == kKelvinatorFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        return getattr(stdAc.fanspeed_t, speed)
    
    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.KELVINATOR
        result.model = -1  # Unused.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwingVertical() else stdAc.swingv_t.kOff
        result.swingh = stdAc.swingh_t.kAuto if self.getSwingHorizontal() else stdAc.swingh_t.kOff
        result.quiet = self.getQuiet()
        result.turbo = self.getTurbo()
        result.light = self.getLight()
        result.filter = self.getIonFilter()
        result.clean = self.getXFan()
        # Not supported.
        result.econo = False
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
            kKelvinatorAuto,
            kKelvinatorCool,
            kKelvinatorHeat,
            kKelvinatorDry,
            kKelvinatorFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kKelvinatorFanMax,
            kKelvinatorFanMin,
            kKelvinatorFanAuto,
            kKelvinatorFanAuto,
            kKelvinatorBasicFanMax
        )
        result += addBoolToString(self.getTurbo(), kTurboStr)
        result += addBoolToString(self.getQuiet(), kQuietStr)
        result += addBoolToString(self.getXFan(), kXFanStr)
        result += addBoolToString(self.getIonFilter(), kIonStr)
        result += addBoolToString(self.getLight(), kLightStr)
        result += addBoolToString(self.getSwingHorizontal(), kSwingHStr)
        result += addBoolToString(self.getSwingVertical(), kSwingVStr)
        return result
  
    def checksum(self, length=kKelvinatorStateLength):
        # Many Bothans died to bring us this information.
        # For each command + options block.
        offset = 0
        while offset + 7 < length:
            setBits(
                self.remote_state[7 + offset],
                kHighNibble,
                kNibbleSize,
                self.calcBlockChecksum(remote_state[offset])
            )
            offset += 8

    def fixup(self):
        # X-Fan mode is only valid in COOL or DRY modes.
        if (
            self.getMode() != kKelvinatorCool and
            self.getMode() != kKelvinatorDry
        ):
            self.setXFan(False)
            self.checksum()  # Calculate the checksums


# Send a Kelvinator A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. (>=kKelvinatorStateLength)
#   repeat: Nr. of times the message is to be repeated. (Default = 0).
#
# Status: STABLE / Known working.
#
def sendKelvinator(data, nbytes, repeat):
    if nbytes < kKelvinatorStateLength:
        return  # Not enough bytes to send a proper message.

    for _ in range(repeat + 1):
        
        # Command Block #1 (4 bytes)
        sendGeneric(
            kKelvinatorHdrMark, 
            kKelvinatorHdrSpace, 
            kKelvinatorBitMark,
            kKelvinatorOneSpace, 
            kKelvinatorBitMark, 
            kKelvinatorZeroSpace,
            0, 
            0,  # No Footer yet.
            data, 
            4, 
            38, 
            False, 
            0, 
            50
        )
        
        # Send Footer for the command block (3 bits (b010))
        sendGeneric(
            0, 
            0,  # No Header
            kKelvinatorBitMark, 
            kKelvinatorOneSpace, 
            kKelvinatorBitMark,
            kKelvinatorZeroSpace, 
            kKelvinatorBitMark, 
            kKelvinatorGapSpace,
            kKelvinatorCmdFooter, 
            kKelvinatorCmdFooterBits, 
            38, 
            False, 
            0,
            50
        )
        # Data Block #1 (4 bytes)
        sendGeneric(
            0, 
            0,  # No header
            kKelvinatorBitMark, 
            kKelvinatorOneSpace, 
            kKelvinatorBitMark,
            kKelvinatorZeroSpace, 
            kKelvinatorBitMark,
            kKelvinatorGapSpace * 2, 
            data + 4, 
            4, 
            38, 
            False, 
            0, 
            50
        )
        # Command Block #2 (4 bytes)
        sendGeneric(
            kKelvinatorHdrMark, 
            kKelvinatorHdrSpace, 
            kKelvinatorBitMark,
            kKelvinatorOneSpace, 
            kKelvinatorBitMark, 
            kKelvinatorZeroSpace,
            0, 
            0,  # No Footer yet.
            data + 8, 
            4, 
            38, 
            False, 
            0, 
            50
        )
        # Send Footer for the command block (3 bits (B010))
        sendGeneric(
            0, 
            0,  # No Header
            kKelvinatorBitMark, 
            kKelvinatorOneSpace, 
            kKelvinatorBitMark,
            kKelvinatorZeroSpace, 
            kKelvinatorBitMark, 
            kKelvinatorGapSpace,
            kKelvinatorCmdFooter, 
            kKelvinatorCmdFooterBits, 
            38,
            False, 
            0,
            50
        )
        # Data Block #2 (4 bytes)
        sendGeneric(
            0, 
            0,  # No header
            kKelvinatorBitMark, 
            kKelvinatorOneSpace, 
            kKelvinatorBitMark,
            kKelvinatorZeroSpace, 
            kKelvinatorBitMark,
            kKelvinatorGapSpace * 2, 
            data + 12, 
            4,
            38,
            False, 
            0,
            50
        )


# Decode the supplied Kelvinator message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kKelvinatorBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Known working.
def decodeKelvinator(results, nbits, strict):
    if (
        results.rawlen <
        2 * (nbits + kKelvinatorCmdFooterBits) + (kHeader + kFooter + 1) * 2 - 1
    ):
        return False  # Can't possibly be a valid Kelvinator message.

    if strict and nbits != kKelvinatorBits:
        return False  # Not strictly a Kelvinator message.

    offset = kStartOffset

    # There are two messages back-to-back in a full Kelvinator IR message
    # sequence.
    pos = 0
    for s in range(2):
        # Header + Data Block #1 (32 bits)
        used = matchGeneric(
            results.rawbuf + offset,
            results.state + pos,
            results.rawlen - offset,
            32,
            kKelvinatorHdrMark,
            kKelvinatorHdrSpace,
            kKelvinatorBitMark,
            kKelvinatorOneSpace,
            kKelvinatorBitMark,
            kKelvinatorZeroSpace,
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
        pos += 4

        # Command data footer (3 bits, B010)
        data_result = matchData(
            results.rawbuf[offset],
            kKelvinatorCmdFooterBits,
            kKelvinatorBitMark,
            kKelvinatorOneSpace,
            kKelvinatorBitMark,
            kKelvinatorZeroSpace,
            _tolerance,
            kMarkExcess,
            False
        )

        if data_result.success is False:
            return False

        if data_result.data != kKelvinatorCmdFooter:
            return False

        offset += data_result.used

        # Gap + Data (Options) (32 bits)
        used = matchGeneric(
            results.rawbuf + offset,
            results.state + pos,
            results.rawlen - offset,
            32,
            kKelvinatorBitMark,
            kKelvinatorGapSpace,
            kKelvinatorBitMark,
            kKelvinatorOneSpace,
            kKelvinatorBitMark,
            kKelvinatorZeroSpace,
            kKelvinatorBitMark,
            kKelvinatorGapSpace * 2,
            s > 0,
            _tolerance,
            kMarkExcess,
            False
        )
        if used == 0:
            return False

        offset += used
        pos += 4

    # Compliance
    # Verify the message's checksum is correct.
    if strict and not IRKelvinatorAC.validChecksum(results.state):
        return False

    # Success
    results.decode_type = decode_type_t.KELVINATOR
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result.state, we don't record value, address, or command as it
    # is a union data type.
    return True
