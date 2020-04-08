# -*- coding: utf-8 -*-

# Copyright 2016 sillyfrog
# Copyright 2017 sillyfrog, crankyoldgit
# Copyright 2018-2019 crankyoldgit

# Supports:
#   Brand: Daikin,  Model: ARC433** remote
#   Brand: Daikin,  Model: ARC477A1 remote
#   Brand: Daikin,  Model: FTXZ25NV1B A/C
#   Brand: Daikin,  Model: FTXZ35NV1B A/C
#   Brand: Daikin,  Model: FTXZ50NV1B A/C
#   Brand: Daikin,  Model: ARC433B69 remote
#   Brand: Daikin,  Model: ARC423A5 remote
#   Brand: Daikin,  Model: FTE12HV2S A/C
#   Brand: Daikin,  Model: BRC4C153 remote
#   Brand: Daikin,  Model: 17 Series A/C (DAIKIN128)
#   Brand: Daikin,  Model: FTXB12AXVJU A/C (DAIKIN128)
#   Brand: Daikin,  Model: FTXB09AXVJU A/C (DAIKIN128)
#   Brand: Daikin,  Model: BRC52B63 remote (DAIKIN128)
#   Brand: Daikin,  Model: ARC480A5 remote (DAIKIN152)

from .IRremoteESP8266 import *
from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRutils import *
from .protocol_base import *


# Constants
kDaikinAuto = 0b000
kDaikinDry = 0b010
kDaikinCool = 0b011
kDaikinHeat = 0b100
kDaikinFan = 0b110
kDaikinModeOffset = 4
kDaikinModeSize = 3
kDaikinMinTemp = 10  # Celsius
kDaikinMaxTemp = 32  # Celsius
kDaikinFanMin = 1
kDaikinFanMed = 3
kDaikinFanMax = 5
kDaikinFanAuto = 0b1010  # 10 / 0xA
kDaikinFanQuiet = 0b1011  # 11 / 0xB
kDaikinFanOffset = 4
kDaikinFanSize = 4
kDaikinSwingOffset = 0
kDaikinSwingSize = 4
kDaikinSwingOn = 0b1111
kDaikinSwingOff = 0b0000
kDaikinHeaderLength = 5
kDaikinSections = 3
kDaikinSection1Length = 8
kDaikinSection2Length = 8
kDaikinSection3Length = kDaikinStateLength - kDaikinSection1Length - kDaikinSection2Length
kDaikinByteComfort = 6
kDaikinByteChecksum1 = 7
kDaikinBitComfortOffset = 4
kDaikinBitComfort = 1 << kDaikinBitComfortOffset
kDaikinByteClockMinsLow = 13
kDaikinByteClockMinsHigh = 14
kDaikinClockMinsHighOffset = 0
kDaikinClockMinsHighSize = 3
kDaikinDoWOffset = 3
kDaikinDoWSize = 3
kDaikinByteChecksum2 = 15
kDaikinBytePower = 21
kDaikinBitPowerOffset = 0
kDaikinBitPower = 1 << kDaikinBitPowerOffset
kDaikinTempOffset = 1
kDaikinTempSize = 6
kDaikinByteTemp = 22
kDaikinByteFan = 24
kDaikinByteSwingH = 25
kDaikinByteOnTimerMinsLow = 26
kDaikinByteOnTimerMinsHigh = 27
kDaikinOnTimerMinsHighOffset = 0
kDaikinOnTimerMinsHighSize = 4
kDaikinByteOffTimerMinsLow = kDaikinByteOnTimerMinsHigh
kDaikinByteOffTimerMinsHigh = 28
kDaikinBytePowerful = 29
kDaikinBitPowerfulOffset = 0
kDaikinBitPowerful = 1 << kDaikinBitPowerfulOffset
kDaikinByteSilent = kDaikinBytePowerful
kDaikinBitSilentOffset = 5
kDaikinBitSilent = 1 << kDaikinBitSilentOffset
kDaikinByteSensor = 32
kDaikinBitSensorOffset = 1
kDaikinBitSensor = 1 << kDaikinBitSensorOffset
kDaikinByteEcono = kDaikinByteSensor
kDaikinBitEconoOffset = 2
kDaikinBitEcono = 1 << kDaikinBitEconoOffset
kDaikinByteEye = kDaikinByteSensor
kDaikinBitEye = 0b10000000
kDaikinByteWeeklyTimer = kDaikinByteSensor
kDaikinBitWeeklyTimerOffset = 7
kDaikinBitWeeklyTimer = 1 << kDaikinBitWeeklyTimerOffset
kDaikinByteMold = 33
kDaikinBitMoldOffset = 1
kDaikinBitMold = 1 << kDaikinBitMoldOffset
kDaikinByteOffTimer = kDaikinBytePower
kDaikinBitOffTimerOffset = 2
kDaikinBitOffTimer = 1 << kDaikinBitOffTimerOffset
kDaikinByteOnTimer = kDaikinByteOffTimer
kDaikinBitOnTimerOffset = 1
kDaikinBitOnTimer = 1 << kDaikinBitOnTimerOffset
kDaikinByteChecksum3 = kDaikinStateLength - 1
kDaikinUnusedTime = 0x600
kDaikinBeepQuiet = 1
kDaikinBeepLoud = 2
kDaikinBeepOff = 3
kDaikinLightBright = 1
kDaikinLightDim = 2
kDaikinLightOff = 3
kDaikinCurBit = kDaikinStateLength
kDaikinCurIndex = kDaikinStateLength + 1
kDaikinTolerance = 35
kDaikinMarkExcess = kMarkExcess
kDaikinHdrMark = 3650   # kDaikinBitMark * 8
kDaikinHdrSpace = 1623  # kDaikinBitMark * 4
kDaikinBitMark = 428
kDaikinZeroSpace = 428
kDaikinOneSpace = 1280
kDaikinGap = 29000
# Note bits in each octet swapped so can be sent as a single value
kDaikinFirstHeader64 = 0b1101011100000000000000001100010100000000001001111101101000010001

# Another variant of the protocol for the Daikin ARC477A1 remote.
kDaikin2Freq = 36700  # Modulation Frequency in Hz.
kDaikin2LeaderMark = 10024
kDaikin2LeaderSpace = 25180
kDaikin2Gap = kDaikin2LeaderMark + kDaikin2LeaderSpace
kDaikin2HdrMark = 3500
kDaikin2HdrSpace = 1728
kDaikin2BitMark = 460
kDaikin2OneSpace = 1270
kDaikin2ZeroSpace = 420
kDaikin2Sections = 2
kDaikin2Section1Length = 20
kDaikin2Section2Length = 19
kDaikin2Tolerance = 5  # Extra percentage tolerance
kDaikin2BitSleepTimerOffset = 5
kDaikin2BitSleepTimer = 1 << kDaikin2BitSleepTimerOffset
kDaikin2BitPurifyOffset = 4
kDaikin2BitPurify = 1 << kDaikin2BitPurifyOffset  # 0b00010000
kDaikin2BitEyeOffset = 1
kDaikin2BitEye = 1 << kDaikin2BitEyeOffset  # 0b00000010
kDaikin2BitEyeAutoOffset = 7
kDaikin2BitEyeAuto = 1 << kDaikin2BitEyeAutoOffset  # 0b10000000
kDaikin2BitMoldOffset = 3
kDaikin2BitMold = 1 << kDaikin2BitMoldOffset    # 0b00001000
kDaikin2BitCleanOffset = 5  # Byte[8]
kDaikin2BitClean = 1 << kDaikin2BitCleanOffset  # 0b00100000
kDaikin2BitFreshAirOffset = 0
kDaikin2BitFreshAir = 1 << kDaikin2BitFreshAirOffset
kDaikin2BitFreshAirHighOffset = 7
kDaikin2BitFreshAirHigh = 1 << kDaikin2BitFreshAirHighOffset
kDaikin2BitPowerOffset = 7
kDaikin2BitPower = 1 << kDaikin2BitPowerOffset  # 0b10000000
# kDaikin2LightMask =    0b00110000  # Byte[7]
kDaikin2LightOffset = 4  # Byte[7]
kDaikin2LightSize = 2
# kDaikin2BeepMask =     0b11000000  # Byte[7]
kDaikin2BeepOffset = 6  # Byte[7]
kDaikin2BeepSize = 2
kDaikin2SwingVHigh = 0x1
kDaikin2SwingVLow = 0x6
kDaikin2SwingVSwing = 0xF
kDaikin2SwingVAuto = 0xE
kDaikin2SwingVBreeze = 0xC
kDaikin2SwingVCirculate = 0xD
kDaikin2FanByte = 28

# Ref:
#   https:#docs.google.com/spreadsheets/d/1f8EGfIbBUo2B-CzUFdrgKQprWakoYNKM80IKZN4KXQE/edit#gid=236366525&range=B25:D32
kDaikin2SwingHWide = 0xA3
kDaikin2SwingHLeftMax = 0xA8
kDaikin2SwingHLeft = 0xA9
kDaikin2SwingHMiddle = 0xAA
kDaikin2SwingHRight = 0xAB
kDaikin2SwingHRightMax = 0xAC
kDaikin2SwingHAuto = 0xBE
kDaikin2SwingHSwing = 0xBF

kDaikin2MinCoolTemp = 18  # Min temp (in C) when in Cool mode.

# Another variant of the protocol for the Daikin ARC433B69 remote.
kDaikin216Freq = 38000  # Modulation Frequency in Hz.
kDaikin216HdrMark = 3440
kDaikin216HdrSpace = 1750
kDaikin216BitMark = 420
kDaikin216OneSpace = 1300
kDaikin216ZeroSpace = 450
kDaikin216Gap = 29650
kDaikin216Sections = 2
kDaikin216Section1Length = 8
kDaikin216Section2Length = kDaikin216StateLength - kDaikin216Section1Length
kDaikin216BytePower = 13
kDaikin216ByteMode = kDaikin216BytePower
# kDaikin216MaskMode = 0b01110000
kDaikin216ByteTemp = 14
# kDaikin216MaskTemp = 0b01111110
kDaikin216TempOffset = 1
kDaikin216TempSize = 6

kDaikin216ByteFan = 16
kDaikin216MaskFan = 0b11110000
kDaikin216ByteSwingV = 16
# kDaikin216MaskSwingV = 0b00001111
kDaikin216SwingSize = 4
kDaikin216SwingOn = 0b1111
kDaikin216SwingOff = 0b0000
kDaikin216ByteSwingH = 17
kDaikin216BytePowerful = 21

# Another variant of the protocol for the Daikin ARC423A5 remote.
kDaikin160Freq = 38000  # Modulation Frequency in Hz.
kDaikin160HdrMark = 5000
kDaikin160HdrSpace = 2145
kDaikin160BitMark = 342
kDaikin160OneSpace = 1786
kDaikin160ZeroSpace = 700
kDaikin160Gap = 29650
kDaikin160Sections = 2
kDaikin160Section1Length = 7
kDaikin160Section2Length = kDaikin160StateLength - kDaikin160Section1Length
kDaikin160BytePower = 12
kDaikin160ByteMode = kDaikin160BytePower
# kDaikin160MaskMode = 0b01110000
kDaikin160ByteTemp = 16
# kDaikin160MaskTemp = 0b01111110
kDaikin160TempOffset = 1
kDaikin160TempSize = 6
kDaikin160ByteFan = 17
kDaikin160MaskFan = 0b00001111
kDaikin160ByteSwingV = 13
kDaikin160MaskSwingV = 0b11110000
kDaikin160SwingVLowest = 0x1
kDaikin160SwingVLow = 0x2
kDaikin160SwingVMiddle = 0x3
kDaikin160SwingVHigh = 0x4
kDaikin160SwingVHighest = 0x5
kDaikin160SwingVAuto = 0xF

# Another variant of the protocol for the Daikin BRC4C153 remote.
kDaikin176Freq = 38000  # Modulation Frequency in Hz.
kDaikin176HdrMark = 5070
kDaikin176HdrSpace = 2140
kDaikin176BitMark = 370
kDaikin176OneSpace = 1780
kDaikin176ZeroSpace = 710
kDaikin176Gap = 29410
kDaikin176Sections = 2
kDaikin176Section1Length = 7
kDaikin176Section2Length = kDaikin176StateLength - kDaikin176Section1Length
kDaikin176Cool = 0b111  # 7
kDaikin176BytePower = 14
kDaikin176ByteMode = 12
kDaikin176MaskMode = 0b01110000
kDaikin176ByteModeButton = 13
kDaikin176ModeButton = 0b00000100
kDaikin176ByteTemp = 17
# kDaikin176MaskTemp = 0b01111110
kDaikin176TempOffset = 1
kDaikin176TempSize = 6
kDaikin176DryFanTemp = 17  # Dry/Fan mode is always 17 Celsius.
kDaikin176ByteFan = 18
kDaikin176MaskFan = 0b11110000
kDaikin176FanMax = 3
kDaikin176ByteSwingH = 18
# kDaikin176MaskSwingH = 0b00001111
kDaikin176SwingHAuto = 0x5
kDaikin176SwingHOff = 0x6

# Another variant of the protocol for the Daikin BRC52B63 remote.
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/827
kDaikin128Freq = 38000  # Modulation Frequency in Hz.
kDaikin128LeaderMark = 9800
kDaikin128LeaderSpace = 9800
kDaikin128HdrMark = 4600
kDaikin128HdrSpace = 2500
kDaikin128BitMark = 350
kDaikin128OneSpace = 954
kDaikin128ZeroSpace = 382
kDaikin128Gap = 20300
kDaikin128FooterMark = kDaikin128HdrMark
kDaikin128Sections = 2
kDaikin128SectionLength = 8
kDaikin128ByteModeFan = 1
# kDaikin128MaskMode =     0b00001111
kDaikin128ModeSize = 4
kDaikin128Dry = 0b00000001
kDaikin128Cool = 0b00000010
kDaikin128Fan = 0b00000100
kDaikin128Heat = 0b00001000
kDaikin128Auto = 0b00001010
kDaikin128MaskFan = 0b11110000
kDaikin128FanAuto = 0b0001
kDaikin128FanHigh = 0b0010
kDaikin128FanMed = 0b0100
kDaikin128FanLow = 0b1000
kDaikin128FanPowerful = 0b0011
kDaikin128FanQuiet =  0b1001
kDaikin128ByteClockMins = 2
kDaikin128ByteClockHours = 3
kDaikin128ByteOnTimer = 4
kDaikin128ByteOffTimer = 5
kDaikin128BitTimerEnabledOffset = 7
kDaikin128BitTimerEnabled = 1 << kDaikin128BitTimerEnabledOffset
kDaikin128TimerOffset = 0
kDaikin128TimerSize = 7
kDaikin128HalfHourOffset = 6
kDaikin128BitHalfHour = 1 << kDaikin128HalfHourOffset
# kDaikin128MaskHours =       0b00111111
kDaikin128HoursOffset = 0
kDaikin128HoursSize = 6
kDaikin128ByteTemp = 6
kDaikin128MinTemp = 16  # C
kDaikin128MaxTemp = 30  # C
kDaikin128BytePowerSwingSleep = 7
kDaikin128BitSwingOffset = 0
kDaikin128BitSwing = 1 << kDaikin128BitSwingOffset  # 0b00000001
kDaikin128BitSleepOffset = 1
kDaikin128BitSleep = 1 << kDaikin128BitSleepOffset  # 0b00000010
kDaikin128BitPowerToggleOffset = 3
kDaikin128BitPowerToggle = 1 << kDaikin128BitPowerToggleOffset
kDaikin128ByteEconoLight = 9
kDaikin128BitEconoOffset = 2
kDaikin128BitEcono = 1 << kDaikin128BitEconoOffset  # 0b00000100
kDaikin128BitWall = 0b00001000
kDaikin128BitCeiling = 0b00000001
kDaikin128MaskLight = kDaikin128BitWall | kDaikin128BitCeiling

# Another variant of the protocol for the Daikin ARC480A5 remote.
# Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/873
kDaikin152Freq = 38000  # Modulation Frequency in Hz.
kDaikin152LeaderBits = 5
kDaikin152HdrMark = 3492
kDaikin152HdrSpace = 1718
kDaikin152BitMark = 433
kDaikin152OneSpace = 1529
kDaikin152ZeroSpace = kDaikin152BitMark
kDaikin152Gap = 25182

# Byte[5]
kDaikin152ModeByte = 5                        # Mask 0b01110000
kDaikin152PowerByte = kDaikin152ModeByte      # Mask 0b00000001
# Byte[6]
kDaikin152TempByte = 6                        # Mask 0b11111110
kDaikin152TempSize = 7
kDaikin152DryTemp = kDaikin2MinCoolTemp  # Celsius
kDaikin152FanTemp = 0x60  # 96 Celsius
# Byte[8]
kDaikin152FanByte = 8
kDaikin152SwingVByte = kDaikin152FanByte
# Byte[13]
kDaikin152QuietByte = 13                      # Mask 0b00100000
kDaikin152PowerfulByte = kDaikin152QuietByte  # Mask 0b00000001
# Byte[16]
kDaikin152EconoByte = 16                      # Mask 0b00000100
kDaikin152ComfortByte = kDaikin152EconoByte   # Mask 0b00000010
kDaikin152ComfortOffset = 1                   # Mask 0b00000010
kDaikin152SensorByte = kDaikin152EconoByte    # Mask 0b00001000
kDaikin152SensorOffset = 3                    # Mask 0b00001000


"""

/*
        Daikin AC map (i.e. DAIKIN, not the other variants)
        byte 6=
          b4:Comfort
        byte 7= checksum of the first part (and last byte before a 29ms pause)
        byte 13=Current time, mins past midnight, low bits
        byte 14
                b5-b3=Day of the week (SUN=1, MON=2, ..., SAT=7)
                b2-b0=Current time, mins past midnight, high bits
        byte 15= checksum of the second part (and last byte before a 29ms pause)
        byte 21=mode
                b7 = 0
                b6+b5+b4 = Mode
                        Modes: b6+b5+b4
                        011 = Cool
                        100 = Heat (temp 23)
                        110 = FAN (temp not shown, but 25)
                        000 = Fully Automatic (temp 25)
                        010 = DRY (temp 0xc0 = 96 degrees c)
                b3 = 1
                b2 = OFF timer set
                b1 = ON timer set
                b0 = Air Conditioner ON
        byte 22=temp*2   (Temp should be between 10 - 32)
        byte 24=Fan
                FAN control
                b7+b6+b5+b4 = Fan speed
                        Fan: b7+b6+b5+b4
                        0×3 = 1 bar
                        0×4 = 2 bar
                        0×5 = 3 bar
                        0×6 = 4 bar
                        0×7 = 5 bar
                        0xa = Auto
                        0xb = Quite
                b3+b2+b1+b0 = Swing control up/down
                        Swing control up/down:
                        0000 = Swing up/down off
                        1111 = Swing up/down on
        byte 25
                        Swing control left/right:
                        0000 = Swing left/right off
                        1111 = Swing left/right on
        byte 26=On timer mins past midnight, low bits
        byte 27
        b0-b3=On timer mins past midnight, high bits
        b4-b7=Off timer mins past midnight, low bits
        byte 28=Off timer mins past midnight, high bits
        byte 29=Aux  .Powerful (bit 1), Silent (bit 5)
        byte 32=Aux2
        b1: Sensor
        b2: Econo mode
        b7: Intelligent eye on
        byte 33=Aux3
        b1: Mold Proof
        byte 34= checksum of the third part
*/


# Legacy defines.
DAIKIN_COOL = kDaikinCool
DAIKIN_HEAT = kDaikinHeat
DAIKIN_FAN = kDaikinFan
DAIKIN_AUTO = kDaikinAuto
DAIKIN_DRY = kDaikinDry
DAIKIN_MIN_TEMP = kDaikinMinTemp
DAIKIN_MAX_TEMP = kDaikinMaxTemp
DAIKIN_FAN_MIN = kDaikinFanMin
DAIKIN_FAN_MAX = kDaikinFanMax
DAIKIN_FAN_AUTO = kDaikinFanAuto
DAIKIN_FAN_QUIET = kDaikinFanQuiet

class IRDaikinESP {
 public:
  explicit IRDaikinESP(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_DAIKIN
  void send(repeat = kDaikinDefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin(void)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(temp)
  getTemp()
  void setFan(fan)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setSwingVertical(bool on)
  bool getSwingVertical(void)
  void setSwingHorizontal(bool on)
  bool getSwingHorizontal(void)
  bool getQuiet(void)
  void setQuiet(bool on)
  bool getPowerful(void)
  void setPowerful(bool on)
  void setSensor(bool on)
  bool getSensor(void)
  void setEcono(bool on)
  bool getEcono(void)
  void setMold(bool on)
  bool getMold(void)
  void setComfort(bool on)
  bool getComfort(void)
  void enableOnTimer(starttime)
  void disableOnTimer(void)
  getOnTime(void)
  bool getOnTimerEnabled()
  void enableOffTimer(endtime)
  void disableOffTimer(void)
  getOffTime(void)
  bool getOffTimerEnabled(void)
  void setCurrentTime(mins_since_midnight)
  getCurrentTime(void)
  void setCurrentDay(day_of_week)
  getCurrentDay(void)
  void setWeeklyTimerEnable(bool on)
  bool getWeeklyTimerEnable(void)
  uint8_t* getRaw(void)
  void setRaw(new_code[],
              length = kDaikinStateLength)
  static bool validChecksum(state[],
                            length = kDaikinStateLength)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote[kDaikinStateLength]
  void stateReset(void)
  void checksum(void)
}

# Class to emulate a Daikin ARC477A1 remote.
class IRDaikin2 {
 public:
  explicit IRDaikin2(pin, bool inverted = False,
                     bool use_modulation = True)

#if SEND_DAIKIN2
  void send(repeat = kDaikin2DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin()
  void on()
  void off()
  void setPower(bool state)
  bool getPower()
  void setTemp(temp)
  getTemp()
  void setFan(fan)
  getFan()
  getMode()
  void setMode(mode)
  void setSwingVertical(position)
  getSwingVertical()
  void setSwingHorizontal(position)
  getSwingHorizontal()
  bool getQuiet()
  void setQuiet(bool on)
  bool getPowerful()
  void setPowerful(bool on)
  void setSensor(bool on)
  bool getSensor()
  void setEcono(bool on)
  bool getEcono()
  void setEye(bool on)
  bool getEye()
  void setEyeAuto(bool on)
  bool getEyeAuto()
  void setPurify(bool on)
  bool getPurify()
  void setMold(bool on)
  bool getMold()
  void enableOnTimer(starttime)
  void disableOnTimer()
  getOnTime()
  bool getOnTimerEnabled()
  void enableSleepTimer(sleeptime)
  void disableSleepTimer()
  getSleepTime()
  bool getSleepTimerEnabled()
  void enableOffTimer(endtime)
  void disableOffTimer()
  getOffTime()
  bool getOffTimerEnabled()
  void setCurrentTime(time)
  getCurrentTime()
  void setBeep(beep)
  getBeep()
  void setLight(light)
  getLight()
  void setClean(bool on)
  bool getClean()
  void setFreshAir(bool on)
  bool getFreshAir()
  void setFreshAirHigh(bool on)
  bool getFreshAirHigh()
  uint8_t* getRaw()
  void setRaw(new_code[])
  getCommand()
  void setCommand(value)
  static bool validChecksum(state[],
                            length = kDaikin2StateLength)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static convertSwingV(stdAc.swingv_t position)
  static convertSwingH(stdAc.swingh_t position)
  static stdAc.swingv_t toCommonSwingV(setting)
  static stdAc.swingh_t toCommonSwingH(setting)
  stdAc.state_t toCommon(void)
  String toString()
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin2StateLength]
  void stateReset()
  void checksum()
  void clearOnTimerFlag()
  void clearSleepTimerFlag()
}

# Class to emulate a Daikin ARC433B69 remote.
class IRDaikin216 {
 public:
  explicit IRDaikin216(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_DAIKIN216
  void send(repeat = kDaikin216DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin()
  uint8_t* getRaw()
  void setRaw(new_code[])
  static bool validChecksum(state[],
                            length = kDaikin216StateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(temp)
  getTemp()
  void setMode(mode)
  getMode(void)
  static convertMode(stdAc.opmode_t mode)
  void setFan(fan)
  getFan(void)
  static convertFan(stdAc.fanspeed_t speed)
  void setSwingVertical(bool on)
  bool getSwingVertical(void)
  void setSwingHorizontal(bool on)
  bool getSwingHorizontal(void)
  void setQuiet(bool on)
  bool getQuiet(void)
  void setPowerful(bool on)
  bool getPowerful(void)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin216StateLength]
  void stateReset()
  void checksum()
}

# Class to emulate a Daikin ARC423A5 remote.
class IRDaikin160 {
 public:
  explicit IRDaikin160(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_DAIKIN160
  void send(repeat = kDaikin160DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin()
  uint8_t* getRaw()
  void setRaw(new_code[])
  static bool validChecksum(state[],
                            length = kDaikin160StateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(temp)
  getTemp()
  void setMode(mode)
  getMode(void)
  static convertMode(stdAc.opmode_t mode)
  void setFan(fan)
  getFan(void)
  static convertFan(stdAc.fanspeed_t speed)
  void setSwingVertical(position)
  getSwingVertical(void)
  static convertSwingV(stdAc.swingv_t position)
  static stdAc.swingv_t toCommonSwingV(setting)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin160StateLength]
  void stateReset()
  void checksum()
}

# Class to emulate a Daikin BRC4C153 remote.
class IRDaikin176 {
 public:
  explicit IRDaikin176(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_DAIKIN176
  void send(repeat = kDaikin176DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin()
  uint8_t* getRaw()
  void setRaw(new_code[])
  static bool validChecksum(state[],
                            length = kDaikin176StateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(temp)
  getTemp()
  void setMode(mode)
  getMode(void)
  static convertMode(stdAc.opmode_t mode)
  void setFan(fan)
  getFan(void)
  static convertFan(stdAc.fanspeed_t speed)
  void setSwingHorizontal(position)
  getSwingHorizontal(void)
  static convertSwingH(stdAc.swingh_t position)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.swingh_t toCommonSwingH(setting)
  stdAc.state_t toCommon(void)
  String toString(void)

#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin176StateLength]
  _saved_temp
  void stateReset()
  void checksum()
}

# Class to emulate a Daikin BRC52B63 remote / Daikin 17 series A/C.
class IRDaikin128 {
 public:
  explicit IRDaikin128(pin, bool inverted = False,
                       bool use_modulation = True)
#if SEND_DAIKIN128
  void send(repeat = kDaikin128DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif  # SEND_DAIKIN128
  void begin()
  void setPowerToggle(bool toggle)
  bool getPowerToggle(void)
  void setTemp(temp)
  getTemp(void)
  void setFan(fan)
  getFan(void)
  getMode(void)
  void setMode(mode)
  void setSwingVertical(bool on)
  bool getSwingVertical()
  bool getSleep(void)
  void setSleep(bool on)
  bool getQuiet(void)
  void setQuiet(bool on)
  bool getPowerful(void)
  void setPowerful(bool on)
  void setEcono(bool on)
  bool getEcono(void)
  void setOnTimer(mins_since_midnight)
  getOnTimer(void)
  bool getOnTimerEnabled(void)
  void setOnTimerEnabled(bool on)
  void setOffTimer(mins_since_midnight)
  getOffTimer(void)
  bool getOffTimerEnabled(void)
  void setOffTimerEnabled(bool on)
  void setClock(mins_since_midnight)
  getClock(void)
  void setLightToggle(unit_type)
  getLightToggle(void)
  uint8_t* getRaw(void)
  void setRaw(new_code[])
  static bool validChecksum(state[])
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  stdAc.state_t toCommon(stdAc.state_t *prev = NULL)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin128StateLength]
  void stateReset(void)
  static calcFirstChecksum(state[])
  static calcSecondChecksum(state[])
  static void setTimer(*ptr, mins_since_midnight)
  static getTimer(*ptr)
  void checksum(void)
  void clearOnTimerFlag(void)
  void clearSleepTimerFlag(void)
}

# Class to emulate a Daikin ARC480A5 remote.
class IRDaikin152 {
 public:
  explicit IRDaikin152(pin, bool inverted = False,
                       bool use_modulation = True)

#if SEND_DAIKIN152
  void send(repeat = kDaikin152DefaultRepeat)
  calibrate(void) { return _irsend.calibrate() }
#endif
  void begin()
  uint8_t* getRaw()
  void setRaw(new_code[])
  static bool validChecksum(state[],
                            length = kDaikin152StateLength)
  void on(void)
  void off(void)
  void setPower(bool on)
  bool getPower(void)
  void setTemp(temp)
  getTemp()
  void setFan(fan)
  getFan(void)
  void setMode(mode)
  getMode(void)
  void setSwingV(bool on)
  bool getSwingV(void)
  bool getQuiet(void)
  void setQuiet(bool on)
  bool getPowerful(void)
  void setPowerful(bool on)
  void setSensor(bool on)
  bool getSensor(void)
  void setEcono(bool on)
  bool getEcono(void)
  void setComfort(bool on)
  bool getComfort(void)
  static convertMode(stdAc.opmode_t mode)
  static convertFan(stdAc.fanspeed_t speed)
  static stdAc.opmode_t toCommonMode(mode)
  static stdAc.fanspeed_t toCommonFanSpeed(speed)
  stdAc.state_t toCommon(void)
  String toString(void)
#ifndef UNIT_TEST

 private:
  IRsend _irsend
#else
  IRsendTest _irsend
#endif
  # # of bytes per command
  remote_state[kDaikin152StateLength]
  void stateReset()
  void checksum()
}
#endif  # IR_DAIKIN_H_

"""
# /*
# An Arduino sketch to emulate IR Daikin ARC433** & ARC477A1 remote control unit
# Read more at:
# http:#harizanov.com/2012/02/control-daikin-air-conditioner-over-the-internet/
# 
# Copyright 2016 sillyfrog
# Copyright 2017 sillyfrog, crankyoldgit
# Copyright 2018-2019 crankyoldgit
# Copyright 2019 pasna (IRDaikin160 class / Daikin176 class)
# */

# Constants
# Ref:
#   https:#github.com/mharizanov/Daikin-AC-remote-control-over-the-Internet/tree/master/IRremote
#   http:#rdlab.cdmt.vn/project-2013/daikin-ir-protocol
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/582

addBoolToString = irutils.addBoolToString
addDayToString = irutils.addDayToString
addIntToString = irutils.addIntToString
addLabeledString = irutils.addLabeledString
addModeToString = irutils.addModeToString
addTempToString = irutils.addTempToString
addFanToString = irutils.addFanToString
bcdToUint8 = irutils.bcdToUint8
minsToString = irutils.minsToString
setBit = irutils.setBit
setBits = irutils.setBits
sumNibbles = irutils.sumNibbles
uint8ToBcd = irutils.uint8ToBcd

class Daikin(ProtocolBase):


    # Send a Daikin A/C message.
    #
    # Args:
    #   data: An array of kDaikinStateLength bytes containing the IR command.
    #
    # Status: STABLE
    #
    # Ref:
    #   IRDaikinESP.cpp
    #   https:#github.com/mharizanov/Daikin-AC-remote-control-over-the-Internet/tree/master/IRremote
    #   https:#github.com/blafois/Daikin-IR-Reverse
    def send_ac(self, data, nbytes, repeat):
        if nbytes < kDaikinStateLengthShort:
            return  # Not enough bytes to send a proper message.

        for _ in range(repeat + 1):
            offset = 0
            # Send the header, 0b00000
            self.sendGeneric(
                0,
                0,  # No header for the header
                kDaikinBitMark,
                kDaikinOneSpace,
                kDaikinBitMark,
                kDaikinZeroSpace,
                kDaikinBitMark,
                kDaikinZeroSpace + kDaikinGap,
                0b00000,
                kDaikinHeaderLength,
                38,
                False,
                0,
                50
            )
            # Data #1
            if nbytes < kDaikinStateLength: # Are we using the legacy size?
                # Do this as a constant to save RAM and keep in flash memory
                self.sendGeneric(
                    kDaikinHdrMark,
                    kDaikinHdrSpace,
                    kDaikinBitMark,
                    kDaikinOneSpace,
                    kDaikinBitMark,
                    kDaikinZeroSpace,
                    kDaikinBitMark,
                    kDaikinZeroSpace + kDaikinGap,
                    kDaikinFirstHeader64,
                    64,
                    38,
                    False,
                    0,
                    50
                )
            else:  # We are using the newer/more correct size.
                self.sendGeneric(
                    kDaikinHdrMark,
                    kDaikinHdrSpace,
                    kDaikinBitMark,
                    kDaikinOneSpace,
                    kDaikinBitMark,
                    kDaikinZeroSpace,
                    kDaikinBitMark,
                    kDaikinZeroSpace + kDaikinGap,
                    data,
                    kDaikinSection1Length,
                    38,
                    False,
                    0,
                    50
                )
            offset += kDaikinSection1Length

            # Data #2
            self.sendGeneric(
                kDaikinHdrMark,
                kDaikinHdrSpace,
                kDaikinBitMark,
                kDaikinOneSpace,
                kDaikinBitMark,
                kDaikinZeroSpace,
                kDaikinBitMark,
                kDaikinZeroSpace + kDaikinGap,
                data[offset:],
                kDaikinSection2Length,
                38,
                False,
                0,
                50
            )

            offset += kDaikinSection2Length

            # Data #3
            self.sendGeneric(
                kDaikinHdrMark,
                kDaikinHdrSpace,
                kDaikinBitMark,
                kDaikinOneSpace,
                kDaikinBitMark,
                kDaikinZeroSpace,
                kDaikinBitMark,
                kDaikinZeroSpace + kDaikinGap,
                data[offset:],
                nbytes - offset,
                38,
                False,
                0,
                50
            )

    # if DECODE_DAIKIN
    # Decode the supplied Daikin A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikinBits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Status: STABLE / Reported as working.
    #
    # Ref:
    #   https:#github.com/mharizanov/Daikin-AC-remote-control-over-the-Internet/tree/master/IRremote
    def decode_ac(self, results, nbits, strict):
        # Is there enough data to match successfully?
        if (
            results.rawlen < (
                2 * (nbits + kDaikinHeaderLength) + kDaikinSections * (kHeader + kFooter) + kFooter - 1
            )
        ):
            return False

        # Compliance
        if strict and nbits != kDaikinBits:
            return False

        offset = kStartOffset

        # Header #1 - Doesn't count as data.
        data_result = self.matchData(
            results.rawbuf[offset],
            kDaikinHeaderLength,
            kDaikinBitMark,
            kDaikinOneSpace,
            kDaikinBitMark,
            kDaikinZeroSpace,
            kDaikinTolerance,
            kDaikinMarkExcess,
            False
        )
        offset += data_result.used
        if data_result.success is False:
            return False  # Fail

        if data_result.data:
            return False  # The header bits should be zero.

        # Footer
        offset += 1
        if not self.matchMark(
                results.rawbuf[offset],
                kDaikinBitMark,
                kDaikinTolerance,
                kDaikinMarkExcess
        ):
            return False
        offset += 1
        if not self.matchSpace(
                results.rawbuf[offset],
                kDaikinZeroSpace + kDaikinGap,
                kDaikinTolerance,
                kDaikinMarkExcess
        ):
            return False

        # Sections
        ksectionSize[kDaikinSections] = [
            kDaikinSection1Length,
            kDaikinSection2Length,
            kDaikinSection3Length
        ]

        pos = 0
        for section in range(kDaikinSections):

            # Section Header + Section Data (7 bytes) + Section Footer
            used = self.matchGeneric(
                results.rawbuf[offset:],
                results.state + pos,
                results.rawlen - offset,
                ksectionSize[section] * 8,
                kDaikinHdrMark,
                kDaikinHdrSpace,
                kDaikinBitMark,
                kDaikinOneSpace,
                kDaikinBitMark,
                kDaikinZeroSpace,
                kDaikinBitMark,
                kDaikinZeroSpace + kDaikinGap,
                section >= kDaikinSections - 1,
                kDaikinTolerance,
                kDaikinMarkExcess,
                False
            )
            if used == 0:
                return False

            offset += used

            pos += ksectionSize[section]

        # Compliance
        # Re-check we got the correct size/length due to the way we read the data.
        if (
            strict and (
                pos * 8 != kDaikinBits or
                not IRDaikinESP.validChecksum(results.state)
            )
        ):
            return False

        # Success
        results.decode_type = DAIKIN
        results.bits = nbits
        # No need to record the state as we stored it as we decoded it.
        # As we use result.state, we don't record value, address, or command as it
        # is a union data type.
        return True


class IRDaikinESP(ProtocolBase):

    def send_ac(self, repeat):
        self._irsend.sendDaikin(self.getRaw(), kDaikinStateLength, repeat)

    # Verify the checksums are valid for a given state.
    # Args:
    #   state:  The array to verify the checksums of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        # Data #1
        if (
            length < kDaikinSection1Length or
            state[kDaikinByteChecksum1] != sumBytes(state, kDaikinSection1Length - 1)
        ):
            return False
        # Data #2
        if (
            length < kDaikinSection1Length + kDaikinSection2Length or
            state[kDaikinByteChecksum2] != sumBytes(
                state + kDaikinSection1Length,
                kDaikinSection2Length - 1
            )
        ):
            return False
        # Data #3
        if (
            length < kDaikinSection1Length + kDaikinSection2Length + 2 or
            state[length - 1] != sumBytes(
                state + kDaikinSection1Length + kDaikinSection2Length,
                length - (kDaikinSection1Length + kDaikinSection2Length) - 1
            )
        ):
            return False

        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikinByteChecksum1] = sumBytes(
            self.remote_state,
            kDaikinSection1Length - 1
        )
        self.remote_state[kDaikinByteChecksum2] = sumBytes(
            self.remote_state[:kDaikinSection1Length],
            kDaikinSection2Length - 1
        )
        self.remote_state[kDaikinByteChecksum3] = sumBytes(
            self.remote_state[kDaikinSection1Length:kDaikinSection2Length],
            kDaikinSection3Length - 1
        )

    def stateReset(self):
        self.remote_state = [0x0] * kDaikinStateLength
        self.remote_state = [
            0x11,
            0xDA,
            0x27,
            0x0,
            0xC5,
            # remote[7] is a checksum byte, it will be set by checksum().
            0x0,
            0x0,
            0x0,
            0x11,
            0xDA,
            0x27,
            0x0,
            0x42,
            0x0,
            0x0,
            0x0,
            # remote[15] is a checksum byte, it will be set by checksum().
            0x11,
            0xDA,
            0x27,
            0x0,
            0x0,
            0x49,
            0x1E,
            0x0,
            0xB0,
            0x0,
            0x0,
            0x06,
            0x60,
            0x0,
            0x0,
            0xC0
            # remote[34] is a checksum byte, it will be set by checksum().
        ]
        self.checksum()

    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote_state[:]

    def setRaw(self, new_code, length):
        offset = 0
        if length == kDaikinStateLengthShort:  # Handle the "short" length case.
            offset = kDaikinStateLength - kDaikinStateLengthShort
            self.stateReset()

        i = 0
        while i < length and i < kDaikinStateLength:
            self.remote_state[i + offset] = new_code[i]
            i += 1

    def setPower(self, on):
        setBit(self.remote_state[kDaikinBytePower], kDaikinBitPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote_state[kDaikinBytePower], kDaikinBitPowerOffset)

    # Set the temp in deg C
    def setTemp(self, temp):
        degrees = max(temp, kDaikinMinTemp)
        degrees = min(degrees, kDaikinMaxTemp)
        self.remote_state[kDaikinByteTemp] = degrees << 1

    def getTemp(self):
        return self.remote_state[kDaikinByteTemp] >> 1

    # Set the speed of the fan, 1-5 or kDaikinFanAuto or kDaikinFanQuiet
    def setFan(self, fan):
        # Set the fan speed bits, leave low 4 bits alone
        if fan == kDaikinFanQuiet or fan == kDaikinFanAuto:
            fanset = fan
        elif fan < kDaikinFanMin or fan > kDaikinFanMax:
            fanset = kDaikinFanAuto
        else:
            fanset = 2 + fan

        setBits(self.remote_state[kDaikinByteFan], kDaikinFanOffset, kDaikinFanSize, fanset)

    def getFan(self):
        fan = GETBITS8(self.remote_state[kDaikinByteFan], kDaikinFanOffset, kDaikinFanSize)
        if fan not in (kDaikinFanQuiet, kDaikinFanAuto):
            fan -= 2

        return fan

    def getMode(self):
        return GETBITS8(self.remote_state[kDaikinBytePower], kDaikinModeOffset, kDaikinModeSize)

    def setMode(self, mode):
        if mode in (
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinFan,
            kDaikinDry
        ):
            setBits(self.remote_state[kDaikinBytePower], kDaikinModeOffset, kDaikinModeSize, mode)
        else:
            self.setMode(kDaikinAuto)

    def setSwingVertical(self, on):
        setBits(
            self.remote_state[kDaikinByteFan],
            kDaikinSwingOffset,
            kDaikinSwingSize,
            kDaikinSwingOn if on else kDaikinSwingOff
        )

    def getSwingVertical(self):
        return GETBITS8(self.remote_state[kDaikinByteFan], kDaikinSwingOffset, kDaikinSwingSize)

    def setSwingHorizontal(self, on):
        setBits(
            self.remote_state[kDaikinByteSwingH],
            kDaikinSwingOffset,
            kDaikinSwingSize,
            kDaikinSwingOn if on else kDaikinSwingOff
        )

    def getSwingHorizontal(self):
        return GETBITS8(self.remote_state[kDaikinByteSwingH], kDaikinSwingOffset, kDaikinSwingSize)

    def setQuiet(self, on):
        setBit(self.remote_state[kDaikinByteSilent], kDaikinBitSilentOffset, on)
        # Powerful & Quiet mode being on are mutually exclusive.
        if on:
            self.setPowerful(False)

    def getQuiet(self):
        return GETBIT8(self.remote_state[kDaikinByteSilent], kDaikinBitSilentOffset)

    def setPowerful(self, on):
        setBit(self.remote_state[kDaikinBytePowerful], kDaikinBitPowerfulOffset, on)
        if on:
            # Powerful, Quiet, & Econo mode being on are mutually exclusive.
            self.setQuiet(False)
            self.setEcono(False)

    def getPowerful(self):
        return GETBIT8(self.remote_state[kDaikinBytePowerful], kDaikinBitPowerfulOffset)

    def setSensor(self, on):
        setBit(self.remote_state[kDaikinByteSensor], kDaikinBitSensorOffset, on)

    def getSensor(self):
        return GETBIT8(self.remote_state[kDaikinByteSensor], kDaikinBitSensorOffset)

    def setEcono(self, on):
        setBit(self.remote_state[kDaikinByteEcono], kDaikinBitEconoOffset, on)
        # Powerful & Econo mode being on are mutually exclusive.
        if on:
            self.setPowerful(False)

    def getEcono(self):
        return GETBIT8(self.remote_state[kDaikinByteEcono], kDaikinBitEconoOffset)

    def setMold(self, on):
        setBit(self.remote_state[kDaikinByteMold], kDaikinBitMoldOffset, on)

    def getMold(self):
        return GETBIT8(self.remote_state[kDaikinByteMold], kDaikinBitMoldOffset)

    def setComfort(self, on):
        setBit(self.remote_state[kDaikinByteComfort], kDaikinBitComfortOffset, on)

    def getComfort(self):
        return GETBIT8(self.remote_state[kDaikinByteComfort], kDaikinBitComfortOffset)

    # starttime: Number of minutes after midnight.
    def enableOnTimer(self, starttime):
        setBit(self.remote_state[kDaikinByteOnTimer], kDaikinBitOnTimerOffset)
        self.remote_state[kDaikinByteOnTimerMinsLow] = starttime
        # only keep 4 bits
        setBits(
            self.remote_state[kDaikinByteOnTimerMinsHigh],
            kDaikinOnTimerMinsHighOffset,
            kDaikinOnTimerMinsHighSize,
            starttime >> 8
        )

    def disableOnTimer(self):
        self.enableOnTimer(kDaikinUnusedTime)
        setBit(self.remote_state[kDaikinByteOnTimer], kDaikinBitOnTimerOffset, False)

    def getOnTime(self):
        return GETBITS8(
            self.remote_state[kDaikinByteOnTimerMinsHigh],
            kDaikinOnTimerMinsHighOffset,
            kDaikinOnTimerMinsHighSize
        ) << 8 + self.remote_state[kDaikinByteOnTimerMinsLow]

    def getOnTimerEnabled(self):
        return GETBIT8(self.remote_state[kDaikinByteOnTimer], kDaikinBitOnTimerOffset)

    # endtime: Number of minutes after midnight.
    def enableOffTimer(self, endtime):
        setBit(self.remote_state[kDaikinByteOffTimer], kDaikinBitOffTimerOffset)
        self.remote_state[kDaikinByteOffTimerMinsHigh] = endtime >> kNibbleSize
        setBits(self.remote_state[kDaikinByteOffTimerMinsLow], kHighNibble, kNibbleSize, endtime)

    def disableOffTimer(self):
        self.enableOffTimer(kDaikinUnusedTime)
        setBit(self.remote_state[kDaikinByteOffTimer], kDaikinBitOffTimerOffset, False)

    def getOffTime(self):
        return (
            self.remote_state[kDaikinByteOffTimerMinsHigh] << kNibbleSize
        ) + GETBITS8(self.remote_state[kDaikinByteOffTimerMinsLow], kHighNibble, kNibbleSize)

    def getOffTimerEnabled(self):
        return GETBIT8(self.remote_state[kDaikinByteOffTimer], kDaikinBitOffTimerOffset)

    def setCurrentTime(self, mins_since_midnight):
        mins = mins_since_midnight
        if mins > 24 * 60:
            mins = 0  # If > 23:59, set to 00:00

        self.remote_state[kDaikinByteClockMinsLow] = mins
        # only keep 3 bits
        setBits(
            self.remote_state[kDaikinByteClockMinsHigh],
            kDaikinClockMinsHighOffset,
            kDaikinClockMinsHighSize,
            mins >> 8
        )

    def getCurrentTime(self):
        return GETBITS8(
            self.remote_state[kDaikinByteClockMinsHigh],
            kDaikinClockMinsHighOffset,
            kDaikinClockMinsHighSize
        ) << 8 + self.remote_state[kDaikinByteClockMinsLow]

    def setCurrentDay(self, day_of_week):
        # 1 is SUN, 2 is MON, ..., 7 is SAT
        setBits(self.remote_state[kDaikinByteClockMinsHigh], kDaikinDoWOffset, kDaikinDoWSize, day_of_week)

    def getCurrentDay(self):
        return GETBITS8(self.remote_state[kDaikinByteClockMinsHigh], kDaikinDoWOffset, kDaikinDoWSize)

    def setWeeklyTimerEnable(self, on):
        # Bit is cleared for `on`.
        setBit(self.remote_state[kDaikinByteWeeklyTimer], kDaikinBitWeeklyTimerOffset, not on)

    def getWeeklyTimerEnable(self):
        return not GETBIT8(self.remote_state[kDaikinByteWeeklyTimer], kDaikinBitWeeklyTimerOffset)

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        if mode == stdAc.opmode_t.kCool:
            return kDaikinCool
        if mode == stdAc.opmode_t.kHeat:
            return kDaikinHeat
        if mode == stdAc.opmode_t.kDry:
            return kDaikinDry
        if mode == stdAc.opmode_t.kFan:
            return kDaikinFan

        return kDaikinAuto

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        if speed == stdAc.fanspeed_t.kMin:
            return kDaikinFanQuiet
        if speed == stdAc.fanspeed_t.kLow:
            return kDaikinFanMin
        if speed == stdAc.fanspeed_t.kMedium:
            return kDaikinFanMed
        if speed == stdAc.fanspeed_t.kHigh:
            return kDaikinFanMax - 1
        if speed == stdAc.fanspeed_t.kMax:
            return kDaikinFanMax

        return kDaikinFanAuto

    # Convert a native mode to it's common equivalent.
    @staticmethod
    def toCommonMode(mode):
        if mode == kDaikinCool:
            return stdAc.opmode_t.kCool
        if mode == kDaikinHeat:
            return stdAc.opmode_t.kHeat
        if mode == kDaikinDry:
            return stdAc.opmode_t.kDry
        if mode == kDaikinFan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    # Convert a native fan speed to it's common equivalent.
    @staticmethod
    def toCommonFanSpeed(speed):
        if speed == kDaikinFanMax:
            return stdAc.fanspeed_t.kMax
        if speed == kDaikinFanMax - 1:
            return stdAc.fanspeed_t.kHigh
        if speed in (
            kDaikinFanMed,
            kDaikinFanMin + 1
        ):
            return stdAc.fanspeed_t.kMedium

        if speed == kDaikinFanMin:
            return stdAc.fanspeed_t.kLow
        if speed == kDaikinFanQuiet:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.DAIKIN
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwingVertical() else stdAc.swingv_t.kOff
        result.swingh = stdAc.swingh_t.kAuto if self.getSwingHorizontal() else stdAc.swingh_t.kOff
        result.quiet = self.getQuiet()
        result.turbo = self.getPowerful()
        result.clean = self.getMold()
        result.econo = self.getEcono()
        # Not supported.
        result.filter = False
        result.light = False
        result.beep = False
        result.sleep = -1
        result.clock = -1

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(self.getMode(), kDaikinAuto, kDaikinCool, kDaikinHeat, kDaikinDry, kDaikinFan)
        result += addTempToString(self.getTemp())
        result += addFanToString(self.getFan(), kDaikinFanMax, kDaikinFanMin, kDaikinFanAuto, kDaikinFanQuiet, kDaikinFanMed)
        result += addBoolToString(self.getPowerful(), kPowerfulStr)
        result += addBoolToString(self.getQuiet(), kQuietStr)
        result += addBoolToString(self.getSensor(), kSensorStr)
        result += addBoolToString(self.getMold(), kMouldStr)
        result += addBoolToString(self.getComfort(), kComfortStr)
        result += addBoolToString(self.getSwingHorizontal(), kSwingHStr)
        result += addBoolToString(self.getSwingVertical(), kSwingVStr)
        result += addLabeledString(minsToString(self.getCurrentTime()), kClockStr)
        result += addDayToString(self.getCurrentDay(), -1)
        result += addLabeledString(minsToString(self.getOnTime()) if self.getOnTimerEnabled() else kOffStr, kOnTimerStr)
        result += addLabeledString(minsToString(self.getOffTime()) if self.getOffTimerEnabled() else kOffStr, kOffTimerStr)
        result += addBoolToString(self.getWeeklyTimerEnable(), kWeeklyTimerStr)
        return result


# Class for handling Daikin2 A/C messages.
#
# Code by crankyoldgit, Reverse engineering analysis by sheppy99
#
# Supported Remotes: Daikin ARC477A1 remote
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/582
#   https:#docs.google.com/spreadsheets/d/1f8EGfIbBUo2B-CzUFdrgKQprWakoYNKM80IKZN4KXQE/edit?usp=sharing
#   https:#www.daikin.co.nz/sites/default/files/daikin-split-system-US7-FTXZ25-50NV1B.pdf

class IRDaikin2(ProtocolBase):

    # Send a Daikin2 A/C message.
    #
    # Args:
    #   data: An array of kDaikin2StateLength bytes containing the IR command.
    #
    # Status: BETA/Appears to work.
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/582
    def send_ac(self):
        data = self.getRaw()
        nbytes = kDaikin2StateLength
        repeat = repeat

        if nbytes < kDaikin2Section1Length:
            return  # Not enough bytes to send a partial message.

        for _ in range(repeat + 1):
            # Leader
            self.sendGeneric(
                kDaikin2LeaderMark,
                kDaikin2LeaderSpace,
                0,
                0,
                0,
                0,
                0,
                0,
                0,  # No data payload.
                0,
                kDaikin2Freq,
                False,
                0,
                50
            )
            # Section #1
            self.sendGeneric(
                kDaikin2HdrMark,
                kDaikin2HdrSpace,
                kDaikin2BitMark,
                kDaikin2OneSpace,
                kDaikin2BitMark,
                kDaikin2ZeroSpace,
                kDaikin2BitMark,
                kDaikin2Gap,
                data,
                kDaikin2Section1Length,
                kDaikin2Freq,
                False,
                0,
                50
            )
            # Section #2
            self.sendGeneric(
                kDaikin2HdrMark,
                kDaikin2HdrSpace,
                kDaikin2BitMark,
                kDaikin2OneSpace,
                kDaikin2BitMark,
                kDaikin2ZeroSpace,
                kDaikin2BitMark,
                kDaikin2Gap,
                data[kDaikin2Section1Length:],
                nbytes - kDaikin2Section1Length,
                kDaikin2Freq,
                False,
                0,
                50
            )

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        # Validate the checksum of section #1.
        if (
            length <= kDaikin2Section1Length - 1 or
            state[kDaikin2Section1Length - 1] != sumBytes(state, kDaikin2Section1Length - 1)
        ):
            return False
        # Validate the checksum of section #2 (a.k.a. the rest)
        if (
            length <= kDaikin2Section1Length + 1 or
            state[length - 1] != sumBytes(
                state + kDaikin2Section1Length,
                length - kDaikin2Section1Length - 1
            )
        ):
            return False
        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikin2Section1Length - 1] = sumBytes(
            self.remote_state,
            kDaikin2Section1Length - 1
        )
        self.remote_state[kDaikin2StateLength -1 ] = sumBytes(
            self.remote_state + kDaikin2Section1Length,
            kDaikin2Section2Length - 1
        )

    def stateReset(self):

        self.remote_state = [
            0x11, 0xDA, 0x27, 0x01,  0x0, 0xC0, 0x70, 0x08, 0x0C, 0x80, 0x04, 0xB0, 0x16, 0x24, 0x0, 0x0, 0xBE, 0xD0,
             0x0, 0x11, 0xDA, 0x27,  0x0,  0x0, 0x08,  0x0,  0x0, 0xA0,  0x0,  0x0,  0x0,  0x0, 0x0, 0x0, 0xC1, 0x80,
            0x60
        ]

        # remote_state[38] is a checksum byte, it will be set by checksum().
        self.remote_state += [0x0] * (kDaikin2StateLength - 38)


        self.disableOnTimer()
        self.disableOffTimer()
        self.disableSleepTimer()
        self.checksum()

    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kDaikin2StateLength]

    def on(self):
        self.setPower(True)

    def off(self):
        self.setPower(False)

    def setPower(self, on):
        setBit(self.remote_state[25], kDaikinBitPowerOffset, on)
        setBit(self.remote_state[6], kDaikin2BitPowerOffset, not on)

    def getPower(self):
        return (
            GETBIT8(self.remote_state[25], kDaikinBitPowerOffset) and
            not GETBIT8(self.remote_state[6], kDaikin2BitPowerOffset)
        )

    def getMode(self):
      return GETBITS8(self.remote_state[25], kHighNibble, kModeBitsSize)

    def setMode(self, mode):
        if mode not in (
            kDaikinCool,
            kDaikinHeat,
            kDaikinFan,
            kDaikinDry
        ):
            mode = kDaikinAuto

        setBits(self.remote_state[25], kHighNibble, kModeBitsSize, mode)
        # Redo the temp setting as Cool mode has a different min temp.
        if mode == kDaikinCool:
            self.setTemp(self.getTemp())

    # Set the temp in deg C
    def setTemp(self, desired):
        # The A/C has a different min temp if in cool mode.
        temp = max(kDaikin2MinCoolTemp if self.getMode() == kDaikinCool else kDaikinMinTemp, desired)
        self.remote_state[26] = min(kDaikinMaxTemp, temp) << 1

    def getTemp(self):
        return self.remote_state[26] >> 1

    # Set the speed of the fan, 1-5 or kDaikinFanAuto or kDaikinFanQuiet
    def setFan(self, fan):
        # Set the fan speed bits, leave low 4 bits alone
        if fan in (kDaikinFanQuiet, kDaikinFanAuto):
            fanset = fan
        elif fan < kDaikinFanMin or fan > kDaikinFanMax:
            fanset = kDaikinFanAuto
        else:
            fanset = 2 + fan

        setBits(self.remote_state[kDaikin2FanByte], kHighNibble, kNibbleSize, fanset)

    def getFan(self):
        fan = GETBITS8(self.remote_state[kDaikin2FanByte], kHighNibble, kNibbleSize)

        if fan in (kDaikinFanAuto, kDaikinFanQuiet):
            return fan

        return fan - 2

    def setSwingVertical(self, position):
        if position in (
            kDaikin2SwingVHigh,
            2,
            3,
            4,
            5,
            kDaikin2SwingVLow,
            kDaikin2SwingVSwing,
            kDaikin2SwingVBreeze,
            kDaikin2SwingVCirculate,
            kDaikin2SwingVAuto
        ):
            setBits(self.remote_state[18], kLowNibble, kNibbleSize, position)

    def getSwingVertical(self):
        return GETBITS8(self.remote_state[18], kLowNibble, kNibbleSize)

    # Convert a standard A/C vertical swing into its native version.
    @staticmethod
    def convertSwingV(position):
        if position in (
            stdAc.swingv_t.kHighest,
            stdAc.swingv_t.kHigh,
            stdAc.swingv_t.kMiddle,
            stdAc.swingv_t.kLow,
            stdAc.swingv_t.kLowest
        ):
            return position + kDaikin2SwingVHigh
        if position == stdAc.swingv_t.kAuto:
            return kDaikin2SwingVSwing

        return kDaikin2SwingVAuto

    # Convert a native vertical swing to it's common equivalent.
    @staticmethod
    def toCommonSwingV(setting):
        if setting == kDaikin2SwingVHigh:
            return stdAc.swingv_t.kHighest
        if setting == kDaikin2SwingVHigh + 1:
            return stdAc.swingv_t.kHigh
        if setting in (
            kDaikin2SwingVHigh + 2,
            kDaikin2SwingVHigh + 3
        ):
            return stdAc.swingv_t.kMiddle
        if setting == kDaikin2SwingVLow - 1:
            return stdAc.swingv_t.kLow
        if setting == kDaikin2SwingVLow:
            return stdAc.swingv_t.kLowest
        if setting == kDaikin2SwingVAuto:
            return stdAc.swingv_t.kOff

        return stdAc.swingv_t.kAuto

    def setSwingHorizontal(self, position):
        self.remote_state[17] = position

    def getSwingHorizontal(self):
        return self.remote_state[17]

    def setCurrentTime(self, numMins):
        mins = numMins
        if numMins > 24 * 60:
            mins = 0  # If > 23:59, set to 00:00

        self.remote_state[5] = mins
        setBits(self.remote_state[6], kLowNibble, kNibbleSize, mins >> 8)

    def getCurrentTime(self):
        return (
            GETBITS8(self.remote_state[6], kLowNibble, kNibbleSize) << 8
        ) | self.remote_state[5]

    # starttime: Number of minutes after midnight.
    # Note: Timer location is shared with sleep timer.
    def enableOnTimer(self, starttime):
        self.clearSleepTimerFlag()
        setBit(self.remote_state[25], kDaikinBitOnTimerOffset)  # Set the On Timer flag.
        self.remote_state[30] = starttime
        setBits(self.remote_state[31], kLowNibble, kNibbleSize, starttime >> 8)

    def clearOnTimerFlag(self):
        setBit(self.remote_state[25], kDaikinBitOnTimerOffset, False)

    def disableOnTimer(self):
        self.enableOnTimer(kDaikinUnusedTime)
        self.clearOnTimerFlag()
        self.clearSleepTimerFlag()

    def getOnTime(self):
        return (
            GETBITS8(self.remote_state[31], kLowNibble, kNibbleSize) << 8
        ) + self.remote_state[30]

    def getOnTimerEnabled(self):
        return GETBIT8(self.remote_state[25], kDaikinBitOnTimerOffset)

    # endtime: Number of minutes after midnight.
    def enableOffTimer(self, endtime):
        # Set the Off Timer flag.
        setBit(self.remote_state[25], kDaikinBitOffTimerOffset)
        self.remote_state[32] = endtime >> 4
        setBits(self.remote_state[31], kHighNibble, kNibbleSize, endtime)

    def disableOffTimer(self):
        self.enableOffTimer(kDaikinUnusedTime)
        # Clear the Off Timer flag.
        setBit(self.remote_state[25], kDaikinBitOffTimerOffset, False)

    def getOffTime(self):
        return (self.remote_state[32] << 4) + GETBITS8(self.remote_state[31], kHighNibble, kNibbleSize)

    def getOffTimerEnabled(self):
        return GETBIT8(self.remote_state[25], kDaikinBitOffTimerOffset)

    def getBeep(self):
        return GETBITS8(self.remote_state[7], kDaikin2BeepOffset, kDaikin2BeepSize)

    def setBeep(self, beep):
        setBits(self.remote_state[7], kDaikin2BeepOffset, kDaikin2BeepSize, beep)

    def getLight(self):
        return GETBITS8(self.remote_state[7], kDaikin2LightOffset, kDaikin2LightSize)

    def setLight(self, light):
        setBits(self.remote_state[7], kDaikin2LightOffset, kDaikin2LightSize, light)

    def setMold(self, on):
        setBit(self.remote_state[8], kDaikin2BitMoldOffset, on)

    def getMold(self):
        return GETBIT8(self.remote_state[8], kDaikin2BitMoldOffset)

    # Auto clean setting.
    def setClean(self, on):
        setBit(self.remote_state[8], kDaikin2BitCleanOffset, on)

    def getClean(self):
        return GETBIT8(self.remote_state[8], kDaikin2BitCleanOffset)

    # Fresh Air settings.
    def setFreshAir(self, on):
        setBit(self.remote_state[8], kDaikin2BitFreshAirOffset, on)

    def getFreshAir(self):
        return GETBIT8(self.remote_state[8], kDaikin2BitFreshAirOffset)

    def setFreshAirHigh(self, on):
        setBit(self.remote_state[8], kDaikin2BitFreshAirHighOffset, on)

    def getFreshAirHigh(self):
        return GETBIT8(self.remote_state[8], kDaikin2BitFreshAirHighOffset)

    def setEyeAuto(self, on):
        setBit(self.remote_state[13], kDaikin2BitEyeAutoOffset, on)

    def getEyeAuto(self):
        return GETBIT8(self.remote_state[13], kDaikin2BitEyeAutoOffset)

    def setEye(self, on):
        setBit(self.remote_state[36], kDaikin2BitEyeOffset, on)

    def getEye(self):
        return GETBIT8(self.remote_state[36], kDaikin2BitEyeOffset)

    def setEcono(self, on):
        setBit(self.remote_state[36], kDaikinBitEconoOffset, on)

    def getEcono(self):
        return GETBIT8(self.remote_state[36], kDaikinBitEconoOffset)

    # sleeptime: Number of minutes.
    # Note: Timer location is shared with On Timer.
    def enableSleepTimer(self, sleeptime):
        self.enableOnTimer(sleeptime)
        self.clearOnTimerFlag()
        # Set the Sleep Timer flag.
        setBit(self.remote_state[36], kDaikin2BitSleepTimerOffset)

    def clearSleepTimerFlag(self):
        setBit(self.remote_state[36], kDaikin2BitSleepTimerOffset, False)

    def disableSleepTimer(self):
        self.disableOnTimer()

    def getSleepTime(self):
        return self.getOnTime()

    def getSleepTimerEnabled(self):
        return GETBIT8(self.remote_state[36],  kDaikin2BitSleepTimerOffset)

    def setQuiet(self, on):
        setBit(self.remote_state[33], kDaikinBitSilentOffset, on)
        # Powerful & Quiet mode being on are mutually exclusive.
        if on:
            self.setPowerful(False)

    def getQuiet(self):
        return GETBIT8(self.remote_state[33], kDaikinBitSilentOffset)

    def setPowerful(self, on):
        setBit(self.remote_state[33], kDaikinBitPowerfulOffset, on)
        # Powerful & Quiet mode being on are mutually exclusive.
        if on:
            self.setQuiet(False)

    def getPowerful(self):
        return GETBIT8(self.remote_state[33], kDaikinBitPowerfulOffset)

    def setPurify(self, on):
        setBit(self.remote_state[36], kDaikin2BitPurifyOffset, on)

    def getPurify(self):
        return GETBIT8(self.remote_state[36],  kDaikin2BitPurifyOffset)

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        return IRDaikinESP.convertMode(mode)

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        return IRDaikinESP.convertFan(speed)

    # Convert a standard A/C horizontal swing into its native version.
    @staticmethod
    def convertSwingH(position):
        if position == stdAc.swingh_t.kAuto:
            return kDaikin2SwingHSwing
        if position == stdAc.swingh_t.kLeftMax:
            return kDaikin2SwingHLeftMax
        if position == stdAc.swingh_t.kLeft:
            return kDaikin2SwingHLeft
        if position == stdAc.swingh_t.kMiddle:
            return kDaikin2SwingHMiddle
        if position == stdAc.swingh_t.kRight:
            return kDaikin2SwingHRight
        if position == stdAc.swingh_t.kRightMax:
            return kDaikin2SwingHRightMax
        if position == stdAc.swingh_t.kWide:
            return kDaikin2SwingHWide

        return kDaikin2SwingHAuto

    # Convert a native horizontal swing to it's common equivalent.
    @staticmethod
    def toCommonSwingH(setting):

        if setting == kDaikin2SwingHSwing:
            return stdAc.swingh_t.kAuto
        if setting == kDaikin2SwingHLeftMax:
            return stdAc.swingh_t.kLeftMax
        if setting == kDaikin2SwingHLeft:
            return stdAc.swingh_t.kLeft
        if setting == kDaikin2SwingHMiddle:
            return stdAc.swingh_t.kMiddle
        if setting == kDaikin2SwingHRight:
            return stdAc.swingh_t.kRight
        if setting == kDaikin2SwingHRightMax:
            return stdAc.swingh_t.kRightMax
        if setting == kDaikin2SwingHWide:
            return stdAc.swingh_t.kWide

        return stdAc.swingh_t.kOff

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.DAIKIN2
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = IRDaikinESP.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = IRDaikinESP.toCommonFanSpeed(self.getFan())
        result.swingv = self.toCommonSwingV(self.getSwingVertical())
        result.swingh = self.toCommonSwingH(self.getSwingHorizontal())
        result.quiet = self.getQuiet()
        result.light = self.getLight() != 3  # 3 is Off, everything else is On.
        result.turbo = self.getPowerful()
        result.clean = self.getMold()
        result.econo = self.getEcono()
        result.filter = self.getPurify()
        result.beep = self.getBeep() != 3  # 3 is Off, everything else is On.
        result.sleep = self.getSleepTime() if self.getSleepTimerEnabled() else -1
        # Not supported.
        result.clock = -1
        return result

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinDry,
            kDaikinFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kDaikinFanMax,
            kDaikinFanMin,
            kDaikinFanAuto,
            kDaikinFanQuiet,
            kDaikinFanMed
        )
        result += addIntToString(self.getSwingVertical(), kSwingVStr)
        result += kSpaceLBraceStr
        swing = self.getSwingVertical()

        if swing == kDaikin2SwingVHigh:
            result += kHighestStr

        elif swing == 2:
            result += kHighStr

        elif swing == 3:
            result += kUpperStr
            result += kMiddleStr

        elif swing == 4:
            result += kLowerStr
            result += kMiddleStr
        elif swing == 5:
            result += kLowStr
        elif swing == kDaikin2SwingVLow:
            result += kLowestStr
        elif swing == kDaikin2SwingVBreeze:
            result += kBreezeStr
        elif swing == kDaikin2SwingVCirculate:
            result += kCirculateStr
        elif swing == kDaikin2SwingVAuto:
            result += kAutoStr
        elif swing == kDaikin2SwingVSwing:
            result += kSwingStr
        else:
            result += kUnknownStr

        result += ')'
        result += addIntToString(self.getSwingHorizontal(), kSwingHStr)
        result += kSpaceLBraceStr

        swing = self.getSwingHorizontal()
        if swing == kDaikin2SwingHAuto:
            result += kAutoStr
        elif swing == kDaikin2SwingHSwing:
            result += kSwingStr
        else:
            result += kUnknownStr

        result += ')'
        result += addLabeledString(minsToString(self.getCurrentTime()), kClockStr)
        result += addLabeledString(
            minsToString(self.getOnTime()) if self.getOnTimerEnabled() else kOffStr,
            kOnTimerStr
        )
        result += addLabeledString(
            minsToString(self.getOffTime()) if self.getOffTimerEnabled() else kOffStr,
            kOffTimerStr
        )
        result += addLabeledString(
            minsToString(self.getSleepTime()) if self.getSleepTimerEnabled() else kOffStr,
            kSleepTimerStr
        )
        result += addIntToString(self.getBeep(), kBeepStr)
        result += kSpaceLBraceStr

        beep = self.getBeep()
        if beep == kDaikinBeepLoud:
            result += kLoudStr

        elif beet == kDaikinBeepQuiet:
            result += kQuietStr

        elif beep == kDaikinBeepOff:
            result += kOffStr
        else:
            result += kUnknownStr

        result += ')'
        result += addIntToString(self.getLight(), kLightStr)
        result += kSpaceLBraceStr
        light = self.getLight()
        if light == kDaikinLightBright:
            result += kHighStr
        elif light == kDaikinLightDim:
            result += kLowStr

        elif light == kDaikinLightOff:
            result += kOffStr
        else:
            result += kUnknownStr

        result += ')'
        result += addBoolToString(self.getMold(), kMouldStr)
        result += addBoolToString(self.getClean(), kCleanStr)
        result += addLabeledString(
            kHighStr if self.getFreshAirHigh() else kOnStr if self.getFreshAir() else kOffStr,
            kFreshStr
        )
        result += addBoolToString(self.getEye(), kEyeStr)
        result += addBoolToString(self.getEyeAuto(), kEyeAutoStr)
        result += addBoolToString(self.getQuiet(), kQuietStr)
        result += addBoolToString(self.getPowerful(), kPowerfulStr)
        result += addBoolToString(self.getPurify(), kPurifyStr)
        result += addBoolToString(self.getEcono(), kEconoStr)
        return result

    #if DECODE_DAIKIN2
    # Decode the supplied Daikin2 A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin2Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin FTXZ25NV1B, FTXZ35NV1B, FTXZ50NV1B Aircon
    # - Daikin ARC477A1 remote
    #
    # Status: BETA / Work as expected.
    #
    # Ref:
    #   https:#github.com/mharizanov/Daikin-AC-remote-control-over-the-Internet/tree/master/IRremote
    def decode_ac(self, results, nbits, strict):
        if results.rawlen < 2 * (nbits + kHeader + kFooter) + kHeader - 1:
            return False

        # Compliance
        if strict and nbits != kDaikin2Bits:
            return False

        offset = kStartOffset
        ksectionSize = [kDaikin2Section1Length, kDaikin2Section2Length]

        # Leader
        offset += 1
        if not self.matchMark(results.rawbuf[offset], kDaikin2LeaderMark, _tolerance + kDaikin2Tolerance):
            return False

        offset += 1
        if not self.matchSpace(results.rawbuf[offset], kDaikin2LeaderSpace, _tolerance + kDaikin2Tolerance):
            return False

        # Sections
        pos = 0
        for section in range(kDaikin2Sections):

            # Section Header + Section Data + Section Footer
            used = self.matchGeneric(
                results.rawbuf[:offset],
                results.state + pos,
                results.rawlen - offset,
                ksectionSize[section] * 8,
                kDaikin2HdrMark,
                kDaikin2HdrSpace,
                kDaikin2BitMark,
                kDaikin2OneSpace,
                kDaikin2BitMark,
                kDaikin2ZeroSpace,
                kDaikin2BitMark,
                kDaikin2Gap,
                section >= kDaikin2Sections - 1,
                _tolerance + kDaikin2Tolerance,
                kDaikinMarkExcess,
                False
            )
            if used == 0:
                return False

            offset += used
            pos += ksectionSize[section]

        # Compliance
        if (
            strict and (
                pos * 8 != kDaikin2Bits or
                not self.validChecksum(results.state)
            )
        ):
            return False

        # Success
        results.decode_type = DAIKIN2
        results.bits = nbits
        # No need to record the state as we stored it as we decoded it.
        # As we use result.state, we don't record value, address, or command as it
        # is a union data type.
        return True


class IRDaikin216(ProtocolBase):

    # Class for handling Daikin 216 bit / 27 byte A/C messages.
    #
    # Code by crankyoldgit.
    #
    # Supported Remotes: Daikin ARC433B69 remote
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/689
    #   https:#github.com/danny-source/Arduino_DY_IRDaikin



    # Send a Daikin 216 bit A/C message.
    #
    # Args:
    #   data: An array of kDaikin216StateLength bytes containing the IR command.
    #
    # Status: Alpha/Untested on a real device.
    #
    # Supported devices:
    # - Daikin ARC433B69 remote.
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/689
    #   https:#github.com/danny-source/Arduino_DY_IRDaikin
    def send_ac(self):
        data = self.getRaw()
        nbytes = kDaikin216StateLength
        repeat = repeat

        if nbytes < kDaikin216Section1Length:
            return  # Not enough bytes to send a partial message.

        for _ in range(repeat + 1):
            # Section #1
            self.sendGeneric(
                kDaikin216HdrMark,
                kDaikin216HdrSpace,
                kDaikin216BitMark,
                kDaikin216OneSpace,
                kDaikin216BitMark,
                kDaikin216ZeroSpace,
                kDaikin216BitMark,
                kDaikin216Gap,
                data,
                kDaikin216Section1Length,
                kDaikin216Freq,
                False,
                0,
                kDutyDefault
            )

            # Section #2
            self.sendGeneric(
                kDaikin216HdrMark,
                kDaikin216HdrSpace,
                kDaikin216BitMark,
                kDaikin216OneSpace,
                kDaikin216BitMark,
                kDaikin216ZeroSpace,
                kDaikin216BitMark,
                kDaikin216Gap,
                data[:kDaikin216Section1Length],
                nbytes - kDaikin216Section1Length,
                kDaikin216Freq,
                False,
                0,
                kDutyDefault
            )


    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        # Validate the checksum of section #1.
        if (
            length <= kDaikin216Section1Length - 1 or
            state[kDaikin216Section1Length - 1] != sumBytes(
                state,
                kDaikin216Section1Length - 1
            )
        ):
            return False
        # Validate the checksum of section #2 (a.k.a. the rest)
        if (
            length <= kDaikin216Section1Length + 1 or
            state[length - 1] != sumBytes(
                state + kDaikin216Section1Length,
                length - kDaikin216Section1Length - 1
            )
        ):
            return False

        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikin216Section1Length - 1] = sumBytes(
            self.remote_state,
            kDaikin216Section1Length - 1
        )

        self.remote_state[kDaikin216StateLength - 1] = sumBytes(
            self.remote_state + kDaikin216Section1Length,
            kDaikin216Section2Length - 1
        )

    def stateReset(self):
        self.remote_state = [0x11, 0xDA, 0x27, 0xF0, 0x0, 0x0, 0x0, 0x0, 0x11, 0xDA, 0x27]
        self.remote_state += [0x0] * (kDaikin216StateLength - 11)
        self.remote_state[23] = 0xC0
        # remote_state[26] is a checksum byte, it will be set by checksum().


    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kDaikin216StateLength]

    def setPower(self, on):
        setBit(self.remote_state[kDaikin216BytePower], kDaikinBitPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote_state[kDaikin216BytePower], kDaikinBitPowerOffset)

    def getMode(self):
        return GETBITS8(self.remote_state[kDaikin216ByteMode], kHighNibble, kModeBitsSize)

    def setMode(self, mode):
        if mode in (
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinFan,
            kDaikinDry
        ):
            setBits(self.remote_state[kDaikin216ByteMode], kHighNibble, kModeBitsSize, mode)
        else:
            self.setMode(kDaikinAuto)

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
      return IRDaikinESP.convertMode(mode)

    # Set the temp in deg C
    def setTemp(self, temp):
        degrees = max(temp, kDaikinMinTemp)
        degrees = min(degrees, kDaikinMaxTemp)
        setBits(self.remote_state[kDaikin216ByteTemp], kDaikin216TempOffset, kDaikin216TempSize, degrees)

    def getTemp(self):
        return GETBITS8(self.remote_state[kDaikin216ByteTemp], kDaikin216TempOffset, kDaikin216TempSize)

    # Set the speed of the fan, 1-5 or kDaikinFanAuto or kDaikinFanQuiet
    def setFan(self, fan):
        # Set the fan speed bits, leave low 4 bits alone
        if fan in (kDaikinFanQuiet, kDaikinFanAuto):
            fanset = fan
        elif fan < kDaikinFanMin or fan > kDaikinFanMax:
            fanset = kDaikinFanAuto
        else:
            fanset = 2 + fan

        setBits(self.remote_state[kDaikin216ByteFan], kHighNibble, kDaikinFanSize, fanset)

    def getFan(self):
        fan = GETBITS8(self.remote_state[kDaikin216ByteFan], kHighNibble, kDaikinFanSize)

        if fan != kDaikinFanQuiet and fan != kDaikinFanAuto:
            fan -= 2

        return fan

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        return IRDaikinESP.convertFan(speed)

    def setSwingVertical(self, on):
        setBits(
            self.remote_state[kDaikin216ByteSwingV],
            kLowNibble,
            kDaikin216SwingSize,
            kDaikin216SwingOn if on else kDaikin216SwingOff
        )

    def getSwingVertical(self):
        return GETBITS8(self.remote_state[kDaikin216ByteSwingV], kLowNibble, kDaikin216SwingSize)

    def setSwingHorizontal(self, on):
        setBits(
            self.remote_state[kDaikin216ByteSwingH],
            kLowNibble,
            kDaikin216SwingSize,
            kDaikin216SwingOn if on else kDaikin216SwingOff
        )

    def getSwingHorizontal(self):
        return GETBITS8(self.remote_state[kDaikin216ByteSwingH], kLowNibble, kDaikin216SwingSize)

    # This is a horrible hack till someone works out the quiet mode bit.
    def setQuiet(self, on):
        if on:
            self.setFan(kDaikinFanQuiet)
            # Powerful & Quiet mode being on are mutually exclusive.
            self.setPowerful(False)
        elif self.getFan() == kDaikinFanQuiet:
            self.setFan(kDaikinFanAuto)

    # This is a horrible hack till someone works out the quiet mode bit.
    def getQuiet(self):
        return self.getFan() == kDaikinFanQuiet

    def setPowerful(self, on):
        setBit(self.remote_state[kDaikin216BytePowerful], kDaikinBitPowerfulOffset, on)
        # Powerful & Quiet mode being on are mutually exclusive.
        if on:
            self.setQuiet(False)

    def getPowerful(self):
        return GETBIT8(self.remote_state[kDaikin216BytePowerful], kDaikinBitPowerfulOffset)

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.DAIKIN216
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = IRDaikinESP.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = IRDaikinESP.toCommonFanSpeed(self.getFan())
        result.swingv = stdAc.swingv_t.kAuto if self.getSwingVertical() else stdAc.swingv_t.kOff
        result.swingh = stdAc.swingh_t.kAuto if self.getSwingHorizontal() else stdAc.swingh_t.kOff
        result.quiet = self.getQuiet()
        result.turbo = self.getPowerful()
        # Not supported.
        result.light = False
        result.clean = False
        result.econo = False
        result.filter = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinDry,
            kDaikinFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kDaikinFanMax,
            kDaikinFanMin,
            kDaikinFanAuto,
            kDaikinFanQuiet,
            kDaikinFanMed
        )
        result += addBoolToString(self.getSwingHorizontal(), kSwingHStr)
        result += addBoolToString(self.getSwingVertical(), kSwingVStr)
        result += addBoolToString(self.getQuiet(), kQuietStr)
        result += addBoolToString(self.getPowerful(), kPowerfulStr)
        return result

    #if DECODE_DAIKIN216
    # Decode the supplied Daikin 216 bit A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin216Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin ARC433B69 remote.
    #
    # Status: BETA / Should be working.
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/689
    #   https:#github.com/danny-source/Arduino_DY_IRDaikin
    def decode_ac(self, results, nbits, strict):
        if results.rawlen < 2 * (nbits + kHeader + kFooter) - 1:
            return False

        # Compliance
        if strict and nbits != kDaikin216Bits:
            return False

        offset = kStartOffset
        ksectionSize = [kDaikin216Section1Length, kDaikin216Section2Length]
        # Sections
        pos = 0
        for section in range(kDaikin216Sections):
            # Section Header + Section Data + Section Footer
            used = self.matchGeneric(
                results.rawbuf[:offset],
                results.state + pos,
                results.rawlen - offset,
                ksectionSize[section] * 8,
                kDaikin216HdrMark,
                kDaikin216HdrSpace,
                kDaikin216BitMark,
                kDaikin216OneSpace,
                kDaikin216BitMark,
                kDaikin216ZeroSpace,
                kDaikin216BitMark,
                kDaikin216Gap,
                section >= kDaikin216Sections - 1,
                kDaikinTolerance,
                kDaikinMarkExcess,
                False
            )
            if used == 0:
                return False

            offset += used
            pos += ksectionSize[section]

        # Compliance
        if strict:
            if pos * 8 != kDaikin216Bits:
                return False
            # Validate the checksum.
            if not self.validChecksum(results.state):
                return False

        # Success
        results.decode_type = decode_type_t.DAIKIN216
        results.bits = nbits
        # No need to record the state as we stored it as we decoded it.
        # As we use result.state, we don't record value, address, or command as it
        # is a union data type.
        return True


class IRDaikin160(ProtocolBase):
    # Class for handling Daikin 160 bit / 20 byte A/C messages.
    #
    # Code by crankyoldgit.
    #
    # Supported Remotes: Daikin ARC423A5 remote
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/731


    # Send a Daikin 160 bit A/C message.
    #
    # Args:
    #   data: An array of kDaikin160StateLength bytes containing the IR command.
    #
    # Status: STABLE / Confirmed working.
    #
    # Supported devices:
    # - Daikin ARC423A5 remote.
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/731
    def send_ac(self):
        data = self.getRaw()
        nbytes = kDaikin160StateLength
        repeat = repeat
        if nbytes < kDaikin160Section1Length:
            return  # Not enough bytes to send a partial message.

        for _ in range(repeat + 1):
            # Section #1
            self.sendGeneric(
                kDaikin160HdrMark,
                kDaikin160HdrSpace,
                kDaikin160BitMark,
                kDaikin160OneSpace,
                kDaikin160BitMark,
                kDaikin160ZeroSpace,
                kDaikin160BitMark,
                kDaikin160Gap,
                data,
                kDaikin160Section1Length,
                kDaikin160Freq,
                False,
                0,
                kDutyDefault
            )

            # Section #2
            self.sendGeneric(
                kDaikin160HdrMark,
                kDaikin160HdrSpace,
                kDaikin160BitMark,
                kDaikin160OneSpace,
                kDaikin160BitMark,
                kDaikin160ZeroSpace,
                kDaikin160BitMark,
                kDaikin160Gap,
                data[:kDaikin160Section1Length],
                nbytes - kDaikin160Section1Length,
                kDaikin160Freq,
                False,
                0,
                kDutyDefault
            )


    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        # Validate the checksum of section #1.
        if (
            length <= kDaikin160Section1Length - 1 or
            state[kDaikin160Section1Length - 1] != sumBytes(state, kDaikin160Section1Length - 1)
        ):
            return False
        # Validate the checksum of section #2 (a.k.a. the rest)
        if (
            length <= kDaikin160Section1Length + 1 or
            state[length - 1] != sumBytes(state + kDaikin160Section1Length, length - kDaikin160Section1Length - 1)
        ):
            return False
        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikin160Section1Length - 1] = sumBytes(
            self.remote_state,
            kDaikin160Section1Length - 1
        )

        self.remote_state[kDaikin160StateLength - 1] = sumBytes(
            self.remote_state + kDaikin160Section1Length,
            kDaikin160Section2Length - 1
        )

    def stateReset(self):
        self.remote_state = [
            0x11, 0xDA, 0x27, 0xF0, 0x0D, 0x0, 0x0, 0x11, 0xDA,
            0x27,  0x0, 0xD3, 0x30, 0x11, 0x0, 0x0, 0x1E, 0x0A, 0x08
        ]
        # remote_state[19] is a checksum byte, it will be set by checksum().
        self.remote_state += [0x0] * (kDaikin160StateLength - 19)


    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kDaikin160StateLength]

    def setPower(self, on):
        setBit(self.remote_state[kDaikin160BytePower], kDaikinBitPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote_state[kDaikin160BytePower], kDaikinBitPowerOffset)

    def getMode(self):
        return GETBITS8(self.remote_state[kDaikin160ByteMode], kHighNibble, kModeBitsSize)

    def setMode(self, mode):
        if mode in (
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinFan,
            kDaikinDry
        ):
          setBits(self.remote_state[kDaikin160ByteMode], kHighNibble, kModeBitsSize, mode)
        else:
            self.setMode(kDaikinAuto)

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        return IRDaikinESP.convertMode(mode)

    # Set the temp in deg C
    def setTemp(self, temp):
        degrees = max(temp, kDaikinMinTemp)
        degrees = min(degrees, kDaikinMaxTemp) - 10
        setBits(self.remote_state[kDaikin160ByteTemp], kDaikin160TempOffset, kDaikin160TempSize, degrees)

    def getTemp(self):
        return GETBITS8(self.remote_state[kDaikin160ByteTemp], kDaikin160TempOffset, kDaikin160TempSize) + 10

    # Set the speed of the fan, 1-5 or kDaikinFanAuto or kDaikinFanQuiet
    def setFan(self, fan):
        if fan in (kDaikinFanQuiet, kDaikinFanAuto):
            fanset = fan
        elif fan < kDaikinFanMin or fan > kDaikinFanMax:
            fanset = kDaikinFanAuto
        else:
            fanset = 2 + fan

        # Set the fan speed bits, leave *upper* 4 bits alone
        setBits(self.remote_state[kDaikin160ByteFan], kLowNibble, kDaikinFanSize, fanset)

    def getFan(self):
        fan = GETBITS8(self.remote_state[kDaikin160ByteFan], kLowNibble, kDaikinFanSize)
        if fan not in (kDaikinFanQuiet, kDaikinFanAuto):
            fan -= 2

        return fan

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        if speed == stdAc.fanspeed_t.kMin:
            return kDaikinFanMin
        if speed == stdAc.fanspeed_t.kLow:
            return kDaikinFanMin + 1
        if speed == stdAc.fanspeed_t.kMedium:
            return kDaikinFanMin + 2
        if speed == stdAc.fanspeed_t.kHigh:
            return kDaikinFanMax - 1
        if speed == stdAc.fanspeed_t.kMax:
            return kDaikinFanMax

        return kDaikinFanAuto

    def setSwingVertical(self, position):
        if position in (
            kDaikin160SwingVLowest,
            kDaikin160SwingVLow,
            kDaikin160SwingVMiddle,
            kDaikin160SwingVHigh,
            kDaikin160SwingVHighest,
            kDaikin160SwingVAuto
        ):
            setBits(self.remote_state[kDaikin160ByteSwingV], kHighNibble, kDaikinSwingSize, position)
        else:
            self.setSwingVertical(kDaikin160SwingVAuto)

    def getSwingVertical(self):
        return GETBITS8(self.remote_state[kDaikin160ByteSwingV], kHighNibble, kDaikinSwingSize)

    # Convert a standard A/C vertical swing into its native version.
    @staticmethod
    def convertSwingV(position):
        if position in (
            stdAc.swingv_t.kHighest,
            stdAc.swingv_t.kHigh,
            stdAc.swingv_t.kMiddle,
            stdAc.swingv_t.kLow,
            stdAc.swingv_t.kLowest
        ):
              return kDaikin160SwingVHighest + 1 - position

        return kDaikin160SwingVAuto

    # Convert a native vertical swing to it's common equivalent.
    @staticmethod
    def toCommonSwingV(setting):
        if setting == kDaikin160SwingVHighest:
            return stdAc.swingv_t.kHighest
        if setting == kDaikin160SwingVHigh:
            return stdAc.swingv_t.kHigh
        if setting == kDaikin160SwingVMiddle:
            return stdAc.swingv_t.kMiddle
        if setting == kDaikin160SwingVLow:
            return stdAc.swingv_t.kLow
        if setting == kDaikin160SwingVLowest:
            return stdAc.swingv_t.kLowest

        return stdAc.swingv_t.kAuto

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.DAIKIN160
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = IRDaikinESP.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = IRDaikinESP.toCommonFanSpeed(self.getFan())
        result.swingv = self.toCommonSwingV(self.getSwingVertical())
        # Not supported.
        result.swingh = stdAc.swingh_t.kOff
        result.quiet = False
        result.turbo = False
        result.light = False
        result.clean = False
        result.econo = False
        result.filter = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kDaikinAuto,
            kDaikinCool,
            kDaikinHeat,
            kDaikinDry,
            kDaikinFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kDaikinFanMax,
            kDaikinFanMin,
            kDaikinFanAuto,
            kDaikinFanQuiet,
            kDaikinFanMed
        )
        result += addIntToString(self.getSwingVertical(), kSwingVStr)
        result += kSpaceLBraceStr

        swing = self.getSwingVertical()
        if swing == kDaikin160SwingVHighest:
            result += kHighestStr
        elif swing == kDaikin160SwingVHigh:
            result += kHighStr
        elif swing == kDaikin160SwingVMiddle:
            result += kMiddleStr
        elif swing == kDaikin160SwingVLow:
            result += kLowStr
        elif swing == kDaikin160SwingVLowest:
            result += kLowestStr
        elif swing == kDaikin160SwingVAuto:
            result += kAutoStr
        else:
            result += kUnknownStr

        result += ')'
        return result

    # Decode the supplied Daikin 160 bit A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin160Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin ARC423A5 remote.
    #
    # Status: STABLE / Confirmed working.
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/731
    def decode_ac(self, results, nbits, strict):
        if results.rawlen < 2 * (nbits + kHeader + kFooter) - 1:
            return False

        # Compliance
        if strict and nbits != kDaikin160Bits:
            return False

        offset = kStartOffset
        ksectionSize = [kDaikin160Section1Length, kDaikin160Section2Length]

        # Sections
        pos = 0
        for section in range(kDaikin160Sections):

            # Section Header + Section Data (7 bytes) + Section Footer
            used = self.matchGeneric(
                results.rawbuf[:offset],
                results.state + pos,
                results.rawlen - offset,
                ksectionSize[section] * 8,
                kDaikin160HdrMark,
                kDaikin160HdrSpace,
                kDaikin160BitMark,
                kDaikin160OneSpace,
                kDaikin160BitMark,
                kDaikin160ZeroSpace,
                kDaikin160BitMark,
                kDaikin160Gap,
                section >= kDaikin160Sections - 1,
                kDaikinTolerance,
                kDaikinMarkExcess,
                False
            )
            if used == 0:
                return False

            offset += used

            pos += ksectionSize[section]

        # Compliance
        if strict and not self.validChecksum(results.state):
            return False

        # Success
        results.decode_type = decode_type_t.DAIKIN160
        results.bits = nbits
        # No need to record the state as we stored it as we decoded it.
        # As we use result.state, we don't record value, address, or command as it
        # is a union data type.
        return True


class Daikin176(ProtocolBase):
    # Class for handling Daikin 176 bit / 22 byte A/C messages.
    #
    # Code by crankyoldgit.
    #
    # Supported Remotes: Daikin BRC4C153 remote
    #

    #if SEND_DAIKIN176
    # Send a Daikin 176 bit A/C message.
    #
    # Args:
    #   data: An array of kDaikin176StateLength bytes containing the IR command.
    #
    # Status: Alpha/Untested on a real device.
    #
    # Supported devices:
    # - Daikin BRC4C153 remote.
    #
    def send_ac(self, data, nbytes, repeat):
        data = self.getRaw()
        nbytes = kDaikin176StateLength
        repeat = repeat

        if nbytes < kDaikin176Section1Length:
            return  # Not enough bytes to send a partial message.

        for _ in range(repeat + 1):
            # Section #1
            self.sendGeneric(
                kDaikin176HdrMark,
                kDaikin176HdrSpace,
                kDaikin176BitMark,
                kDaikin176OneSpace,
                kDaikin176BitMark,
                kDaikin176ZeroSpace,
                kDaikin176BitMark,
                kDaikin176Gap,
                data,
                kDaikin176Section1Length,
                kDaikin176Freq,
                False,
                0,
                kDutyDefault
            )
            # Section #2
            self.sendGeneric(
                kDaikin176HdrMark,
                kDaikin176HdrSpace,
                kDaikin176BitMark,
                kDaikin176OneSpace,
                kDaikin176BitMark,
                kDaikin176ZeroSpace,
                kDaikin176BitMark,
                kDaikin176Gap,
                data + kDaikin176Section1Length,
                nbytes - kDaikin176Section1Length,
                kDaikin176Freq,
                False,
                0,
                kDutyDefault
            )

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    @staticmethod
    def validChecksum(state, length):
        # Validate the checksum of section #1.
        if (
            length <= kDaikin176Section1Length - 1 or
            state[kDaikin176Section1Length - 1] != sumBytes(state, kDaikin176Section1Length - 1)
        ):
            return False
        # Validate the checksum of section #2 (a.k.a. the rest)
        if (
            length <= kDaikin176Section1Length + 1 or
            state[length - 1] != sumBytes(state + kDaikin176Section1Length, length - kDaikin176Section1Length - 1)
        ):
            return False

        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikin176Section1Length - 1] = sumBytes(self.remote_state, kDaikin176Section1Length - 1)
        self.remote_state[kDaikin176StateLength - 1] = sumBytes(self.remote_state + kDaikin176Section1Length, kDaikin176Section2Length - 1)

    def stateReset(self):


        self.remote_state[0] =  [
            0x11, 0xDA, 0x17, 0x18, 0x04, 0x0, 0x0, 0x11, 0xDA, 0x17,
            0x18,  0x0, 0x73,  0x0, 0x20, 0x0, 0x0,  0x0, 0x16,  0x0, 0x20
        ]

        # remote_state[21] is a checksum byte, it will be set by checksum().
        self.remote_state += [0x0] * (kDaikin176StateLength - 21)
        self._saved_temp = self.getTemp()

    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kDaikin176StateLength]
        self._saved_temp = self.getTemp()

    def setPower(self, on):
        self.remote_state[kDaikin176ByteModeButton] = 0
        setBit(self.remote_state[kDaikin176BytePower], kDaikinBitPowerOffset, on)

    def getPower(self):
        return GETBIT8(self.remote_state[kDaikin176BytePower], kDaikinBitPowerOffset)

    def getMode(self):
        return GETBITS8(self.remote_state[kDaikin176ByteMode], kHighNibble, kModeBitsSize)

    def setMode(self, mode):
        if mode == kDaikinFan:
            altmode = 0
        elif mode == kDaikinDry:
            altmode = 7
        elif mode == kDaikin176Cool:
            altmode = 2
        else:
            self.setMode(kDaikin176Cool)
            return

        # Set the mode.
        setBits(self.remote_state[kDaikin176ByteMode], kHighNibble, kModeBitsSize, mode)
        setBits(self.remote_state[kDaikin176BytePower], kHighNibble, kModeBitsSize, altmode)
        self.setTemp(self._saved_temp)
        # Needs to happen after setTemp() as it will clear it.
        self.remote_state[kDaikin176ByteModeButton] = kDaikin176ModeButton

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        if mode == stdAc.opmode_t.kDry:
            return kDaikinDry
        if mode in (stdAc.opmode_t.kHeat, stdAc.opmode_t.kFan):
            return kDaikinFan

        return kDaikin176Cool

    # Convert a native mode to it's common equivalent.
    @staticmethod
    def toCommonMode(mode):
        if mode == kDaikinDry:
            return stdAc.opmode_t.kDry
        if mode in (kDaikinHeat, kDaikinFan):
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kCool

    # Set the temp in deg C
    def setTemp(self, temp):
        degrees = min(kDaikinMaxTemp, max(temp, kDaikinMinTemp))
        self._saved_temp = degrees

        mode = self.getMode()

        if mode in (kDaikinDry, kDaikinFan):
            degrees = kDaikin176DryFanTemp

        setBits(self.remote_state[kDaikin176ByteTemp], kDaikin176TempOffset, kDaikin176TempSize, degrees - 9)
        self.remote_state[kDaikin176ByteModeButton] = 0

    def getTemp(self):
        return GETBITS8(self.remote_state[kDaikin176ByteTemp], kDaikin176TempOffset, kDaikin176TempSize) + 9

    # Set the speed of the fan, 1 for Min or 3 for Max
    def setFan(self, fan):
        if fan in (kDaikinFanMin, kDaikin176FanMax):
            setBits(self.remote_state[kDaikin176ByteFan], kHighNibble, kDaikinFanSize, fan)
            self.remote_state[kDaikin176ByteModeButton] = 0
        else:
            self.setFan(kDaikin176FanMax)

    def getFan(self):
        return GETBITS8(self.remote_state[kDaikin176ByteFan], kHighNibble, kDaikinFanSize)

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        if speed in (stdAc.fanspeed_t.kMin, stdAc.fanspeed_t.kLow):
            return kDaikinFanMin
        else:
            return kDaikin176FanMax

    def setSwingHorizontal(self, position):
        if position in (kDaikin176SwingHOff, kDaikin176SwingHAuto):
            setBits(self.remote_state[kDaikin176ByteSwingH], kLowNibble, kDaikinSwingSize, position)
        else:
            self.setSwingHorizontal(kDaikin176SwingHAuto)

    def getSwingHorizontal(self):
        return GETBITS8(self.remote_state[kDaikin176ByteSwingH], kLowNibble, kDaikinSwingSize)

    # Convert a standard A/C horizontal swing into its native version.
    @staticmethod
    def convertSwingH(position):
        if position == stdAc.swingh_t.kOff:
            return kDaikin176SwingHOff
        if position == stdAc.swingh_t.kAuto:
            return kDaikin176SwingHAuto

        return kDaikin176SwingHAuto

    # Convert a native horizontal swing to it's common equivalent.
    @staticmethod
    def toCommonSwingH(setting):
        if setting == kDaikin176SwingHOff:
            return stdAc.swingh_t.kOff
        if setting == kDaikin176SwingHAuto:
            return stdAc.swingh_t.kAuto

        return stdAc.swingh_t.kAuto

    # Convert a native fan speed to it's common equivalent.
    @staticmethod
    def toCommonFanSpeed(speed):
      return stdAc.fanspeed_t.kMin if speed == kDaikinFanMin else stdAc.fanspeed_t.kMax

    # Convert the A/C state to it's common equivalent.
    def toCommon(self):
        result = stdAc.state_t()
        result.protocol = decode_type_t.DAIKIN176
        result.model = -1  # No models used.
        result.power = self.getPower()
        result.mode = self.toCommonMode(self.getMode())
        result.celsius = True
        result.degrees = self.getTemp()
        result.fanspeed = self.toCommonFanSpeed(self.getFan())
        result.swingh = self.toCommonSwingH(self.getSwingHorizontal())

        # Not supported.
        result.swingv = stdAc.swingv_t.kOff
        result.quiet = False
        result.turbo = False
        result.light = False
        result.clean = False
        result.econo = False
        result.filter = False
        result.beep = False
        result.sleep = -1
        result.clock = -1
        return result

    # Convert the internal state into a human readable string.
    def toString(self):
        result = ""
        result += addBoolToString(self.getPower(), kPowerStr, False)
        result += addModeToString(
            self.getMode(),
            kDaikinAuto,
            kDaikin176Cool,
            kDaikinHeat,
            kDaikinDry,
            kDaikinFan
        )
        result += addTempToString(self.getTemp())
        result += addFanToString(
            self.getFan(),
            kDaikin176FanMax,
            kDaikinFanMin,
            kDaikinFanMin,
            kDaikinFanMin,
            kDaikinFanMin
        )
        result += addIntToString(self.getSwingHorizontal(), kSwingHStr)
        result += kSpaceLBraceStr
        swing = self.getSwingHorizontal()

        if swing == kDaikin176SwingHAuto:
          result += kAutoStr
        elif swing == kDaikin176SwingHOff:
          result += kOffStr
        else:
            result += kUnknownStr

        result += ')'
        return result


    # Decode the supplied Daikin 176 bit A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin176Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin BRC4C153 remote.
    #
    # Status: BETA / Probably works.
    #

    def decode_ac(self, results, nbits, strict):
        if results.rawlen < 2 * (nbits + kHeader + kFooter) - 1:
            return False

        # Compliance
        if strict and nbits != kDaikin176Bits:
            return False

        offset = kStartOffset
        ksectionSize = [kDaikin176Section1Length, kDaikin176Section2Length]

        # Sections
        pos = 0
        for section in range(kDaikin176Sections):
            # Section Header + Section Data (7 bytes) + Section Footer
            used = self.matchGeneric(
                results.rawbuf[:offset],
                results.state + pos,
                results.rawlen - offset,
                ksectionSize[section] * 8,
                kDaikin176HdrMark,
                kDaikin176HdrSpace,
                kDaikin176BitMark,
                kDaikin176OneSpace,
                kDaikin176BitMark,
                kDaikin176ZeroSpace,
                kDaikin176BitMark,
                kDaikin176Gap,
                section >= kDaikin176Sections - 1,
                kDaikinTolerance,
                kDaikinMarkExcess,
                False
            )
            if used == 0:
                return False

            offset += used
            pos += ksectionSize[section]

        # Compliance
        if strict and not self.validChecksum(results.state):
            return False

        # Success
        results.decode_type = decode_type_t.DAIKIN176
        results.bits = nbits
        # No need to record the state as we stored it as we decoded it.
        # As we use result.state, we don't record value, address, or command as it
        # is a union data type.
        return True


class Daikin128(ProtocolBase):
    # Class for handling Daikin 128 bit / 16 byte A/C messages.
    #
    # Code by crankyoldgit.
    # Analysis by Daniel Vena
    #
    # Status: STABLE / Known Working.
    #
    # Supported Remotes: Daikin BRC52B63 remote
    #


    # Send a Daikin 128 bit A/C message.
    #
    # Args:
    #   data: An array of kDaikin128StateLength bytes containing the IR command.
    #
    # Status: STABLE / Known Working.
    #
    # Supported devices:
    # - Daikin BRC52B63 remote.
    #
    # Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/827
    def send_ac(self):
        data = self.getRaw()
        nbytes = kDaikin128StateLength
        repeat = repeat

        if nbytes < kDaikin128SectionLength:
            return  # Not enough bytes to send a partial message.

        for _ in range(repeat + 1):
            enableIROut(kDaikin128Freq)
            # Leader
            for i in range(2):
                self.mark(kDaikin128LeaderMark)
                self.space(kDaikin128LeaderSpace)

            # Section #1 (Header + Data)
            self.sendGeneric(
                kDaikin128HdrMark,
                kDaikin128HdrSpace,
                kDaikin128BitMark,
                kDaikin128OneSpace,
                kDaikin128BitMark,
                kDaikin128ZeroSpace,
                kDaikin128BitMark,
                kDaikin128Gap,
                data,
                kDaikin128SectionLength,
                kDaikin128Freq,
                False,
                0,
                kDutyDefault
            )
            # Section #2 (Data + Footer)
            self.sendGeneric(
                0,
                0,
                kDaikin128BitMark,
                kDaikin128OneSpace,
                kDaikin128BitMark,
                kDaikin128ZeroSpace,
                kDaikin128FooterMark,
                kDaikin128Gap,
                data + kDaikin128SectionLength,
                nbytes - kDaikin128SectionLength,
                kDaikin128Freq,
                False,
                0,
                kDutyDefault
            )

    @staticmethod
    def calcFirstChecksum(state):
        return sumNibbles(
            state,
            kDaikin128SectionLength - 1,
            state[kDaikin128SectionLength - 1] & 0x0F
        ) & 0x0F

    @staticmethod
    def calcSecondChecksum(state):
        return sumNibbles(state + kDaikin128SectionLength, kDaikin128SectionLength - 1)

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    # Returns:
    #   A boolean.
    @classmethod
    def validChecksum(cls, state):
        # Validate the checksum of section #1.
        if state[kDaikin128SectionLength - 1] >> 4 != cls.calcFirstChecksum(state):
            return False
        # Validate the checksum of section #2
        if state[kDaikin128StateLength - 1] != cls.calcSecondChecksum(state):
            return False

        return True

    # Calculate and set the checksum values for the internal state.
    def checksum(self):
        self.remote_state[kDaikin128SectionLength - 1] &= 0x0F  # Clear upper half.
        self.remote_state[kDaikin128SectionLength - 1] |= (self.calcFirstChecksum(self.remote_state) << 4)
        self.remote_state[kDaikin128StateLength - 1] = self.calcSecondChecksum(self.remote_state)

    def stateReset(self):
        self.remote_state = [0x16, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x04, 0xA1]
        self.remote_state += [0x0] * (kDaikin128StateLength - 9)

    def getRaw(self):
        self.checksum()  # Ensure correct settings before sending.
        return self.remote_state[:]

    def setRaw(self, new_code):
        self.remote_state = new_code[:kDaikin128StateLength]

    def setPowerToggle(self, toggle):
        setBit(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitPowerToggleOffset, toggle)

    def getPowerToggle(self):
        return GETBIT8(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitPowerToggleOffset)

    def getMode(self):
        return GETBITS8(self.remote_state[kDaikin128ByteModeFan], kLowNibble, kDaikin128ModeSize)

    def setMode(self, mode):
        if mode in (
            kDaikin128Auto,
            kDaikin128Cool,
            kDaikin128Heat,
            kDaikin128Fan,
            kDaikin128Dry
        ):
            setBits(self.remote_state[kDaikin128ByteModeFan], kLowNibble, kDaikin128ModeSize, mode)
        else:
            self.setMode(kDaikin128Auto)
            return

        # Force a reset of mode dependant things.
        self.setFan(self.getFan())  # Covers Quiet & Powerful too.
        self.setEcono(self.getEcono())

    # Convert a standard A/C mode into its native mode.
    @staticmethod
    def convertMode(mode):
        if mode == stdAc.opmode_t.kCool:
            return kDaikin128Cool
        if mode == stdAc.opmode_t.kHeat:
            return kDaikin128Heat
        if mode == stdAc.opmode_t.kDry:
            return kDaikinDry
        if mode == stdAc.opmode_t.kFan:
            return kDaikin128Fan

        return kDaikin128Auto

    # Convert a native mode to it's common equivalent.
    @staticmethod
    def toCommonMode(mode):
        if mode == kDaikin128Cool:
            return stdAc.opmode_t.kCool
        if mode == kDaikin128Heat:
            return stdAc.opmode_t.kHeat
        if mode == kDaikin128Dry:
            return stdAc.opmode_t.kDry
        if mode == kDaikin128Fan:
            return stdAc.opmode_t.kFan

        return stdAc.opmode_t.kAuto

    # Set the temp in deg C
    def setTemp(self, temp):
        self.remote_state[kDaikin128ByteTemp] = uint8ToBcd(min(kDaikin128MaxTemp, max(temp, kDaikin128MinTemp)))

    def getTemp(self):
        return bcdToUint8(self.remote_state[kDaikin128ByteTemp])

    def getFan(self):
        return GETBITS8(self.remote_state[kDaikin128ByteModeFan], kHighNibble, kDaikinFanSize)

    def setFan(self, speed):
        new_speed = speed
        mode = self.getMode()

        if speed in (
                kDaikin128FanAuto,
                kDaikin128FanHigh,
                kDaikin128FanMed,
                kDaikin128FanLow,
                kDaikin128FanQuiet,
                kDaikin128FanPowerful
        ):

            if speed in (kDaikin128FanQuiet, kDaikin128FanPowerful):
                if mode == kDaikin128Auto:
                    new_speed = kDaikin128FanAuto

            setBits(self.remote_state[kDaikin128ByteModeFan], kHighNibble, kDaikinFanSize, new_speed)

        else:
            self.setFan(kDaikin128FanAuto)

    # Convert a standard A/C Fan speed into its native fan speed.
    @staticmethod
    def convertFan(speed):
        if speed == stdAc.fanspeed_t.kMin:
            return kDaikinFanQuiet
        if speed == stdAc.fanspeed_t.kLow:
            return kDaikin128FanLow
        if speed == stdAc.fanspeed_t.kMedium:
            return kDaikin128FanMed
        if speed == stdAc.fanspeed_t.kHigh:
            return kDaikin128FanHigh
        if speed == stdAc.fanspeed_t.kMax:
            return kDaikin128FanPowerful

        return kDaikin128FanAuto

    # Convert a native fan speed to it's common equivalent.
    @staticmethod
    def toCommonFanSpeed(speed):
        if speed == kDaikin128FanPowerful:
            return stdAc.fanspeed_t.kMax
        if speed == kDaikin128FanHigh:
            return stdAc.fanspeed_t.kHigh
        if speed == kDaikin128FanMed:
            return stdAc.fanspeed_t.kMedium
        if speed == kDaikin128FanLow:
            return stdAc.fanspeed_t.kLow
        if speed == kDaikinFanQuiet:
            return stdAc.fanspeed_t.kMin

        return stdAc.fanspeed_t.kAuto

    def setSwingVertical(self, on)
        setBit(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitSwingOffset, on)

    def getSwingVertical(self):
        return GETBIT8(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitSwingOffset)

    def setSleep(self, on):
        setBit(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitSleepOffset, on)

    def getSleep(self):
        return GETBIT8(self.remote_state[kDaikin128BytePowerSwingSleep], kDaikin128BitSleepOffset)

    def setEcono(self, on):
        mode = self.getMode()
        setBit(
            self.remote_state[kDaikin128ByteEconoLight],
            kDaikin128BitEconoOffset,
            on and (mode == kDaikin128Cool or mode == kDaikin128Heat)
        )

    def getEcono(self):
        return GETBIT8(self.remote_state[kDaikin128ByteEconoLight], kDaikin128BitEconoOffset)

    def setQuiet(self, on):
        mode = self.getMode()
        if on and (mode == kDaikin128Cool or mode == kDaikin128Heat):
            self.setFan(kDaikin128FanQuiet)
        elif getFan() == kDaikin128FanQuiet:
            self.setFan(kDaikin128FanAuto)

    def getQuiet(self):
        return self.getFan() == kDaikin128FanQuiet

    def setPowerful(self, on):
        mode = self.getMode()
        if on and (mode == kDaikin128Cool or mode == kDaikin128Heat):
            self.setFan(kDaikin128FanPowerful)
        elif self.getFan() == kDaikin128FanPowerful
            setFan(kDaikin128FanAuto)

    def getPowerful(self):
        return self.getFan() == kDaikin128FanPowerful

    # Set the clock in mins since midnight
    def setClock(self, mins_since_midnight):
        mins = mins_since_midnight
        if mins_since_midnight >= 24 * 60:
            mins = 0  # Bounds check.

        # Hours.
        self.remote_state[kDaikin128ByteClockHours] = uint8ToBcd(mins / 60)
        # Minutes.
        self.remote_state[kDaikin128ByteClockMins] = uint8ToBcd(mins % 60)

    def getClock(self):
        return (
            bcdToUint8(self.remote_state[kDaikin128ByteClockHours]) * 60 +
            bcdToUint8(self.remote_state[kDaikin128ByteClockMins])
        )

    void IRDaikin128.setOnTimerEnabled(bool on) {
      setBit(&remote_state[kDaikin128ByteOnTimer], kDaikin128BitTimerEnabledOffset,
             on)
    }

    bool IRDaikin128.getOnTimerEnabled(void) {
      return GETBIT8(remote_state[kDaikin128ByteOnTimer],
                     kDaikin128BitTimerEnabledOffset)
    }

    # Timer is rounds down to the nearest half hour.
    # Args:
    #   ptr: A PTR to the byte containing the Timer value to be updated.
    #   mins_since_midnight: The number of minutes the new timer should be set to.
    void IRDaikin128.setTimer(*ptr, mins_since_midnight) {
      mins = mins_since_midnight
      if (mins_since_midnight >= 24 * 60) mins = 0  # Bounds check.
      # Set the half hour bit
      setBit(ptr, kDaikin128HalfHourOffset, (mins % 60) >= 30)
      # Set the nr of whole hours.
      setBits(ptr, kDaikin128HoursOffset, kDaikin128HoursSize,
              uint8ToBcd(mins / 60))
    }

    # Timer is stored in nr of half hours internally.
    # Args:
    #   ptr: A PTR to the byte containing the Timer value.
    # Returns:
    #   A containing the number of minutes since midnight.
    IRDaikin128.getTimer(*ptr) {
      return bcdToUint8(GETBITS8(*ptr, kDaikin128HoursOffset,
                                 kDaikin128HoursSize)) * 60 +
          (GETBIT8(*ptr, kDaikin128HalfHourOffset) ? 30 : 0)
    }

    void IRDaikin128.setOnTimer(mins_since_midnight) {
      setTimer(remote_state + kDaikin128ByteOnTimer, mins_since_midnight)
    }

    IRDaikin128.getOnTimer(void) {
      return getTimer(remote_state + kDaikin128ByteOnTimer)
    }

    void IRDaikin128.setOffTimerEnabled(bool on) {
      setBit(&remote_state[kDaikin128ByteOffTimer], kDaikin128BitTimerEnabledOffset,
             on)
    }

    bool IRDaikin128.getOffTimerEnabled(void) {
      return GETBIT8(remote_state[kDaikin128ByteOffTimer],
                     kDaikin128BitTimerEnabledOffset)
    }

    void IRDaikin128.setOffTimer(mins_since_midnight) {
      setTimer(remote_state + kDaikin128ByteOffTimer, mins_since_midnight)
    }

    IRDaikin128.getOffTimer(void) {
      return getTimer(remote_state + kDaikin128ByteOffTimer)
    }

    void IRDaikin128.setLightToggle(unit) {
      switch (unit) {
        case 0:
        case kDaikin128BitCeiling:
        case kDaikin128BitWall:
          remote_state[kDaikin128ByteEconoLight] &= ~kDaikin128MaskLight
          remote_state[kDaikin128ByteEconoLight] |= unit
          break
        default: setLightToggle(0)
      }
    }

    IRDaikin128.getLightToggle(void) {
      return remote_state[kDaikin128ByteEconoLight] & kDaikin128MaskLight
    }

    # Convert the internal state into a human readable string.
    String IRDaikin128.toString(void) {
      String result = ""
      result.reserve(240)  # Reserve some heap for the string to reduce fragging.
      result += addBoolToString(getPowerToggle(), kPowerToggleStr, False)
      result += addModeToString(getMode(), kDaikin128Auto, kDaikin128Cool,
                                kDaikin128Heat, kDaikin128Dry, kDaikin128Fan)
      result += addTempToString(getTemp())
      result += addFanToString(getFan(), kDaikin128FanHigh, kDaikin128FanLow,
                               kDaikin128FanAuto, kDaikin128FanQuiet,
                               kDaikin128FanMed)
      result += addBoolToString(getPowerful(), kPowerfulStr)
      result += addBoolToString(getQuiet(), kQuietStr)
      result += addBoolToString(getSwingVertical(), kSwingVStr)
      result += addBoolToString(getSleep(), kSleepStr)
      result += addBoolToString(getEcono(), kEconoStr)
      result += addLabeledString(minsToString(getClock()), kClockStr)
      result += addBoolToString(getOnTimerEnabled(), kOnTimerStr)
      result += addLabeledString(minsToString(getOnTimer()), kOnTimerStr)
      result += addBoolToString(getOffTimerEnabled(), kOffTimerStr)
      result += addLabeledString(minsToString(getOffTimer()), kOffTimerStr)
      result += addIntToString(getLightToggle(), kLightToggleStr)
      result += kSpaceLBraceStr
      switch (getLightToggle()) {
        case kDaikin128BitCeiling: result += kCeilingStr break
        case kDaikin128BitWall: result += kWallStr break
        case 0: result += kOffStr break
        default: result += kUnknownStr
      }
      result += ')'
      return result
    }

    # Convert the A/C state to it's common equivalent.
    stdAc.state_t IRDaikin128.toCommon(stdAc.state_t *prev) {
      stdAc.state_t result
      if (prev != NULL) result = *prev
      result.protocol = decode_type_t.DAIKIN128
      result.model = -1  # No models used.
      result.power ^= getPowerToggle()
      result.mode = toCommonMode(getMode())
      result.celsius = True
      result.degrees = getTemp()
      result.fanspeed = toCommonFanSpeed(getFan())
      result.swingv = getSwingVertical() ? stdAc.swingv_t.kAuto
                                         : stdAc.swingv_t.kOff
      result.quiet = getQuiet()
      result.turbo = getPowerful()
      result.econo = getEcono()
      result.light ^= (getLightToggle() != 0)
      result.sleep = getSleep() ? 0 : -1
      result.clock = getClock()
      # Not supported.
      result.swingh = stdAc.swingh_t.kOff
      result.clean = False
      result.filter = False
      result.beep = False
      return result
    }

    #if DECODE_DAIKIN128
    # Decode the supplied Daikin 128 bit A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin128Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin BRC52B63 remote.
    #
    # Status: STABLE / Known Working.
    #
    # Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/827
    bool IRrecv.decodeDaikin128(decode_results *results, nbits,
                                 bool strict) {
      if (results.rawlen < 2 * (nbits + kHeader) + kFooter - 1)
        return False
      if (nbits / 8 <= kDaikin128SectionLength) return False

      # Compliance
      if (strict and nbits != kDaikin128Bits) return False

      offset = kStartOffset

      # Leader
      for (i = 0 i < 2 i++) {
        if (!matchMark(results.rawbuf[offset++], kDaikin128LeaderMark,
                       kDaikinTolerance, kDaikinMarkExcess)) return False
        if (!matchSpace(results.rawbuf[offset++], kDaikin128LeaderSpace,
                        kDaikinTolerance, kDaikinMarkExcess)) return False
      }
      ksectionSize[kDaikin128Sections] = {
          kDaikin128SectionLength, (uint16_t)(nbits / 8 - kDaikin128SectionLength)}
      # Data Sections
      pos = 0
      for (section = 0 section < kDaikin128Sections section++) {
        used
        # Section Header (first section only) + Section Data (8 bytes) +
        #     Section Footer (Not for first section)
        used = matchGeneric(results.rawbuf + offset, results.state + pos,
                            results.rawlen - offset, ksectionSize[section] * 8,
                            section == 0 ? kDaikin128HdrMark : 0,
                            section == 0 ? kDaikin128HdrSpace : 0,
                            kDaikin128BitMark, kDaikin128OneSpace,
                            kDaikin128BitMark, kDaikin128ZeroSpace,
                            section > 0 ? kDaikin128FooterMark : kDaikin128BitMark,
                            kDaikin128Gap,
                            section > 0,
                            kDaikinTolerance, kDaikinMarkExcess, False)
        if (used == 0) return False
        offset += used
        pos += ksectionSize[section]
      }
      # Compliance
      if (strict) {
        if (!IRDaikin128.validChecksum(results.state)) return False
      }

      # Success
      results.decode_type = decode_type_t.DAIKIN128
      results.bits = nbits
      # No need to record the state as we stored it as we decoded it.
      # As we use result.state, we don't record value, address, or command as it
      # is a union data type.
      return True
    }
    #endif  # DECODE_DAIKIN128


class Daikin152(ProtocolBase):
    #if SEND_DAIKIN152
    # Send a Daikin 152 bit A/C message.
    #
    # Args:
    #   data: An array of kDaikin152StateLength bytes containing the IR command.
    #
    # Supported devices:
    # - Daikin ARC480A5 remote.
    #
    # Status: STABLE / Known working.
    #
    # Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/873
    void IRsend.sendDaikin152(unsigned char data[], nbytes,
                               repeat) {
      for (r = 0 r <= repeat r++) {
        # Leader
        sendGeneric(0, 0, kDaikin152BitMark, kDaikin152OneSpace,
                    kDaikin152BitMark, kDaikin152ZeroSpace,
                    kDaikin152BitMark, kDaikin152Gap,
                    (uint64_t)0, kDaikin152LeaderBits,
                    kDaikin152Freq, False, 0, kDutyDefault)
        # Header + Data + Footer
        sendGeneric(kDaikin152HdrMark, kDaikin152HdrSpace, kDaikin152BitMark,
                    kDaikin152OneSpace, kDaikin152BitMark, kDaikin152ZeroSpace,
                    kDaikin152BitMark, kDaikin152Gap, data,
                    nbytes, kDaikin152Freq, False, 0, kDutyDefault)
      }
    }
    #endif  # SEND_DAIKIN152

    #if DECODE_DAIKIN152
    # Decode the supplied Daikin 152 bit A/C message.
    # Args:
    #   results: Ptr to the data to decode and where to store the decode result.
    #   nbits:   Nr. of bits to expect in the data portion. (kDaikin152Bits)
    #   strict:  Flag to indicate if we strictly adhere to the specification.
    # Returns:
    #   boolean: True if it can decode it, False if it can't.
    #
    # Supported devices:
    # - Daikin ARC480A5 remote.
    #
    # Status: STABLE / Known working.
    #
    # Ref: https:#github.com/crankyoldgit/IRremoteESP8266/issues/873
    bool IRrecv.decodeDaikin152(decode_results *results, nbits,
                                 bool strict) {
      if (results.rawlen < 2 * (5 + nbits + kFooter) + kHeader - 1)
        return False
      if (nbits / 8 < kDaikin152StateLength) return False

      # Compliance
      if (strict and nbits != kDaikin152Bits) return False

      offset = kStartOffset
      used

      # Leader
      leader = 0
      used = matchGeneric(results.rawbuf + offset, &leader,
                          results.rawlen - offset, kDaikin152LeaderBits,
                          0, 0,  # No Header
                          kDaikin152BitMark, kDaikin152OneSpace,
                          kDaikin152BitMark, kDaikin152ZeroSpace,
                          kDaikin152BitMark, kDaikin152Gap,  # Footer gap
                          False, _tolerance, kMarkExcess, False)
      if (used == 0 or leader != 0) return False
      offset += used

      # Header + Data + Footer
      used = matchGeneric(results.rawbuf + offset, results.state,
                          results.rawlen - offset, nbits,
                          kDaikin152HdrMark, kDaikin152HdrSpace,
                          kDaikin152BitMark, kDaikin152OneSpace,
                          kDaikin152BitMark, kDaikin152ZeroSpace,
                          kDaikin152BitMark, kDaikin152Gap,
                          True, _tolerance, kMarkExcess, False)
      if (used == 0) return False

      # Compliance
      if (strict) {
        if (!IRDaikin152.validChecksum(results.state)) return False
      }

      # Success
      results.decode_type = decode_type_t.DAIKIN152
      results.bits = nbits
      # No need to record the state as we stored it as we decoded it.
      # As we use result.state, we don't record value, address, or command as it
      # is a union data type.
      return True
    }
    #endif  # DECODE_DAIKIN152

    # Class for handling Daikin 152 bit / 19 byte A/C messages.
    #
    # Code by crankyoldgit.
    #
    # Supported Remotes: Daikin ARC480A5 remote
    #
    # Ref:
    #   https:#github.com/crankyoldgit/IRremoteESP8266/issues/873
    #   https:#github.com/ToniA/arduino-heatpumpir/blob/master/DaikinHeatpumpARC480A14IR.cpp
    #   https:#github.com/ToniA/arduino-heatpumpir/blob/master/DaikinHeatpumpARC480A14IR.h
    IRDaikin152.IRDaikin152(pin, bool inverted,
                             bool use_modulation)
        : _irsend(pin, inverted, use_modulation) { stateReset() }

    void IRDaikin152.begin(void) { _irsend.begin() }

    #if SEND_DAIKIN152
    void IRDaikin152.send(repeat) {
      _irsend.sendDaikin152(getRaw(), kDaikin152StateLength, repeat)
    }
    #endif  # SEND_DAIKIN152

    # Verify the checksum is valid for a given state.
    # Args:
    #   state:  The array to verify the checksum of.
    #   length: The size of the state.
    # Returns:
    #   A boolean.
    bool IRDaikin152.validChecksum(state[], length) {
      # Validate the checksum of the given state.
      if (length <= 1 or state[length - 1] != sumBytes(state, length - 1))
        return False
      else
        return True
    }

    # Calculate and set the checksum values for the internal state.
    void IRDaikin152.checksum(void) {
      remote_state[kDaikin152StateLength - 1] = sumBytes(
          remote_state, kDaikin152StateLength - 1)
    }

    void IRDaikin152.stateReset(void) {
      for (i = 3 i < kDaikin152StateLength i++) remote_state[i] = 0x00
      remote_state[0] =  0x11
      remote_state[1] =  0xDA
      remote_state[2] =  0x27
      remote_state[15] = 0xC5
      # remote_state[19] is a checksum byte, it will be set by checksum().
    }

    *IRDaikin152.getRaw(void) {
      checksum()  # Ensure correct settings before sending.
      return remote_state
    }

    void IRDaikin152.setRaw(new_code[]) {
      memcpy(remote_state, new_code, kDaikin152StateLength)
    }

    void IRDaikin152.on(void) { setPower(True) }

    void IRDaikin152.off(void) { setPower(False) }

    void IRDaikin152.setPower(bool on) {
      setBit(&remote_state[kDaikin152PowerByte], kDaikinBitPowerOffset, on)
    }

    bool IRDaikin152.getPower(void) {
      return GETBIT8(remote_state[kDaikin152PowerByte], kDaikinBitPowerOffset)
    }

    IRDaikin152.getMode(void) {
      return GETBITS8(remote_state[kDaikin152ModeByte], kDaikinModeOffset,
                      kDaikinModeSize)
    }

    void IRDaikin152.setMode(mode) {
      switch (mode) {
        case kDaikinFan:
          setTemp(kDaikin152FanTemp)  # Handle special temp for fan mode.
          break
        case kDaikinDry:
          setTemp(kDaikin152DryTemp)  # Handle special temp for dry mode.
          break
        case kDaikinAuto:
        case kDaikinCool:
        case kDaikinHeat:
          break
        default:
          self.setMode(kDaikinAuto)
          return
      }
      setBits(&remote_state[kDaikin152ModeByte], kDaikinModeOffset,
              kDaikinModeSize, mode)
    }

    # Convert a standard A/C mode into its native mode.
    IRDaikin152.convertMode(stdAc.opmode_t mode) {
      return IRDaikinESP.convertMode(mode)
    }

    # Set the temp in deg C
    void IRDaikin152.setTemp(temp) {
      degrees = std.max(
          temp, (getMode() == kDaikinHeat) ? kDaikinMinTemp : kDaikin2MinCoolTemp)
      degrees = std.min(degrees, kDaikinMaxTemp)
      if (temp == kDaikin152FanTemp) degrees = temp  # Handle fan only temp.
      setBits(&remote_state[kDaikin152TempByte], kDaikinTempOffset,
              kDaikin152TempSize, degrees)
    }

    IRDaikin152.getTemp(void) {
      return GETBITS8(remote_state[kDaikin152TempByte], kDaikinTempOffset,
                      kDaikin152TempSize)
    }

    # Set the speed of the fan, 1-5 or kDaikinFanAuto or kDaikinFanQuiet
    void IRDaikin152.setFan(fan) {
      # Set the fan speed bits, leave low 4 bits alone
      fanset
      if (fan == kDaikinFanQuiet or fan == kDaikinFanAuto)
        fanset = fan
      else if (fan < kDaikinFanMin or fan > kDaikinFanMax)
        fanset = kDaikinFanAuto
      else
        fanset = 2 + fan
      setBits(&remote_state[kDaikin152FanByte], kHighNibble, kNibbleSize, fanset)
    }

    IRDaikin152.getFan(void) {
      fan = GETBITS8(remote_state[kDaikin152FanByte], kHighNibble,
                                   kNibbleSize)
      switch (fan) {
        case kDaikinFanAuto:
        case kDaikinFanQuiet: return fan
        default: return fan - 2
      }
    }

    # Convert a standard A/C Fan speed into its native fan speed.
    IRDaikin152.convertFan(stdAc.fanspeed_t speed) {
      return IRDaikinESP.convertFan(speed)
    }

    void IRDaikin152.setSwingV(bool on) {
      setBits(&remote_state[kDaikin152SwingVByte], kDaikinSwingOffset,
              kDaikinSwingSize, on ? kDaikinSwingOn : kDaikinSwingOff)
    }

    bool IRDaikin152.getSwingV(void) {
      return GETBITS8(remote_state[kDaikin152SwingVByte], kDaikinSwingOffset,
                      kDaikinSwingSize)
    }

    void IRDaikin152.setQuiet(bool on) {
      setBit(&remote_state[kDaikin152QuietByte], kDaikinBitSilentOffset, on)
      # Powerful & Quiet mode being on are mutually exclusive.
      if (on) self.setPowerful(False)
    }

    bool IRDaikin152.getQuiet(void) {
      return GETBIT8(remote_state[kDaikin152QuietByte], kDaikinBitSilentOffset)
    }

    void IRDaikin152.setPowerful(bool on) {
      setBit(&remote_state[kDaikin152PowerfulByte], kDaikinBitPowerfulOffset, on)
      if (on) {
        # Powerful, Quiet, Comfortm & Econo mode being on are mutually exclusive.
        self.setQuiet(False)
        self.setComfort(False)
        self.setEcono(False)
      }
    }

    bool IRDaikin152.getPowerful(void) {
      return GETBIT8(remote_state[kDaikin152PowerfulByte],
                     kDaikinBitPowerfulOffset)
    }

    void IRDaikin152.setEcono(bool on) {
      setBit(&remote_state[kDaikin152EconoByte], kDaikinBitEconoOffset, on)
      # Powerful & Econo mode being on are mutually exclusive.
      if (on) self.setPowerful(False)
    }

    bool IRDaikin152.getEcono(void) {
      return GETBIT8(remote_state[kDaikin152EconoByte], kDaikinBitEconoOffset)
    }

    void IRDaikin152.setSensor(bool on) {
      setBit(&remote_state[kDaikin152SensorByte], kDaikin152SensorOffset, on)
    }

    bool IRDaikin152.getSensor(void) {
      return GETBIT8(remote_state[kDaikin152SensorByte], kDaikin152SensorOffset)
    }

    void IRDaikin152.setComfort(bool on) {
      setBit(&remote_state[kDaikin152ComfortByte], kDaikin152ComfortOffset, on)
      if (on) {
        # Comfort mode is incompatible with Powerful mode.
        setPowerful(False)
        # It also sets the fan to auto and turns off swingv.
        setFan(kDaikinFanAuto)
        setSwingV(False)
      }
    }

    bool IRDaikin152.getComfort(void) {
      return GETBIT8(remote_state[kDaikin152ComfortByte], kDaikin152ComfortOffset)
    }

    # Convert the A/C state to it's common equivalent.
    stdAc.state_t IRDaikin152.toCommon(void) {
      stdAc.state_t result
      result.protocol = decode_type_t.DAIKIN152
      result.model = -1  # No models used.
      result.power = self.getPower()
      result.mode = IRDaikinESP.toCommonMode(self.getMode())
      result.celsius = True
      result.degrees = self.getTemp()
      result.fanspeed = IRDaikinESP.toCommonFanSpeed(self.getFan())
      result.swingv = self.getSwingV() ? stdAc.swingv_t.kAuto
                                        : stdAc.swingv_t.kOff
      result.quiet = self.getQuiet()
      result.turbo = self.getPowerful()
      result.econo = self.getEcono()
      # Not supported.
      result.swingh = stdAc.swingh_t.kOff
      result.clean = False
      result.filter = False
      result.light = False
      result.beep = False
      result.sleep = -1
      result.clock = -1
      return result
    }

    # Convert the internal state into a human readable string.
    String IRDaikin152.toString(void) {
      String result = ""
      result.reserve(180)  # Reserve some heap for the string to reduce fragging.
      result += addBoolToString(getPower(), kPowerStr, False)
      result += addModeToString(getMode(), kDaikinAuto, kDaikinCool, kDaikinHeat,
                                kDaikinDry, kDaikinFan)
      result += addTempToString(getTemp())
      result += addFanToString(getFan(), kDaikinFanMax, kDaikinFanMin,
                               kDaikinFanAuto, kDaikinFanQuiet, kDaikinFanMed)
      result += addBoolToString(getSwingV(), kSwingVStr)
      result += addBoolToString(getPowerful(), kPowerfulStr)
      result += addBoolToString(getQuiet(), kQuietStr)
      result += addBoolToString(getEcono(), kEconoStr)
      result += addBoolToString(getSensor(), kSensorStr)
      result += addBoolToString(getComfort(), kComfortStr)
      return result
    }
