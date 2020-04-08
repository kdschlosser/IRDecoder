# -*- coding: utf-8 -*-

# Copyright 2009 Ken Shirriff
# Copyright 2015 Mark Szabo
# Copyright 2017,2019 David Conran
# Coptright 2020 Kevin Schlosser

# Originally from https:#github.com/shirriff/Arduino-IRremote/
# Updated by markszabo (https:#github.com/crankyoldgit/IRremoteESP8266) for
# sending IR code on ESP8266
# Ported to python

from .IRremoteESP8266 import *
from .IRtimer import *

# Constants
# Offset (in microseconds) to use in Period time calculations to account for
# code excution time in producing the software PWM signal.
UINT16_MAX = 0xFFFF

kPeriodOffset = -5
kDutyDefault = 50  # Percentage
kDutyMax = 100     # Percentage
# delayMicroseconds() is only accurate to 16383us.
# Ref: https:#www.arduino.cc/en/Reference/delayMicroseconds
kMaxAccurateUsecDelay = 16383
#  Usecs to wait between messages we don't know the proper gap time.
kDefaultMessageGap = 100000


class stdAc(object):
    class opmode_t(object):
        kOff = -1
        kAuto = 0
        kCool = 1
        kHeat = 2
        kDry = 3
        kFan = 4
        # Add new entries before this one, and update it to point to the last entry
        kLastOpmodeEnum = kFan

    class fanspeed_t(object):
        kAuto = 0
        kMin = 1
        kLow = 2
        kMedium = 3
        kHigh = 4
        kMax = 5
        # Add new entries before this one, and update it to point to the last entry
        kLastFanspeedEnum = kMax

    class swingv_t(object):
        kOff = -1
        kAuto = 0
        kHighest = 1
        kHigh = 2
        kMiddleHigh = 6
        kMiddle = 3
        kMiddleLow = 7
        kLow = 4
        kLowest = 5
        # Add new entries before this one, and update it to point to the last entry
        kLastSwingvEnum = kMiddleLow

    class swingh_t(object):
        kOff = -1
        kAuto = 0  # a.k.a. On.
        kLeftMax = 1
        kLeft = 2
        kMiddle = 3
        kRight = 4
        kRightMax = 5
        kWide = 6  # a.k.a. left & right at the same time.
        # Add new entries before this one, and update it to point to the last entry
        kLastSwinghEnum = kWide

    # Structure to hold a common A/C state.
    class state_t(object):
        def __init__(self):
            self.protocol = None
            self.model = None
            self.power = False
            self.mode = None
            self.degrees = 0.0
            self.celsius = True
            self.fanspeed = None
            self.swingv = None
            self.swingh = None
            self.quiet = False
            self.turbo = False
            self.econo = False
            self.light = False
            self.filter = False
            self.clean = False
            self.beep = False
            self.sleep = None
            self.clock = None


class fujitsu_ac_remote_model_t(object):
    ARRAH2E = 1  # (1) AR-RAH2E, AR-RAC1E, AR-RAE1E (Default)
    ARDB1 = 2  # (2) AR-DB1, AR-DL10 (AR-DL10 swing doesn't work)
    ARREB1E = 3  # (3) AR-REB1E
    ARJW2 = 4  # (4) AR-JW2  (Same as ARDB1 but with horiz control)
    ARRY4 = 5  # (5) AR-RY4 (Same as AR-RAH2E but with clean & filter)


class gree_ac_remote_model_t(object):
    YAW1F = 1  # (1) Ultimate, EKOKAI, RusClimate (Default)
    YBOFB = 2  # (2) Green, YBOFB2, YAPOF3


class panasonic_ac_remote_model_t(object):
    kPanasonicUnknown = 0
    kPanasonicLke = 1
    kPanasonicNke = 2
    kPanasonicDke = 3  # PKR too.
    kPanasonicJke = 4
    kPanasonicCkp = 5
    kPanasonicRkr = 6


class whirlpool_ac_remote_model_t(object):
    DG11J13A = 1  # DG11J1-04 too
    DG11J191 = 2


class lg_ac_remote_model_t(object):
    GE6711AR2853M = 1  # (1) LG 28-bit Protocol (default)
    AKB75215403 = 2  # (2) LG2 28-bit Protocol


class IRsend(object):
    def __init__(self, ir_pin, inverted=False, use_modulation=True):
        # IRsend ----------------------------------------------------------------------
        # Create an IRsend object.
        #
        # Args:
        #   IRsendPin:  Which GPIO pin to use when sending an IR command.
        #   inverted:   *DANGER* Optional flag to invert the output. (default = False)
        #               e.g. LED is illuminated when GPIO is LOW rather than HIGH.
        #               Setting this to something other than the default could
        #               easily destroy your IR LED if you are overdriving it.
        #               Unless you *REALLY* know what you are doing, don't change this.
        #   use_modulation: Do we do frequency modulation during transmission?
        #                   i.e. If not, assume a 100% duty cycle. Ignore attempts
        #                        to change the duty cycle etc.
        # Returns:
        #   An IRsend object.
        
        self.on_time_period = 0
        self.off_time_period = 0
        self.ir_pin = ir_pin
        self.period_offset = kPeriodOffset
        if inverted:
            self.output_on = 0
            self.output_off = 1
        else:
            self.output_on = 1
            self.output_off = 0

        self.modulation = use_modulation
        if self.modulation:
            self._dutycycle = kDutyDefault
        else:
            self._dutycycle = kDutyMax
    
    def begin(self):
        # Enable the pin for output.
        # pinMode(self.ir_pin, OUTPUT)
        self.led_off()  # Ensure the LED is in a known safe state when we start.

    def enable_ir_out(self, freq, duty=kDutyDefault):
        # Set the output frequency modulation and duty cycle.
        #
        # Args:
        #   freq: The freq we want to modulate at. Assumes < 1000 means kHz else Hz.
        #   duty: Percentage duty cycle of the LED. e.g. 25 = 25% = 1/4 on, 3/4 off.
        #         This is ignored if modulation is disabled at object instantiation.
        #
        # Note:
        #   Integer timing functions & math mean we can't do fractions of
        #   microseconds timing. Thus minor changes to the freq & duty values may have
        #   limited effect. You've been warned.

        # Set the duty cycle to use if we want freq. modulation.
        if self.modulation:
            self._dutycycle = min(duty, kDutyMax)
        else:
            self._dutycycle = kDutyMax

        if freq < 1000:  # Were we given kHz? Supports the old call usage.
            freq *= 1000

        period = self.calc_usec_period(freq)
        # Nr. of uSeconds the LED will be on per pulse.
        self.on_time_period = (period * self._dutycycle) / kDutyMax
        # Nr. of uSeconds the LED will be off per pulse.
        self.off_time_period = period - self.on_time_period
    
    @staticmethod
    def _delay_microseconds(usec):
        # A version of delayMicroseconds() that handles large values and does NOT use
        # the watch-dog friendly delay() calls where appropriate.
        # Args:
        #   usec: Nr. of uSeconds to delay for.
        #
        # NOTE: Use this only if you know what you are doing as it may cause the WDT
        #       to reset the ESP8266.

        while usec > kMaxAccurateUsecDelay:
            delay_microseconds(kMaxAccurateUsecDelay)
            delay_microseconds(usec)
            usec -= kMaxAccurateUsecDelay
    
    def mark(self, usec):
        # Modulate the IR LED for the given period (usec) and at the duty cycle set.
        #
        # Args:
        #   usec: The period of time to modulate the IR LED for, in microseconds.
        # Returns:
        #   Nr. of pulses actually sent.
        #
        # Note:
        #   The ESP8266 has no good way to do hardware PWM, so we have to do it all
        #   in software. There is a horrible kludge/brilliant hack to use the second
        #   serial TX line to do fairly accurate hardware PWM, but it is only
        #   available on a single specific GPIO and only available on some modules.
        #   e.g. It's not available on the ESP-01 module.
        #   Hence, for greater compatibility & choice, we don't use that method.
        # Ref:
        #   https:#www.analysir.com/blog/2017/01/29/updated-esp8266-nodemcu-backdoor-upwm-hack-for-ir-signals/

        # Handle the simple case of no required frequency modulation.
        if not self.modulation or self._dutycycle >= 100:
            self.led_on()
            self._delay_microseconds(usec)
            self.led_off()
            return 1

        # Not simple, so do it assuming frequency modulation.
        counter = 0
        usec_timer = IRtimer()
        # Cache the time taken so far. This saves us calling time, and we can be
        # assured that we can't have odd math problems. i.e. unsigned under/overflow.
        elapsed = usec_timer.elapsed()

        while elapsed < usec:  # Loop until we've met/exceeded our required time.
            self.led_on()

            # Calculate how long we should pulse on for.
            # e.g. Are we to close to the end of our requested mark time (usec)?
            self._delay_microseconds(min(self.on_time_period, usec - elapsed))
            self.led_off()
            counter += 1

            if elapsed + self.on_time_period >= usec:
                return counter  # LED is now off & we've passed our allotted time.
            # Wait for the lesser of the rest of the duty cycle, or the time remaining.
            self._delay_microseconds(
                min(usec - elapsed - self.on_time_period, self.off_time_period)
            )
            elapsed = usec_timer.elapsed()  # Update & recache the actual elapsed time.

        return counter
    
    def space(self, usec):
        # Turn the pin (LED) off for a given time.
        # Sends an IR space for the specified number of microseconds.
        # A space is no output, so the PWM output is disabled.
        #
        # Args:
        #   time: Time in microseconds (us).
        self.led_off()

        if usec == 0:
            return

        self._delay_microseconds(usec)
    
    def calibrate(self, hz=38000):
        # Calculate & set any offsets to account for execution times.
        #
        # Args:
        #   hz: The frequency to calibrate at >= 1000Hz. Default is 38000Hz.
        #
        # Returns:
        #   The calculated period offset (in uSeconds) which is now in use. e.g. -5.
        #
        # Status:  Stable / Working.
        #
        # NOTE:
        #   This will generate an 65535us mark() IR LED signal.
        #   This only needs to be called once, if at all.

        if hz < 1000:  # Were we given kHz? Supports the old call usage.
            hz *= 1000

        self.period_offset = 0  # Turn off any existing offset while we calibrate.
        self.enable_ir_out(hz)

        usec_timer = IRtimer()  # Start a timer *just* before we do the call.
        pulses = self.mark(UINT16_MAX)  # Generate a PWM of 65,535 us. (Max.)
        time_taken = usec_timer.elapsed()  # Record the time it took.

        # While it shouldn't be necessary, assume at least 1 pulse, to avoid a
        # divide by 0 situation.
        pulses = max(pulses, 1)
        calc_period = self.calc_usec_period(hz)  # e.g. @38kHz it should be 26us.

        # Assuming 38kHz for the example calculations:
        # In a 65535us pulse, we should have 2520.5769 pulses @ 26us periods.
        # e.g. 65535.0us / 26us = 2520.5769
        # This should have caused approx 2520 loops through the main loop in mark().
        # The average over that many interations should give us a reasonable
        # approximation at what offset we need to use to account for instruction
        # execution times.
        #
        # Calculate the actual period from the actual time & the actual pulses
        # generated.
        actual_period = time_taken / pulses

        # Store the difference between the actual time per period vs. calculated.
        self.period_offset = calc_period - actual_period
        return self.period_offset
    
    def send_raw(self, buf, length, hz):
        # Send a raw IRremote message.
        #
        # Args:
        #   buf: An array of uint16_t's that has microseconds elements.
        #   len: Nr. of elements in the buf[] array.
        #   hz:  Frequency to send the message at. (kHz < 1000 Hz >= 1000)
        #
        # Status: STABLE / Known working.
        #
        # Notes:
        #   Even elements are Mark times (On), Odd elements are Space times (Off).
        #
        # Ref:
        #   examples/IRrecvDumpV2/IRrecvDumpV2.ino

        # Set IR carrier frequency
        self.enable_ir_out(hz)

        for ii in range(length):
            if ii & 1:  # Odd bit.
                self.space(buf[ii])
            else:  # Even bit.
                self.mark(buf[ii])

        self.led_off()  # We potentially have ended with a mark(), so turn of the LED.
    
    def send_data(
        self, 
        one_mark, 
        one_space, 
        zero_mark, 
        zero_space, 
        data, 
        nbits, 
        msb_first=True
    ):
        # Generic method for sending data that is common to most protocols.
        # Will send leading or trailing 0's if the nbits is larger than the number
        # of bits in data.
        #
        # Args:
        #   onemark:    Nr. of usecs for the led to be pulsed for a '1' bit.
        #   onespace:   Nr. of usecs for the led to be fully off for a '1' bit.
        #   zeromark:   Nr. of usecs for the led to be pulsed for a '0' bit.
        #   zerospace:  Nr. of usecs for the led to be fully off for a '0' bit.
        #   data:       The data to be transmitted.
        #   nbits:      Nr. of bits of data to be sent.
        #   MSBfirst:   Flag for bit transmission order. Defaults to MSB->LSB order.

        if nbits == 0:  # If we are asked to send nothing, just return.
            return

        if msb_first:  # Send the MSB first.
            # Send 0's until we get down to a bit size we can actually manage.
            while nbits > len(data) * 8:
                self.mark(zero_mark)
                self.space(zero_space)
                nbits -= 1

            # Send the supplied data.
            mask = 1 << (nbits - 1)

            while mask:
                if data & mask:  # Send a 1
                    self.mark(one_mark)
                    self.space(one_space)
                else:  # Send a 0
                    self.mark(zero_mark)
                    self.space(zero_space)

                mask >>= 1

        else:  # Send the Least Significant Bit (LSB) first / MSB last.
            for bit in range(nbits):
                if data & 1:  # Send a 1
                    self.mark(one_mark)
                    self.space(one_space)
                else:  # Send a 0
                    self.mark(zero_mark)
                    self.space(zero_space)

                data >>= 1
    
    def send_generic(
        self,
        header_mark, 
        header_space, 
        one_mark, 
        one_space, 
        zero_mark, 
        zero_space, 
        footer_mark, 
        gap, 
        data, 
        nbits, 
        frequency, 
        msb_first, 
        repeat, 
        duty_cycle
    ):
        # Generic method for sending simple protocol messages.
        # Will send leading or trailing 0's if the nbits is larger than the number
        # of bits in data.
        #
        # Args:
        #   headermark:  Nr. of usecs for the led to be pulsed for the header mark.
        #                A value of 0 means no header mark.
        #   headerspace: Nr. of usecs for the led to be off after the header mark.
        #                A value of 0 means no header space.
        #   onemark:     Nr. of usecs for the led to be pulsed for a '1' bit.
        #   onespace:    Nr. of usecs for the led to be fully off for a '1' bit.
        #   zeromark:    Nr. of usecs for the led to be pulsed for a '0' bit.
        #   zerospace:   Nr. of usecs for the led to be fully off for a '0' bit.
        #   footermark:  Nr. of usecs for the led to be pulsed for the footer mark.
        #                A value of 0 means no footer mark.
        #   gap:         Nr. of usecs for the led to be off after the footer mark.
        #                This is effectively the gap between messages.
        #                A value of 0 means no gap space.
        #   data:        The data to be transmitted.
        #   nbits:       Nr. of bits of data to be sent.
        #   frequency:   The frequency we want to modulate at.
        #                Assumes < 1000 means kHz otherwise it is in Hz.
        #                Most common value is 38000 or 38, for 38kHz.
        #   MSBfirst:    Flag for bit transmission order. Defaults to MSB->LSB order.
        #   repeat:      Nr. of extra times the message will be sent.
        #                e.g. 0 = 1 message sent, 1 = 1 initial + 1 repeat = 2 messages
        #   dutycycle:   Percentage duty cycle of the LED.
        #                e.g. 25 = 25% = 1/4 on, 3/4 off.
        #                If you are not sure, try 50 percent.

        self.send_generic(
            header_mark,
            header_space,
            one_mark,
            one_space,
            zero_mark,
            zero_space,
            footer_mark,
            gap,
            0,
            data,
            nbits,
            frequency,
            msb_first,
            repeat,
            duty_cycle
        )

    def send_generic(
        self,
        header_mark,
        header_space,
        one_mark,
        one_space,
        zero_mark,
        zero_space,
        footer_mark,
        gap,
        mesg_time,
        data,
        nbits,
        frequency,
        msb_first,
        repeat,
        duty_cycle
    ):
        # Generic method for sending simple protocol messages.
        # Will send leading or trailing 0's if the nbits is larger than the number
        # of bits in data.
        #
        # Args:
        #   headermark:  Nr. of usecs for the led to be pulsed for the header mark.
        #                A value of 0 means no header mark.
        #   headerspace: Nr. of usecs for the led to be off after the header mark.
        #                A value of 0 means no header space.
        #   onemark:     Nr. of usecs for the led to be pulsed for a '1' bit.
        #   onespace:    Nr. of usecs for the led to be fully off for a '1' bit.
        #   zeromark:    Nr. of usecs for the led to be pulsed for a '0' bit.
        #   zerospace:   Nr. of usecs for the led to be fully off for a '0' bit.
        #   footermark:  Nr. of usecs for the led to be pulsed for the footer mark.
        #                A value of 0 means no footer mark.
        #   gap:         Min. nr. of usecs for the led to be off after the footer mark.
        #                This is effectively the absolute minimum gap between messages.
        #   mesgtime:    Min. nr. of usecs a single message needs to be.
        #                This is effectively the min. total length of a single message.
        #   data:        The data to be transmitted.
        #   nbits:       Nr. of bits of data to be sent.
        #   frequency:   The frequency we want to modulate at.
        #                Assumes < 1000 means kHz otherwise it is in Hz.
        #                Most common value is 38000 or 38, for 38kHz.
        #   MSBfirst:    Flag for bit transmission order. Defaults to MSB->LSB order.
        #   repeat:      Nr. of extra times the message will be sent.
        #                e.g. 0 = 1 message sent, 1 = 1 initial + 1 repeat = 2 messages
        #   dutycycle:   Percentage duty cycle of the LED.
        #                e.g. 25 = 25% = 1/4 on, 3/4 off.
        #                If you are not sure, try 50 percent.

        # Setup
        self.enable_ir_out(frequency, duty_cycle)
        usecs = IRtimer()

        # We always send a message, even for repeat=0, hence '<= repeat'.
        for _ in range(repeat):
            usecs.reset()

            # Header
            if header_mark:
                self.mark(header_mark)
            if header_space:
                self.space(header_space)

            # Data
            self.send_data(one_mark, one_space, zero_mark, zero_space, data, nbits, msb_first)

            # Footer
            if footer_mark:
                self.mark(footer_mark)

            elapsed = usecs.elapsed()
            # Avoid potential unsigned integer underflow. e.g. when mesgtime is 0.
            if elapsed >= mesg_time:
                self.space(gap)
            else:
                self.space(max(gap, mesg_time - elapsed))
    
    def send_generic(
        self,
        header_mark,
        header_space,
        one_mark,
        one_space,
        zero_mark,
        zero_space,
        footer_mark,
        gap,
        dataptr,
        nbytes,
        frequency,
        msb_first,
        repeat, 
        duty_cycle
    ):
        # Generic method for sending simple protocol messages.
        #
        # Args:
        #   headermark:  Nr. of usecs for the led to be pulsed for the header mark.
        #                A value of 0 means no header mark.
        #   headerspace: Nr. of usecs for the led to be off after the header mark.
        #                A value of 0 means no header space.
        #   onemark:     Nr. of usecs for the led to be pulsed for a '1' bit.
        #   onespace:    Nr. of usecs for the led to be fully off for a '1' bit.
        #   zeromark:    Nr. of usecs for the led to be pulsed for a '0' bit.
        #   zerospace:   Nr. of usecs for the led to be fully off for a '0' bit.
        #   footermark:  Nr. of usecs for the led to be pulsed for the footer mark.
        #                A value of 0 means no footer mark.
        #   gap:         Nr. of usecs for the led to be off after the footer mark.
        #                This is effectively the gap between messages.
        #                A value of 0 means no gap space.
        #   dataptr:     Pointer to the data to be transmitted.
        #   nbytes:      Nr. of bytes of data to be sent.
        #   frequency:   The frequency we want to modulate at.
        #                Assumes < 1000 means kHz otherwise it is in Hz.
        #                Most common value is 38000 or 38, for 38kHz.
        #   MSBfirst:    Flag for bit transmission order. Defaults to MSB->LSB order.
        #   repeat:      Nr. of extra times the message will be sent.
        #                e.g. 0 = 1 message sent, 1 = 1 initial + 1 repeat = 2 messages
        #   dutycycle:   Percentage duty cycle of the LED.
        #                e.g. 25 = 25% = 1/4 on, 3/4 off.
        #                If you are not sure, try 50 percent.

        # Setup
        self.enable_ir_out(frequency, duty_cycle)

        # We always send a message, even for repeat=0, hence '<= repeat'.
        for _ in range(repeat):
            # Header
            if header_mark:
                self.mark(header_mark)
            if header_space:
                self.space(header_space)

            # Data
            for ii in range(nbytes):
                self.send_data(
                    one_mark,
                    one_space,
                    zero_mark,
                    zero_space,
                    (dataptr + ii),
                    8,
                    msb_first
                )

            # Footer
            if footer_mark:
                self.mark(footer_mark)

            self.space(gap)

    @staticmethod
    def min_repeats(protocol):
        # Get the minimum number of repeats for a given protocol.
        # Args:
        #   protocol:  Protocol number/type of the message you want to send.
        # Returns:
        #   int16_t:  The number of repeats required.

        # Single repeats
        if protocol in (
            AIWA_RC_T501,
            AMCOR,
            COOLIX,
            GICABLE,
            INAX,
            MITSUBISHI,
            MITSUBISHI2,
            MITSUBISHI_AC,
            SHERWOOD,
            TOSHIBA_AC
        ):
            return kSingleRepeat
        # Special
        if protocol == DISH:
            return kDishMinRepeat
        if protocol == SONY:
            return kSonyMinRepeat

        return kNoRepeat

    @staticmethod
    def default_bits(protocol):
        # Get the default number of bits for a given protocol.
        # Args:
        #   protocol:  Protocol number/type you want the default nr. of bits for.
        # Returns:
        #   int16_t:  The number of bits.
        if protocol == RC5:
            return 12
        if protocol in (LASERTAG, RC5X):
            return 13
        if protocol in (AIWA_RC_T501, DENON, SHARP):
            return 15
        if protocol in (DISH, GICABLE, JVC, LEGOPF, MITSUBISHI, MITSUBISHI2):
            return 16
        if protocol in (RC6, SONY):
            return 20
        if protocol in (COOLIX, INAX, NIKAI, RCMM):
            return 24
        if protocol in (LG, LG2):
            return 28
        if protocol in (CARRIER_AC, NEC, NEC_LIKE, SAMSUNG, SHERWOOD, WHYNTER):
            return 32
        if protocol in (LUTRON, TECO):
            return 35
        if protocol == SAMSUNG36:
            return 36
        if protocol == SANYO_LC7461:
            return kSanyoLC7461Bits  # 42
        if protocol in (GOODWEATHER, MIDEA, PANASONIC):
            return 48
        if protocol in (MAGIQUEST, VESTEL_AC):
            return 56
        if protocol in (AMCOR, PIONEER):
            return 64
        if protocol == ARGO:
            return kArgoBits
        if protocol == DAIKIN:
            return kDaikinBits
        if protocol == DAIKIN128:
            return kDaikin128Bits
        if protocol == DAIKIN152:
            return kDaikin152Bits
        if protocol == DAIKIN160:
            return kDaikin160Bits
        if protocol == DAIKIN176:
            return kDaikin176Bits
        if protocol == DAIKIN2:
            return kDaikin2Bits
        if protocol == DAIKIN216:
            return kDaikin216Bits
        if protocol == ELECTRA_AC:
            return kElectraAcBits
        if protocol == GREE:
            return kGreeBits
        if protocol == HAIER_AC:
            return kHaierACBits
        if protocol == HAIER_AC_YRW02:
            return kHaierACYRW02Bits
        if protocol == HITACHI_AC:
            return kHitachiAcBits
        if protocol == HITACHI_AC1:
            return kHitachiAc1Bits
        if protocol == HITACHI_AC2:
            return kHitachiAc2Bits
        if protocol == HITACHI_AC424:
            return kHitachiAc424Bits
        if protocol == KELVINATOR:
            return kKelvinatorBits
        if protocol == MITSUBISHI_AC:
            return kMitsubishiACBits
        if protocol == MITSUBISHI136:
            return kMitsubishi136Bits
        if protocol == MITSUBISHI112:
            return kMitsubishi112Bits
        if protocol == MITSUBISHI_HEAVY_152:
            return kMitsubishiHeavy152Bits
        if protocol == MITSUBISHI_HEAVY_88:
            return kMitsubishiHeavy88Bits
        if protocol == NEOCLIMA:
            return kNeoclimaBits
        if protocol == PANASONIC_AC:
            return kNeoclimaBits
        if protocol == SAMSUNG_AC:
            return kSamsungAcBits
        if protocol == SHARP_AC:
            return kSharpAcBits
        if protocol == TCL112AC:
            return kTcl112AcBits
        if protocol == TOSHIBA_AC:
            return kToshibaACBits
        if protocol == TROTEC:
            return kTrotecBits
        if protocol == WHIRLPOOL_AC:
            return kWhirlpoolAcBits

        # No default amount of bits.
        if protocol in (FUJITSU_AC, MWM):
            return 0

        return 0

    def send(self, _type, data, nbits, repeat=kNoRepeat):
        # Send a simple (up to 64 bits) IR message of a given type.
        # An unknown/unsupported type will do nothing.
        # Args:
        #   type:  # Protocol number/type of the message you want to send.
        #   data:  The data you want to send (up to 64 bits).
        #   nbits: How many bits long the message is to be.
        #   repeat: How many repeats to do?
        # Returns:
        #   bool: True if it is a type we can attempt to send, False if not.
        min_repeat = max(self.min_repeats(_type), repeat)

        if _type == AIWA_RC_T501:
            self.sendAiwaRCT501(data, nbits, min_repeat)
        elif _type == CARRIER_AC:
            self.sendCarrierAC(data, nbits, min_repeat)
        elif _type == COOLIX:
            self.sendCOOLIX(data, nbits, min_repeat)
        elif _type == DENON:
            self.sendDenon(data, nbits, min_repeat)
        elif _type == DISH:
            self.sendDISH(data, nbits, min_repeat)
        elif _type == GICABLE:
            self.sendGICable(data, nbits, min_repeat)
        elif _type == GOODWEATHER:
            self.sendGoodweather(data, nbits, min_repeat)
        elif _type == GREE:
            self.sendGree(data, nbits=nbits, repeat=min_repeat)
        elif _type == INAX:
            self.sendInax(data, nbits, min_repeat)
        elif _type == JVC:
            self.sendJVC(data, nbits, min_repeat)
        elif _type == LASERTAG:
            self.sendLasertag(data, nbits, min_repeat)
        elif _type == LEGOPF:
            self.sendLegoPf(data, nbits, min_repeat)
        elif _type == LG:
            self.sendLG(data, nbits, min_repeat)
        elif _type == LG2:
            self.sendLG2(data, nbits, min_repeat)
        elif _type == LUTRON:
            self.sendLutron(data, nbits, min_repeat)
        elif _type == MAGIQUEST:
            self.sendMagiQuest(data, nbits, min_repeat)
        elif _type == MIDEA:
            self.sendMidea(data, nbits, min_repeat)
        elif _type == MITSUBISHI:
            self.sendMitsubishi(data, nbits, min_repeat)
        elif _type == MITSUBISHI2:
            self.sendMitsubishi2(data, nbits, min_repeat)
        elif _type == NIKAI:
            self.sendNikai(data, nbits, min_repeat)
        elif _type == NEC:
            self.sendNEC(data, nbits, min_repeat)
        elif _type == NEC_LIKE:
            self.sendNEC(data, nbits, min_repeat)
        elif _type == PANASONIC:
            self.sendPanasonic64(data, nbits, min_repeat)
        elif _type == PIONEER:
            self.sendPioneer(data, nbits, min_repeat)
        elif _type == RC5:
            self.sendRC5(data, nbits, min_repeat)
        elif _type == RC5X:
            self.sendRC5(data, nbits, min_repeat)
        elif _type == RC6:
            self.sendRC6(data, nbits, min_repeat)
        elif _type == RCMM:
            self.sendRCMM(data, nbits, min_repeat)
        elif _type == SAMSUNG:
            self.sendSAMSUNG(data, nbits, min_repeat)
        elif _type == SAMSUNG36:
            self.sendSamsung36(data, nbits, min_repeat)
        elif _type == SANYO_LC7461:
            self.sendSanyoLC7461(data, nbits, min_repeat)
        elif _type == SHARP:
            self.sendSharpRaw(data, nbits, min_repeat)
        elif _type == SHERWOOD:
            self.sendSherwood(data, nbits, min_repeat)
        elif _type == SONY:
            self.sendSony(data, nbits, min_repeat)
        elif _type == TECO:
            self.sendTeco(data, nbits, min_repeat)
        elif _type == VESTEL_AC:
            self.sendVestelAc(data, nbits, min_repeat)
        elif _type == WHYNTER:
            self.sendWhynter(data, nbits, min_repeat)
        else:
            return False

        return True

    def send(self, _type, state, nbytes):
        # Send a complex (>= 64 bits) IR message of a given type.
        # An unknown/unsupported type will do nothing.
        # Args:
        #   type: # Protocol number type of the message you want to send.
        #   state:  A pointer to the array of bytes that make up the state[].
        #   nbytes: How many bytes are in the state.
        # Returns:
        #   bool: True if it is a type we can attempt to send, False if not.
        if _type == AMCOR:
            self.sendAmcor(state, nbytes)
        elif _type == ARGO:
            self.sendArgo(state, nbytes)
        elif _type == DAIKIN:
            self.sendDaikin(state, nbytes)
        elif _type == DAIKIN128:
            self.sendDaikin128(state, nbytes)
        elif _type == DAIKIN152:
            self.sendDaikin152(state, nbytes)
        elif _type == DAIKIN160:
            self.sendDaikin160(state, nbytes)
        elif _type == DAIKIN176:
            self.sendDaikin176(state, nbytes)
        elif _type == DAIKIN2:
            self.sendDaikin2(state, nbytes)
        elif _type == DAIKIN216:
            self.sendDaikin216(state, nbytes)
        elif _type == ELECTRA_AC:
            self.sendElectraAC(state, nbytes)
        elif _type == FUJITSU_AC:
            self.sendFujitsuAC(state, nbytes)
        elif _type == GREE:
            self.sendGree(state, nbytes=nbytes)
        elif _type == HAIER_AC:
            self.sendHaierAC(state, nbytes)
        elif _type == HAIER_AC_YRW02:
            self.sendHaierACYRW02(state, nbytes)
        elif _type == HITACHI_AC:
            self.sendHitachiAC(state, nbytes)
        elif _type == HITACHI_AC1:
            self.sendHitachiAC1(state, nbytes)
        elif _type == HITACHI_AC2:
            self.sendHitachiAC2(state, nbytes)
        elif _type == HITACHI_AC424:
            self.sendHitachiAc424(state, nbytes)
        elif _type == KELVINATOR:
            self.sendKelvinator(state, nbytes)
        elif _type == MITSUBISHI_AC:
            self.sendMitsubishiAC(state, nbytes)
        elif _type == MITSUBISHI136:
            self.sendMitsubishi136(state, nbytes)
        elif _type == MITSUBISHI112:
            self.sendMitsubishi112(state, nbytes)
        elif _type == MITSUBISHI_HEAVY_88:
            self.sendMitsubishiHeavy88(state, nbytes)
        elif _type == MITSUBISHI_HEAVY_152:
            self.sendMitsubishiHeavy152(state, nbytes)
        elif _type == MWM:
            self.sendMWM(state, nbytes)
        elif _type == NEOCLIMA:
            self.sendNeoclima(state, nbytes)
        elif _type == PANASONIC_AC:
            self.sendPanasonicAC(state, nbytes)
        elif _type == SAMSUNG_AC:
            self.sendSamsungAC(state, nbytes)
        elif _type == SHARP_AC:
            self.sendSharpAc(state, nbytes)
        elif _type == TCL112AC:
            self.sendTcl112Ac(state, nbytes)
        elif _type == TOSHIBA_AC:
            self.sendToshibaAC(state, nbytes)
        elif _type == TROTEC:
            self.sendTrotec(state, nbytes)
        elif _type == WHIRLPOOL_AC:
            self.sendWhirlpoolAC(state, nbytes)
        else:
            return False
        return True

    def sendNEC(self, data, nbits=kNECBits, repeat=kNoRepeat):
        pass

    def encodeNEC(self, address, command):
        pass
  
    # sendSony() should typically be called with repeat=2 as Sony devices
    # expect the code to be sent at least 3 times. (code + 2 repeats = 3 codes)
    # Legacy use of this procedure was to only send a single code so call it with
    # repeat=0 for backward compatibility. As of v2.0 it defaults to sending
    # a Sony command that will be accepted be a device.
    def sendSony(self, data, nbits=kSony20Bits, repeat=kSonyMinRepeat):
        pass

    def encodeSony(self, nbits, command, address, extended=0):
        pass
  
    def sendSherwood(self, data, nbits=kSherwoodBits, repeat=kSherwoodMinRepeat):
        pass
    
    def sendSAMSUNG(self, data, nbits=kSamsungBits, repeat=kNoRepeat):
        pass

    def encodeSAMSUNG(self, customer, command):
        pass

    def sendSamsung36(self, data, nbits=kSamsung36Bits, repeat=kNoRepeat):
        pass

    def sendSamsungAC(self, data, nbytes=kSamsungAcStateLength, repeat=kSamsungAcDefaultRepeat):
        pass
  
    def sendLG(self, data, nbits=kLgBits, repeat=kNoRepeat):
        pass

    def sendLG2(self, data, nbits=kLgBits, repeat=kNoRepeat):
        pass

    def encodeLG(self, address, command):
        pass
    
    def encodeSharp(self, address, command, expansion=1, check=0, msb_first=False):
        pass

    def sendSharp(self, address, command, nbits=kSharpBits, repeat=kNoRepeat):
        pass

    def sendSharpRaw(self, data, nbits=kSharpBits, repeat=kNoRepeat):
        pass

    def sendSharpAc(self, data, nbytes=kSharpAcStateLength, repeat=kSharpAcDefaultRepeat):
        pass
    
    def sendJVC(self, data, nbits=kJvcBits, repeat=kNoRepeat):
        pass

    def encodeJVC(self, address, command):
        pass
  
    def sendDenon(self, data, nbits=kDenonBits, repeat=kNoRepeat):
        pass
  
    def encodeSanyoLC7461(self, address, command):
        pass

    def sendSanyoLC7461(self, data, nbits=kSanyoLC7461Bits, repeat=kNoRepeat):
        pass
  
    # sendDISH() should typically be called with repeat=3 as DISH devices
    # expect the code to be sent at least 4 times. (code + 3 repeats = 4 codes)
    # Legacy use of this procedure was only to send a single code
    # so use repeat=0 for backward compatibility.
    def sendDISH(self, data, nbits=kDishBits, repeat=kDishMinRepeat):
        pass
  
    def sendPanasonic64(self, data, nbits=kPanasonicBits, repeat=kNoRepeat):
        pass

    def sendPanasonic(self, address, data, nbits=kPanasonicBits, repeat=kNoRepeat):
        pass

    def encodePanasonic(self, manufacturer, device, subdevice, function):
        pass

    def sendRC5(self, data, nbits=kRC5XBits, repeat=kNoRepeat):
        pass

    def encodeRC5(self, address, command, key_released=False):
        pass

    def encodeRC5X(self, address, command, key_released=False):
        pass

    def toggleRC5(self, data):
        pass
  
    def sendRC6(self, data, nbits=kRC6Mode0Bits, repeat=kNoRepeat):
        pass

    def encodeRC6(self, address, command, mode=kRC6Mode0Bits):
        pass

    def toggleRC6(self, data, nbits=kRC6Mode0Bits):
        pass
  
    def sendRCMM(self, data, nbits=kRCMMBits, repeat=kNoRepeat):
        pass
  
    def sendCOOLIX(self, data, nbits=kCoolixBits, repeat=kCoolixDefaultRepeat):
        pass
  
    def sendWhynter(self, data, nbits=kWhynterBits, repeat=kNoRepeat):
        pass
  
    def sendMitsubishi(self, data, nbits=kMitsubishiBits, repeat=kMitsubishiMinRepeat):
        pass

    def sendMitsubishi136(self, data, nbytes=kMitsubishi136StateLength, repeat=kMitsubishi136MinRepeat):
        pass

    def sendMitsubishi112(self, data, nbytes=kMitsubishi112StateLength, repeat=kMitsubishi112MinRepeat):
        pass

    def sendMitsubishi2(self, data, nbits=kMitsubishiBits, repeat=kMitsubishiMinRepeat):
        pass

    def sendMitsubishiAC(self, data, nbytes=kMitsubishiACStateLength, repeat=kMitsubishiACMinRepeat):
        pass

    def sendMitsubishiHeavy88(self, data, nbytes=kMitsubishiHeavy88StateLength, repeat=kMitsubishiHeavy88MinRepeat):
        pass

    def sendMitsubishiHeavy152(self, data, nbytes=kMitsubishiHeavy152StateLength, repeat=kMitsubishiHeavy152MinRepeat):
        pass
  
    def sendFujitsuAC(self, data, nbytes, repeat=kFujitsuAcMinRepeat):
        pass
  
    def sendInax(self, data, nbits=kInaxBits, repeat=kInaxMinRepeat):
        pass
  
    def sendGC(self, buf, length):
        pass
  
    def sendKelvinator(self, data, nbytes=kKelvinatorStateLength, repeat=kKelvinatorDefaultRepeat):
        pass
  
    def sendDaikin(self, data, nbytes=kDaikinStateLength, repeat=kDaikinDefaultRepeat):
        pass

    def sendDaikin128(self, data, nbytes=kDaikin128StateLength, repeat=kDaikin128DefaultRepeat):
        pass

    def sendDaikin152(self, data, nbytes=kDaikin152StateLength, repeat=kDaikin152DefaultRepeat):
        pass

    def sendDaikin160(self, data, nbytes=kDaikin160StateLength, repeat=kDaikin160DefaultRepeat):
        pass

    def sendDaikin176(self, data, nbytes=kDaikin176StateLength, repeat=kDaikin176DefaultRepeat):
        pass

    def sendDaikin2(self, data, nbytes=kDaikin2StateLength, repeat=kDaikin2DefaultRepeat):
        pass

    def sendDaikin216(self, data, nbytes=kDaikin216StateLength, repeat=kDaikin216DefaultRepeat):
        pass

    def sendAiwaRCT501(self, data, nbits=kAiwaRcT501Bits, repeat=kAiwaRcT501MinRepeats):
        pass

    def sendGree(self, data, nbits=kGreeBits, nbytes=kGreeStateLength, repeat=kGreeDefaultRepeat):
        pass
  
    def sendGoodweather(self, data, nbits=kGoodweatherBits, repeat=kGoodweatherMinRepeat):
        pass
  
    def sendPronto(self, data, length, repeat=kNoRepeat):
        pass
  
    def sendArgo(self, data, nbytes=kArgoStateLength, repeat=kArgoDefaultRepeat):
        pass
  
    def sendTrotec(self, data, nbytes=kTrotecStateLength, repeat=kTrotecDefaultRepeat):
        pass
  
    def sendNikai(self, data, nbits=kNikaiBits, repeat=kNoRepeat):
        pass
  
    def sendToshibaAC(self, data, nbytes=kToshibaACStateLength, repeat=kToshibaACMinRepeat):
        pass
  
    def sendMidea(self, data, nbits=kMideaBits, repeat=kMideaMinRepeat):
        pass
  
    def sendMagiQuest(self, data, nbits=kMagiquestBits, repeat=kNoRepeat):
        pass

    def encodeMagiQuest(self, wand_id, magnitude):
        pass
  
    def sendLasertag(self, data, nbits=kLasertagBits, repeat=kLasertagMinRepeat):
        pass
  
    def sendCarrierAC(self, data, nbits=kCarrierAcBits, repeat=kCarrierAcMinRepeat):
        pass
  
    def sendHaierAC(self, data, nbytes=kHaierACStateLength, repeat=kHaierAcDefaultRepeat):
        pass
  
    def sendHaierACYRW02(self, data, nbytes=kHaierACYRW02StateLength, repeat=kHaierAcYrw02DefaultRepeat):
        pass
  
    def sendHitachiAC(self, data, nbytes=kHitachiAcStateLength, repeat=kHitachiAcDefaultRepeat):
        pass

    def sendHitachiAC1(self, data, nbytes=kHitachiAc1StateLength, repeat=kHitachiAcDefaultRepeat):
        pass

    def sendHitachiAC2(self, data, nbytes=kHitachiAc2StateLength, repeat=kHitachiAcDefaultRepeat):
        pass

    def sendHitachiAc424(self, data, nbytes=kHitachiAc424StateLength, repeat=kHitachiAcDefaultRepeat):
        pass
  
    def sendGICable(self, data, nbits=kGicableBits, repeat=kGicableMinRepeat):
        pass
  
    def sendWhirlpoolAC(self, data, nbytes=kWhirlpoolAcStateLength, repeat=kWhirlpoolAcDefaultRepeat):
        pass
  
    def sendLutron(self, data, nbits=kLutronBits, repeat=kNoRepeat):
        pass
  
    def sendElectraAC(self, data, nbytes=kElectraAcStateLength, repeat=kNoRepeat):
        pass
  
    def sendPanasonicAC(self, data, nbytes=kPanasonicAcStateLength, repeat=kPanasonicAcDefaultRepeat):
        pass
  
    def sendPioneer(self, data, nbits=kPioneerBits, repeat=kNoRepeat):
        pass

    def encodePioneer(self, address, command):
        pass
  
    def sendMWM(self, data, nbytes, repeat=kNoRepeat):
        pass
  
    def sendVestelAc(self, data, nbits=kVestelAcBits, repeat=kNoRepeat):
        pass
  
    def sendTcl112Ac(self, data, nbytes=kTcl112AcStateLength, repeat=kTcl112AcDefaultRepeat):
        pass
  
    def sendTeco(self, data, nbits=kTecoBits, repeat=kNoRepeat):
        pass
  
    def sendLegoPf(self, data, nbits=kLegoPfBits, repeat=kLegoPfMinRepeat):
        pass
  
    def sendNeoclima(self, data, nbytes=kNeoclimaStateLength, repeat=kNeoclimaMinRepeat):
        pass
  
    def sendAmcor(self, data, nbytes=kAmcorStateLength, repeat=kAmcorDefaultRepeat):
        pass

    def led_off(self):
        # Turn off the IR LED.
        # digitalWrite(self.ir_pin, self.output_off)
        pass

    def led_on(self):
        # Turn on the IR LED.
        # digitalWrite(self.ir_pin, self.output_on)
        pass

    def calc_usec_period(self, hz, use_offset=True):
        # Calculate the period for a given frequency. (T = 1/f)
        #
        # Args:
        #   freq: Frequency in Hz.
        #   use_offset: Should we use the calculated offset or not?
        # Returns:
        #   nr. of uSeconds.

        if hz == 0:
            hz = 1  # Avoid Zero hz. Divide by Zero is nasty.
        period = (1000000 + hz / 2) / hz  # The equiv of round(1000000/hz).

        # Apply the offset and ensure we don't result in a <= 0 value.
        if use_offset:
            return max(1, period + self.period_offset)
        else:
            return max(1, period)
