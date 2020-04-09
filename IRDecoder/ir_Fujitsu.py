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

from .protocol_base import ACProtocolBase

class IRFujitsuAC(ACProtocolBase):
    def __init__(self, pin, model=fujitsu_ac_remote_model_t.ARRAH2E, inverted=False, use_modulation=True):
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
        self.mode = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
        if model in (
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
            self._state_length_short = kFujitsuAcStateLengthShort
        
    def state_reset(self):
        # Reset the state of the remote to a known good state/sequence.
        self._temp = 24
        self._fanSpeed = kFujitsuAcFanHigh
        self._mode = kFujitsuAcModeCool
        self._swingMode = kFujitsuAcSwingBoth
        self._cmd = kFujitsuAcCmdTurnOn
        self._filter = False
        self._clean = False
        self.build_state()
    
    def send(self, repeat=kFujitsuAcMinRepeat):
        # Send the current desired state to the IR LED.
        self.build_state()
        self._irsend.sendFujitsuAC(self.remote_state, self.get_state_length(), repeat)

    def step_swing_horz(self):
        self.set_cmd(kFujitsuAcCmdStepHoriz)
        
    def toggle_swing_horz(self, update=True):
        # Toggle the current setting.
        if update:
            self._swingMode ^= kFujitsuAcSwingHoriz
            
        # and set the appropriate special command.
        self.set_cmd(kFujitsuAcCmdToggleSwingHoriz)
        
    def step_vert(self):
        self.set_cmd(kFujitsuAcCmdStepVert)
        
    def toggle_swing_vert(self, update=True):
        # Toggle the current setting.
        if update:
            self._swingMode ^= kFujitsuAcSwingVert

        # and set the appropriate special command.
        self.set_cmd(kFujitsuAcCmdToggleSwingVert)
        
    def set_cmd(self, cmd):
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
            if self._model == fujitsu_ac_remote_model_t.ARREB1E:
                self._cmd = cmd
            else:
                self._cmd = kFujitsuAcCmdStayOn
          
        else:
            self._cmd = kFujitsuAcCmdStayOn
     
    @property
    def temperature(self):
        return self._temp

    @temperature.setter
    def temperature(self, temp):
        # Set the temp. in deg C
        self._temp = max(kFujitsuAcMinTemp, temp)
        self._temp = min(kFujitsuAcMaxTemp, self._temp)
        self.set_cmd(kFujitsuAcCmdStayOn)  # No special command involved.

    @property
    def fan_speed(self):
        return self.to_common_fan_speed(self._fanSpeed)

    @fan_speed.setter
    def fan_speed(self, value):
        self._fanSpeed = self.to_common_fan_speed(value)
        self.set_cmd(kFujitsuAcCmdStayOn)  # No special command involved.

    @property
    def mode(self):
        return self.to_common_mode(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = self.from_common_mode(value)
        # Set the requested climate operation mode of the a/c unit.
        self.set_cmd(kFujitsuAcCmdStayOn)  # No special command involved.

    @property
    def swing_vert(self):
        if self._swingMode & kFujitsuAcSwingVert:
            return stdAc.swingv_t.kAuto

        return stdAc.swingv_t.kOff

    @swing_vert.setter
    def swing_vert(self, value):
        if value == stdAc.swingv_t.kAuto:
            self._swingMode |= kFujitsuAcSwingVert
        elif value == stdAc.swingv_t.kOff:
            self._swingMode ^= kFujitsuAcSwingVert

        self.set_cmd(kFujitsuAcCmdStayOn)

    @property
    def swing_horz(self):
        if self._model in (
            fujitsu_ac_remote_model_t.ARREB1E,
            fujitsu_ac_remote_model_t.ARRAH2E,
            fujitsu_ac_remote_model_t.ARRY4
        ):
            return stdAc.swingh_t.kOff

        if self._swingMode & kFujitsuAcSwingHoriz:
            return stdAc.swingh_t.kAuto

        return stdAc.swingh_t.kOff

    @swing_horz.setter
    def swing_horz(self, value):
        if self._model in (
            # No Horizontal support.
            fujitsu_ac_remote_model_t.ARDB1,
            fujitsu_ac_remote_model_t.ARREB1E,
            fujitsu_ac_remote_model_t.ARRY4
        ):
            return

        if value == stdAc.swingh_t.kAuto:
            self._swingMode |= kFujitsuAcSwingHoriz
        elif value == stdAc.swingh_t.kOff:
            self._swingMode ^= kFujitsuAcSwingHoriz

        self.set_cmd(kFujitsuAcCmdStayOn)

    def get_raw(self):
        # Return a pointer to the internal state date of the remote.
        self.build_state()
        return self.remote_state[:]
        
    def set_raw(self, newState, length=kFujitsuAcStateLength):
        if length > kFujitsuAcStateLength:
            return False
            
        for i in range(kFujitsuAcStateLength):
            if i < length:
                self.remote_state[i] = newState[i]
            else:
                self.remote_state[i] = 0
                
        self.build_from_state(length)
        return True
    
    def get_state_length(self):
        self.build_state()  # Force an update of the internal state.
        if self.remote_state[5] != 0xFE:
            if self._model in (
                fujitsu_ac_remote_model_t.ARRAH2E,
                fujitsu_ac_remote_model_t.ARREB1E,
                fujitsu_ac_remote_model_t.ARRY4
            ):
                return self._state_length_short

        if self.remote_state[5] != 0xFC:
            if self._model in (
                fujitsu_ac_remote_model_t.ARDB1,
                fujitsu_ac_remote_model_t.ARJW2
            ):
                return self._state_length_short

        return self._state_length
    
    @classmethod
    def valid_checksum(cls, state, length=kFujitsuAcStateLength):
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

    @property
    def power(self):
        return self._cmd != kFujitsuAcCmdTurnOff

    @power.setter
    def power(self, state):
        if state:
            state = kFujitsuAcCmdTurnOn
        else:
            state = kFujitsuAcCmdTurnOff

        # Set the requested power state of the A/C.
        self.set_cmd(state)

    @property
    def clean(self):
        if self.model != fujitsu_ac_remote_model_t.ARRY4:
            return False

        return self._clean

    @clean.setter
    def clean(self, state):
        if self.model != fujitsu_ac_remote_model_t.ARRY4:
            return

        if state:
            state = True
        else:
            state = False

        self._clean = state
        self.set_cmd(kFujitsuAcCmdStayOn)

    @property
    def filter(self):
        if self.model != fujitsu_ac_remote_model_t.ARRY4:
            return False

        return self._filter

    @filter.setter
    def filter(self, state):
        if self.model != fujitsu_ac_remote_model_t.ARRY4:
            return

        if state:
            state = True
        else:
            state = False

        self._filter = state
        self.set_cmd(kFujitsuAcCmdStayOn)

    @property
    def quiet(self):
        if self.model != fujitsu_ac_remote_model_t.ARREB1E:
            return False

        return self._outsideQuiet

    @quiet.setter
    def quiet(self, state):
        if self.model != fujitsu_ac_remote_model_t.ARREB1E:
            return

        if state:
            state = True
        else:
            state = False

        self._outsideQuiet = state
        self.set_cmd(kFujitsuAcCmdStayOn)  # No special command involved.

    @classmethod
    def to_common_mode(cls, mode):
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

    @classmethod
    def from_common_mode(cls, mode):
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

    @classmethod
    def to_common_fan_speed(cls, speed):
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

    @classmethod
    def from_common_fan_speed(cls, speed):
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

    def build_state(self):
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
                    setBit(self.remote_state[14], 5, 0)  # |= 0b00100000
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

    def build_from_state(self, length):
        if length in (
            kFujitsuAcStateLength - 1,
            kFujitsuAcStateLengthShort - 1
        ):
            self.model = fujitsu_ac_remote_model_t.ARDB1
            # ARJW2 has horizontal swing.
            swing_mode = GETBITS8(self.remote_state[10], kHighNibble, kFujitsuAcSwingSize)
            
            if swing_mode > kFujitsuAcSwingVert:
                self.model = fujitsu_ac_remote_model_t.ARJW2
        
        elif self.remote_state[5] in (
            kFujitsuAcCmdEcono,
            kFujitsuAcCmdPowerful
        ):
            self.model = fujitsu_ac_remote_model_t.ARREB1E
        else:
            self.model = fujitsu_ac_remote_model_t.ARRAH2E
              
        if self.remote_state[6] == 8:
            if self.model != fujitsu_ac_remote_model_t.ARJW2:
                self.model = fujitsu_ac_remote_model_t.ARDB1
                
        elif self.remote_state[6] == 9:
            if self.model != fujitsu_ac_remote_model_t.ARREB1E:
                self.model = fujitsu_ac_remote_model_t.ARRAH2E
        
        self.temperature = (self.remote_state[8] >> 4) + kFujitsuAcMinTemp
        if GETBIT8(self.remote_state[8], 0):
            self.set_cmd(kFujitsuAcCmdTurnOn)
        else:
            self.set_cmd(kFujitsuAcCmdStayOn)
                
        self.mode = self.to_common_mode(GETBITS8(self.remote_state[9], kLowNibble, kModeBitsSize))
        self.fan_speed = self.to_common_fan_speed(GETBITS8(self.remote_state[10], kLowNibble, kFujitsuAcFanSize))
        
        swing = GETBITS8(self.remote_state[10], kHighNibble, kFujitsuAcSwingSize)
        
        if swing & kFujitsuAcSwingHoriz:
            self.swing_horz = stdAc.swingh_t.kAuto
        else:
            self.swing_horz = stdAc.swingh_t.kOff
        if swing & kFujitsuAcSwingVert:
            self.swing_vert = stdAc.swingv_t.kAuto
        else:
            self.swing_vert = stdAc.swingv_t.kOff
        
        clean = GETBIT8(self.remote_state[9], kFujitsuAcCleanOffset)
        filtr = GETBIT8(self.remote_state[14], kFujitsuAcFilterOffset)
        
        self.clean = clean
        self.filter = filtr
        
        # Currently the only way we know how to tell ARRAH2E & ARRY4 apart is if
        # either the raw Filter or Clean setting is on.
        if self.model == fujitsu_ac_remote_model_t.ARRAH2E and (filtr or clean):
            self.model = fujitsu_ac_remote_model_t.ARRY4
            
        if self.remote_state[5] in (
            kFujitsuAcCmdTurnOff,
            kFujitsuAcCmdStepHoriz,
            kFujitsuAcCmdToggleSwingHoriz,
            kFujitsuAcCmdStepVert,
            kFujitsuAcCmdToggleSwingVert,
            kFujitsuAcCmdEcono,
            kFujitsuAcCmdPowerful
        ):
            self.set_cmd(self.remote_state[5])

        if self._state_length == kFujitsuAcStateLength:
            self._outsideQuiet = GETBIT8(self.remote_state[14], kFujitsuAcOutsideQuietOffset)

            # Only ARREB1E seems to have this mode.
            if self._outsideQuiet:
                self.model = fujitsu_ac_remote_model_t.ARREB1E

        else:
            self._outsideQuiet = False


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

    if not IRFujitsuAC.valid_checksum(results.state, dataBitsSoFar / 8):
        return False

    # Success
    return True  # All good.


IRrecv.decodeFujitsuAC = decodeFujitsuAC
