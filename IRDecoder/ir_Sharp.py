# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2017, 2019 David Conran

# Sharp remote emulation

# Equipment it seems compatible with:
#  * Sharp LC-52D62U
#  * <Add models (devices & remotes) you've gotten it working with here>
#

# Copyright 2019 crankyoldgit

# Supports:
#   Brand: Sharp,  Model: LC-52D62U TV
#   Brand: Sharp,  Model: AY-ZP40KR A/C

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Constants
kSharpAcHdrMark = 3800
kSharpAcHdrSpace = 1900
kSharpAcBitMark = 470
kSharpAcZeroSpace = 500
kSharpAcOneSpace = 1400
kSharpAcGap = kDefaultMessageGap

kSharpAcAuto = 0b000
kSharpAcDry = 0b011
kSharpAcCool = 0b010
kSharpAcHeat = 0b001
kSharpAcMinTemp = 15  # Celsius
kSharpAcMaxTemp = 30  # Celsius
kSharpAcFanAuto = 0b010  # 2
kSharpAcFanMin = 0b100  # 4 (FAN1)
kSharpAcFanMed = 0b011  # 3 (FAN2)
kSharpAcFanHigh = 0b101  # 5 (FAN3)
kSharpAcFanMax = 0b111  # 7 (FAN4)
kSharpAcByteTemp = 4
kSharpAcBytePower = 5
kSharpAcBitPowerOffset = 4
kSharpAcBitModeNonAutoOffset = 5  # 0b00100000
kSharpAcByteMode = 6
kSharpAcModeSize = 2  # Mask 0b00000011
kSharpAcByteFan = kSharpAcByteMode
kSharpAcFanOffset = 4  # Mask 0b01110000
kSharpAcFanSize = 3  # Nr. of Bits
kSharpAcByteManual = 10
kSharpAcBitFanManualOffset = 0   # 0b00000001
kSharpAcBitTempManualOffset = 2  # 0b00000100

# Constants
# period time = 1/38000Hz = 26.316 microseconds.
# Ref:
#   GlobalCache's IR Control Tower data.
#   http:#www.sbprojects.com/knowledge/ir/sharp.php
kSharpTick = 26
kSharpBitMarkTicks = 10
kSharpBitMark = kSharpBitMarkTicks * kSharpTick
kSharpOneSpaceTicks = 70
kSharpOneSpace = kSharpOneSpaceTicks * kSharpTick
kSharpZeroSpaceTicks = 30
kSharpZeroSpace = kSharpZeroSpaceTicks * kSharpTick
kSharpGapTicks = 1677
kSharpGap = kSharpGapTicks * kSharpTick
# Address(5) + Command(8) + Expansion(1) + Check(1)
kSharpToggleMask = (1 << (kSharpBits - kSharpAddressBits)) - 1
kSharpAddressMask = (1 << kSharpAddressBits) - 1
kSharpCommandMask = (1 << kSharpCommandBits) - 1

addBoolToString = irutils.addBoolToString
addFanToString = irutils.addFanToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits


class IRSharpAc(object):

    def __init__(self, pin, inverted=False, use_modulation=True):
        self.remote = [0x0] * kSharpAcStateLength
        self._sendir = SendIR(pin, inverted, use_modulation)
        self.stateReset()
        
    def send(self, repeat=kSharpAcDefaultRepeat):
        self._irsend.sendSharpAc(self.getRaw(), kSharpAcStateLength, repeat)

    def calibrate(self):
        return self._irsend.calibrate()
    
    def begin(self):
        self._sendir.begin()
        
    def on(self):
        self.setPower(True)
        
    def off(self):
        self.setPower(False)
        
    def setPower(self, on):
        setBit(self.remote[kSharpAcBytePower], kSharpAcBitPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote[kSharpAcBytePower], kSharpAcBitPowerOffset)
    
    def setTemp(self, temp):
        # Set the temp in deg C
        mode = self.getMode()
        # Auto & Dry don't allow temp changes and have a special temp.
        if mode in (
            kSharpAcAuto,
            kSharpAcDry
        ):
            self.remote[kSharpAcByteTemp] = 0
            self.remote[kSharpAcByteManual] = 0  # When in Dry/Auto this byte is 0.
        else:
            self.remote[kSharpAcByteTemp] = 0xC0
            setBit(self.remote[kSharpAcByteManual], kSharpAcBitTempManualOffset)

            degrees = max(temp, kSharpAcMinTemp)
            degrees = min(degrees, kSharpAcMaxTemp)
            setBits(self.remote[kSharpAcByteTemp], kLowNibble, kNibbleSize, degrees - kSharpAcMinTemp)

    def getTemp(self):
        return GETBITS8(self.remote[kSharpAcByteTemp], kLowNibble, kNibbleSize) + kSharpAcMinTemp

    def setFan(self, fan):
        # Set the speed of the fan
        if fan in (
            kSharpAcFanAuto,
            kSharpAcFanMin,
            kSharpAcFanMed,
            kSharpAcFanHigh,
            kSharpAcFanMax
        ):
            setBit(self.remote[kSharpAcByteManual], kSharpAcBitFanManualOffset, fan != kSharpAcFanAuto)
            setBits(self.remote[kSharpAcByteFan], kSharpAcFanOffset, kSharpAcFanSize, fan)
        else:
            self.setFan(kSharpAcFanAuto)
    
    def getFan(self):
        return GETBITS8(self.remote[kSharpAcByteFan], kSharpAcFanOffset, kSharpAcFanSize)

    def setMode(self, mode):
        setBit(self.remote[kSharpAcBytePower], kSharpAcBitModeNonAutoOffset, mode != kSharpAcAuto)

        if mode in (
            kSharpAcCool,
            kSharpAcHeat,
            kSharpAcAuto,
            kSharpAcDry
        ):
            if mode in (
                kSharpAcAuto,
                kSharpAcDry
            ):
                self.setTemp(0)  # Dry/Auto have no temp setting.
                # FALLTHRU

            setBits(self.remote[kSharpAcByteMode], kLowNibble, kSharpAcModeSize, mode)
        else:
            self.setMode(kSharpAcAuto)
    
    def getMode(self):
        return GETBITS8(self.remote[kSharpAcByteMode], kLowNibble, kSharpAcModeSize)

    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote[:]
    
    def setRaw(self, new_code, length=kSharpAcStateLength):
        self.remote = new_code[:min(length, kSharpAcStateLength)]

    @staticmethod
    def validChecksum(state, length=kSharpAcStateLength):
        # Verify the checksums are valid for a given state.
        # Args:
        #   state:  The array to verify the checksums of.
        #   length: The size of the state.
        # Returns:
        #   A boolean.
        return GETBITS8(state[length - 1], kHighNibble, kNibbleSize) == IRSharpAc.calcChecksum(state, length)

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kSharpAcCool
        if mode == stdAc.opmode_t.kHeat:
            return kSharpAcHeat
        if mode == stdAc.opmode_t.kDry:
            return kSharpAcDry

        return kSharpAcAuto
    
    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed in (
            stdAc.fanspeed_t.kMin,
            stdAc.fanspeed_t.kLow
        ):
            return kSharpAcFanMin
        if speed == stdAc.fanspeed_t.kMedium:
            return kSharpAcFanMed
        if speed == stdAc.fanspeed_t.kHigh:
            return kSharpAcFanHigh
        if speed == stdAc.fanspeed_t.kMax:
            return kSharpAcFanMax

        return kSharpAcFanAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kSharpAcCool:
            return stdAc.opmode_t.kCool
        if mode == kSharpAcHeat:
            return stdAc.opmode_t.kHeat
        if mode == kSharpAcDry:
            return stdAc.opmode_t.kDry

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kSharpAcFanMax:
            return stdAc.fanspeed_t.kMax
        if speed == kSharpAcFanHigh:
            return stdAc.fanspeed_t.kHigh
        if speed == kSharpAcFanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kSharpAcFanMin:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.SHARP_AC
        result.model = -1  # Not supported.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        # Not supported.
        result.swingv = stdAc.swingv_t.kOff
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.turbo = False
        result.clean = False
        result.beep = False
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
            kSharpAcAuto,
            kSharpAcCool,
            kSharpAcHeat,
            kSharpAcDry,
            kSharpAcAuto
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kSharpAcFanMax,
            kSharpAcFanMin,
            kSharpAcFanAuto,
            kSharpAcFanAuto,
            kSharpAcFanMed
        )
        return result

    def stateReset(self):
        reset = [
            0xAA, 0x5A, 0xCF, 0x10, 0x00, 0x01, 0x00, 0x00, 0x08, 0x80, 0x00, 0xE0, 0x01
        ]
        self.remote = reset[:]
  
    def checksum(self):
        # Calculate and set the checksum values for the internal state.
        setBits(
            self.remote[kSharpAcStateLength - 1],
            kHighNibble,
            kNibbleSize,
            self.calcChecksum(remote)
        )

    @staticmethod
    def calcChecksum(state, length=kSharpAcStateLength):
        # Calculate the checksum for a given state.
        # Args:
        #   state:  The array to verify the checksums of.
        #   length: The size of the state.
        # Returns:
        #   The 4 bit checksum.
        xorsum = xorBytes(state, length - 1)
        xorsum ^= GETBITS8(state[length - 1], kLowNibble, kNibbleSize)
        xorsum ^= GETBITS8(xorsum, kHighNibble, kNibbleSize)
        return GETBITS8(xorsum, kLowNibble, kNibbleSize)


# Send a (raw) Sharp message
#
# Args:
#   data:   Contents of the message to be sent.
#   nbits:  Nr. of bits of data to be sent. Typically kSharpBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: BETA / Previously working fine.
#
# Notes:
#   This procedure handles the inversion of bits required per protocol.
#   The protocol spec says to send the LSB first, but legacy code & usage
#   has us sending the MSB first. Grrrr. Normal invocation of encodeSharp()
#   handles this for you, assuming you are using the correct/standard values.
#   e.g. sendSharpRaw(encodeSharp(address, command))
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sharp.htm
#   http:#lirc.sourceforge.net/remotes/sharp/GA538WJSA
#   http:#www.mwftr.com/ucF08/LEC14%20PIC%20IR.pdf
#   http:#www.hifi-remote.com/johnsfine/DecodeIR.html#Sharp
def sendSharpRaw(data, nbits, repeat):
    tempdata = data
    for i in range(repeat + 1):
        # Protocol demands that the data be sent twice once normally,
        # then with all but the address bits inverted.
        # Note: Previously this used to be performed 3 times (normal, inverted,
        #       normal), however all data points to that being incorrect.
        for n in range(2):
            sendGeneric(
                0,
                0,  # No Header
                kSharpBitMark,
                kSharpOneSpace,
                kSharpBitMark,
                kSharpZeroSpace,
                kSharpBitMark,
                kSharpGap,
                tempdata,
                nbits,
                38,
                True,
                0,  # Repeats are handled already.
                33
            )

            # Invert the data per protocol. This is always called twice, so it's
            # retured to original upon exiting the inner loop.
            tempdata ^= kSharpToggleMask


# Encode a (raw) Sharp message from it's components.
#
# Args:
#   address:   The value of the address to be sent.
#   command:   The value of the address to be sent. (8 bits)
#   expansion: The value of the expansion bit to use. (0 or 1, typically 1)
#   check:     The value of the check bit to use. (0 or 1, typically 0)
#   MSBfirst:  Flag indicating MSB first or LSB first order. (Default: False)
# Returns:
#   An containing the raw Sharp message for sendSharpRaw().
#
# Status: BETA / Should work okay.
#
# Notes:
#   Assumes the standard Sharp bit sizes.
#   Historically sendSharp() sends address & command in
#     MSB first order. This is actually incorrect. It should be sent in LSB
#     order. The behaviour of sendSharp() hasn't been changed to maintain
#     backward compatibility.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sharp.htm
#   http:#lirc.sourceforge.net/remotes/sharp/GA538WJSA
#   http:#www.mwftr.com/ucF08/LEC14%20PIC%20IR.pdf
def encodeSharp(address, command, expansion, check, MSBfirst):
    # Mask any unexpected bits.
    tempaddress = GETBITS16(address, 0, kSharpAddressBits)
    tempcommand = GETBITS16(command, 0, kSharpCommandBits)
    tempexpansion = GETBITS16(expansion, 0, 1)
    tempcheck = GETBITS16(check, 0, 1)

    if not MSBfirst:  # Correct bit order if needed.
        tempaddress = reverseBits(tempaddress, kSharpAddressBits)
        tempcommand = reverseBits(tempcommand, kSharpCommandBits)

    # Concatinate all the bits.
    return (tempaddress << (kSharpCommandBits + 2)) | (tempcommand << 2) | (tempexpansion << 1) | tempcheck


# Send a Sharp message
#
# Args:
#   address:  Address value to be sent.
#   command:  Command value to be sent.
#   nbits:    Nr. of bits of data to be sent. Typically kSharpBits.
#   repeat:   Nr. of additional times the message is to be sent.
#
# Status:  DEPRICATED / Previously working fine.
#
# Notes:
#   This procedure has a non-standard invocation style compared to similar
#     sendProtocol() routines. This is due to legacy, compatibility, & historic
#     reasons. Normally the calling syntax version is like sendSharpRaw().
#   This procedure transmits the address & command in MSB first order, which is
#     incorrect. This behaviour is left as-is to maintain backward
#     compatibility with legacy code.
#   In short, you should use sendSharpRaw(), encodeSharp(), and the correct
#     values of address & command instead of using this, & the wrong values.
#
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sharp.htm
#   http:#lirc.sourceforge.net/remotes/sharp/GA538WJSA
#   http:#www.mwftr.com/ucF08/LEC14%20PIC%20IR.pdf
def sendSharp(address, command, nbits, repeat):
    sendSharpRaw(encodeSharp(address, command, 1, 0, True), nbits, repeat)


# Decode the supplied Sharp message.
#
# Args:
#   results:   Ptr to the data to decode and where to store the decode result.
#   nbits:     Nr. of data bits to expect. Typically kSharpBits.
#   strict:    Flag indicating if we should perform strict matching.
#   expansion: Should we expect the expansion bit to be set. Default is True.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Working fine.
#
# Note:
#   This procedure returns a value suitable for use in sendSharpRaw().
# TODO(crankyoldgit): Need to ensure capture of the inverted message as it can
#   be missed due to the interrupt timeout used to detect an end of message.
#   Several compliance checks are disabled until that is resolved.
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/sharp.php
#   http:#www.mwftr.com/ucF08/LEC14%20PIC%20IR.pdf
#   http:#www.hifi-remote.com/johnsfine/DecodeIR.html#Sharp
def decodeSharp(results, nbits, strict, expansion):
    if results.rawlen < 2 * nbits + kFooter - 1:
        return False  # Not enough entries to be a Sharp message.

    # Compliance
    if strict and nbits != kSharpBits:
        return False  # Request is out of spec.
        # DISABLED - See TODO

    data = 0
    offset = kStartOffset

    # Match Data + Footer
    used = matchGeneric(
        results.rawbuf + offset,
        data,
        results.rawlen - offset,
        nbits,
        0,
        0,  # No Header
        kSharpBitMark,
        kSharpOneSpace,
        kSharpBitMark,
        kSharpZeroSpace,
        kSharpBitMark,
        kSharpGap,
        True,
        35
    )

    if not used:
        return False

    offset += used
    # Compliance
    if strict:
        # Check the state of the expansion bit is what we expect.
        if (data & 0b10) >> 1 != expansion:
            return False

        # The check bit should be cleared in a normal message.
        if data & 0b1:
            return False
        # DISABLED - See TODO

    # Success
    results.decode_type = SHARP
    results.bits = nbits
    results.value = data
    # Address & command are actually transmitted in LSB first order.
    results.address = reverseBits(data, nbits) & kSharpAddressMask
    results.command = reverseBits((data >> 2) & kSharpCommandMask, kSharpCommandBits)
    return True


# Send a Sharp A/C message.
#
# Args:
#   data: An array of kSharpAcStateLength bytes containing the IR command.
#   nbytes: Nr. of bytes of data to send. i.e. length of `data`.
#   repeat: Nr. of times the message should be repeated.
#
# Status: Alpha / Untested.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/638
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/SharpHeatpumpIR.cpp
def sendSharpAc(data, nbytes, repeat):
    if nbytes < kSharpAcStateLength:
        return  # Not enough bytes to send a proper message.

    sendGeneric(
        kSharpAcHdrMark,
        kSharpAcHdrSpace,
        kSharpAcBitMark,
        kSharpAcOneSpace,
        kSharpAcBitMark,
        kSharpAcZeroSpace,
        kSharpAcBitMark,
        kSharpAcGap,
        data,
        nbytes,
        38000,
        False,
        repeat,
        50
    )


# Decode the supplied Sharp A/C message.
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion. (kSharpAcBits)
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: BETA / Should be working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/638
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/SharpHeatpumpIR.cpp
def decodeSharpAc(results, nbits, strict):
    # Is there enough data to match successfully?
    if results.rawlen < 2 * nbits + kHeader + kFooter - 1:
        return False

    # Compliance
    if strict and nbits != kSharpAcBits:
        return False

    offset = kStartOffset
    # Match Header + Data + Footer

    used = matchGeneric(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        kSharpAcHdrMark,
        kSharpAcHdrSpace,
        kSharpAcBitMark,
        kSharpAcOneSpace,
        kSharpAcBitMark,
        kSharpAcZeroSpace,
        kSharpAcBitMark,
        kSharpAcGap,
        True,
        _tolerance,
        kMarkExcess,
        False
    )

    if used == 0:
        return False

    offset += used
    # Compliance
    if strict and not IRSharpAc.validChecksum(results.state):
        return False

    # Success
    results.decode_type = SHARP_AC
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result->state, we don't record value, address, or command as it
    # is a union data type.
    return True
