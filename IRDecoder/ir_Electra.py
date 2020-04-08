# -*- coding: utf-8 -*-
# Copyright 2018, 2019 David Conran
# Copyright 2020 Kevin Schlosser

# Supports:
#   Brand: AUX,  Model: KFR-35GW/BpNFW=3 A/C
#   Brand: AUX,  Model: YKR-T/011 remote
# Ref:
#  https:#github.com/ToniA/arduino-heatpumpir/blob/master/AUXHeatpumpIR.cpp

# Electra A/C added by crankyoldgit
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/527
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/642
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/778
#   https:#github.com/ToniA/arduino-heatpumpir/blob/master/AUXHeatpumpIR.cpp

from .IRrecv import *
from .IRutils import *
from .IRsend import *
from .IRremoteESP8266 import *
from .protocol_base import ACProtocolBase

# Constants
kElectraAcHdrMark = 9166
kElectraAcBitMark = 646
kElectraAcHdrSpace = 4470
kElectraAcOneSpace = 1647
kElectraAcZeroSpace = 547
kElectraAcMessageGap = kDefaultMessageGap  # Just a guess.


# state[1]
class Temperature(TemperatureBase):
    # Temp  0b11111000
    byte_num = 1
    bit_num = 3
    num_bits = 5
    min = 16
    max = 32
    delta = 8


class SwingVert(SwingVertBase):
    # SwingVMask = 0b00000111
    byte_num = 1
    bit_num = 0
    num_bits = 3
    auto = 0b000
    off = 0b111


# state[2]
class SwingHorz(SwingHorzBase):
    # SwingHMask = 0b11100000
    byte_num = 2
    bit_num = 5
    num_bits = 3
    auto = 0b000
    off = 0b111


# state[4]
class FanSpeed(FanSpeedBase):
    # FanMask =    0b11100000
    byte_num = 4
    bit_num = 5
    num_bits = 3
    auto = 0b101
    low = 0b011
    medium = 0b010
    high = 0b001


# state[6]
class Mode(ModeBase):
    # Mode 0b11100000
    byte_num = 6
    bit_num = 5
    num_bits = 3

    auto = 0b000
    cool = 0b001
    dry = 0b010
    heat = 0b100
    fan = 0b110


# state[9]
class Power(PowerBase):
    byte_num = 9
    bit_num = 5


class IRElectraAc(ACProtocolBase):
    _packet_len = kElectraAcStateLength
    _reset = [0x00] * kElectraAcStateLength
    _reset[0] = 0xC3
    _reset[11] = 0x08
    _min_repeat = kElectraAcMinRepeat
    _power = Power
    _fan_speed = FanSpeed
    _temperature = Temperature
    _mode = Mode
    _swing_horz = SwingHorz
    _swing_vert = SwingVert

    def send(self, repeat=_min_repeat):
        self.checksum()
        self._irsend.sendElectraAC(self.remote_state, kElectraAcStateLength, repeat)


# Send a Electra message
#
# Args:
#   data:   Contents of the message to be sent. (Guessing MSBF order)
#   nbits:  Nr. of bits of data to be sent. Typically kElectraAcBits.
#   repeat: Nr. of additional times the message is to be sent.
#
# Status: Alpha / Needs testing against a real device.
def sendElectraAC(self, data, nbytes, repeat):
    for r in range(repeat + 1):
        self.send_generic(
            kElectraAcHdrMark,
            kElectraAcHdrSpace,
            kElectraAcBitMark,
            kElectraAcOneSpace,
            kElectraAcBitMark,
            kElectraAcZeroSpace,
            kElectraAcBitMark,
            kElectraAcMessageGap,
            data,
            nbytes,
            38000,  # Complete guess of the modulation frequency.
            False,  # Send data in LSB order per byte
            0,
            50
        )


IRsend.sendElectraAC = sendElectraAC


# Decode the supplied Electra A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kElectraAcBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE / Known working.
def decodeElectraAC(self, results, nbits, strict):
    if strict and nbits != kElectraAcBits:
        return False  # Not strictly a ELECTRA_AC message.

    offset = kStartOffset
    # Match Header + Data + Footer
    if not self.match_generic(
        results.rawbuf + offset,
        results.state,
        results.rawlen - offset,
        nbits,
        kElectraAcHdrMark,
        kElectraAcHdrSpace,
        kElectraAcBitMark,
        kElectraAcOneSpace,
        kElectraAcBitMark,
        kElectraAcZeroSpace,
        kElectraAcBitMark,
        kElectraAcMessageGap,
        True,
        self._tolerance,
        0,
        False
    ):
        return False

    # Compliance
    # Verify the checksum.
    if strict and not IRElectraAc.valid_checksum(results.state):
        return False

    # Success
    results.decode_type = decode_type_t.ELECTRA_AC
    results.bits = nbits
    # No need to record the state as we stored it as we decoded it.
    # As we use result.state, we don't record value, address, or command as it
    # is a union data type.
    return True


IRrecv.decodeElectraAC = decodeElectraAC
