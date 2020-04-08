# -*- coding: utf-8 -*-

# Copyright 2017 Jonny Graham
# Copyright 2017-2019 David Conran

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *

# Fujitsu A/C support added by Jonny Graham & David Conran

# Equipment it seems compatible with:
#  * Fujitsu ASYG30LFCA with remote AR-RAH2E
#  * Fujitsu AST9RSGCW with remote AR-DB1
#  * Fujitsu ASYG7LMCA with remote AR-REB1E
#  * Fujitsu AR-RAE1E remote.
#  * Fujitsu General with remote AR-JW2
#  * <Add models (A/C & remotes) you've gotten it working with here>

# Ref:
# These values are based on averages of measurements
kFujitsuAcHdrMark = 3324
kFujitsuAcHdrSpace = 1574
kFujitsuAcBitMark = 448
kFujitsuAcOneSpace = 1182
kFujitsuAcZeroSpace = 390
kFujitsuAcMinGap = 8100

addBoolToString = irutils.addBoolToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addModelToString = irutils.addModelToString
addFanToString = irutils.addFanToString
addTempToString = irutils.addTempToString
setBit = irutils.setBit
setBits = irutils.setBits

# Supports:
#   Brand: Fujitsu,  Model: AR-RAH2E remote
#   Brand: Fujitsu,  Model: ASYG30LFCA A/C
#   Brand: Fujitsu,  Model: AR-DB1 remote
#   Brand: Fujitsu,  Model: AST9RSGCW A/C
#   Brand: Fujitsu,  Model: AR-REB1E remote
#   Brand: Fujitsu,  Model: ASYG7LMCA A/C
#   Brand: Fujitsu,  Model: AR-RAE1E remote
#   Brand: Fujitsu,  Model: AGTV14LAC A/C
#   Brand: Fujitsu,  Model: AR-RAC1E remote
#   Brand: Fujitsu,  Model: ASTB09LBC A/C
#   Brand: Fujitsu,  Model: AR-RY4 remote
#   Brand: Fujitsu General,  Model: AR-JW2 remote
#   Brand: Fujitsu,  Model: AR-DL10 remote
#   Brand: Fujitsu,  Model: ASU30C1 A/C

# FUJITSU A/C support added by Jonny Graham

# Constants
kFujitsuAcModeAuto = 0x00
kFujitsuAcModeCool = 0x01
kFujitsuAcModeDry = 0x02
kFujitsuAcModeFan = 0x03
kFujitsuAcModeHeat = 0x04

kFujitsuAcCmdStayOn = 0x00            # b00000000
kFujitsuAcCmdTurnOn = 0x01            # b00000001
kFujitsuAcCmdTurnOff = 0x02           # b00000010
kFujitsuAcCmdEcono = 0x09             # b00001001
kFujitsuAcCmdPowerful = 0x39          # b00111001
kFujitsuAcCmdStepVert = 0x6C          # b01101100
kFujitsuAcCmdToggleSwingVert = 0x6D   # b01101101
kFujitsuAcCmdStepHoriz = 0x79         # b01111001
kFujitsuAcCmdToggleSwingHoriz = 0x7A  # b01111010

kFujitsuAcFanAuto = 0x00
kFujitsuAcFanHigh = 0x01
kFujitsuAcFanMed = 0x02
kFujitsuAcFanLow = 0x03
kFujitsuAcFanQuiet = 0x04
kFujitsuAcFanSize = 3  # Bits

kFujitsuAcMinTemp = 16  # 16C
kFujitsuAcMaxTemp = 30  # 30C

kFujitsuAcSwingSize = 2
kFujitsuAcSwingOff = 0x00
kFujitsuAcSwingVert = 0x01
kFujitsuAcSwingHoriz = 0x02
kFujitsuAcSwingBoth = 0x03

kFujitsuAcOutsideQuietOffset = 7
kFujitsuAcCleanOffset = 3
kFujitsuAcFilterOffset = 3


class IRFujitsuAC(object):
    def __init__(self, pin, model=ARRAH2E, inverted=False, use_modulation=True):
        self.remote_state = [0x0] * kFujitsuAcStateLength
        self._temp = 0
        self._fanSpeed = 0
        self._mode = 0
        self._swingMode = 0
        self._cmd = 0
        self._model = 0
        self._state_length = 0
        self._state_length_short = 0
        self._outsideQuiet = False
        self._clean = False
        self._filter = False
        self._irsend = IRsend(pin, inverted, use_modulation)
        self.setModel(model)
        self.stateReset()

    def setModel(self, model):
        self._model = model
        if mode in (
            fujitsu_ac_remote_model_t.ARDB1,
            fujitsu_ac_remote_model_t.ARJW2
        ):
            self._state_length = kFujitsuAcStateLength - 1
            self._state_length_short = kFujitsuAcStateLengthShort - 1
        # elif mode in (
        # fujitsu_ac_remote_model_t.ARRY4,
        # fujitsu_ac_remote_model_t.ARRAH2E,
        # fujitsu_ac_remote_model_t.ARREB1E):
        
        else:
            self._state_length = kFujitsuAcStateLength
            sefl._state_length_short = kFujitsuAcStateLengthShort
    
    def getModel(self):
        return self._model
        
    def stateReset(self):
        # Reset the state of the remote to a known good state/sequence.
        self._temp = 24
        self._fanSpeed = kFujitsuAcFanHigh
        self._mode = kFujitsuAcModeCool
        self._swingMode = kFujitsuAcSwingBoth
        self._cmd = kFujitsuAcCmdTurnOn
        self._filter = False
        self._clean = False
        self.buildState()
    
    def send(self, repeat=kFujitsuAcMinRepeat):
        # Send the current desired state to the IR LED.
        self.buildState()
        self._irsend.sendFujitsuAC(self.remote_state, self.getStateLength(), repeat)
    
    def calibrate(self):
        self._irsend.calibrate()
        
    def begin(self):
        # Configure the pin for output.
        self._irsend.begin()

    def stepHoriz(self):
        self.setCmd(kFujitsuAcCmdStepHoriz)
        
    def toggleSwingHoriz(self, update=True):
        # Toggle the current setting.
        if update:
            self.setSwing(self.getSwing() ^ kFujitsuAcSwingHoriz)
            
        # and set the appropriate special command.
        self.setCmd(kFujitsuAcCmdToggleSwingHoriz)
        
    def stepVert(self):
        self.setCmd(kFujitsuAcCmdStepVert)
        
    def toggleSwingVert(self, update=True):
        # Toggle the current setting.
        if update:
            self.setSwing(self.getSwing() ^ kFujitsuAcSwingVert)
            
        # and set the appropriate special command.
        self.setCmd(kFujitsuAcCmdToggleSwingVert)
        
    def setCmd(self, cmd):
        # Set the requested command of the A/C.
        
        if cmd in (
            kFujitsuAcCmdTurnOff,
            kFujitsuAcCmdTurnOn,
            kFujitsuAcCmdStayOn,
            kFujitsuAcCmdStepVert,
            kFujitsuAcCmdToggleSwingVert
        ):
            self._cmd = cmd
        elif cmd in (
            kFujitsuAcCmdStepHoriz,
            kFujitsuAcCmdToggleSwingHoriz
        ):
            if self._model in (
                # Only these remotes have horizontal.
                fujitsu_ac_remote_model_t.ARRAH2E,
                fujitsu_ac_remote_model_t.ARJW2
            ):
                self._cmd = cmd
            else:
                self._cmd = kFujitsuAcCmdStayOn
                
        elif cmd in (
            kFujitsuAcCmdEcono,
            kFujitsuAcCmdPowerful
        ):
            if self._model == ARREB1E:
                self._cmd = cmd
            else:
                self._cmd = kFujitsuAcCmdStayOn
          
        else:
            self._cmd = kFujitsuAcCmdStayOn
                
    def getCmd(self, raw=False):
        # Get the special command part of the message.
        # Args:
        #   raw: Do we need to get it from first principles from the raw data?
        # Returns:
        #   A uint8_t containing the contents of the special command byte.

        if raw:
            return self.remote_state[5]
        else:
            return self._cmd 
            
    def setTemp(self, temp):
        # Set the temp. in deg C
        self._temp = max(kFujitsuAcMinTemp, temp)
        self._temp = min(kFujitsuAcMaxTemp, self._temp)
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.
        
    def getTemp(self):
        return self._temp
        
    def setFanSpeed(self, fan):        
        # Set the speed of the fan
        if fan > kFujitsuAcFanQuiet:
            self._fanSpeed = kFujitsuAcFanHigh  # Set the fan to maximum if out of range.
        else:
            self._fanSpeed = fan
            
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.

    def getFanSpeed(self):
        return self._fanSpeed
    
    def setMode(self, mode):
        # Set the requested climate operation mode of the a/c unit.

        if mode > kFujitsuAcModeHeat:
            self._mode = kFujitsuAcModeHeat  # Set the mode to maximum if out of range.
        else:
            self._mode = mode
            
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.
        
    def getMode(self):
        return self._mode
    
    def setSwing(self, mode):
        # Set the requested swing operation mode of the a/c unit.

        self._swingMode = mode
        if self._model in (
            # No Horizontal support.
            fujitsu_ac_remote_model_t.ARDB1,
            fujitsu_ac_remote_model_t.ARREB1E,
            fujitsu_ac_remote_model_t.ARRY4
        ):
            # Set the mode to max if out of range
            if mode > kFujitsuAcSwingVert:
                self._swingMode = kFujitsuAcSwingVert
        elif self._model in (
            # Has Horizontal support.
            fujitsu_ac_remote_model_t.ARRAH2E,
            fujitsu_ac_remote_model_t.ARJW2
        ):
            # Set the mode to max if out of range
            if mode > kFujitsuAcSwingBoth:
                self._swingMode = kFujitsuAcSwingBoth
        
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.

    def getSwing(self, raw=False):
        # Get what the swing part of the message should be.
        # Args:
        #   raw: Do we need to get it from first principles from the raw data?
        # Returns:
        #   A uint8_t containing the contents of the swing state.
        if raw:
            self._swingMode = GETBITS8(self.remote_state[10], kHighNibble, kFujitsuAcSwingSize)
            
        return self._swingMode
    
    def getRaw(self):
        # Return a pointer to the internal state date of the remote.
        self.buildState()
        return self.remote_state
        
    def setRaw(self, newState, length):
        if length > kFujitsuAcStateLength:
            return False
            
        for i in range(kFujitsuAcStateLength):
            if i < length:
                self.remote_state[i] = newState[i]
            else:
                self.remote_state[i] = 0
                
        self.buildFromState(length)
        return True
    
    def getStateLength(self):
        self.buildState()  # Force an update of the internal state.
        if (
            (
                self._model in (
                    fujitsu_ac_remote_model_t.ARRAH2E,
                    fujitsu_ac_remote_model_t.ARREB1E,
                    fujitsu_ac_remote_model_t.ARRY4
                ) and self.remote_state[5] != 0xFE
            ) or
            (
                self._model in (fujitsu_ac_remote_model_t.ARDB1, fujitsu_ac_remote_model_t.ARJW2) and
                self.remote_state[5] != 0xFC
            )
        ):
            return self._state_length_short
        else:
            return self._state_length
    
    @staticmethod
    def validChecksum(state, length):
        sm_complement = 0
        checksum = state[length - 1]
        if length == kFujitsuAcStateLengthShort:  # ARRAH2E, ARREB1E, & ARRY4
            return state[length - 1] == ~state[length - 2]

        if length == kFujitsuAcStateLength - 1:  # ARDB1 & ARJW2
            sm = sumBytes(state, length - 1)
            sm_complement = 0x9B
        elif length == kFujitsuAcStateLength:  # ARRAH2E, ARRY4, & ARREB1E
            sm = sumBytes(state + kFujitsuAcStateLengthShort, length - 1 - kFujitsuAcStateLengthShort)

        else:  # Includes ARDB1 & ARJW2 short.
            return True  # Assume the checksum is valid for other lengths.

        return checksum == (sm_complement - sm)  # Does it match?

    def setPower(self, on):
        # Set the requested power state of the A/C.
        self.setCmd(kFujitsuAcCmdTurnOn if on else kFujitsuAcCmdTurnOff)
    
    def off(self):
        self.setPower(True)
      
    def on(self):
        self.setPower(False)
        
    def getPower(self):
        return self._cmd != kFujitsuAcCmdTurnOff
    
    def setClean(self, on):
        self._clean = on
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.

    def getClean(self, raw=False):
        if raw:
            return GETBIT8(self.remote_state[9], kFujitsuAcCleanOffset)
        elif self.getModel() == fujitsu_ac_remote_model_t.ARRY4:
            return self._clean
        else:
            return False

    def setFilter(self, on):
        self._filter = on
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.

    def getFilter(self, raw=False):
        if raw:
            return GETBIT8(self.remote_state[14], kFujitsuAcFilterOffset)
        elif self.getModel() == fujitsu_ac_remote_model_t.ARRY4:
            return self._filter
        else:
            return False
    
    def setOutsideQuiet(self, on):
        self._outsideQuiet = on
        self.setCmd(kFujitsuAcCmdStayOn)  # No special command involved.

    def getOutsideQuiet(self, raw=False):
        # Get the status of the Outside Quiet setting.
        # Args:
        #   raw: Do we get the result from base data?
        # Returns:
        #   A boolean for if it is set or not.

        if self._state_length == kFujitsuAcStateLength and raw:
            self._outsideQuiet = GETBIT8(self.remote_state[14], kFujitsuAcOutsideQuietOffset)
            
        # Only ARREB1E seems to have this mode.
        if self._outsideQuiet:
            self.setModel(fujitsu_ac_remote_model_t.ARREB1E)
            
        return self._outsideQuiet

    @staticmethod
    def convertMode(mode):
        # Convert a standard A/C mode into its native mode.
        if mode == stdAc.opmode_t.kCool:
            return kFujitsuAcModeCool
        if mode == stdAc.opmode_t.kHeat:
            return kFujitsuAcModeHeat
        if mode == stdAc.opmode_t.kDry:
            return kFujitsuAcModeDry
        if mode == stdAc.opmode_t.kFan:
            return kFujitsuAcModeFan

        return kFujitsuAcModeAuto
    
    @staticmethod
    def convertFan(speed):
        # Convert a standard A/C Fan speed into its native fan speed.
        if speed == stdAc.fanspeed_t.kMin:
            return kFujitsuAcFanQuiet
        if speed == stdAc.fanspeed_t.kLow:
            return kFujitsuAcFanLow
        if speed == stdAc.fanspeed_t.kMedium:
            return kFujitsuAcFanMed
        if speed in (
            stdAc.fanspeed_t.kHigh,
            stdAc.fanspeed_t.kMax
        ):
            return kFujitsuAcFanHigh

        return kFujitsuAcFanAuto

    @staticmethod
    def toCommonMode(mode):
        # Convert a native mode to it's common equivalent.
        if mode == kFujitsuAcModeCool:
            return stdAc.opmode_t.kCool
        if mode == kFujitsuAcModeHeat:
            return stdAc.opmode_t.kHeat
        if mode == kFujitsuAcModeDry:
            return stdAc.opmode_t.kDry
        if mode == kFujitsuAcModeFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    @staticmethod
    def toCommonFanSpeed(speed):
        # Convert a native fan speed to it's common equivalent.
        if speed == kFujitsuAcFanHigh:
            return stdAc.fanspeed_t.kMax
        if speed == kFujitsuAcFanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kFujitsuAcFanLow:
            return stdAc.fanspeed_t.kLow
        if speed == kFujitsuAcFanQuiet:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    def toCommon(self):
        # Convert the A/C state to it's common equivalent.
        result = stdAc.state_t()
        result.protocol = decode_type_t.FUJITSU_AC
        result.model = self.getModel()
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFanSpeed())
        swing = self.getSwing()

        if self._model in (
            fujitsu_ac_remote_model_t.ARREB1E,
            fujitsu_ac_remote_model_t.ARRAH2E,
            fujitsu_ac_remote_model_t.ARRY4
        ):
            result.clean = _clean
            result.filter = _filter
            result.swingv = stdAc.swingv_t.kAuto if swing & kFujitsuAcSwingVert else stdAc.swingv_t.kOff
            result.swingh = stdAc.swingh_t.kAuto if swing & kFujitsuAcSwingHoriz else stdAc.swingh_t.kOff
        else:
            result.swingv = stdAc.swingv_t.kOff
            result.swingh = stdAc.swingh_t.kOff

        result.quiet = (self.getFanSpeed() == kFujitsuAcFanQuiet)
        result.turbo = self.getCmd() == kFujitsuAcCmdPowerful
        result.econo = self.getCmd() == kFujitsuAcCmdEcono
        # Not supported.
        result.light = False
        result.filter = False
        result.clean = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    def toString(self):
        # Convert the internal state into a human readable string.
        result = ""
        model = self.getModel()
        result += addModelToString(
            decode_type_t.FUJITSU_AC,
            model,
            False
        )
        result += addBoolToString(self.getPower(), kPowerStr)
        result += addModeToString(
            self.getMode(),
            kFujitsuAcModeAuto,
            kFujitsuAcModeCool,
            kFujitsuAcModeHeat,
            kFujitsuAcModeDry,
            kFujitsuAcModeFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFanSpeed(),
            kFujitsuAcFanHigh,
            kFujitsuAcFanLow,
            kFujitsuAcFanAuto,
            kFujitsuAcFanQuiet,
            kFujitsuAcFanMed
        )

        # These models have no internal swing, clean. or filter state.
        if model not in (
            fujitsu_ac_remote_model_t.ARDB1,
            fujitsu_ac_remote_model_t.ARJW2
        ):
            result += addBoolToString(self.getClean(), kCleanStr)
            result += addBoolToString(self.getFilter(), kFilterStr)
            result += addIntToString(self.getSwing(), kSwingStr)
            result += kSpaceLBraceStr
            swing = self.getSwing()

            if swing == kFujitsuAcSwingOff:
                result += kOffStr
            elif sping == kFujitsuAcSwingVert:
                result += kSwingVStr
            elif swing == kFujitsuAcSwingHoriz:
                result += kSwingHStr
            elif swing == kFujitsuAcSwingBoth:
                result += kSwingVStr
                result += '+'
                result += kSwingHStr
            else:
                result += kUnknownStr

            result += ')'

        result += kCommaSpaceStr
        result += kCommandStr
        result += kColonSpaceStr

        cmd = self.getCmd()

        if cmd == kFujitsuAcCmdStepHoriz:
            result += kStepStr
            result += ' '
            result += kSwingHStr
        elif cmd == kFujitsuAcCmdStepVert:
            result += kStepStr
            result += ' '
            result += kSwingVStr
        elif cmd == kFujitsuAcCmdToggleSwingHoriz:
            result += kToggleStr
            result += ' '
            result += kSwingHStr
        elif cmd == kFujitsuAcCmdToggleSwingVert:
            result += kToggleStr
            result += ' '
            result += kSwingVStr

        elif cmd == kFujitsuAcCmdEcono:
            result += kEconoStr
        elif cmd == kFujitsuAcCmdPowerful:
            result += kPowerfulStr
        else:
            result += kNAStr

        if self.getModel() == fujitsu_ac_remote_model_t.ARREB1E:
            result += addBoolToString(self.getOutsideQuiet(), kOutsideQuietStr)

        return result

    def buildState(self):
        self.remote_state[0] = 0x14
        self.remote_state[1] = 0x63
        self.remote_state[2] = 0x00
        self.remote_state[3] = 0x10
        self.remote_state[4] = 0x10
        
        if self._cmd in (
            kFujitsuAcCmdTurnOff, 
            kFujitsuAcCmdEcono, 
            kFujitsuAcCmdPowerful, 
            kFujitsuAcCmdStepVert, 
            kFujitsuAcCmdToggleSwingVert, 
            kFujitsuAcCmdStepHoriz,
            kFujitsuAcCmdToggleSwingHoriz
        ):
            self.remote_state[5] = self._cmd
            fullCmd = False
            
        elif self._model in (
            fujitsu_ac_remote_model_t.ARRY4,
            fujitsu_ac_remote_model_t.ARRAH2E,
            fujitsu_ac_remote_model_t.ARREB1E
        ):
            self.remote_state[5] = 0xFE
            fullCmd = True

        elif self._model in (
            fujitsu_ac_remote_model_t.ARDB1,
            fujitsu_ac_remote_model_t.ARJW2
        ):
            self.remote_state[5] = 0xFC
            fullCmd = True
            
        else:
            fullCmd = True
            
        if fullCmd:  # long codes
            tempByte = self._temp - kFujitsuAcMinTemp
            # Nr. of bytes in the message after this byte.
            self.remote_state[6] = self._state_length - 7

            self.remote_state[7] = 0x30
            self.remote_state[8] = (self._cmd == kFujitsuAcCmdTurnOn) | (tempByte << 4)
            self.remote_state[9] = self._mode | 0 << 4  # timer off
            self.remote_state[10] = self._fanSpeed
            self.remote_state[11] = 0  # timerOff values
            self.remote_state[12] = 0  # timerOff/On values
            self.remote_state[13] = 0  # timerOn values
            if self._model == fujitsu_ac_remote_model_t.ARRY4:
                self.remote_state[14] = self._filter << 3
                self.remote_state[9] |= (self._clean << 3)
            else:
                self.remote_state[14] = 0

            checksum_complement = 0
            
            if self._model in (
                fujitsu_ac_remote_model_t.ARDB1,
                fujitsu_ac_remote_model_t.ARJW2
            ):
                checksum = sumBytes(self.remote_state, self._state_length - 1)
                checksum_complement = 0x9B
                
            else:
                if self._model == fujitsu_ac_remote_model_t.ARREB1E:
                    setBit(self.remote_state[14], kFujitsuAcOutsideQuietOffset, self._outsideQuiet)
                
                if self._model in (
                    fujitsu_ac_remote_model_t.ARRAH2E,
                    fujitsu_ac_remote_model_t.ARRY4
                ):
                    setBit(self.remote_state[14], 5)  # |= 0b00100000
                    setBits(self.remote_state[10], kHighNibble, kFujitsuAcSwingSize, self._swingMode)
                
                checksum = sumBytes(
                    self.remote_state + self._state_length_short, 
                    self._state_length - self._state_length_short - 1
                )
            
            # and negate the checksum and store it in the last byte.
            self.remote_state[self._state_length - 1] = checksum_complement - checksum
            
        else:  # short codes
            if self._model in (
                fujitsu_ac_remote_model_t.ARRY4,
                fujitsu_ac_remote_model_t.ARRAH2E,
                fujitsu_ac_remote_model_t.ARREB1E
            ):
                # The last byte is the inverse of penultimate byte
                self.remote_state[self._state_length_short - 1] = ~self.remote_state[self._state_length_short - 2]
            else:
                # We don't need to do anything for the others.
                pass
        
        # Zero the rest of the state.
        for i in range(self._state_length_short, kFujitsuAcStateLength):
            self.remote_state[i] = 0

    def buildFromState(self, length):
        if length in (
            kFujitsuAcStateLength - 1,
            kFujitsuAcStateLengthShort - 1
        ):
            self.setModel(fujitsu_ac_remote_model_t.ARDB1)
            # ARJW2 has horizontal swing.
            if self.getSwing(True) > kFujitsuAcSwingVert:
                self.setModel(fujitsu_ac_remote_model_t.ARJW2)
        elif self.getCmd(True) in (
            kFujitsuAcCmdEcono,
            kFujitsuAcCmdPowerful
        ):
            self.setModel(fujitsu_ac_remote_model_t.ARREB1E)
        else:
            self.setModel(fujitsu_ac_remote_model_t.ARRAH2E)
              
        if self.remote_state[6] == 8:
            if self.getModel() != fujitsu_ac_remote_model_t.ARJW2:
                self.setModel(fujitsu_ac_remote_model_t.ARDB1)
                
        elif self.remote_state[6] == 9:
            if self.getModel() != fujitsu_ac_remote_model_t.ARREB1E:
                self.setModel(fujitsu_ac_remote_model_t.ARRAH2E)
        
        self.setTemp((self.remote_state[8] >> 4) + kFujitsuAcMinTemp)
        if GETBIT8(self.remote_state[8], 0):
            self.setCmd(kFujitsuAcCmdTurnOn)
        else:
            self.setCmd(kFujitsuAcCmdStayOn)
                
        self.setMode(GETBITS8(self.remote_state[9], kLowNibble, kModeBitsSize))
        self.setFanSpeed(GETBITS8(self.remote_state[10], kLowNibble, kFujitsuAcFanSize))
        self.setSwing(GETBITS8(self.remote_state[10], kHighNibble, kFujitsuAcSwingSize))
        self.setClean(self.getClean(True))
        self.setFilter(self.getFilter(True))
        
        # Currently the only way we know how to tell ARRAH2E & ARRY4 apart is if
        # either the raw Filter or Clean setting is on.
        if self.getModel() == fujitsu_ac_remote_model_t.ARRAH2E and (self.getFilter(True) or self.getClean(True)):
            self.setModel(fujitsu_ac_remote_model_t.ARRY4)
            
        if self.remote_state[5] in (
            kFujitsuAcCmdTurnOff,
            kFujitsuAcCmdStepHoriz,
            kFujitsuAcCmdToggleSwingHoriz,
            kFujitsuAcCmdStepVert,
            kFujitsuAcCmdToggleSwingVert,
            kFujitsuAcCmdEcono,
            kFujitsuAcCmdPowerful
        ):
            self.setCmd(self.remote_state[5])
            
        self._outsideQuiet = self.getOutsideQuiet(True)


# Send a Fujitsu A/C message.
#
# Args:
#   data: An array of bytes containing the IR command.
#   nbytes: Nr. of bytes of data in the array. Typically one of:
#           kFujitsuAcStateLength
#           kFujitsuAcStateLength - 1
#           kFujitsuAcStateLengthShort
#           kFujitsuAcStateLengthShort - 1
#   repeat: Nr. of times the message is to be repeated.
#          (Default = kFujitsuAcMinRepeat).
#
# Status: STABLE / Known Good.
#
def sendFujitsuAC(self, data, nbytes, repeat):
    self.send_generic(
        kFujitsuAcHdrMark,
        kFujitsuAcHdrSpace,
        kFujitsuAcBitMark,
        kFujitsuAcOneSpace,
        kFujitsuAcBitMark,
        kFujitsuAcZeroSpace,
        kFujitsuAcBitMark,
        kFujitsuAcMinGap,
        data,
        nbytes,
        38,
        False,
        repeat,
        50
    )


IRsend.sendFujitsuAC = sendFujitsuAC


# Decode a Fujitsu AC IR message if possible.
# Places successful decode information in the results pointer.
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kFujitsuAcBits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status:  ALPHA / Untested.
#
# Ref:
#
def decodeFujitsuAC(self, results, nbits, strict):
    offset = kStartOffset
    dataBitsSoFar = 0

    # Have we got enough data to successfully decode?
    if results.rawlen < (2 * kFujitsuAcMinBits) + kHeader + kFooter - 1:
        return False  # Can't possibly be a valid message.

    # Compliance
    if strict:
        if nbits not in (
            kFujitsuAcBits,
            kFujitsuAcBits - 8,
            kFujitsuAcMinBits,
            kFujitsuAcMinBits + 8
        ):
            return False  # Must be called with the correct nr. of bits.

    # Header

    offset += 1

    if not self.match_mark(results.rawbuf[offset], kFujitsuAcHdrMark):
        return False

    offset += 1
    if not self.match_space(results.rawbuf[offset], kFujitsuAcHdrSpace):
        return False

    # Data (Fixed signature)
    data_result = self.match_data(
        results.rawbuf[offset],
        kFujitsuAcMinBits - 8,
        kFujitsuAcBitMark,
        kFujitsuAcOneSpace,
        kFujitsuAcBitMark,
        kFujitsuAcZeroSpace,
        self._tolerance,
        kMarkExcess,
        False
    )

    if data_result.success is False:
        return False      # Fail

    if data_result.data != 0x1010006314:
        return False  # Signature failed.

    dataBitsSoFar += kFujitsuAcMinBits - 8
    offset += data_result.used

    results.state[0] = 0x14
    results.state[1] = 0x63
    results.state[2] = 0x00
    results.state[3] = 0x10
    results.state[4] = 0x10

    # Keep reading bytes until we either run out of message or state to fill.

    ii = 5

    while offset <= results.rawlen - 16 and ii < kFujitsuAcStateLength + 1:
        data_result = self.match_data(
            results.rawbuf[offset],
            8,
            kFujitsuAcBitMark,
            kFujitsuAcOneSpace,
            kFujitsuAcBitMark,
            kFujitsuAcZeroSpace,
            self._tolerance,
            kMarkExcess,
            False
        )
        if data_result.success is False:
            break  # Fail

        results.state[ii] = data_result.data

        offset += data_result.used
        dataBitsSoFar += 8

    # Footer
    offset += 1
    if (
        offset > results.rawlen or
        not self.match_mark(results.rawbuf[offset], kFujitsuAcBitMark)
    ):
        return False
    # The space is optional if we are out of capture.
    if (
        offset < results.rawlen and
        not self.match_at_least(results.rawbuf[offset], kFujitsuAcMinGap)
    ):
        return False

    # Compliance
    if strict and dataBitsSoFar != nbits:
        return False

    results.decode_type = FUJITSU_AC
    results.bits = dataBitsSoFar

    # Compliance
    if dataBitsSoFar == kFujitsuAcMinBits:
        # Check if this values indicate that this should have been a long state
        # message.
        if results.state[5] == 0xFC:
            return False

        return True  # Success

    if dataBitsSoFar == kFujitsuAcMinBits + 8:
        # Check if this values indicate that this should have been a long state
        # message.
        if results.state[5] == 0xFE:
            return False

        # The last byte needs to be the inverse of the penultimate byte.
        if results.state[5] != ~results.state[6]:
            return False

        return True  # Success

    if dataBitsSoFar == kFujitsuAcBits - 8:
        # Long messages of this size require this byte be correct.
        if results.state[5] != 0xFC:
            return False
    elif dataBitsSoFar == kFujitsuAcBits:
        # Long messages of this size require this byte be correct.
        if results.state[5] != 0xFE:
            return False
    else:
        return False  # Unexpected size.

    if not IRFujitsuAC.validChecksum(results.state, dataBitsSoFar / 8):
        return False

    # Success
    return True  # All good.


IRrecv.decodeFujitsuAC = decodeFujitsuAC
