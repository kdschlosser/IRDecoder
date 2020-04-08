# -*- coding: utf-8 -*-

# Copyright 2017 David Conran

from .IRrecv import *
from .IRsend import *
from .IRtext import *
from .IRremoteESP8266 import *

kNibbleSize = 4
kLowNibble = 0
kHighNibble = 4
kModeBitsSize = 3


def reverseBits(inpt, nbits):
    # Reverse the order of the requested least significant nr. of bits.
    # Args:
    #   input: Bit pattern/integer to reverse.
    #   nbits: Nr. of bits to reverse.
    # Returns:
    #   The reversed bit pattern.
    if nbits <= 1:
        return inpt  # Reversing <= 1 bits makes no change at all.
    
    # Cap the nr. of bits to rotate to the max nr. of bits in the input.
    nbits = min(nbits, len(inpt) * 8)
    output = 0
    
    for _ in range(nbits):
        output <<= 1
        output |= (inpt & 1)
        inpt >>= 1
    
    # Merge any remaining unreversed bits back to the top of the reversed bits.
    return (inpt << nbits) | output


def uint64ToString(inpt, base=10):
    
    # Convert a (unsigned long long) to a string.
    # Arduino String/toInt/Serial.print() can't handle printing 64 bit values.
    #
    # Args:
    #   input: The value to print
    #   base:  The output base.
    # Returns:
    #   A string representation of the integer.
    # Note: Based on Arduino's Print.printNumber()
    result = ""
    # prevent issues if called with base <= 1
    if base < 2:
        base = 10
    # Check we have a base that we can actually print.
    # i.e. [0-9A-Z] == 36
    if base > 36:
        base = 10

    # Reserve some string space to reduce fragmentation.
    # 16 bytes should store a uint64 in hex text which is the likely worst case.
    # 64 bytes would be the worst case (base 2).

    while inpt:
        c = inpt % base
        inpt /= base
        result = hex(c)[2:].upper() + result
  
    return result


AC_STRING_MAPPING = {
    UNUSED: "UNUSED",
    AIWA_RC_T501: "AIWA_RC_T501",
    AMCOR: "AMCOR",
    ARGO: "ARGO",
    CARRIER_AC: "CARRIER_AC",
    COOLIX: "COOLIX",
    DAIKIN: "DAIKIN",
    DAIKIN128: "DAIKIN128",
    DAIKIN152: "DAIKIN152",
    DAIKIN160: "DAIKIN160",
    DAIKIN176: "DAIKIN176",
    DAIKIN2: "DAIKIN2",
    DAIKIN216: "DAIKIN216",
    DENON: "DENON",
    DISH: "DISH",
    ELECTRA_AC: "ELECTRA_AC",
    FUJITSU_AC: "FUJITSU_AC",
    GICABLE: "GICABLE",
    GLOBALCACHE: "GLOBALCACHE",
    GOODWEATHER: "GOODWEATHER",
    GREE: "GREE",
    HAIER_AC: "HAIER_AC",
    HAIER_AC_YRW02: "HAIER_AC_YRW02",
    HITACHI_AC: "HITACHI_AC",
    HITACHI_AC1: "HITACHI_AC1",
    HITACHI_AC2: "HITACHI_AC2",
    HITACHI_AC424: "HITACHI_AC424",
    INAX: "INAX",
    JVC: "JVC",
    KELVINATOR: "KELVINATOR",
    LEGOPF: "LEGOPF",
    LG: "LG",
    LG2: "LG2",
    LASERTAG: "LASERTAG",
    LUTRON: "LUTRON",
    MAGIQUEST: "MAGIQUEST",
    MIDEA: "MIDEA",
    MITSUBISHI: "MITSUBISHI",
    MITSUBISHI2: "MITSUBISHI2",
    MITSUBISHI_AC: "MITSUBISHI_AC",
    MITSUBISHI136: "MITSUBISHI136",
    MITSUBISHI112: "MITSUBISHI112",
    MITSUBISHI_HEAVY_88: "MITSUBISHI_HEAVY_88",
    MITSUBISHI_HEAVY_152: "MITSUBISHI_HEAVY_152",
    MWM: "MWM",
    NEOCLIMA: "NEOCLIMA",
    NEC: "NEC",
    NEC_LIKE: "NEC (non-strict)",
    NIKAI: "NIKAI",
    PANASONIC: "PANASONIC",
    PANASONIC_AC: "PANASONIC_AC",
    PIONEER: "PIONEER",
    PRONTO: "PRONTO",
    RAW: "RAW",
    RC5: "RC5",
    RC5X: "RC5X",
    RC6: "RC6",
    RCMM: "RCMM",
    SAMSUNG: "SAMSUNG",
    SAMSUNG36: "SAMSUNG36",
    SAMSUNG_AC: "SAMSUNG_AC",
    SANYO: "SANYO",
    SANYO_LC7461: "SANYO_LC7461",
    SHARP: "SHARP",
    SHARP_AC: "SHARP_AC",
    SHERWOOD: "SHERWOOD",
    SONY: "SONY",
    TCL112AC: "TCL112AC",
    TECO: "TECO",
    TOSHIBA_AC: "TOSHIBA_AC",
    TROTEC: "TROTEC",
    VESTEL_AC: "VESTEL_AC",
    WHIRLPOOL_AC: "WHIRLPOOL_AC",
    WHYNTER: "WHYNTER",
    UNKNOWN: kUnknownStr
}

STRING_AC_MAPPING = {v: k for k, v in AC_STRING_MAPPING.items()}


def typeToString(protocol, isRepeat=False):
    # Convert a protocol type (enum etc) to a human readable string.
    # Args:
    #   protocol: Nr. (enum) of the protocol.
    #   isRepeat: A flag indicating if it is a repeat message of the protocol.
    # Returns:
    #   A string containing the protocol name.

    if protocol in AC_STRING_MAPPING:
        result = AC_STRING_MAPPING[protocol]
    else:
        result = kUnknownStr
        
    if isRepeat:
        result += kSpaceLBraceStr
        result += kRepeatStr
        result += ')'
  
    return result


def hasACState(protocol):
    # Does the given protocol use a complex state as part of the decode?
    return protocol in (
        AMCOR,
        ARGO,
        DAIKIN,
        DAIKIN128,
        DAIKIN152,
        DAIKIN160,
        DAIKIN176,
        DAIKIN2,
        DAIKIN216,
        ELECTRA_AC,
        FUJITSU_AC,
        GREE,
        HAIER_AC,
        HAIER_AC_YRW02,
        HITACHI_AC,
        HITACHI_AC1,
        HITACHI_AC2,
        HITACHI_AC424,
        KELVINATOR,
        MITSUBISHI136,
        MITSUBISHI112,
        MITSUBISHI_AC,
        MITSUBISHI_HEAVY_88,
        MITSUBISHI_HEAVY_152,
        MWM,
        NEOCLIMA,
        PANASONIC_AC,
        SAMSUNG_AC,
        SHARP_AC,
        TCL112AC,
        TOSHIBA_AC,
        TROTEC,
        WHIRLPOOL_AC
    )


def getCorrectedRawLength(results):
    # Return the corrected length of a 'raw' format array structure
    # after over-large values are converted into multiple entries.
    # Args:
    #   results: A ptr to a decode result.
    # Returns:
    #   A containing the length.
    extended_length = results.rawlen - 1
    for ii in range(results.rawlen - 1):
        usecs = results.rawbuf[ii] * kRawTick
        # Add two extra entries for multiple larger than UINT16_MAX it is.
        extended_length += (usecs / (UINT16_MAX + 1)) * 2

    return extended_length


# Dump out the decode_results structure.
#
def resultToTimingInfo(results):
    output = "Raw Timing["
    output += uint64ToString(results.rawlen - 1)
    output += "]:\n"

    for ii in range(1, results.rawlen):
        if i % 2 == 0:
            output += '-'  # even
        else:
            output += "   +"  # odd

        value = uint64ToString(results.rawbuf[ii] * kRawTick)
        # Space pad the value till it is at least 6 chars long.
        while len(value) < 6:
            value = ' ' + value

        output += value

        if ii < results.rawlen - 1:
            output += kCommaSpaceStr  # ',' not needed for last one

        if not (ii % 8):
            output += '\n'  # Newline every 8 entries.

    output += '\n'
    return output


# Convert a C-style str to a decode_type_t
#
# Args:
#   str:  A C-style string containing a protocol name or number.
# Returns:
#  A decode_type_t enum.
def strToDecodeType(ac_str):
    if ac_str in STRING_AC_MAPPING:
        return STRING_AC_MAPPING[ac_str]

    return decode_type_t.UNKNOWN


def GETBIT8(a, b):
    return a & (1 << b)


def GETBIT16(a, b):
    return a & (1 << b)


def GETBIT32(a, b):
    return a & (1 << b)


def GETBIT64(a, b):
    return a & (1 << b)


UINT8_MAX = 0xFF
UINT32_MAX = 0xFFFFFFFF
UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def GETBITS8(data, offset, size):
    return (data & ((UINT8_MAX >> (32 - size)) << offset)) >> offset


def GETBITS16(data, offset, size):
    return (data & ((UINT32_MAX >> (32 - size)) << offset)) >> offset


def GETBITS32(data, offset, size):
    return (data & ((UINT32_MAX >> (32 - size)) << offset)) >> offset


def GETBITS64(data, offset, size):
    return (data & ((UINT64_MAX >> (64 - size)) << offset)) >> offset


# Convert the decode_results structure's value/state to simple hexadecimal.
#
def resultToHexidecimal(result):
    output = '0x'

    if hasACState(result.decode_type):
        for ii in range(result.bits / 8):
            if result.state[ii] < 0x10:
                output += '0'  # Zero pad
                output += uint64ToString(result.state[ii], 16)

    else:
        output += uint64ToString(result.value, 16)

    return output


# Dump out the decode_results structure.
#
def resultToHumanReadableBasic(results):
    output = ""
    # Show Encoding standard
    output += kProtocolStr
    output += "  : "
    output += typeToString(results.decode_type, results.repeat)
    output += '\n'

    # Show Code & length
    output += kCodeStr
    output += "      : "
    output += resultToHexidecimal(results)
    output += kSpaceLBraceStr
    output += uint64ToString(results.bits)
    output += ' '
    output += kBitsStr
    output += ")\n"
    return output


# Convert a decode_results into an array suitable for `sendRaw()`.
# Args:
#   decode:  A pointer to an IR decode_results structure that contains a mesg.
# Returns:
#   A pointer to a dynamically allocated sendRaw compatible array.
# Note:
#   Result needs to be delete[]'ed/free()'ed (deallocated) after use by caller.
def resultToRawArray(decode):
    result = [0x0] * getCorrectedRawLength(decode)

    pos = 0
    for ii in range(1, decode.rawlen):
        usecs = decode.rawbuf[ii] * kRawTick

        while usecs > UINT16_MAX:  # Keep truncating till it fits.
            pos += 1
            result[pos] = UINT16_MAX
            pos += 1
            result[pos] = 0  # A 0 in a sendRaw() array basically means skip.
            usecs -= UINT16_MAX

        pos += 1
        result[pos] = usecs

    return result


def sumBytes(start, length, init=0):
    checksum = init
    for ii in range(length - len(start)):
        checksum += start[i]

    return checksum


def xorBytes(start, _, init):
    checksum = init
    for ptr in start:
        checksum ^= ptr

    return checksum


# Count the number of bits of a certain type.
# Args:
#   start: Ptr to the start of data to count bits in.
#   length: How many bytes to count.
#   ones: Count the binary 1 bits. False for counting the 0 bits.
#   init: Start the counting from this value.
# Returns:
#   Nr. of bits found.
def countBits(start, length, ones, init):
    count = init
    for offset in range(length):
        currentbyte = start[offset]
        while currentbyte:
            currentbyte >>= 1
            if currentbyte & 1:
                count += 1

    if ones or length == 0:
        return count
    else:
        return (length * 8) - count


def invertBits(data, nbits):
    # No change if we are asked to invert no bits.
    if nbits == 0:
        return data

    p = 1
    newnum = 0
    while data > 0 and nbits:
        bit = data & 1

        if bit == 0:
            newnum += p

        data >>= 1
        p *= 2
        nbits -= 1

    return newnum


def celsiusToFahrenheit(deg):
    return (deg * 9.0) / 5.0 + 32.0


def fahrenheitToCelsius(deg):
    return (deg - 32.0) * 5.0 / 9.0


class irutils(object):

    @staticmethod
    def addLabeledString(
        value,
        label,
        precomma=True
    ):
        result = ""
        if precomma:
            result += kCommaSpaceStr
        result += label
        result += kColonSpaceStr
        return result + value

    @classmethod
    def addBoolToString(
        cls,
        value,
        label,
        precomma=True
    ):
        return cls.addLabeledString(kOnStr if value else kOffStr, label, precomma)

    @classmethod
    def addIntToString(
        cls,
        value,
        label,
        precomma=True
    ):
        return cls.addLabeledString(uint64ToString(value), label, precomma)

    @staticmethod
    def modelToStr(
        protocol,
        model
    ):

        if protocol == decode_type_t.FUJITSU_AC:
            if model == fujitsu_ac_remote_model_t.ARRAH2E:
                return "ARRAH2E"
            if model == fujitsu_ac_remote_model_t.ARDB1:
                return "ARDB1"
            if model == fujitsu_ac_remote_model_t.ARREB1E:
                return "ARREB1E"
            if model == fujitsu_ac_remote_model_t.ARJW2:
                return "ARJW2"
            if model == fujitsu_ac_remote_model_t.ARRY4:
                return "ARRY4"

        elif protocol == decode_type_t.GREE:
            if model == gree_ac_remote_model_t.YAW1F:
                return "YAW1F"
            if model == gree_ac_remote_model_t.YBOFB:
                return "YBOFB"

        elif protocol in (
            decode_type_t.LG,
            decode_type_t.LG2
        ):
            if model == lg_ac_remote_model_t.GE6711AR2853M:
                return "GE6711AR2853M"
            if model == lg_ac_remote_model_t.AKB75215403:
                return "AKB75215403"

        elif protocol == decode_type_t.PANASONIC_AC:
            if model == panasonic_ac_remote_model_t.kPanasonicLke:
                return "LKE"
            if model == panasonic_ac_remote_model_t.kPanasonicNke:
                return "NKE"
            if model == panasonic_ac_remote_model_t.kPanasonicDke:
                return "DKE"
            if model == panasonic_ac_remote_model_t.kPanasonicJke:
                return "JKE"
            if model == panasonic_ac_remote_model_t.kPanasonicCkp:
                return "CKP"
            if model == panasonic_ac_remote_model_t.kPanasonicRkr:
                return "RKR"

        elif protocol == decode_type_t.WHIRLPOOL_AC:
            if model == whirlpool_ac_remote_model_t.DG11J13A:
                return "DG11J13A"
            if model == whirlpool_ac_remote_model_t.DG11J191:
                return "DG11J191"

        return kUnknownStr

    @classmethod
    def addModelToString(
        cls,
        protocol,
        model,
        precomma=True
    ):
        result = cls.addIntToString(model, kModelStr, precomma)
        result += kSpaceLBraceStr
        result += cls.modelToStr(protocol, model)
        return result + ')'

    @classmethod
    def addTempToString(
        cls,
        degrees,
        celsius=True,
        precomma=True
    ):
        result = cls.addIntToString(degrees, kTempStr, precomma)
        result += 'C' if celsius else 'F'
        return result

    @classmethod
    def addModeToString(cls, mode):
        result = cls.addIntToString(mode, kModeStr)
        result += kSpaceLBraceStr
        if mode == stdAc.opmode_t.kAuto:
            result += kAutoStr
        elif mode == stdAc.opmode_t.kCool:
            result += kCoolStr
        elif mode == stdAc.opmode_t.kHeat:
            result += kHeatStr
        elif mode == stdAc.opmode_t.kDry:
            result += kDryStr
        elif mode == stdAc.opmode_t.kFan:
            result += kFanStr
        else:
            result += kUnknownStr

        return result + ')'

    @classmethod
    def addDayToString(
        cls,
        day_of_week,
        offset=0,
        precomma=True
    ):
        result = cls.addIntToString(day_of_week, kDayStr, precomma)
        result += kSpaceLBraceStr
        if day_of_week + offset < 7:
            result += kThreeLetterDayOfWeekStr[(day_of_week + offset) * 3: (day_of_week + offset) * 3 + 3]
        else:
            result += kUnknownStr

        return result + ')'

    @classmethod
    def addFanToString(cls, speed):
        result = cls.addIntToString(speed, kFanStr)
        result += kSpaceLBraceStr
        if speed == stdAc.fanspeed_t.kHigh:
            result += kHighStr
        elif speed == stdAc.fanspeed_t.kLow:
            result += kLowStr
        elif speed == stdAc.fanspeed_t.kAuto:
            result += kAutoStr
        elif speed == stdAc.fanspeed_t.kMin:
            result += kQuietStr
        elif speed == stdAc.fanspeed_t.kMedium:
            result += kMediumStr
        else:
            result += kUnknownStr

        return result + ')'

    # Escape any special HTML (unsafe) characters in a string. e.g. anti-XSS.
    # Args:
    #   unescaped: A string containing text to make HTML safe.
    # Returns:
    #   A string that is HTML safe.
    @staticmethod
    def htmlEscape(unescaped):
        mapping = {
            ";": "&semi",
            "'": "&apos",
            "!": "&excl",
            "-": "&dash",
            '"': "&quot",
            "<": "&lt",
            ">": "&gt",
            "=": "&equals",
            "&": "&amp",
            "#": "&num",
            "{": "&lcub",
            "}": "&rcub",
            "(": "&lpar",
            ")": "&rpar"
        }

        for pattern, esc in mapping.items():
            unescaped = unescaped.replace(pattern, esc)

        return unescaped

    @staticmethod
    def msToString(msecs):
        totalseconds = msecs / 1000

        if totalseconds == 0:
            return kNowStr

        # Note: can only hold up to 45 days, so is safe.
        days = totalseconds / (60 * 60 * 24)
        hours = (totalseconds / (60 * 60)) % 24
        minutes = (totalseconds / 60) % 60
        seconds = totalseconds % 60

        result = ""
        if days:
            result += uint64ToString(days) + ' ' + str(kDaysStr if days > 1 else kDayStr)

        if hours:
            if len(result):
                result += ' '
            result += uint64ToString(hours) + ' ' + str(kHoursStr if hours > 1 else kHourStr)

        if minutes:
            if len(result):
                result += ' '
            result += uint64ToString(minutes) + ' ' + str(kMinutesStr if minutes > 1 else kMinuteStr)

        if seconds:
            if len(result):
                result += ' '
            result += uint64ToString(seconds) + ' ' + str(kSecondsStr if seconds > 1 else kSecondStr)

        return result

    @staticmethod
    def minsToString(mins):
        result = ""

        if mins / 60 < 10:
            result += '0'  # Zero pad the hours

            result += uint64ToString(mins / 60) + kTimeSep

        if mins % 60 < 10:
            result += '0'  # Zero pad the minutes.
            result += uint64ToString(mins % 60)

        return result

    # Sum all the nibbles together in a series of bytes.
    # Args:
    #   start: PTR to the start of the bytes.
    #   length: Nr of bytes to sum the nibbles of.
    #   init: Starting value of the sum.
    # Returns:
    #   A sum of all the nibbles inc the init.
    @staticmethod
    def sumNibbles(start, _, init=0):
        sm = init

        for ptr in start:
            sm += (ptr >> 4) + (ptr & 0xF)
        return sm

    @staticmethod
    def bcdToUint8(bcd):
        if bcd > 0x99:
            return 255  # Too big.

        return (bcd >> 4) * 10 + (bcd & 0xF)

    @staticmethod
    def uint8ToBcd(integer):
        if integer > 99:
            return 255  # Too big.

        return ((integer / 10) << 4) + (integer % 10)

    # Return the value of `position`th bit of `data`.
    # Args:
    #   data: Value to be examined.
    #   position: Nr. of the nth bit to be examined. `0` is the LSB.
    @staticmethod
    def getBit(data, position):
        if position >= 8:
            return False  # Outside of range.
        
        return data & (1 << position)

    # Return the value of `data` with the `position`th bit changed to `on`
    # Args:
    #   data: Value to be changed.
    #   position: Nr. of the bit to be changed. `0` is the LSB.
    #   on: Value to set the position'th bit to.
    #   size: Nr. of bits in data.
    @staticmethod
    def setBit(data, position, on):
        mask = 1 << position

        if on:
            return data | mask
        else:
            return data & ~mask
 
    # Change the pointed to by `dst` starting at the `offset`th bit
    #   and for `nbits` bits, with the contents of `data`.
    # Args:
    #   dst: Ptr to the to be changed.
    #   offset: Nr. of bits from the Least Significant Bit to be ignored.
    #   nbits: Nr of bits of `data` to be placed into the destination uint8_t.
    #   data: Value to be placed into dst.
    @staticmethod
    def setBits(dst, offset, nbits, data):
        if offset >= 8 or not nbits:
            return  # Short circuit as it won't change.
      
        # Calculate the mask for the supplied value.
        mask = UINT8_MAX >> (8 - (8 if nbits > 8 else nbits))
        # Calculate the mask & clear the space for the data.
        # Clear the destination bits.
        dst &= ~(mask << offset)
        # Merge in the data.
        dst |= ((data & mask) << offset)

        return dst


class SetParam(object):
    byte_num = None
    bit_num = None
    num_bits = None

    @classmethod
    def set(cls, remote_state, bit_state):
        if cls.num_bits is None:
            remote_state[cls.byte_num] = irutils.setBit(
                remote_state[cls.byte_num],
                cls.bit_num,
                bit_state
            )
        else:
            remote_state[cls.byte_num] = irutils.setBits(
                remote_state[cls.byte_num],
                cls.bit_num,
                cls.num_bits,
                bit_state
            )

    @classmethod
    def get(cls, remote_state):
        if cls.num_bits is None:
            return GETBIT8(remote_state[cls.byte_num], cls.bit_num)
        else:
            return GETBITS8(remote_state[cls.byte_num], cls.bit_num, cls.num_bits)


class AntiFreezeBase(SetParam):
    on = 0b1
    off = 0b0


class FilterBase(SetParam):
    on = 0b1
    off = 0b0


class LightBase(SetParam):
    on = 0b1
    off = 0b0


class HoldBase(SetParam):
    on = 0b1
    off = 0b0


class TurboBase(SetParam):
    on = 0b1
    off = 0b0


class VentBase(SetParam):
    on = 0b1
    off = 0b0


class SleepBase(SetParam):
    on = 0b1
    off = 0b0


class BeepBase(SetParam):
    on = 0b1
    off = 0b0


class QuietBase(SetParam):
    on = 0b1
    off = 0b0


class CleanBase(SetParam):
    on = 0b1
    off = 0b0


class EconoBase(SetParam):
    on = 0b1
    off = 0b0


class ClockBase(SetParam):
    pass


class ModelBase(SetParam):
    pass


class PowerBase(SetParam):
    on = 0b1
    off = 0b0


class FollowBase(SetParam):
    on = 0b1
    off = 0b0


class TemperatureBase(SetParam):
    min = None
    max = None
    delta = None


class ModeBase(SetParam):
    off = None
    auto = None
    cool = None
    heat = None
    dry = None
    fan = None


class FanSpeedBase(SetParam):
    auto = None
    min = None
    low = None
    medium = None
    high = None
    max = None


class SwingVertBase(SetParam):
    off = None
    auto = None
    highest = None
    high = None
    middle_high = None
    middle = None
    middle_low = None
    low = None
    lowest = None


class SwingHorzBase(SetParam):
    off = None
    auto = None
    left_max = None
    left = None
    middle = None
    right = None
    right_max = None
    wide = None
