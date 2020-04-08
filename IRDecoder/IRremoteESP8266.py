# -*- coding: utf-8 -*-
# ***************************************************
# * IRremote for ESP8266
# *
# * Based on the IRremote library for Arduino by Ken Shirriff
# * Version 0.11 August, 2009
# * Copyright 2009 Ken Shirriff
# * For details, see http://arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
# *
# * Edited by Mitra to add new controller SANYO
# *
# * Interrupt code based on NECIRrcv by Joe Knapp
# * http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1210243556
# * Also influenced by http://zovirl.com/2008/11/12/building-a-universal-remote-with-an-arduino/
# *
# * JVC and Panasonic protocol added by Kristian Lauszus (Thanks to zenwheel and other people at the original blog post)
# * LG added by Darryl Smith (based on the JVC protocol)
# * Whynter A/C ARC-110WD added by Francesco Meschia
# * Coolix A/C / heatpump added by (send) bakrus & (decode) crankyoldgit
# * Denon: sendDenon, decodeDenon added by Massimiliano Pinto
#          (from https://github.com/z3t0/Arduino-IRremote/blob/master/ir_Denon.cpp)
# * Kelvinator A/C and Sherwood added by crankyoldgit
# * Mitsubishi (TV) sending added by crankyoldgit
# * Pronto code sending added by crankyoldgit
# * Mitsubishi & Toshiba A/C added by crankyoldgit
# *     (derived from https://github.com/r45635/HVAC-IR-Control)
# * DISH decode by marcosamarinho
# * Gree Heatpump sending added by Ville Skyttä (scop)
# *     (derived from https://github.com/ToniA/arduino-heatpumpir/blob/master/GreeHeatpumpIR.cpp)
# * Updated by markszabo (https://github.com/crankyoldgit/IRremoteESP8266) for sending IR code on ESP8266
# * Updated by Sebastien Warin (http://sebastien.warin.fr) for receiving IR code on ESP8266
# *
# * Updated by sillyfrog for Daikin, adopted from
# * (https://github.com/mharizanov/Daikin-AC-remote-control-over-the-Internet/)
# * Fujitsu A/C code added by jonnygraham
# * Trotec AC code by stufisher
# * Carrier & Haier AC code by crankyoldgit
# * Vestel AC code by Erdem U. Altınyurt
# * Teco AC code by Fabien Valthier (hcoohb)
# * Mitsubishi 112 AC Code by kuchel77
# *
# *  GPL license, all text above must be included in any redistribution
# ****************************************************/

# Library Version
_IRREMOTEESP8266_VERSION_ = "2.7.2"


# *
# * Always add to the end of the list and should never remove entries
# * or change order. Projects may save the type number for later usage
# * so numbering should always stay the same.
# */
class decode_type_t(object):
    UNKNOWN = -1
    UNUSED = 0
    RC5 = 1
    RC6 = 2
    NEC = 3
    SONY = 4
    PANASONIC = 5
    JVC = 6
    SAMSUNG = 7
    WHYNTER = 8
    AIWA_RC_T501 = 9
    LG = 10
    SANYO = 11
    MITSUBISHI = 12
    DISH = 13
    SHARP = 14
    COOLIX = 15
    DAIKIN = 16
    DENON = 17
    KELVINATOR = 18
    SHERWOOD = 19
    MITSUBISHI_AC = 20
    RCMM = 21
    SANYO_LC7461 = 22
    RC5X = 23
    GREE = 24
    PRONTO = 25
    NEC_LIKE = 26
    ARGO = 27
    TROTEC = 28
    NIKAI = 29
    RAW = 30
    GLOBALCACHE = 31
    TOSHIBA_AC = 32
    FUJITSU_AC = 33
    MIDEA = 34
    MAGIQUEST = 35
    LASERTAG = 36
    CARRIER_AC = 37
    HAIER_AC = 38
    MITSUBISHI2 = 39
    HITACHI_AC = 40
    HITACHI_AC1 = 41
    HITACHI_AC2 = 42
    GICABLE = 43
    HAIER_AC_YRW02 = 44
    WHIRLPOOL_AC = 45
    SAMSUNG_AC = 46
    LUTRON = 47
    ELECTRA_AC = 48
    PANASONIC_AC = 49
    PIONEER = 50
    LG2 = 51
    MWM = 52
    DAIKIN2 = 53
    VESTEL_AC = 54
    TECO = 55
    SAMSUNG36 = 56
    TCL112AC = 57
    LEGOPF = 58
    MITSUBISHI_HEAVY_88 = 59
    MITSUBISHI_HEAVY_152 = 60
    DAIKIN216 = 61
    SHARP_AC = 62
    GOODWEATHER = 63
    INAX = 64
    DAIKIN160 = 65
    NEOCLIMA = 66
    DAIKIN176 = 67
    DAIKIN128 = 68
    AMCOR = 69
    DAIKIN152 = 70
    MITSUBISHI136 = 71
    MITSUBISHI112 = 72
    HITACHI_AC424 = 73
    # Add new entries before this one, and update it to point to the last entry.
    kLastDecodeType = HITACHI_AC424


UNKNOWN = decode_type_t.UNKNOWN
UNUSED = decode_type_t.UNUSED
RC5 = decode_type_t.RC5
RC6 = decode_type_t.RC6
NEC = decode_type_t.NEC
SONY = decode_type_t.SONY
PANASONIC = decode_type_t.PANASONIC
JVC = decode_type_t.JVC
SAMSUNG = decode_type_t.SAMSUNG
WHYNTER = decode_type_t.WHYNTER
AIWA_RC_T501 = decode_type_t.AIWA_RC_T501
LG = decode_type_t.LG
SANYO = decode_type_t.SANYO
MITSUBISHI = decode_type_t.MITSUBISHI
DISH = decode_type_t.DISH
SHARP = decode_type_t.SHARP
COOLIX = decode_type_t.COOLIX
DAIKIN = decode_type_t.DAIKIN
DENON = decode_type_t.DENON
KELVINATOR = decode_type_t.KELVINATOR
SHERWOOD = decode_type_t.SHERWOOD
MITSUBISHI_AC = decode_type_t.MITSUBISHI_AC
RCMM = decode_type_t.RCMM
SANYO_LC7461 = decode_type_t.SANYO_LC7461
RC5X = decode_type_t.RC5X
GREE = decode_type_t.GREE
PRONTO = decode_type_t.PRONTO
NEC_LIKE = decode_type_t.NEC_LIKE
ARGO = decode_type_t.ARGO
TROTEC = decode_type_t.TROTEC
NIKAI = decode_type_t.NIKAI
RAW = decode_type_t.RAW
GLOBALCACHE = decode_type_t.GLOBALCACHE
TOSHIBA_AC = decode_type_t.TOSHIBA_AC
FUJITSU_AC = decode_type_t.FUJITSU_AC
MIDEA = decode_type_t.MIDEA
MAGIQUEST = decode_type_t.MAGIQUEST
LASERTAG = decode_type_t.LASERTAG
CARRIER_AC = decode_type_t.CARRIER_AC
HAIER_AC = decode_type_t.HAIER_AC
MITSUBISHI2 = decode_type_t.MITSUBISHI2
HITACHI_AC = decode_type_t.HITACHI_AC
HITACHI_AC1 = decode_type_t.HITACHI_AC1
HITACHI_AC2 = decode_type_t.HITACHI_AC2
GICABLE = decode_type_t.GICABLE
HAIER_AC_YRW02 = decode_type_t.HAIER_AC_YRW02
WHIRLPOOL_AC = decode_type_t.WHIRLPOOL_AC
SAMSUNG_AC = decode_type_t.SAMSUNG_AC
LUTRON = decode_type_t.LUTRON
ELECTRA_AC = decode_type_t.ELECTRA_AC
PANASONIC_AC = decode_type_t.PANASONIC_AC
PIONEER = decode_type_t.PIONEER
LG2 = decode_type_t.LG2
MWM = decode_type_t.MWM
DAIKIN2 = decode_type_t.DAIKIN2
VESTEL_AC = decode_type_t.VESTEL_AC
TECO = decode_type_t.TECO
SAMSUNG36 = decode_type_t.SAMSUNG36
TCL112AC = decode_type_t.TCL112AC
LEGOPF = decode_type_t.LEGOPF
MITSUBISHI_HEAVY_88 = decode_type_t.MITSUBISHI_HEAVY_88
MITSUBISHI_HEAVY_152 = decode_type_t.MITSUBISHI_HEAVY_152
DAIKIN216 = decode_type_t.DAIKIN216
SHARP_AC = decode_type_t.SHARP_AC
GOODWEATHER = decode_type_t.GOODWEATHER
INAX = decode_type_t.INAX
DAIKIN160 = decode_type_t.DAIKIN160
NEOCLIMA = decode_type_t.NEOCLIMA
DAIKIN176 = decode_type_t.DAIKIN176
DAIKIN128 = decode_type_t.DAIKIN128
AMCOR = decode_type_t.AMCOR
DAIKIN152 = decode_type_t.DAIKIN152
MITSUBISHI136 = decode_type_t.MITSUBISHI136
MITSUBISHI112 = decode_type_t.MITSUBISHI112
HITACHI_AC424 = decode_type_t.HITACHI_AC424

# Message lengths & required repeat values
kNoRepeat = 0
kSingleRepeat = 1

kAiwaRcT501Bits = 15
kAiwaRcT501MinRepeats = kSingleRepeat
kAlokaBits = 32
kAmcorStateLength = 8
kAmcorBits = kAmcorStateLength * 8
kAmcorDefaultRepeat = kSingleRepeat
kArgoStateLength = 12
kArgoBits = kArgoStateLength * 8
kArgoDefaultRepeat = kNoRepeat
kCoolixBits = 24
kCoolixDefaultRepeat = kSingleRepeat
kCarrierAcBits = 32
kCarrierAcMinRepeat = kNoRepeat
kDaikinStateLength = 35
kDaikinBits = kDaikinStateLength * 8
kDaikinStateLengthShort = kDaikinStateLength - 8
kDaikinBitsShort = kDaikinStateLengthShort * 8
kDaikinDefaultRepeat = kNoRepeat
kDaikin2StateLength = 39
kDaikin2Bits = kDaikin2StateLength * 8
kDaikin2DefaultRepeat = kNoRepeat
kDaikin160StateLength = 20
kDaikin160Bits = kDaikin160StateLength * 8
kDaikin160DefaultRepeat = kNoRepeat
kDaikin128StateLength = 16
kDaikin128Bits = kDaikin128StateLength * 8
kDaikin128DefaultRepeat = kNoRepeat
kDaikin152StateLength = 19
kDaikin152Bits = kDaikin152StateLength * 8
kDaikin152DefaultRepeat = kNoRepeat
kDaikin176StateLength = 22
kDaikin176Bits = kDaikin176StateLength * 8
kDaikin176DefaultRepeat = kNoRepeat
kDaikin216StateLength = 27
kDaikin216Bits = kDaikin216StateLength * 8
kDaikin216DefaultRepeat = kNoRepeat
kDenonBits = 15
kDenon48Bits = 48
kDenonLegacyBits = 14
kDishBits = 16
kDishMinRepeat = 3
kElectraAcStateLength = 13
kElectraAcBits = kElectraAcStateLength * 8
kElectraAcMinRepeat = kNoRepeat
kFujitsuAcMinRepeat = kNoRepeat
kFujitsuAcStateLength = 16
kFujitsuAcStateLengthShort = 7
kFujitsuAcBits = kFujitsuAcStateLength * 8
kFujitsuAcMinBits = (kFujitsuAcStateLengthShort - 1) * 8
kGicableBits = 16
kGicableMinRepeat = kSingleRepeat
kGoodweatherBits = 48
kGoodweatherMinRepeat = kNoRepeat
kGreeStateLength = 8
kGreeBits = kGreeStateLength * 8
kGreeDefaultRepeat = kNoRepeat
kHaierACStateLength = 9
kHaierACBits = kHaierACStateLength * 8
kHaierAcDefaultRepeat = kNoRepeat
kHaierACYRW02StateLength = 14
kHaierACYRW02Bits = kHaierACYRW02StateLength * 8
kHaierAcYrw02DefaultRepeat = kNoRepeat
kHitachiAcStateLength = 28
kHitachiAcBits = kHitachiAcStateLength * 8
kHitachiAcDefaultRepeat = kNoRepeat
kHitachiAc1StateLength = 13
kHitachiAc1Bits = kHitachiAc1StateLength * 8
kHitachiAc2StateLength = 53
kHitachiAc2Bits = kHitachiAc2StateLength * 8
kHitachiAc424StateLength = 53
kHitachiAc424Bits = kHitachiAc424StateLength * 8
kInaxBits = 24
kInaxMinRepeat = kSingleRepeat
kJvcBits = 16
kKelvinatorStateLength = 16
kKelvinatorBits = kKelvinatorStateLength * 8
kKelvinatorDefaultRepeat = kNoRepeat
kLasertagBits = 13
kLasertagMinRepeat = kNoRepeat
kLegoPfBits = 16
kLegoPfMinRepeat = kNoRepeat
kLgBits = 28
kLg32Bits = 32
kLgDefaultRepeat = kNoRepeat
kLutronBits = 35
kMagiquestBits = 56
kMideaBits = 48
kMideaMinRepeat = kNoRepeat
kMitsubishiBits = 16
# TODO(anyone): Verify that the Mitsubishi repeat is really needed.
#               Based on marcosamarinho's code.
kMitsubishiMinRepeat = kSingleRepeat
kMitsubishiACStateLength = 18
kMitsubishiACBits = kMitsubishiACStateLength * 8
kMitsubishiACMinRepeat = kSingleRepeat
kMitsubishi136StateLength = 17
kMitsubishi136Bits = kMitsubishi136StateLength * 8
kMitsubishi136MinRepeat = kNoRepeat
kMitsubishi112StateLength = 14
kMitsubishi112Bits = kMitsubishi112StateLength * 8
kMitsubishi112MinRepeat = kNoRepeat
kMitsubishiHeavy88StateLength = 11
kMitsubishiHeavy88Bits = kMitsubishiHeavy88StateLength * 8
kMitsubishiHeavy88MinRepeat = kNoRepeat
kMitsubishiHeavy152StateLength = 19
kMitsubishiHeavy152Bits = kMitsubishiHeavy152StateLength * 8
kMitsubishiHeavy152MinRepeat = kNoRepeat
kNikaiBits = 24
kNECBits = 32
kNeoclimaStateLength = 12
kNeoclimaBits = kNeoclimaStateLength * 8
kNeoclimaMinRepeat = kNoRepeat
kPanasonicBits = 48
kPanasonicManufacturer = 0x4004
kPanasonicAcStateLength = 27
kPanasonicAcStateShortLength = 16
kPanasonicAcBits = kPanasonicAcStateLength * 8
kPanasonicAcShortBits = kPanasonicAcStateShortLength * 8
kPanasonicAcDefaultRepeat = kNoRepeat
kPioneerBits = 64
kProntoMinLength = 6
kRC5RawBits = 14
kRC5Bits = kRC5RawBits - 2
kRC5XBits = kRC5RawBits - 1
kRC6Mode0Bits = 20  # Excludes the 'start' bit.
kRC6_36Bits = 36  # Excludes the 'start' bit.
kRCMMBits = 24
kSamsungBits = 32
kSamsung36Bits = 36
kSamsungAcStateLength = 14
kSamsungAcBits = kSamsungAcStateLength * 8
kSamsungAcExtendedStateLength = 21
kSamsungAcExtendedBits = kSamsungAcExtendedStateLength * 8
kSamsungAcDefaultRepeat = kNoRepeat
kSanyoSA8650BBits = 12
kSanyoLC7461AddressBits = 13
kSanyoLC7461CommandBits = 8
kSanyoLC7461Bits = (kSanyoLC7461AddressBits + kSanyoLC7461CommandBits) * 2
kSharpAddressBits = 5
kSharpCommandBits = 8
kSharpBits = kSharpAddressBits + kSharpCommandBits + 2  # 15
kSharpAcStateLength = 13
kSharpAcBits = kSharpAcStateLength * 8  # 104
kSharpAcDefaultRepeat = kNoRepeat
kSherwoodBits = kNECBits
kSherwoodMinRepeat = kSingleRepeat
kSony12Bits = 12
kSony15Bits = 15
kSony20Bits = 20
kSonyMinBits = 12
kSonyMinRepeat = 2
kTcl112AcStateLength = 14
kTcl112AcBits = kTcl112AcStateLength * 8
kTcl112AcDefaultRepeat = kNoRepeat
kTecoBits = 35
kTecoDefaultRepeat = kNoRepeat
kToshibaACStateLength = 9
kToshibaACBits = kToshibaACStateLength * 8
kToshibaACMinRepeat = kSingleRepeat
kTrotecStateLength = 9
kTrotecBits = kTrotecStateLength * 8
kTrotecDefaultRepeat = kNoRepeat
kWhirlpoolAcStateLength = 21
kWhirlpoolAcBits = kWhirlpoolAcStateLength * 8
kWhirlpoolAcDefaultRepeat = kNoRepeat
kWhynterBits = 32
kVestelAcBits = 56


# Legacy defines. (Deprecated)
AIWA_RC_T501_BITS = kAiwaRcT501Bits
ARGO_COMMAND_LENGTH = kArgoStateLength
COOLIX_BITS = kCoolixBits
CARRIER_AC_BITS = kCarrierAcBits
DAIKIN_COMMAND_LENGTH = kDaikinStateLength
DENON_BITS = kDenonBits
DENON_48_BITS = kDenon48Bits
DENON_LEGACY_BITS = kDenonLegacyBits
DISH_BITS = kDishBits
FUJITSU_AC_MIN_REPEAT = kFujitsuAcMinRepeat
FUJITSU_AC_STATE_LENGTH = kFujitsuAcStateLength
FUJITSU_AC_STATE_LENGTH_SHORT = kFujitsuAcStateLengthShort
FUJITSU_AC_BITS = kFujitsuAcBits
FUJITSU_AC_MIN_BITS = kFujitsuAcMinBits
GICABLE_BITS = kGicableBits
GREE_STATE_LENGTH = kGreeStateLength
HAIER_AC_STATE_LENGTH = kHaierACStateLength
HAIER_AC_YRW02_STATE_LENGTH = kHaierACYRW02StateLength
HITACHI_AC_STATE_LENGTH = kHitachiAcStateLength
HITACHI_AC_BITS = kHitachiAcBits
HITACHI_AC1_STATE_LENGTH = kHitachiAc1StateLength
HITACHI_AC1_BITS = kHitachiAc1Bits
HITACHI_AC2_STATE_LENGTH = kHitachiAc2StateLength
HITACHI_AC2_BITS = kHitachiAc2Bits
JVC_BITS = kJvcBits
KELVINATOR_STATE_LENGTH = kKelvinatorStateLength
LASERTAG_BITS = kLasertagBits
LG_BITS = kLgBits
LG32_BITS = kLg32Bits
MAGIQUEST_BITS = kMagiquestBits
MIDEA_BITS = kMideaBits
MITSUBISHI_BITS = kMitsubishiBits
MITSUBISHI_AC_STATE_LENGTH = kMitsubishiACStateLength
NEC_BITS = kNECBits
NIKAI_BITS = kNikaiBits
PANASONIC_BITS = kPanasonicBits
RC5_BITS = kRC5Bits
RC5X_BITS = kRC5XBits
RC6_MODE0_BITS = kRC6Mode0Bits
RC6_36_BITS = kRC6_36Bits
RCMM_BITS = kRCMMBits
SANYO_LC7461_BITS = kSanyoLC7461Bits
SAMSUNG_BITS = kSamsungBits
SANYO_SA8650B_BITS = kSanyoSA8650BBits
SHARP_BITS = kSharpBits
SHERWOOD_BITS = kSherwoodBits
SONY_12_BITS = kSony12Bits
SONY_15_BITS = kSony15Bits
SONY_20_BITS = kSony20Bits
TOSHIBA_AC_STATE_LENGTH = kToshibaACStateLength
TROTEC_COMMAND_LENGTH = kTrotecStateLength
WHYNTER_BITS = kWhynterBits
