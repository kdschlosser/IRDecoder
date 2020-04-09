# -*- coding: utf-8 -*-
# Copyright 2016 Hisham Khalifa
# Copyright 2017 David Conran
# Copyright 2020 Kevin Schlosser

# Global Cache IR format sender originally added by Hisham Khalifa
#   (http:#www.hishamkhalifa.com)

from .IRsend import *

# Constants
kGlobalCacheMaxRepeat = 50
kGlobalCacheMinUsec = 80
kGlobalCacheFreqIndex = 0
kGlobalCacheRptIndex = kGlobalCacheFreqIndex + 1
kGlobalCacheRptStartIndex = kGlobalCacheRptIndex + 1
kGlobalCacheStartIndex = kGlobalCacheRptStartIndex + 1


# Send a shortened GlobalCache (GC) IRdb/control tower formatted message.
#
# Args:
#   buf: An array of containing the shortened GlobalCache data.
#   len: Nr. of entries in the buf[] array.
#
# Status: STABLE / Known working.
#
# Note:
#   Global Cache format without the emitter ID or request ID.
#   Starts at the frequency (Hertz), followed by nr. of times to emit (count),
#   then the offset for repeats (where a repeat will start from),
#   then the rest of entries are the actual IR message as units of periodic
#   time.
#   e.g. sendir,1:1,1,38000,1,1,9,70,9,30,9,... .38000,1,1,9,70,9,30,9,...
# Ref:
#   https:#irdb.globalcache.com/Home/Database
def sendGC(self, buf, length):
    hz = buf[kGlobalCacheFreqIndex]  # GC frequency is in Hz.
    self.enable_ir_out(hz)
    periodic_time = self.calc_usec_period(hz, False)
    emits = min(buf[kGlobalCacheRptIndex], kGlobalCacheMaxRepeat)
    # Repeat
    repeat = 0
    while repeat < emits:
        # First time through, start at the beginning (kGlobalCacheStartIndex),
        # otherwise for repeats, we start a specified offset from that.
        offset = kGlobalCacheStartIndex
        if repeat:
            offset += buf[kGlobalCacheRptStartIndex] - 1
        # Data
        while offset < length:
            # Convert periodic units to microseconds.
            # Minimum is kGlobalCacheMinUsec for actual GC units.
            microseconds = max(buf[offset] * periodic_time, kGlobalCacheMinUsec)
            # These codes start at an odd index (not even as with sendRaw).
            if offset & 1:  # Odd bit.
                self.mark(microseconds)
            else:  # Even bit.
                self.space(microseconds)
            offset += 1
        repeat += 1
    # It's possible that we've ended on a mark(), thus ensure the LED is off.
    self.led_off()


IRsend.sendGC = sendGC
