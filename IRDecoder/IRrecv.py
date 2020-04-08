# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2015 Mark Szabo
# Copyright 2015 Sebastien Warin
# Copyright 2017 David Conran

from .IRremoteESP8266 import *
from .IRutils import *

ONCE = 0

# Constants
kHeader = 2        # Usual nr. of header entries.
kFooter = 2        # Usual nr. of footer (stop bits) entries.
kStartOffset = 1   # Usual rawbuf entry to start from.


def MS_TO_USEC(x):
    return x * 1000  # Convert milli-Seconds to micro-Seconds.


# Marks tend to be 100us too long, and spaces 100us too short
# when received due to sensor lag.
kMarkExcess = 50
kRawBuf = 100  # Default length of raw capture buffer
kRepeat = UINT64_MAX
# Default min size of reported UNKNOWN messages.
kUnknownThreshold = 6

# receiver states
kIdleState = 2
kMarkState = 3
kSpaceState = 4
kStopState = 5
kTolerance = 25   # default percent tolerance in measurements.
kUseDefTol = 255  # Indicate to use the class default tolerance.
kRawTick = 2     # Capture tick to uSec factor.
RAWTICK = kRawTick  # Deprecated. For legacy user code support only.
# How long (ms) before we give up wait for more data?
# Don't exceed kMaxTimeoutMs without a good reason.
# That is the capture buffers maximum value size. (UINT16_MAX / kRawTick)
# Typically messages/protocols tend to repeat around the 100ms timeframe,
# thus we should timeout before that to give us some time to try to decode
# before we need to start capturing a possible new message.
# Typically 15ms suits most applications. However, some protocols demand a
# higher value. e.g. 90ms for XMP-1 and some aircon units.
kTimeoutMs = 15  # In MilliSeconds.
TIMEOUT_MS = kTimeoutMs   # For legacy documentation.
kMaxTimeoutMs = kRawTick * (UINT16_MAX / MS_TO_USEC(1))

# Use FNV hash algorithm: http:#isthe.com/chongo/tech/comp/fnv/#FNV-param
kFnvPrime32 = 16777619
kFnvBasis32 = 2166136261

# Which of the ESP32 timers to use by default. (0-3)
kDefaultESP32Timer = 3

# Hitachi AC is the current largest state size.
kStateSizeMax = kHitachiAc2StateLength


# Types
# information for the interrupt handler
class irparams_t(object):
    def __init__(self):
        self.recvpin = None   # pin for IR data from detector
        self.rcvstate = None  # state machine
        self.timer = None    # state timer, counts 50uS ticks.
        self.bufsize = None  # max. nr. of entries in the capture buffer.
        self.rawbuf = None  # raw data
        # is used for rawlen as it saves 3 bytes of iram in the interrupt
        # handler. Don't ask why, I don't know. It just does.
        self.rawlen = None   # counter of entries in rawbuf.
        self.overflow = None  # Buffer overflow indicator.
        self.timeout = None   # Nr. of milliSeconds before we give up.


# results from a data match
class match_result_t(object):
  
    def __init__(self):
        self.success = False   # Was the match successful?
        self.data = None  # The data found.
        self.used = None  # How many buffer positions were used.


# Classes

# Results returned from the decoder
class decode_results(object):
  
    def __init__(self):
        self.decode_type = None  # NEC, SONY, RC5, UNKNOWN
        # value, address, & command are all mutually exclusive with state.
        # i.e. They MUST NOT be used at the same time as state, so we can use a union
        # structure to save us a handful of valuable bytes of memory.
        self.value = None    # Decoded value
        self.address = None  # Decoded device address.
        self.command = None  # Decoded command.
        self.state = [0x0] * kStateSizeMax  # Multi-byte results.
        self.bits = None              # Number of bits in decoded value
        self.rawbuf = None  # Raw intervals in .5 us ticks
        self.rawlen = None            # Number of records in rawbuf.
        self.overflow = False
        self.repeat = False  # Is the result a repeat code?


# main class for receiving IR
class IRrecv(object):

    def __init__(self, recvpin, bufsize=kRawBuf, timeout=kTimeoutMs, save_buffer=False):  # Constructor 
        # Class constructor
        # Args:
        #   recvpin: GPIO pin the IR receiver module's data pin is connected to.
        #   bufsize: Nr. of entries to have in the capture buffer. (Default: kRawBuf)
        #   timeout: Nr. of milli-Seconds of no signal before we stop capturing data.
        #            (Default: kTimeoutMs)
        #   save_buffer: Use a second (save) buffer to decode from. (Default: False)
        #   timer_num: Which ESP32 timer number to use? ESP32 only, otherwise unused.
        #              (Range: 0-3. Default: kDefaultESP32Timer)
        # Returns:
        #   An IRrecv class object.
        
        self.irparams = irparams_t()
        self.irparams.recvpin = recvpin
        self.irparams.bufsize = bufsize
        # Ensure we are going to be able to store all possible values in the
        # capture buffer.
        self.irparams.timeout = min(timeout, kMaxTimeoutMs)
        self.irparams.rawbuf = [0x0] * bufsize

        # If we have been asked to use a save buffer (for decoding), then create one.
        if save_buffer:
            self.irparams_save = irparams_t()
            self.irparams_save.rawbuf = [0x0] * bufsize
            # Check we allocated the memory successfully.
        else:
            self.irparams_save = None

        self._unknown_threshold = kUnknownThreshold
        self._tolerance = kTolerance

    def setTolerance(self, percent=kTolerance):
        # Set the base tolerance percentage for matching incoming IR messages.
        self._tolerance = min(percent, 100)
    
    def getTolerance(self):
        # Get the base tolerance percentage for matching incoming IR messages.
        return self._tolerance
    
    def decode(self, results, save=None):
        # Decodes the received IR message.
        # If the interrupt state is saved, we will immediately resume waiting
        # for the next IR message to avoid missing messages.
        # Note: There is a trade-off here. Saving the state means less time lost until
        # we can receiving the next message vs. using more RAM. Choose appropriately.
        #
        # Args:
        #   results:  A pointer to where the decoded IR message will be stored.
        #   save:  A pointer to an irparams_t instance in which to save
        #          the interrupt's memory/state. NULL means don't save it.
        # Returns:
        #   A boolean indicating if an IR message is ready or not.
        # Proceed only if an IR message been received.
        
        if self.irparams.rcvstate != kStopState:
            return False

        # Clear the entry we are currently pointing to when we got the timeout.
        # i.e. Stopped collecting IR data.
        # It's junk as we never wrote an entry to it and can only confuse decoding.
        # This is done here rather than logically the best place in read_timeout()
        # as it saves a few bytes of ICACHE_RAM as that routine is bound to an
        # interrupt. decode() is not stored in ICACHE_RAM.
        # Another better option would be to zero the entire irparams.rawbuf[] on
        # resume() but that is a much more expensive operation compare to this.
        self.irparams.rawbuf[self.irparams.rawlen] = 0

        # If we were requested to use a save buffer previously, do so.
        if save is None:
            save = self.irparams_save

        if not save.rawbuf:
            # We haven't been asked to copy it so use the existing memory.
            results.rawbuf = self.irparams.rawbuf
            results.rawlen = self.irparams.rawlen
            results.overflow = self.irparams.overflow
        else:
            self.copyIrParams(self.irparams, save)  # Duplicate the interrupt's memory.

            # Point the results at the saved copy.
            results.rawbuf = save.rawbuf
            results.rawlen = save.rawlen
            results.overflow = save.overflow

        # Reset any previously partially processed results.
        results.decode_type = UNKNOWN
        results.bits = 0
        results.value = 0
        results.address = 0
        results.command = 0
        results.repeat = False

        print("Attempting Aiwa RC T501 decode")
        # Try decodeAiwaRCT501() before decodeSanyoLC7461() & decodeNEC()
        # because the protocols are similar. This protocol is more specific than
        # those ones, so should got before them.
        if self.decodeAiwaRCT501(results):
            return True

        print("Attempting Sanyo LC7461 decode")
        # Try decodeSanyoLC7461() before decodeNEC() because the protocols are
        # similar in timings & structure, but the Sanyo one is much longer than the
        # NEC protocol (42 vs 32 bits) so this one should be tried first to try to
        # reduce False detection as a NEC packet.
        if self.decodeSanyoLC7461(results):
            return True

        print("Attempting Carrier AC decode")
        # Try decodeCarrierAC() before decodeNEC() because the protocols are
        # similar in timings & structure, but the Carrier one is much longer than the
        # NEC protocol (3x32 bits vs 1x32 bits) so this one should be tried first to
        # try to reduce False detection as a NEC packet.
        if self.decodeCarrierAC(results):
            return True

        print("Attempting Pioneer decode")
        # Try decodePioneer() before decodeNEC() because the protocols are
        # similar in timings & structure, but the Pioneer one is much longer than the
        # NEC protocol (2x32 bits vs 1x32 bits) so this one should be tried first to
        # try to reduce False detection as a NEC packet.
        if self.decodePioneer(results):
            return True

        print("Attempting NEC decode")
        if self.decodeNEC(results):
            return True

        print("Attempting Sony decode")
        if self.decodeSony(results):
            return True

        print("Attempting Mitsubishi decode")
        if self.decodeMitsubishi(results):
            return True

        print("Attempting Mitsubishi AC decode")
        if self.decodeMitsubishiAC(results):
            return True
        print("Attempting Mitsubishi2 decode")

        if self.decodeMitsubishi2(results):
            return True

        print("Attempting RC5 decode")
        if self.decodeRC5(results):
            return True

        print("Attempting RC6 decode")
        if self.decodeRC6(results):
            return True

        print("Attempting RC-MM decode")
        if self.decodeRCMM(results):
            return True

        # Fujitsu A/C needs to precede Panasonic and Denon as it has a short
        # message which looks exactly the same as a Panasonic/Denon message.
        print("Attempting Fujitsu A/C decode")
        if self.decodeFujitsuAC(results):
            return True

        # Denon needs to precede Panasonic as it is a special case of Panasonic.
        print("Attempting Denon decode")
        if (
            self.decodeDenon(results, kDenon48Bits) or
            self.decodeDenon(results, kDenonBits) or
            self.decodeDenon(results, kDenonLegacyBits)
        ):
            return True

        print("Attempting Panasonic decode")
        if self.decodePanasonic(results):
            return True

        print("Attempting LG (28-bit) decode")
        if self.decodeLG(results, kLgBits, True):
            return True

        print("Attempting LG (32-bit) decode")
        # LG32 should be tried before Samsung
        if self.decodeLG(results, kLg32Bits, True):
            return True

        # Note: Needs to happen before JVC decode, because it looks similar except
        #       with a required NEC-like repeat code.
        print("Attempting GICable decode")
        if self.decodeGICable(results):
            return True

        print("Attempting JVC decode")
        if self.decodeJVC(results):
            return True

        print("Attempting SAMSUNG decode")
        if self.decodeSAMSUNG(results):
            return True

        print("Attempting Samsung36 decode")
        if self.decodeSamsung36(results):
            return True

        print("Attempting Whynter decode")
        if self.decodeWhynter(results):
            return True

        print("Attempting DISH decode")
        if self.decodeDISH(results):
            return True

        print("Attempting Sharp decode")
        if self.decodeSharp(results):
            return True

        print("Attempting Coolix decode")
        if self.decodeCOOLIX(results):
            return True

        print("Attempting Nikai decode")
        if self.decodeNikai(results):
            return True

        # Kelvinator based-devices use a similar code to Gree ones, to avoid False
        # matches this needs to happen before decodeGree().
        print("Attempting Kelvinator decode")
        if self.decodeKelvinator(results):
            return True

        print("Attempting Daikin decode")
        if self.decodeDaikin(results):
            return True

        print("Attempting Daikin2 decode")
        if self.decodeDaikin2(results):
            return True

        print("Attempting Daikin216 decode")
        if self.decodeDaikin216(results):
            return True

        print("Attempting Toshiba AC decode")
        if self.decodeToshibaAC(results):
            return True

        print("Attempting Midea decode")
        if self.decodeMidea(results):
            return True

        print("Attempting Magiquest decode")
        if self.decodeMagiQuest(results):
            return True

        # NOTE: Disabled due to poor quality.
        # The Sanyo S866500B decoder is very poor quality & depricated.
        # *IF* you are going to enable it, do it near last to avoid False positive
        # matches.
        print("Attempting Sanyo SA8650B decode")
        if self.decodeSanyo(results):
            return True

        # Some devices send NEC-like codes that don't follow the True NEC spec.
        # This should detect those. e.g. Apple TV remote etc.
        # This needs to be done after all other codes that use strict and some
        # other protocols that are NEC-like as well, as turning off strict may
        # cause this to match other valid protocols.
        print("Attempting NEC (non-strict) decode")
        if self.decodeNEC(results, kNECBits, False):
            results.decode_type = NEC_LIKE
            return True

        print("Attempting Lasertag decode")
        if self.decodeLasertag(results):
            return True

        # Gree based-devices use a similar code to Kelvinator ones, to avoid False
        # matches this needs to happen after decodeKelvinator().
        print("Attempting Gree decode")
        if self.decodeGree(results):
            return True

        print("Attempting Haier AC decode")
        if self.decodeHaierAC(results):
            return True

        print("Attempting Haier AC YR-W02 decode")
        if self.decodeHaierACYRW02(results):
            return True

        # HitachiAc424 should be checked before HitachiAC & HitachiAC2
        print("Attempting Hitachi AC 424 decode")
        if self.decodeHitachiAc424(results, kHitachiAc424Bits):
            return True

        # HitachiAC2 should be checked before HitachiAC
        print("Attempting Hitachi AC2 decode")
        if self.decodeHitachiAC(results, kHitachiAc2Bits):
            return True

        print("Attempting Hitachi AC decode")
        if self.decodeHitachiAC(results, kHitachiAcBits):
            return True

        print("Attempting Hitachi AC1 decode")
        if self.decodeHitachiAC(results, kHitachiAc1Bits):
            return True

        print("Attempting Whirlpool AC decode")
        if self.decodeWhirlpoolAC(results):
            return True

        print("Attempting Samsung AC (extended) decode")
        # Check the extended size first, as it should fail fast due to longer length.
        if self.decodeSamsungAC(results, kSamsungAcExtendedBits, False):
            return True

        # Now check for the more common length.
        print("Attempting Samsung AC decode")
        if self.decodeSamsungAC(results, kSamsungAcBits):
            return True

        print("Attempting Electra AC decode")
        if self.decodeElectraAC(results):
            return True

        print("Attempting Panasonic AC decode")
        if self.decodePanasonicAC(results):
            return True

        print("Attempting Panasonic AC short decode")
        if self.decodePanasonicAC(results, kPanasonicAcShortBits):
            return True

        print("Attempting Lutron decode")
        if self.decodeLutron(results):
            return True

        print("Attempting MWM decode")
        if self.decodeMWM(results):
            return True

        print("Attempting Vestel AC decode")
        if self.decodeVestelAc(results):
            return True

        # Mitsubish112 and Tcl112 share the same decoder.
        print("Attempting Mitsubishi112/TCL112AC decode")
        if self.decodeMitsubishi112(results):
            return True

        print("Attempting Teco decode")
        if self.decodeTeco(results):
            return True

        print("Attempting LEGOPF decode")
        if self.decodeLegoPf(results):
            return True

        print("Attempting MITSUBISHIHEAVY (152 bit) decode")
        if self.decodeMitsubishiHeavy(results, kMitsubishiHeavy152Bits):
            return True

        print("Attempting MITSUBISHIHEAVY (88 bit) decode")
        if self.decodeMitsubishiHeavy(results, kMitsubishiHeavy88Bits):
            return True

        print("Attempting Argo decode")
        if self.decodeArgo(results):
            return True

        print("Attempting SHARP_AC decode")
        if self.decodeSharpAc(results):
            return True

        print("Attempting GOODWEATHER decode")
        if self.decodeGoodweather(results):
            return True

        print("Attempting Inax decode")
        if self.decodeInax(results):
            return True

        print("Attempting Trotec decode")
        if self.decodeTrotec(results):
            return True

        print("Attempting Daikin160 decode")
        if self.decodeDaikin160(results):
            return True

        print("Attempting Neoclima decode")
        if self.decodeNeoclima(results):
            return True

        print("Attempting Daikin176 decode")
        if self.decodeDaikin176(results):
            return True

        print("Attempting Daikin128 decode")
        if self.decodeDaikin128(results):
            return True

        print("Attempting Amcor decode")
        if self.decodeAmcor(results):
            return True

        print("Attempting Daikin152 decode")
        if self.decodeDaikin152(results):
            return True

        print("Attempting Mitsubishi136 decode")
        if self.decodeMitsubishi136(results):
            return True

        # Typically new protocols are added above this line.
        # decodeHash returns a hash on any input.
        # Thus, it needs to be last in the list.
        # If you add any decodes, add them before this.
        if self.decodeHash(results):
            return True

        # Throw away and start over
        return False

    def getBufSize(self):
        # Obtain the maximum number of entries possible in the capture buffer.
        # i.e. It's size.
        return self.irparams.bufsize
    
    def setUnknownThreshold(self, length):
        # Set the minimum length we will consider for reporting UNKNOWN message types.
        self._unknown_threshold = length
    
    def match(self, measured, desired, tolerance=kUseDefTol, delta=0):
        # Check if we match a pulse(measured) with the desired within
        # +/-tolerance percent and/or +/- a fixed delta range.
        #
        # Args:
        #   measured:  The recorded period of the signal pulse.
        #   desired:  The expected period (in useconds) we are matching against.
        #   tolerance:  A percentage expressed as an integer. e.g. 10 is 10%.
        #   delta:  A non-scaling (+/-) error margin (in useconds).
        #
        # Returns:
        #   Boolean: True if it matches, False if it doesn't.
        measured *= kRawTick  # Convert to uSecs.
        print("Matching: ")
        print(self.ticksLow(desired, tolerance, delta))
        print(" <= ")
        print(measured)
        print(" <= ")
        print(self.ticksHigh(desired, tolerance, delta))
    
    def matchMark(self, measured, desired, tolerance=kUseDefTol, excess=kMarkExcess):
        # Check if we match a mark signal(measured) with the desired within
        # +/-tolerance percent, after an expected is excess is added.
        #
        # Args:
        #   measured:  The recorded period of the signal pulse.
        #   desired:  The expected period (in useconds) we are matching against.
        #   tolerance:  A percentage expressed as an integer. e.g. 10 is 10%.
        #   excess:  Nr. of useconds.
        #
        # Returns:
        #   Boolean: True if it matches, False if it doesn't.
        print("Matching MARK ")
        print(measured * kRawTick)
        print(" vs ")
        print(desired)
        print(" + ")
        print(excess)
        print(". ")
        return self.match(measured, desired + excess, tolerance)
    
    def matchSpace(self, measured, desired, tolerance=kUseDefTol, excess=kMarkExcess):
        # Check if we match a space signal(measured) with the desired within
        # +/-tolerance percent, after an expected is excess is removed.
        #
        # Args:
        #   measured:  The recorded period of the signal pulse.
        #   desired:  The expected period (in useconds) we are matching against.
        #   tolerance:  A percentage expressed as an integer. e.g. 10 is 10%.
        #   excess:  Nr. of useconds.
        #
        # Returns:
        #   Boolean: True if it matches, False if it doesn't.
        print("Matching SPACE ")
        print(measured * kRawTick)
        print(" vs ")
        print(desired)
        print(" - ")
        print(excess)
        print(". ")
        return self.match(measured, desired - excess, tolerance)

    # These are called by decode
    def _validTolerance(self, percentage):
        # Convert the tolerance percentage into something valid.
        return self._tolerance if percentage > 100 else percentage

    @staticmethod
    def copyIrParams(src, dst):
        # Make a copy of the interrupt state & buffer data.
        # Needed because irparams is marked as volatile, thus memcpy() isn't allowed.
        # Only call this when you know the interrupt handlers won't modify anything.
        # i.e. In kStopState.
        #
        # Args:
        #   src: Pointer to an irparams_t structure to copy from.
        #   dst: Pointer to an irparams_t structure to copy to.

        # Save the pointer to the destination's rawbuf so we don't lose it as
        # the for-loop/copy after this will overwrite it with src's rawbuf pointer.
        # This isn't immediately obvious due to typecasting/different variable names.
        dst_rawbuf_ptr = dst.rawbuf[:]

        # Restore the buffer pointer
        dst.rawbuf = dst_rawbuf_ptr

        # Copy the rawbuf
        for i in range(dst.bufsize):
            dst.rawbuf[i] = src.rawbuf[i]

    @staticmethod
    def compare(oldval, newval):
        # * -----------------------------------------------------------------------
        # * hashdecode - decode an arbitrary IR code.
        # * Instead of decoding using a standard encoding scheme
        # * (e.g. Sony, NEC, RC5), the code is hashed to a 32-bit value.
        # *
        # * The algorithm: look at the sequence of MARK signals, and see if each one
        # * is shorter (0), the same length (1), or longer (2) than the previous.
        # * Do the same with the SPACE signals.  Hash the resulting sequence of 0's,
        # * 1's, and 2's to a 32-bit value.  This will give a unique value for each
        # * different code (probably), for most code systems.
        # *
        # * http:#arcfn.com/2010/01/using-arbitrary-remotes-with-arduino.html
        # */
  
        # Compare two tick values, returning 0 if newval is shorter,
        # 1 if newval is equal, and 2 if newval is longer
        # Use a tolerance of 20%
        if newval < oldval * 0.8:
            return 0
        elif oldval < newval * 0.8:
            return 2
        else:
            return 1
      
    def ticksLow(self, usecs, tolerance=kUseDefTol, delta=0):
        # Calculate the lower bound of the nr. of ticks.
        #
        # Args:
        #   usecs:  Nr. of uSeconds.
        #   tolerance:  Percent as an integer. e.g. 10 is 10%
        #   delta:  A non-scaling amount to reduce usecs by.
        # Returns:
        #   Nr. of ticks.
        # max() used to ensure the result can't drop below 0 before the cast.
        return (
            max((usecs * (1.0 - self._validTolerance(tolerance) / 100.0) - delta), 0)
        )

    def ticksHigh(self, usecs, tolerance=kUseDefTol, delta=0):
        # Calculate the upper bound of the nr. of ticks.
        #
        # Args:
        #   usecs:  Nr. of uSeconds.
        #   tolerance:  Percent as an integer. e.g. 10 is 10%
        #   delta:  A non-scaling amount to increase usecs by.
        # Returns:
        #   Nr. of ticks.
        return (
            (usecs * (1.0 + self._validTolerance(tolerance) / 100.0)) + 1 + delta
        )
      
    def matchAtLeast(self, measured, desired, tolerance=kUseDefTol, delta=0):
        # Check if we match a pulse(measured) of at least desired within
        # tolerance percent and/or a fixed delta margin.
        #
        # Args:
        #   measured:  The recorded period of the signal pulse.
        #   desired:  The expected period (in useconds) we are matching against.
        #   tolerance:  A percentage expressed as an integer. e.g. 10 is 10%.
        #   delta:  A non-scaling amount to reduce usecs by.
  
        #
        # Returns:
        #   Boolean: True if it matches, False if it doesn't.
        measured *= kRawTick  # Convert to uSecs.
        print("Matching ATLEAST ")
        print(measured)
        print(" vs ")
        print(desired)
        print(". Matching: ")
        print(measured)
        print(" >= ")
        print(self.ticksLow(min(desired, MS_TO_USEC(self.irparams.timeout)), tolerance, delta))
        print(" [min(")
        print(self.ticksLow(desired, tolerance, delta))
        print(", ")
        print(self.ticksLow(MS_TO_USEC(self.irparams.timeout), tolerance, delta))
        print(")]")

        # We really should never get a value of 0, except as the last value
        # in the buffer. If that is the case, then assume infinity and return True.
        if measured == 0:
            return True

        return measured >= ticksLow(min(desired, MS_TO_USEC(self.irparams.timeout)), tolerance, delta)
    
    def _matchGeneric(
        self,
        data_ptr,
        result_bits_ptr,
        result_bytes_ptr,
        use_bits,
        remaining,
        nbits,
        hdrmark,
        hdrspace,
        onemark,
        onespace,
        zeromark,
        zerospace,
        footermark,
        footerspace,
        atleast=False,
        tolerance=kUseDefTol,
        excess=kMarkExcess,
        MSBfirst=True
    ):

        # Match & decode a generic/typical IR message.
        # The data is stored in result_bits_ptr or result_bytes_ptr depending on flag
        # `use_bits`.
        # Values of 0 for hdrmark, hdrspace, footermark, or footerspace mean skip
        # that requirement.
        #
        # Args:
        #   data_ptr: A pointer to where we are at in the capture buffer.
        #   result_bits_ptr: A pointer to where to start storing the bits we decoded.
        #   result_bytes_ptr: A pointer to where to start storing the bytes we decoded.
        #   use_bits: A flag indicating if we are to decode bits or bytes.
        #   remaining: The size of the capture buffer are remaining.
        #   nbits:        Nr. of data bits we expect.
        #   hdrmark:      Nr. of uSeconds for the expected header mark signal.
        #   hdrspace:     Nr. of uSeconds for the expected header space signal.
        #   onemark:      Nr. of uSeconds in an expected mark signal for a '1' bit.
        #   onespace:     Nr. of uSeconds in an expected space signal for a '1' bit.
        #   zeromark:     Nr. of uSeconds in an expected mark signal for a '0' bit.
        #   zerospace:    Nr. of uSeconds in an expected space signal for a '0' bit.
        #   footermark:   Nr. of uSeconds for the expected footer mark signal.
        #   footerspace:  Nr. of uSeconds for the expected footer space/gap signal.
        #   atleast:      Is the match on the footerspace a matchAtLeast or matchSpace?
        #   tolerance: Percentage error margin to allow. (Def: kUseDefTol)
        #   excess:  Nr. of useconds. (Def: kMarkExcess)
        #   MSBfirst: Bit order to save the data in. (Def: True)
        # Returns:
        #  A uint16_t: If successful, how many buffer entries were used. Otherwise 0.

        # If we are expecting byte sizes, check it's a factor of 8 or fail.
        if not use_bits and nbits % 8 != 0:
            return 0
        # Calculate how much remaining buffer is required.
        min_remaining = nbits * 2

        if hdrmark:
            min_remaining += 1
        if hdrspace:
            min_remaining += 1
        if footermark:
            min_remaining += 1

        # Don't need to extend for footerspace because it could be the end of message

        # Check if there is enough capture buffer to possibly have the message.
        if remaining < min_remaining:
            return 0  # Nope, so abort.
        offset = 0

        # Header
        offset += 1
        if hdrmark and not self.matchMark(data_ptr[offset], hdrmark, tolerance, excess):
            return 0

        offset += 1
        if hdrspace and not self.matchSpace(data_ptr[offset], hdrspace, tolerance, excess):
            return 0

        # Data
        if use_bits:  # Bits.
            result = self.matchData(
                data_ptr[offset],
                nbits,
                onemark,
                onespace,
                zeromark,
                zerospace,
                tolerance,
                excess,
                MSBfirst
            )

            if not result.success:
                return 0

            result_bits_ptr += result.data[:]

            offset += result.used

        else:  # bytes
            data_used = self.matchBytes(
                data_ptr[offset],
                result_bytes_ptr,
                remaining - offset,
                nbits / 8,
                onemark,
                onespace,
                zeromark,
                zerospace,
                tolerance,
                excess,
                MSBfirst
            )

            if not data_used:
                return 0

            offset += data_used

        # Footer
        offset += 1
        if footermark and not self.matchMark(data_ptr[offset], footermark, tolerance, excess):
            return 0

        # If we have something still to match & haven't reached the end of the buffer
        if footerspace and offset < remaining and atleast:
            if not self.matchAtLeast(data_ptr[offset], footerspace, tolerance, excess):
                return 0
            elif not self.matchSpace(data_ptr[offset], footerspace, tolerance, excess):
                return 0

            offset += 1

        return offset
      
    def matchData(
        self,
        data_ptr,
        nbits,
        onemark,
        onespace,
        zeromark,
        zerospace,
        tolerance=kUseDefTol,
        excess=kMarkExcess,
        MSBfirst=True
    ):
        # Match & decode the typical data section of an IR message.
        # The data value is stored in the least significant bits reguardless of the
        # bit ordering requested.
        #
        # Args:
        #   data_ptr: A pointer to where we are at in the capture buffer.
        #   nbits:     Nr. of data bits we expect.
        #   onemark:   Nr. of uSeconds in an expected mark signal for a '1' bit.
        #   onespace:  Nr. of uSeconds in an expected space signal for a '1' bit.
        #   zeromark:  Nr. of uSeconds in an expected mark signal for a '0' bit.
        #   zerospace: Nr. of uSeconds in an expected space signal for a '0' bit.
        #   tolerance: Percentage error margin to allow. (Def: kUseDefTol)
        #   excess:  Nr. of useconds. (Def: kMarkExcess)
        #   MSBfirst: Bit order to save the data in. (Def: True)
        # Returns:
        #  A match_result_t structure containing the success (or not), the data value,
        #  and how many buffer entries were used.

        result = match_result_t()
        result.success = False  # Fail by default.
        result.data = 0
        result.used = 0
        while result.used < nbits * 2:
            # Is the bit a '1'?
            if (
                self.matchMark(data_ptr[0], onemark, tolerance, excess) and
                self.matchSpace(data_ptr[1], onespace, tolerance, excess)
            ):
                result.data = (result.data << 1) | 1

            elif (
                self.matchMark(data_ptr[0], zeromark, tolerance, excess) and
                self.matchSpace(data_ptr[1], zerospace, tolerance, excess)
            ):
                result.data <<= 1  # The bit is a '0'.
            else:
                if not MSBfirst:
                    result.data = self.reverseBits(result.data, result.used / 2)
                    return result  # It's neither, so fail.

            result.used += 2
            data_ptr += 2

        result.success = True
        if not MSBfirst:
            result.data = self.reverseBits(result.data, nbits)

        return result
    
    def matchBytes(
        self,
        data_ptr,
        result_ptr,
        remaining,
        nbytes,
        onemark,
        onespace,
        zeromark,
        zerospace,
        tolerance=kUseDefTol,
        excess=kMarkExcess,
        MSBfirst=True
    ):
        # Match & decode the typical data section of an IR message.
        # The bytes are stored at result_ptr. The first byte in the result equates to
        # the first byte encountered, and so on.
        #
        # Args:
        #   data_ptr: A pointer to where we are at in the capture buffer.
        #   result_ptr: A pointer to where to start storing the bytes we decoded.
        #   remaining: The size of the capture buffer are remaining.
        #   nbytes:    Nr. of data bytes we expect.
        #   onemark:   Nr. of uSeconds in an expected mark signal for a '1' bit.
        #   onespace:  Nr. of uSeconds in an expected space signal for a '1' bit.
        #   zeromark:  Nr. of uSeconds in an expected mark signal for a '0' bit.
        #   zerospace: Nr. of uSeconds in an expected space signal for a '0' bit.
        #   tolerance: Percentage error margin to allow. (Def: kUseDefTol)
        #   excess:  Nr. of useconds. (Def: kMarkExcess)
        #   MSBfirst: Bit order to save the data in. (Def: True)
        # Returns:
        #  A uint16_t: If successful, how many buffer entries were used. Otherwise 0.

        # Check if there is enough capture buffer to possibly have the desired bytes.
        if remaining < nbytes * 8 * 2:
            return 0  # Nope, so abort.
        offset = 0
        for byte_pos in range(nbytes):
            result = self.matchData(
                data_ptr[offset],
                8,
                onemark,
                onespace,
                zeromark,
                zerospace,
                tolerance,
                excess,
                MSBfirst
            )
            if result.success is False:
                return 0  # Fail

            result_ptr[byte_pos] = result.data
            offset += result.used

        return offset
    
    def matchGeneric(
        self,
        data_ptr,
        result_ptr,
        remaining,
        nbits,
        hdrmark,
        hdrspace,
        onemark,
        onespace,
        zeromark,
        zerospace,
        footermark,
        footerspace,
        atleast=False,
        tolerance=kUseDefTol,
        excess=kMarkExcess,
        MSBfirst=True
    ):
        if result_ptr <= 255:
            return self._matchGeneric(
                data_ptr,
                NULL,
                result_ptr,
                False,
                remaining,
                nbits,
                hdrmark,
                hdrspace,
                onemark,
                onespace,
                zeromark,
                zerospace,
                footermark,
                footerspace,
                atleast,
                tolerance,
                excess,
                MSBfirst
            )
        else:
            return self._matchGeneric(
                data_ptr,
                result_ptr,
                NULL,
                True,
                remaining,
                nbits,
                hdrmark,
                hdrspace,
                onemark,
                onespace,
                zeromark,
                zerospace,
                footermark,
                footerspace,
                atleast,
                tolerance,
                excess,
                MSBfirst
            )

    def decodeHash(self, results):
        # * Converts the raw code values into a 32-bit hash code.
        # * Hopefully this code is unique for each button.
        # * This isn't a "real" decoding, just an arbitrary value.
        # */
        # Require at least some samples to prevent triggering on noise
        if results.rawlen < self._unknown_threshold:
            return False

        hsh = kFnvBasis32
        # 'rawlen - 2' to avoid the look ahead from going out of bounds.
        # Should probably be -3 to avoid comparing the trailing space entry,
        # however it is left this way for compatibility with previously captured
        # values.
        for i in range(1, results.rawlen - 2):
            value = self.compare(results.rawbuf[i], results.rawbuf[i + 2])
            # Add value into the hash
            hsh = (hsh * kFnvPrime32) ^ value

        results.value = hsh & 0xFFFFFFFF
        results.bits = results.rawlen / 2
        results.address = 0
        results.command = 0
        results.decode_type = UNKNOWN
        return True
      
    def decodeNEC(self, results, nbits=kNECBits, strict=True):
        from . import ir_NEC
        return ir_NEC.decodeNEC(results, nbits, strict)

    def decodeArgo(self, results, nbits=kArgoBits, strict=True):
        from . import ir_Argo
        return ir_Argo.decodeArgo(results, nbits, strict)

    def decodeSony(self, results, nbits=kSonyMinBits, strict=False):
        from . import ir_Sony
        return ir_Sony.decodeSony(results, nbits, strict)

    def decodeSanyo(self, results, nbits=kSanyoSA8650BBits, strict=False):
        from . import ir_Sanyo
        return ir_Sanyo.decodeSanyo(results, nbits, strict)

    def decodeSanyoLC7461(self, results, nbits=kSanyoLC7461Bits, strict=True):
        from . import ir_Sanyo
        return ir_Sanyo.decodeSanyoLC7461(results, nbits, strict)

    def decodeMitsubishi(self, results, nbits=kMitsubishiBits, strict=True):
        from . import ir_Mitsubishi
        return ir_Mitsubishi.decodeMitsubishi(results, nbits, strict)

    def decodeMitsubishi2(self, results, nbits=kMitsubishiBits, strict=True):
        from . import ir_Mitsubishi
        return ir_Mitsubishi.decodeMitsubishi2(results, nbits, strict)

    def decodeMitsubishiAC(self, results, nbits=kMitsubishiACBits, strict=False):
        from . import ir_Mitsubishi

        return ir_Mitsubishi.decodeMitsubishiAC(results, nbits, strict)

    def decodeMitsubishi136(self, results, nbits=kMitsubishi136Bits, strict=True):
        from . import ir_Mitsubishi

        return ir_Mitsubishi.decodeMitsubishi136(results, nbits, strict)

    def decodeMitsubishi112(self, results, nbits=kMitsubishi112Bits, strict=True):
        from . import ir_Mitsubishi

        return ir_Mitsubishi.decodeMitsubishi112(results, nbits, strict)

    def decodeMitsubishiHeavy(self, results, nbits, strict=True):
        from . import ir_MitsubishiHeavy

        return ir_MitsubishiHeavy.decodeMitsubishiHeavy(results, nbits, strict)

    def getRClevel(self, results, offset, used, bitTime, tolerance=kUseDefTol, excess=kMarkExcess, delta=0, maxwidth=3):
        pass

    def decodeRC5(self, results, nbits=kRC5XBits, strict=True):
        from . import ir_RC5_RC6

        return ir_RC5_RC6.decodeRC5(results, nbits, strict)

    def decodeRC6(self, results, nbits=kRC6Mode0Bits,strict=False):
        from . import ir_RC5_RC6

        return ir_RC5_RC6.decodeRC6(results, nbits, strict)

    def decodeRCMM(self, results, nbits=kRCMMBits, strict=False):
        from . import ir_RCMM

        return ir_RCMM.decodeRCMM(results, nbits, strict)

    def decodePanasonic(self, results, nbits=kPanasonicBits, strict=False, manufacturer=kPanasonicManufacturer):
        from . import ir_Panasonic

        return ir_Panasonic.decodePanasonic(results, nbits, strict, manufacturer)

    def decodeLG(self, results, nbits=kLgBits,strict=False):
        from . import ir_LG

        return ir_LG.decodeLG(results, nbits, strict)

    def decodeInax(self, results, nbits=kInaxBits, strict=True):
        from . import ir_Inax

        return ir_Inax.decodeInax(results, nbits, strict)

    def decodeJVC(self, results, nbits=kJvcBits, strict=True):
        from . import ir_JVC

        return ir_JVC.decodeJVC(results, nbits, strict)

    def decodeSAMSUNG(self, results, nbits=kSamsungBits,strict=True):
        from . import ir_Samsung

        return ir_Samsung.decodeSAMSUNG(results, nbits, strict)

    def decodeSamsung36(self, results, nbits=kSamsung36Bits,strict=True):
        from . import ir_Samsung

        return ir_Samsung.decodeSamsung36(results, nbits, strict)

    def decodeSamsungAC(self, results, nbits=kSamsungAcBits,strict=True):
        from . import ir_Samsung

        return ir_Samsung.decodeSamsungAC(results, nbits, strict)

    def decodeWhynter(self, results, nbits=kWhynterBits, strict=True):
        from . import ir_Whynter

        return ir_Whynter.decodeWhynter(results, nbits, strict)

    def decodeCOOLIX(self, results, nbits=kCoolixBits, strict=True):
        from . import ir_Coolix

        return ir_Coolix.decodeCOOLIX(results, nbits, strict)

    def decodeDenon(self, results, nbits=kDenonBits, strict=True):
        from . import ir_Denon

        return ir_Denon.decodeDenon(results, nbits, strict)

    def decodeDISH(self, results, nbits=kDishBits, strict=True):
        from . import ir_Dish

        return ir_Dish.decodeDISH(results, nbits, strict)

    def decodeSharp(self, results, nbits=kSharpBits, strict=True, expansion=True):
        from . import ir_Sharp

        return ir_Sharp.decodeSharp(results, nbits, strict, expansion)

    def decodeSharpAc(self, results, nbits=kSharpAcBits, strict=True):
        from . import ir_Sharp

        return ir_Sharp.decodeSharpAc(results, nbits, strict)

    def decodeAiwaRCT501(self, results, nbits=kAiwaRcT501Bits, strict=True):
        from . import ir_Aiwa

        return ir_Aiwa.decodeAiwaRCT501(results, nbits, strict)

    def decodeNikai(self, results, nbits=kNikaiBits, strict=True):
        from . import ir_Nikai

        return ir_Nikai.decodeNikai(results, nbits, strict)

    def decodeMagiQuest(self, results, nbits=kMagiquestBits, strict=True):
        from . import ir_MagiQuest

        return ir_MagiQuest.decodeMagiQuest(results, nbits, strict)

    def decodeKelvinator(self, results, nbits=kKelvinatorBits, strict=True):
        from . import ir_Kelvinator

        return ir_Kelvinator.decodeKelvinator(results, nbits, strict)

    def decodeDaikin(self, results, nbits=kDaikinBits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin(results, nbits, strict)

    def decodeDaikin128(self, results, nbits=kDaikin128Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin128(results, nbits, strict)

    def decodeDaikin152(self, results, nbits=kDaikin152Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin152(results, nbits, strict)

    def decodeDaikin160(self, results, nbits=kDaikin160Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin160(results, nbits, strict)

    def decodeDaikin176(self, results, nbits=kDaikin176Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin176(results, nbits, strict)

    def decodeDaikin2(self, results, nbits=kDaikin2Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin2(results, nbits, strict)

    def decodeDaikin216(self, results, nbits=kDaikin216Bits, strict=True):
        from . import ir_Daikin

        return ir_Daikin.decodeDaikin216(results, nbits, strict)

    def decodeToshibaAC(self, results, nbytes=kToshibaACBits, strict=True):
        from . import ir_Toshiba

        return ir_Toshiba.decodeToshibaAC(results, nbytes, strict)

    def decodeTrotec(self, results, nbits=kTrotecBits, strict=True):
        from . import ir_Trotec

        return ir_Trotec.decodeTrotec(results, nbits, strict)

    def decodeMidea(self, results, nbits=kMideaBits, strict=True):
        from . import ir_Midea

        return ir_Midea.decodeMidea(results, nbits, strict)

    def decodeFujitsuAC(self, results, nbits=kFujitsuAcBits, strict=False):
        from . import ir_Fujitsu

        return ir_Fujitsu.decodeFujitsuAC(results, nbits, strict)

    def decodeLasertag(self, results, nbits=kLasertagBits, strict=True):
        from . import ir_Lasertag

        return ir_Lasertag.decodeLasertag(results, nbits, strict)

    def decodeCarrierAC(self, results, nbits=kCarrierAcBits, strict=True):
        from . import ir_Carrier

        return ir_Carrier.decodeCarrierAC(results, nbits, strict)

    def decodeGoodweather(self, results,nbits=kGoodweatherBits, strict=True):
        from . import ir_Goodweather

        return ir_Goodweather.decodeGoodweather(results, nbits, strict)

    def decodeGree(self, results, nbits=kGreeBits, strict=True):
        from . import ir_Gree

        return ir_Gree.decodeGree(results, nbits, strict)

    def decodeHaierAC(self, results, nbits=kHaierACBits, strict=True):
        from . import ir_Haier

        return ir_Haier.decodeHaierAC(results, nbits, strict)

    def decodeHaierACYRW02(self, results, nbits=kHaierACYRW02Bits, strict=True):
        from . import ir_Haier

        return ir_Haier.decodeHaierACYRW02(results, nbits, strict)

    def decodeHitachiAC(self, results, nbits=kHitachiAcBits, strict=True):
        from . import ir_Hitachi

        return ir_Hitachi.decodeHitachiAC(results, nbits, strict)

    def decodeHitachiAC1(self, results, nbits=kHitachiAc1Bits, strict=True):
        from . import ir_Hitachi

        return ir_Hitachi.decodeHitachiAC1(results, nbits, strict)

    def decodeHitachiAc424(self, results, nbits=kHitachiAc424Bits, strict=True):
        from . import ir_Hitachi

        return ir_Hitachi.decodeHitachiAc424(results, nbits, strict)

    def decodeGICable(self, results, nbits=kGicableBits, strict=True):
        from . import ir_GICable

        return ir_GICable.decodeGICable(results, nbits, strict)

    def decodeWhirlpoolAC(self, results, nbits=kWhirlpoolAcBits, strict=True):
        from . import ir_Whirlpool

        return ir_Whirlpool.decodeWhirlpoolAC(results, nbits, strict)

    def decodeLutron(self, results, nbits=kLutronBits, strict=True):
        from . import ir_Lutron

        return ir_Lutron.decodeLutron(results, nbits, strict)

    def decodeElectraAC(self, results, nbits=kElectraAcBits, strict=True):
        from . import ir_Electra

        return ir_Electra.decodeElectraAC(results, nbits, strict)

    def decodePanasonicAC(self, results, nbits=kPanasonicAcBits, strict=True):
        from . import ir_Panasonic

        return ir_Panasonic.decodePanasonicAC(results, nbits, strict)

    def decodePioneer(self, results, nbits=kPioneerBits, strict=True):
        from . import ir_Pioneer

        return ir_Pioneer.decodePioneer(results, nbits, strict)

    def decodeMWM(self, results, nbits=24, strict=True):
        from . import ir_MWM

        return ir_MWM.decodeMWM(results, nbits, strict)

    def decodeVestelAc(self, results, nbits=kVestelAcBits, strict=True):
        from . import ir_Vestel

        return ir_Vestel.decodeVestelAc(results, nbits, strict)

    def decodeTeco(self, results, nbits=kTecoBits, strict=False):
        from . import ir_Teco

        return ir_Teco.decodeTeco(results, nbits, strict)

    def decodeLegoPf(self, results, nbits=kLegoPfBits, strict=True):
        from . import ir_Lego

        return ir_Lego.decodeLegoPf(results, nbits, strict)

    def decodeNeoclima(self, results, nbits=kNeoclimaBits, strict=True):
        from . import ir_Neoclima

        return ir_Neoclima.decodeNeoclima(results, nbits, strict)

    def decodeAmcor(self, results, nbits=kAmcorBits,strict=True):
        from . import ir_Amcor

        return ir_Amcor.decodeAmcor(results, nbits, strict)
