# Copyright 2015 Kristian Lauszus
# Copyright 2017 David Conran

from IRrecv import *
from IRsend import *
from IRtimer import *
from IRutils import *

# JVC originally added by Kristian Lauszus
# (Thanks to zenwheel and other people at the original blog post)

# Constants
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
kJvcTick = 75
kJvcHdrMarkTicks = 112
kJvcHdrMark = kJvcHdrMarkTicks * kJvcTick
kJvcHdrSpaceTicks = 56
kJvcHdrSpace = kJvcHdrSpaceTicks * kJvcTick
kJvcBitMarkTicks = 7
kJvcBitMark = kJvcBitMarkTicks * kJvcTick
kJvcOneSpaceTicks = 23
kJvcOneSpace = kJvcOneSpaceTicks * kJvcTick
kJvcZeroSpaceTicks = 7
kJvcZeroSpace = kJvcZeroSpaceTicks * kJvcTick
kJvcRptLengthTicks = 800
kJvcRptLength = kJvcRptLengthTicks * kJvcTick
kJvcMinGapTicks =
    kJvcRptLengthTicks -
    (kJvcHdrMarkTicks + kJvcHdrSpaceTicks +
     kJvcBits * (kJvcBitMarkTicks + kJvcOneSpaceTicks) + kJvcBitMarkTicks)
kJvcMinGap = kJvcMinGapTicks * kJvcTick

# Decode the supplied JVC message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits of data to expect. Typically kJvcBits.
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: STABLE
#
# Note:
#   JVC repeat codes don't have a header.
# Ref:
#   http:#www.sbprojects.com/knowledge/ir/jvc.php
def decodeJVC(results, nbits, strict):
  if strict and nbits != kJvcBits:
    return False  # Must be called with the correct nr. of bits.
  if results.rawlen < 2 * nbits + kFooter - 1:
    return False  # Can't possibly be a valid JVC message.

  data = 0
  offset = kStartOffset
  isRepeat = True

  # Header
  # (Optional as repeat codes don't have the header)
  if matchMark(results.rawbuf[offset], kJvcHdrMark):
    isRepeat = False
    offset += 1
    if results.rawlen < 2 * nbits + 4:
      return False  # Can't possibly be a valid JVC message with a header.
    
    offset += 1
    if not matchSpace(results.rawbuf[offset], kJvcHdrSpace):
       return False

  # Data + Footer
  if not matchGeneric(
      results.rawbuf + offset, 
      &data,
      results.rawlen - offset, 
      nbits,
      0, 
      0,
      kJvcBitMark, 
      kJvcOneSpace,
      kJvcBitMark, 
      kJvcZeroSpace,
      kJvcBitMark, 
      kJvcMinGap, 
      True
   ):
      return False
      
  # Success
  results.decode_type = JVC
  results.bits = nbits
  results.value = data
  # command & address are transmitted LSB first, so we need to reverse them.
  results.address = reverseBits(data >> 8, 8)    # The first 8 bits sent.
  results.command = reverseBits(data & 0xFF, 8)  # The last 8 bits sent.
  results.repeat = isRepeat
  return True

