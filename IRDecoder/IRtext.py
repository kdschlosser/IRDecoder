# -*- coding: utf-8 -*-
# Copyright 2019 - David Conran (@crankyoldgit)

from .IRremoteESP8266 import *

# Copyright 2019 - David Conran (@crankyoldgit)
# The default text to use throughout the library.
# The library will use this text if no locale (_IR_LOCALE_) is set or if
# the locale doesn't define particular values.
# If they are defined, this file should NOT override them.
#
# This file should contain a #define for every translateable/locale dependant
# string used by the library. Language specific files don't have to include
# everything.
#
# NOTE: ASCII/UTF-8 characters only. Unicode is NOT supported.
#
# The defaults are English (AU) / en-AU. Australia (AU) is pretty much the same
# as English (UK) for this libraries use case.

D_STR_AUTO = 'Auto'
D_STR_AUTOMATIC = 'Automatic'
D_STR_MANUAL = 'Manual'
D_STR_COOL = 'Cool'
D_STR_HEAT = 'Heat'
D_STR_FAN = 'Fan'
D_STR_FANONLY = 'fan_only'
D_STR_DRY = 'Dry'

D_STR_CENTRE = 'Center'
D_STR_MOULD = 'Mold'

D_STR_UNKNOWN = 'UNKNOWN'
D_STR_PROTOCOL = 'Protocol'
D_STR_POWER = 'Power'
D_STR_ON = 'On'
D_STR_OFF = 'Off'
D_STR_MODE = 'Mode'
D_STR_TOGGLE = 'Toggle'
D_STR_TURBO = 'Turbo'
D_STR_SUPER = 'Super'
D_STR_SLEEP = 'Sleep'
D_STR_LIGHT = 'Light'
D_STR_POWERFUL = 'Powerful'
D_STR_QUIET = 'Quiet'
D_STR_ECONO = 'Econo'
D_STR_SWING = 'Swing'
D_STR_SWINGH = D_STR_SWING + '(H)'
D_STR_SWINGV = D_STR_SWING + '(V)'
D_STR_BEEP = 'Beep'
D_STR_CLEAN = 'Clean'
D_STR_PURIFY = 'Purify'
D_STR_TIMER = 'Timer'
D_STR_ONTIMER = D_STR_ON + ' ' + D_STR_TIMER
D_STR_OFFTIMER = D_STR_OFF + ' ' + D_STR_TIMER
D_STR_CLOCK = 'Clock'
D_STR_COMMAND = 'Command'
D_STR_XFAN = 'XFan'
D_STR_HEALTH = 'Health'
D_STR_MODEL = 'Model'
D_STR_TEMP = 'Temp'
D_STR_IFEEL = 'IFeel'
D_STR_HUMID = 'Humid'
D_STR_SAVE = 'Save'
D_STR_EYE = 'Eye'
D_STR_FOLLOW = 'Follow'
D_STR_ION = 'Ion'
D_STR_FRESH = 'Fresh'
D_STR_VENT = 'Vent'
D_STR_HOLD = 'Hold'
D_STR_8C_HEAT = '8C ' + D_STR_HEAT
D_STR_BUTTON = 'Button'
D_STR_NIGHT = 'Night'
D_STR_SILENT = 'Silent'
D_STR_FILTER = 'Filter'
D_STR_3D = '3D'
D_STR_CELSIUS = 'Celsius'
D_STR_UP = 'Up'
D_STR_TEMPUP = D_STR_TEMP + ' ' + D_STR_UP
D_STR_DOWN = 'Down'
D_STR_TEMPDOWN = D_STR_TEMP + ' ' + D_STR_DOWN
D_STR_CHANGE = 'Change'
D_STR_START = 'Start'
D_STR_STOP = 'Stop'
D_STR_MOVE = 'Move'
D_STR_SET = 'Set'
D_STR_CANCEL = 'Cancel'
D_STR_COMFORT = 'Comfort'
D_STR_SENSOR = 'Sensor'
D_STR_WEEKLY = 'Weekly'
D_STR_WEEKLYTIMER = D_STR_WEEKLY + ' ' + D_STR_TIMER
D_STR_WIFI = 'WiFi'
D_STR_LAST = 'Last'
D_STR_FAST = 'Fast'
D_STR_SLOW = 'Slow'
D_STR_AIRFLOW = 'Air Flow'
D_STR_STEP = 'Step'
D_STR_NA = 'N/A'
D_STR_OUTSIDE = 'Outside'
D_STR_LOUD = 'Loud'
D_STR_UPPER = 'Upper'
D_STR_LOWER = 'Lower'
D_STR_BREEZE = 'Breeze'
D_STR_CIRCULATE = 'Circulate'
D_STR_CEILING = 'Ceiling'
D_STR_WALL = 'Wall'
D_STR_ROOM = 'Room'
D_STR_6THSENSE = '6th Sense'
D_STR_ZONEFOLLOW = 'Zone Follow'
D_STR_FIXED = 'Fixed'

D_STR_MAX = 'Max'
D_STR_MAXIMUM = 'Maximum'
D_STR_MIN = 'Min'
D_STR_MINIMUM = 'Minimum'
D_STR_MED = 'Med'
D_STR_MEDIUM = 'Medium'

D_STR_HIGHEST = 'Highest'
D_STR_HIGH = 'High'
D_STR_HI = 'Hi'
D_STR_MID = 'Mid'
D_STR_MIDDLE = 'Middle'
D_STR_LOW = 'Low'
D_STR_LO = 'Lo'
D_STR_LOWEST = 'Lowest'
D_STR_RIGHT = 'Right'
D_STR_MAXRIGHT = D_STR_MAX + ' ' + D_STR_RIGHT
D_STR_RIGHTMAX_NOSPACE = D_STR_RIGHT + D_STR_MAX
D_STR_LEFT = 'Left'
D_STR_MAXLEFT = D_STR_MAX + ' ' + D_STR_LEFT
D_STR_LEFTMAX_NOSPACE = D_STR_LEFT + D_STR_MAX
D_STR_WIDE = 'Wide'
D_STR_TOP = 'Top'
D_STR_BOTTOM = 'Bottom'

# Compound words/phrases/descriptions from pre-defined words.
# Note: Obviously these need to be defined *after* their component words.
D_STR_EYEAUTO = D_STR_EYE + ' ' + D_STR_AUTO
D_STR_LIGHTTOGGLE = D_STR_LIGHT + ' ' + D_STR_TOGGLE
D_STR_OUTSIDEQUIET = D_STR_OUTSIDE + ' ' + D_STR_QUIET
D_STR_POWERTOGGLE = D_STR_POWER + ' ' + D_STR_TOGGLE
D_STR_SENSORTEMP = D_STR_SENSOR + ' ' + D_STR_TEMP
D_STR_SLEEP_TIMER = D_STR_SLEEP + ' ' + D_STR_TIMER
D_STR_SWINGVMODE = D_STR_SWINGV + ' ' + D_STR_MODE
D_STR_SWINGVTOGGLE = D_STR_SWINGV + ' ' + D_STR_TOGGLE

# Separators
D_CHR_TIME_SEP = ':'
D_STR_SPACELBRACE = ' ('
D_STR_COMMASPACE = ', '
D_STR_COLONSPACE = ': '

D_STR_DAY = 'Day'
D_STR_DAYS = D_STR_DAY + 's'
D_STR_HOUR = 'Hour'
D_STR_HOURS = D_STR_HOUR + 's'
D_STR_MINUTE = 'Minute'
D_STR_MINUTES = D_STR_MINUTE + 's'
D_STR_SECOND = 'Second'
D_STR_SECONDS = D_STR_SECOND + 's'
D_STR_NOW = 'Now'
D_STR_THREELETTERDAYS = 'SunMonTueWedThuFriSat'

D_STR_YES = 'Yes'
D_STR_NO = 'No'
D_STR_TRUE = 'True'
D_STR_FALSE = 'False'

D_STR_REPEAT = 'Repeat'
D_STR_CODE = 'Code'
D_STR_BITS = 'Bits'

# IRrecvDumpV2
D_STR_TIMESTAMP = 'Timestamp'
D_STR_LIBRARY = 'Library'
D_STR_MESGDESC = 'Mesg Desc.'
D_STR_IRRECVDUMP_STARTUP = 'IRrecvDumpV2 is now running and waiting for IR input on Pin %d'
D_WARN_BUFFERFULL = (
    'WARNING: IR code is too big for buffer (>= %d). This result shouldn\'t be trusted '
    'until this is resolved. Edit & increase \'kCaptureBufferSize\''
)

# Common

kUnknownStr = D_STR_UNKNOWN
kProtocolStr = D_STR_PROTOCOL
kPowerStr = D_STR_POWER
kOnStr = D_STR_ON
kOffStr = D_STR_OFF
kModeStr = D_STR_MODE
kToggleStr = D_STR_TOGGLE
kTurboStr = D_STR_TURBO
kSuperStr = D_STR_SUPER
kSleepStr = D_STR_SLEEP
kLightStr = D_STR_LIGHT
kPowerfulStr = D_STR_POWERFUL
kQuietStr = D_STR_QUIET
kEconoStr = D_STR_ECONO
kSwingStr = D_STR_SWING
kSwingHStr = D_STR_SWINGH
kSwingVStr = D_STR_SWINGV
kBeepStr = D_STR_BEEP
kZoneFollowStr = D_STR_ZONEFOLLOW
kFixedStr = D_STR_FIXED
kMouldStr = D_STR_MOULD
kCleanStr = D_STR_CLEAN
kPurifyStr = D_STR_PURIFY
kTimerStr = D_STR_TIMER
kOnTimerStr = D_STR_ONTIMER
kOffTimerStr = D_STR_OFFTIMER
kClockStr = D_STR_CLOCK
kCommandStr = D_STR_COMMAND
kXFanStr = D_STR_XFAN
kHealthStr = D_STR_HEALTH
kModelStr = D_STR_MODEL
kTempStr = D_STR_TEMP
kIFeelStr = D_STR_IFEEL
kHumidStr = D_STR_HUMID
kSaveStr = D_STR_SAVE
kEyeStr = D_STR_EYE
kFollowStr = D_STR_FOLLOW
kIonStr = D_STR_ION
kFreshStr = D_STR_FRESH
kVentStr = D_STR_VENT
kHoldStr = D_STR_HOLD
kButtonStr = D_STR_BUTTON
k8CHeatStr = D_STR_8C_HEAT
kNightStr = D_STR_NIGHT
kSilentStr = D_STR_SILENT
kFilterStr = D_STR_FILTER
k3DStr = D_STR_3D
kCelsiusStr = D_STR_CELSIUS
kTempUpStr = D_STR_TEMPUP
kTempDownStr = D_STR_TEMPDOWN
kStartStr = D_STR_START
kStopStr = D_STR_STOP
kMoveStr = D_STR_MOVE
kSetStr = D_STR_SET
kCancelStr = D_STR_CANCEL
kUpStr = D_STR_UP
kDownStr = D_STR_DOWN
kChangeStr = D_STR_CHANGE
kComfortStr = D_STR_COMFORT
kSensorStr = D_STR_SENSOR
kWeeklyTimerStr = D_STR_WEEKLYTIMER
kWifiStr = D_STR_WIFI
kLastStr = D_STR_LAST
kFastStr = D_STR_FAST
kSlowStr = D_STR_SLOW
kAirFlowStr = D_STR_AIRFLOW
kStepStr = D_STR_STEP
kNAStr = D_STR_NA
kOutsideStr = D_STR_OUTSIDE
kLoudStr = D_STR_LOUD
kLowerStr = D_STR_LOWER
kUpperStr = D_STR_UPPER
kBreezeStr = D_STR_BREEZE
kCirculateStr = D_STR_CIRCULATE
kCeilingStr = D_STR_CEILING
kWallStr = D_STR_WALL
kRoomStr = D_STR_ROOM
k6thSenseStr = D_STR_6THSENSE

kAutoStr = D_STR_AUTO
kAutomaticStr = D_STR_AUTOMATIC
kManualStr = D_STR_MANUAL
kCoolStr = D_STR_COOL
kHeatStr = D_STR_HEAT
kFanStr = D_STR_FAN
kDryStr = D_STR_DRY
kFanOnlyStr = D_STR_FANONLY

kMaxStr = D_STR_MAX
kMaximumStr = D_STR_MAXIMUM
kMinStr = D_STR_MIN
kMinimumStr = D_STR_MINIMUM
kMedStr = D_STR_MED
kMediumStr = D_STR_MEDIUM

kHighestStr = D_STR_HIGHEST
kHighStr = D_STR_HIGH
kHiStr = D_STR_HI
kMidStr = D_STR_MID
kMiddleStr = D_STR_MIDDLE
kLowStr = D_STR_LOW
kLoStr = D_STR_LO
kLowestStr = D_STR_LOWEST
kMaxRightStr = D_STR_MAXRIGHT
kRightMaxStr = D_STR_RIGHTMAX_NOSPACE
kRightStr = D_STR_RIGHT
kLeftStr = D_STR_LEFT
kMaxLeftStr = D_STR_MAXLEFT
kLeftMaxStr = D_STR_LEFTMAX_NOSPACE
kWideStr = D_STR_WIDE
kCentreStr = D_STR_CENTRE
kTopStr = D_STR_TOP
kBottomStr = D_STR_BOTTOM

# Compound words/phrases/descriptions from pre-defined words.
kEyeAutoStr = D_STR_EYEAUTO
kLightToggleStr = D_STR_LIGHTTOGGLE
kOutsideQuietStr = D_STR_OUTSIDEQUIET
kPowerToggleStr = D_STR_POWERTOGGLE
kSensorTempStr = D_STR_SENSORTEMP
kSleepTimerStr = D_STR_SLEEP_TIMER
kSwingVModeStr = D_STR_SWINGVMODE
kSwingVToggleStr = D_STR_SWINGVTOGGLE

# Separators
kTimeSep = D_CHR_TIME_SEP
kSpaceLBraceStr = D_STR_SPACELBRACE
kCommaSpaceStr = D_STR_COMMASPACE
kColonSpaceStr = D_STR_COLONSPACE

# IRutils
#  - Time
kDayStr = D_STR_DAY
kDaysStr = D_STR_DAYS
kHourStr = D_STR_HOUR
kHoursStr = D_STR_HOURS
kMinuteStr = D_STR_MINUTE
kMinutesStr = D_STR_MINUTES
kSecondStr = D_STR_SECOND
kSecondsStr = D_STR_SECONDS
kNowStr = D_STR_NOW
kThreeLetterDayOfWeekStr = D_STR_THREELETTERDAYS

kYesStr = D_STR_YES
kNoStr = D_STR_NO
kTrueStr = D_STR_TRUE
kFalseStr = D_STR_FALSE

kRepeatStr = D_STR_REPEAT
kCodeStr = D_STR_CODE
kBitsStr = D_STR_BITS
