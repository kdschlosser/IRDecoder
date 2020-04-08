# -*- coding: utf-8 -*-

# Copyright 2017, 2019 David Conran

# Supports:
#   Brand: LG,  Model: 6711A20083V remote
#   Brand: LG,  Model: AKB74395308 remote
#   Brand: LG,  Model: S4-W12JA3AA A/C (LG2)
#   Brand: LG,  Model: AKB75215403 remote (LG2)
#   Brand: General Electric,  Model: AG1BH09AW101 Split A/C
#   Brand: General Electric,  Model: 6711AR2853M A/C Remote


from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *
from .IRac import *
from .protocol_base import ProtocolBase


kLgAcChecksumOffset = 0  # Nr. of bits
kLgAcChecksumSize = kNibbleSize  # Nr. of bits
kLgAcFanOffset = 4  # Nr. of bits
kLgAcFanSize = 3  # Nr. of bits
kLgAcFanLow = 0     # 0b000
kLgAcFanMedium = 2  # 0b010
kLgAcFanHigh = 4    # 0b100
kLgAcFanAuto = 5    # 0b101
kLgAcTempOffset = 8  # Nr. of bits
kLgAcTempSize = 4  # Nr. of bits
kLgAcTempAdjust = 15
kLgAcMinTemp = 16  # Celsius
kLgAcMaxTemp = 30  # Celsius
kLgAcModeOffset = 12  # Nr. of bits
kLgAcModeSize = 3  # Nr. of bits
kLgAcCool = 0  # 0b000
kLgAcDry = 1   # 0b001
kLgAcFan = 2   # 0b010
kLgAcAuto = 3  # 0b011
kLgAcHeat = 4  # 0b100
kLgAcPowerOffset = 18  # Nr. of bits
kLgAcPowerSize = 2  # Nr. of bits
kLgAcPowerOff = 3  # 0b11
kLgAcPowerOn = 0   # 0b00
kLgAcSignatureOffset = 20  # Nr. of bits
kLgAcSignatureSize = 8  # Nr. of bits
kLgAcSignature = 0x88

kLgAcOffCommand = 0x88C0051

addBoolToString = irutils.addBoolToString
addModeToString = irutils.addModeToString
addModelToString = irutils.addModelToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits

# LG decode originally added by Darryl Smith (based on the JVC protocol)
# LG send originally added by https:#github.com/chaeplin

# Constants
kLgTick = 50
kLgHdrMarkTicks = 170
kLgHdrMark = kLgHdrMarkTicks * kLgTick  # 8500
kLgHdrSpaceTicks = 85
kLgHdrSpace = kLgHdrSpaceTicks * kLgTick  # 4250
kLgBitMarkTicks = 11
kLgBitMark = kLgBitMarkTicks * kLgTick  # 550
kLgOneSpaceTicks = 32
kLgOneSpace = kLgOneSpaceTicks * kLgTick  # 1600
kLgZeroSpaceTicks = 11
kLgZeroSpace = kLgZeroSpaceTicks * kLgTick  # 550
kLgRptSpaceTicks = 45
kLgRptSpace = kLgRptSpaceTicks * kLgTick  # 2250
kLgMinGapTicks = 795
kLgMinGap = kLgMinGapTicks * kLgTick  # 39750
kLgMinMessageLengthTicks = 2161
kLgMinMessageLength = kLgMinMessageLengthTicks * kLgTick

kLg32HdrMarkTicks = 90
kLg32HdrMark = kLg32HdrMarkTicks * kLgTick  # 4500
kLg32HdrSpaceTicks = 89
kLg32HdrSpace = kLg32HdrSpaceTicks * kLgTick  # 4450
kLg32RptHdrMarkTicks = 179
kLg32RptHdrMark = kLg32RptHdrMarkTicks * kLgTick  # 8950

kLg2HdrMarkTicks = 64
kLg2HdrMark = kLg2HdrMarkTicks * kLgTick  # 3200
kLg2HdrSpaceTicks = 197
kLg2HdrSpace = kLg2HdrSpaceTicks * kLgTick  # 9850
kLg2BitMarkTicks = 10
kLg2BitMark = kLg2BitMarkTicks * kLgTick  # 500



"""


calcLGChecksum(data)

# Classes
class IRLgAc {
 public:
  explicit IRLgAc(pin, bool inverted = False,
                  bool use_modulation = True)

  void stateReset(void)
  static calcChecksum(state)
  static bool validChecksum(state)
  bool isValidLgAc(void)
#if SEND_LG
  void send(repeat = kLgDefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_LG
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(degrees)
  getTemp(void)
  void setFan(speed)
  getFan(void)
  void setMode(mode)
  getMode(void)
  getRaw(void)
  void setRaw(new_code)
  convertMode(stdAc.opmode_t mode)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static convertFan(stdAc.fanspeed_t speed)
  stdAc.state_t toCommon(void)
  String toString(void)
  void setModel(lg_ac_remote_model_t model)
  lg_ac_remote_model_t getModel(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # The state of the IR remote in IR code form.
  remote_state
  _temp
  decode_type_t _protocol
  void checksum(void)
  void _setTemp(value)
}

#endif  # IR_LG_H_

"""


class LG(ProtocolBase):
      
    # Calculate the rolling 4-bit wide checksum over all of the data.
    #  Args:
    #    data: The value to be checksum'ed.
    #  Returns:
    #    A 4-bit checksum.
    @staticmethod
    def calcLGChecksum(data):
        return (
            (
                (data >> 12) + 
                ((data >> 8) & 0xF) + 
                ((data >> 4) & 0xF) + 
                (data & 0xF)
            ) & 0xF
        )
    
    # Send an LG formatted message.
    #
    # Args:
    #   data:   The contents of the message you want to send.
    #   nbits:  The bit size of the message being sent.
    #           Typically kLgBits or kLg32Bits.
    #   repeat: The number of times you want the message to be repeated.
    #
    # Status: Beta / Should be working.
    #
    # Notes:
    #   LG has a separate message to indicate a repeat, like NEC does.
    # Supports:
    #   IR Remote models: 6711A20083V        
    
    # Send an LG Variant-2 formatted message.
    #
    # Args:
    #   data:   The contents of the message you want to send.
    #   nbits:  The bit size of the message being sent.
    #           Typically kLgBits or kLg32Bits.
    #   repeat: The number of times you want the message to be repeated.
    #
    # Status: Beta / Should be working.
    #
    # Notes:
    #   LG has a separate message to indicate a repeat, like NEC does.
    # Supports:
    #   IR Remote models: AKB74395308
    def send_ir(self, data, nbits, repeat):
        if nbits >= kLg32Bits:
            # Let the original routine handle it.

            repeatHeaderMark = 0
            duty = kDutyDefault

            if nbits >= kLg32Bits:
                # LG 32bit protocol is near identical to Samsung except for repeats.
                sendSAMSUNG(data, nbits, 0)  # Send it as a single Samsung message.
                repeatHeaderMark = kLg32RptHdrMark
                duty = 33
                repeat += 1
            else:
                # LG (28-bit) protocol.
                repeatHeaderMark = kLgHdrMark
                self.sendGeneric(
                    kLgHdrMark,
                    kLgHdrSpace,
                    kLgBitMark,
                    kLgOneSpace,
                    kLgBitMark,
                    kLgZeroSpace,
                    kLgBitMark,
                    kLgMinGap,
                    kLgMinMessageLength,
                    data,
                    nbits,
                    38,
                    True,
                    0,  # Repeats are handled later.
                    duty
                )

            # Repeat
            # Protocol has a mandatory repeat-specific code sent after every command.
            if repeat:
                self.sendGeneric(
                    repeatHeaderMark,
                    kLgRptSpace,
                    0,
                    0,
                    0,
                    0,  # No data is sent.
                    kLgBitMark,
                    kLgMinGap,
                    kLgMinMessageLength,
                    0,
                    0,  # No data.
                    38,
                    True,
                    repeat - 1,
                    duty
                )
                
        else:
            # LGv2 (28-bit) protocol.
            self.sendGeneric(
                kLg2HdrMark, 
                kLg2HdrSpace, 
                kLgBitMark, 
                kLgOneSpace, 
                kLgBitMark,
                kLgZeroSpace, 
                kLgBitMark, 
                kLgMinGap, 
                kLgMinMessageLength, 
                data,
                nbits, 
                38, 
                True, 
                0,  # Repeats are handled later.
                50
            )
          
            # TODO(crackn): Verify the details of what repeat messages look like.
            # Repeat
            # Protocol has a mandatory repeat-specific code sent after every command.
            if repeat:
                self.sendGeneric(
                    kLg2HdrMark, 
                    kLgRptSpace, 
                    0, 
                    0, 
                    0, 
                    0,  # No data is sent.
                    kLgBitMark, 
                    kLgMinGap, 
                    kLgMinMessageLength, 
                    0, 
                    0,  # No data.
                    38, 
                    True, 
                    repeat - 1, 
                    50
                )
    
    # Construct a raw 28-bit LG message code from the supplied address & command.
    #
    # Args:
    #   address: The address code.
    #   command: The command code.
    # Returns:
    #   A raw 28-bit LG message code suitable for sendLG() etc.
    #
    # Status: BETA / Should work.
    #
    # Notes:
    #   e.g. Sequence of bits = address + command + checksum.
    @classmethod
    def encode_ir(cls, address, command):
        return (address << 20) | (command << 4) | cls.calcLGChecksum(command)
    
    # Decode the supplied LG message.
    # LG protocol has a repeat code which is 4 items long.
    # Even though the protocol has 28/32 bits of data, only 24/28 bits are
    # distinct.
    # In transmission order, the 28/32 bits are constructed as follows:
    #   8/12 bits of address + 16 bits of command + 4 bits of checksum.
    #
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion.
    #            Typically kLgBits or kLg32Bits.
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Status: BETA / Should work.
    #
    # Note:
    #   LG 32bit protocol appears near identical to the Samsung protocol.
    #   They possibly differ on how they repeat and initial HDR mark.
    #
    # Supports:
    #   IR Remote models: 6711A20083V, AKB74395308
    
    # Ref:
    #   https:#funembedded.wordpress.com/2014/11/08/
    #        ir-remote-control-for-lg-conditioner-using-stm32f302-mcu-on-mbed-platform/
    def decode_ir(self, results, nbits, strict):
        if nbits >= kLg32Bits:
            if results.rawlen < 2 * nbits + 2 * (kHeader + kFooter) - 1:
                return False  # Can't possibly be a valid LG32 message.
            elif results.rawlen < 2 * nbits + kHeader + kFooter - 1:
                return False  # Can't possibly be a valid LG message.

        if strict and nbits != kLgBits and nbits != kLg32Bits:
            return False  # Doesn't comply with expected LG protocol.
    
        offset = kStartOffset
        isLg2 = False
    
        # Header

        if self.matchMark(results.rawbuf[offset], kLgHdrMark):
            offset += 1
            m_tick = results.rawbuf[offset] * kRawTick / kLgHdrMarkTicks
        elif self.matchMark(results.rawbuf[offset], kLg2HdrMark):
            offset += 1
            m_tick = results.rawbuf[offset] * kRawTick / kLg2HdrMarkTicks
            isLg2 = True
        elif self.matchMark(results.rawbuf[offset], kLg32HdrMark):
            offset += 1
            m_tick = results.rawbuf[offset] * kRawTick / kLg32HdrMarkTicks
        else:
            return False

        if isLg2:
            if self.matchSpace(results.rawbuf[offset], kLg2HdrSpace):
                offset += 1
                s_tick = results.rawbuf[offset] * kRawTick / kLg2HdrSpaceTicks
            else:
                return False
        else:
            if self.matchSpace(results.rawbuf[offset], kLgHdrSpace):
                offset += 1
                s_tick = results.rawbuf[offset] * kRawTick / kLgHdrSpaceTicks
            elif self.matchSpace(results.rawbuf[offset], kLg2HdrSpace):
                offset += 1
                s_tick = results.rawbuf[offset] * kRawTick / kLg32HdrSpaceTicks
            else:
                return False

        # Set up the expected tick sizes based on variant.
        if isLg2:
            bitmarkticks = kLg2BitMarkTicks
        else:
            bitmarkticks = kLgBitMarkTicks

        # Data
        data_result = self.matchData(
            results.rawbuf[offset],
            nbits,
            bitmarkticks * m_tick,
            kLgOneSpaceTicks * s_tick,
            bitmarkticks * m_tick,
            kLgZeroSpaceTicks * s_tick,
            _tolerance,
            0
        )

        if data_result.success is False:
            return False

        data = data_result.data
        offset += data_result.used
    
        # Footer
        offset += 1
        if not self.matchMark(results.rawbuf[offset], bitmarkticks * m_tick):
            return False

        if (
            offset < results.rawlen and
            not self.matchAtLeast(results.rawbuf[offset], kLgMinGapTicks * s_tick)
        ):
            return False
    
        # Repeat
        if nbits >= kLg32Bits:
            # If we are expecting the LG 32-bit protocol, there is always
            # a repeat message. So, check for it.
            offset += 2

            if not self.matchMark(results.rawbuf[offset], kLg32RptHdrMarkTicks * m_tick):
                return False

            offset += 1
            if not self.matchSpace(results.rawbuf[offset], kLgRptSpaceTicks * s_tick):
                return False

            offset += 1
            if not self.matchMark(results.rawbuf[offset], bitmarkticks * m_tick):
                return False

            if (
                offset < results.rawlen and
                not self.matchAtLeast(results.rawbuf[offset], kLgMinGapTicks * s_tick)
            ):
                return False
    
        # Compliance
        command = (data >> 4) & 0xFFFF  # The 16 bits before the checksum.
    
        if strict and (data & 0xF) != self.calcLGChecksum(command):
            return False  # The last 4 bits sent are the expected checksum.
    
        # Success
        if isLg2:
            results.decode_type = LG2
        else:
            results.decode_type = LG

        results.bits = nbits
        results.value = data
        results.command = command
        results.address = data >> 20  # The bits before the command.
        return True

    # LG A/C Class
    # Support for LG-type A/C units.
    # Ref:
    #   https:#github.com/arendst/Tasmota/blob/54c2eb283a02e4287640a4595e506bc6eadbd7f2/sonoff/xdrv_05_irremote.ino#L327-438

    def stateReset(self):
        self.setRaw(kLgAcOffCommand)
        self.setModel(lg_ac_remote_model_t.GE6711AR2853M)

    def send_ac(self, repeat):
        if self.getPower():
            self._irsend.send(self._protocol, self.getRaw(), kLgBits, repeat)
        else:
            # Always send the special Off command if the power is set to off.
            # Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/1008#issuecomment-570763580
            self._irsend.send(self._protocol, kLgAcOffCommand, kLgBits, repeat)

    def setModel(self, model):

        if model == lg_ac_remote_model_t.AKB75215403:
            self._protocol = decode_type_t.LG2
        elif model == lg_ac_remote_model_t.GE6711AR2853M or model:
            self._protocol = decode_type_t.LG

    def getModel(self):
        if self._protocol == LG2:
            return lg_ac_remote_model_t.AKB75215403
        if self._protocol == LG:
            pass

        return lg_ac_remote_model_t.GE6711AR2853M

    def getRaw(self):
        self.checksum()
        return self.remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:]
        self._temp = 15  # Ensure there is a "sane" previous temp.
        self._temp = self.getTemp()

    # Calculate the checksum for a given state.
    # Args:
    #   state:  The value to calculate the checksum of.
    # Returns:
    #   A of the checksum.
    @classmethod
    def calcChecksum(cls, state):
        return cls.calcLGChecksum(state >> 4)

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The value to verify the checksum of.
    # Returns:
    #   A boolean.
    @classmethod
    def validChecksum(cls, state):
        return cls.calcChecksum(state) == GETBITS32(state, kLgAcChecksumOffset, kLgAcChecksumSize)

    def checksum(self):
        setBits(self.remote_state, kLgAcChecksumOffset, kLgAcChecksumSize, self.calcChecksum(self.remote_state))

    def setPower(self, on):
        setBits(self.remote_state, kLgAcPowerOffset, kLgAcPowerSize, kLgAcPowerOn if on else kLgAcPowerOff)
        if on:
            self.setTemp(self._temp)  # Reset the temp if we are on.
        else:
            self._setTemp(0)  # Off clears the temp.

    def getPower(self):
        return GETBITS32(self.remote_state, kLgAcPowerOffset, kLgAcPowerSize) == kLgAcPowerOn

    # Set the temp. (Internal use only)
    def _setTemp(self, value):
        setBits(self.remote_state, kLgAcTempOffset, kLgAcTempSize, value)

    # Set the temp. in deg C
    def setTemp(self, degrees):
        temp = max(kLgAcMinTemp, degrees)
        temp = min(kLgAcMaxTemp, temp)
        self._temp = temp
        self._setTemp(temp - kLgAcTempAdjust)

    # Return the set temp. in deg C
    def getTemp(self):
        if self.getPower():
            return GETBITS32(self.remote_state, kLgAcTempOffset, kLgAcTempSize) + kLgAcTempAdjust
        else:
            return self._temp

    # Set the speed of the fan.
    def setFan(self, speed):
        if speed in (
            kLgAcFanAuto,
            kLgAcFanLow,
            kLgAcFanMedium,
            kLgAcFanHigh
        ):
            setBits(self.remote_state, kLgAcFanOffset, kLgAcFanSize, speed)
        else:
            self.setFan(kLgAcFanAuto)

    def getFan(self):
        return GETBITS32(self.remote_state, kLgAcFanOffset, kLgAcFanSize)

    def getMode(self):
        return GETBITS32(self.remote_state, kLgAcModeOffset, kLgAcModeSize)

    def setMode(self, mode):
        if mode in (
            kLgAcAuto,
            kLgAcDry,
            kLgAcHeat,
            kLgAcCool,
            kLgAcFan
        ):
            setBits(self.remote_state, kLgAcModeOffset, kLgAcModeSize, mode)
        else:
            # If we get an unexpected mode, default to AUTO.
            self.setMode(kLgAcAuto)

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        if mode == stdAc.opmode_t.kCool:
            return kLgAcCool
        if mode == stdAc.opmode_t.kHeat:
            return kLgAcHeat
        if mode == stdAc.opmode_t.kFan:
            return kLgAcFan
        if mode == stdAc.opmode_t.kDry:
            return kLgAcDry

        return kLgAcAuto

    # Convert a native mode to it's common equivalent.
    @staticmethod
    def toCommonMode(mode):
        if mode == kLgAcCool:
            return stdAc.opmode_t.kCool
        if mode == kLgAcHeat:
            return stdAc.opmode_t.kHeat
        if mode == kLgAcDry:
            return stdAc.opmode_t.kDry
        if mode == kLgAcFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        if speed in (stdAc.fanspeed_t.kMin, stdAc.fanspeed_t.kLow):
            return kLgAcFanLow
        if speed == stdAc.fanspeed_t.kMedium:
            return kLgAcFanMedium
        if speed in (stdAc.fanspeed_t.kHigh, stdAc.fanspeed_t.kMax):
            return kHitachiAcFanHigh

        return kHitachiAcFanAuto

    # Convert a native fan speed to it's common equivalent.
    @staticmethod
    def toCommonFanSpeed(speed):
        if speed == kLgAcFanHigh:
            return stdAc.fanspeed_t.kMax
        if speed == kLgAcFanMedium:
            return stdAc.fanspeed_t.kMedium
        if speed == kLgAcFanLow:
            return stdAc.fanspeed_t.kLow

        return stdAc.fanspeed_t.kAuto

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.LG
        result.model = self.getModel()
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
        result.light = False
        result.filter = False
        result.clean = False
        result.econo = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addModelToString(self._protocol, self.getModel(), False)
        result += addBoolToString(self.getPower(), kPowerStr)
        if self.getPower():  # Only display the rest if is in power on state.
            result += addModeToString(
                self.getMode(),
                kLgAcAuto,
                kLgAcCool,
                kLgAcHeat,
                kLgAcDry,
                kLgAcFan
            )
            result += addTempToString(self.getTemp())
            result += addFanToString(
                self.getFan(),
                kLgAcFanHigh,
                kLgAcFanLow,
                kLgAcFanAuto,
                kLgAcFanAuto,
                kLgAcFanMedium
            )
        return result

    def isValidLgAc(self):
        return (
            self.validChecksum(remote_state) and
            GETBITS32(remote_state, kLgAcSignatureOffset, kLgAcSignatureSize) == kLgAcSignature
        )
