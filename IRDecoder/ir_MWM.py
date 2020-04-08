# Copyright 2018 Brett T. Warden

# MWM

# derived from ir_Lasertag.cpp, Copyright 2017 David Conran

#include <algorithm>
#include "IRrecv.h"
#include "IRsend.h"
#include "IRutils.h"

# Constants
kMWMMinSamples = 6  # Msgs are >=3 bytes, bytes have >=2
                                    # samples
kMWMTick = 417
kMWMMinGap = 30000  # Typical observed delay b/w commands
kMWMTolerance = 0    # Percentage error margin.
kMWMExcess = 0      # See kMarkExcess.
kMWMDelta = 150     # Use instead of Excess and Tolerance.
kMWMMaxWidth = 9     # Maximum number of successive bits at a
                                    # single level - worst case
kSpace = 1
kMark = 0

# Send a MWM packet.
# This protocol is 2400 bps serial, 1 start bit (mark), 1 stop bit (space), no
# parity
#
# Args:
#   data:    The message you wish to send.
#   nbits:   Bit size of the protocol you want to send.
#   repeat:  Nr. of extra times the data will be sent.
#
# Status: Implemented.
#
def sendMWM(data, nbytes, repeat):
    if nbytes < 3:
        return  # Shortest possible message is 3 bytes

    # Set 38kHz IR carrier frequency & a 1/4 (25%) duty cycle.
    # NOTE: duty cycle is not confirmed. Just guessing based on RC5/6 protocols.
    enableIROut(38, 25)

    for _ in range(repeat + 1):
        # Data
        for i in range(nbytes):
            byte = data[i]

            # Start bit
            mark(kMWMTick)

            # LSB first, space=1

            mask = 0x1
            while mask:
                if byte & mask:  # 1
                    space(kMWMTick)
                else:  # 0
                    mark(kMWMTick)

                mask <<= 1

        # Stop bit
        space(kMWMTick)

        # Footer
        space(kMWMMinGap)


# Decode the supplied MWM message.
# This protocol is 2400 bps serial, 1 start bit (mark), 1 stop bit (space), no
# parity
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Implemented.
#
def decodeMWM(results, nbits, strict):
    # Compliance
    if results.rawlen < kMWMMinSamples:
        return False

    offset = kStartOffset
    used = 0
    data = 0
    frame_bits = 0
    data_bits = 0

    # No Header

    # Data
    bits_per_frame = 10

    while offset < results.rawlen and results.bits < 8 * kStateSizeMax:
        level = getRClevel(results, offset, used, kMWMTick, kMWMTolerance, kMWMExcess, kMWMDelta, kMWMMaxWidth)
        if level < 0:
            break

        frame_bits += 1

        val = frame_bits % bits_per_frame
        if val == 0:
            # Start bit
            if level != kMark:
                goto done
            if level == 9:
                # Stop bit
                if level != kSpace:
                    return False
                else:
                    results.state[data_bits / 8 - 1] = data & 0xFF
                    results.bits = data_bits
                    data = 0

            break
      default:
        # Data bits
        DPRINT("DEBUG: decodeMWM: Storing bit: ")
        DPRINTLN((level == kSpace))
        # Transmission is LSB-first, space=1
        data |= ((level == kSpace)) << 8
        data >>= 1
        data_bits++
        break
    }
  }

done:
  # Footer (None)

  # Compliance

  if (data_bits < nbits) {
    return False  # Less data than we expected.
  }

  payload_length = 0
  switch (results->state[0] & 0xf0) {
    case 0x90:
    case 0xf0:
      # Normal commands
      payload_length = results->state[0] & 0x0f
      DPRINT("DEBUG: decodeMWM: payload_length = ")
      DPRINTLN(payload_length)
      break
    default:
      if (strict) {
        # Show commands
        if (results->state[0] != 0x55 and results->state[1] != 0xAA) {
          return False
        }
      }
      break
  }
  if (data_bits < (payload_length + 3) * 8) {
    DPRINT("DEBUG: decodeMWM: too few bytes expected ")
    DPRINTLN((payload_length + 3))
    return False
  }
  if (strict) {
    if (payload_length and (data_bits > (payload_length + 3) * 8)) {
      DPRINT("DEBUG: decodeMWM: too many bytes expected ")
      DPRINTLN((payload_length + 3))
      return False
    }
  }

  # Success
  results->decode_type = MWM
  results->repeat = False
  return True
}
#endif  # DECODE_MWM

# vim: et:ts=2:sw=2
