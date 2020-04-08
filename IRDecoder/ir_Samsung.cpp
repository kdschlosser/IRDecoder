# Copyright 2009 Ken Shirriff
# Copyright 2017, 2018, 2019 David Conran

# Samsung remote emulation

from IRtext import *
from IRutils import *

# Samsung originally added from https:#github.com/shirriff/Arduino-IRremote/

# Constants
# Ref:
#   http:#elektrolab.wz.cz/katalog/samsung_protocol.pdf
kSamsungTick = 560
kSamsungHdrMarkTicks = 8
kSamsungHdrMark = kSamsungHdrMarkTicks * kSamsungTick
kSamsungHdrSpaceTicks = 8
kSamsungHdrSpace = kSamsungHdrSpaceTicks * kSamsungTick
kSamsungBitMarkTicks = 1
kSamsungBitMark = kSamsungBitMarkTicks * kSamsungTick
kSamsungOneSpaceTicks = 3
kSamsungOneSpace = kSamsungOneSpaceTicks * kSamsungTick
kSamsungZeroSpaceTicks = 1
kSamsungZeroSpace = kSamsungZeroSpaceTicks * kSamsungTick
kSamsungRptSpaceTicks = 4
kSamsungRptSpace = kSamsungRptSpaceTicks * kSamsungTick
kSamsungMinMessageLengthTicks = 193
kSamsungMinMessageLength = kSamsungMinMessageLengthTicks * kSamsungTick
kSamsungMinGapTicks = kSamsungMinMessageLengthTicks - (kSamsungHdrMarkTicks + kSamsungHdrSpaceTicks + kSamsungBits * (kSamsungBitMarkTicks + kSamsungOneSpaceTicks) + kSamsungBitMarkTicks)
kSamsungMinGap = kSamsungMinGapTicks * kSamsungTick

kSamsungAcHdrMark = 690
kSamsungAcHdrSpace = 17844
kSamsungAcSections = 2
kSamsungAcSectionMark = 3086
kSamsungAcSectionSpace = 8864
kSamsungAcSectionGap = 2886
kSamsungAcBitMark = 586
kSamsungAcOneSpace = 1432
kSamsungAcZeroSpace = 436


# Decode the supplied Samsung36 message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   Nr. of bits to expect in the data portion.
#            Typically kSamsung36Bits.
#   strict:  Flag to indicate if we strictly adhere to the specification.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Alpha / Experimental
#
# Note:
#   Protocol is used by Samsung Bluray Remote: ak59-00167a
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/621
def decodeSamsung36(results, nbits, strict):
  if results.rawlen < 2 * nbits + kHeader + kFooter * 2 - 1:
    return False  # Can't possibly be a valid Samsung message.
    
  # We need to be looking for > 16 bits to make sense.
  if nbits <= 16:
      return False
  if strict and nbits != kSamsung36Bits:
    return False  # We expect nbits to be 36 bits of message.

  data = 0
  offset = kStartOffset

  # Match Header + Data + Footer
  used = matchGeneric(results.rawbuf + offset, data,
                      results.rawlen - offset, 16,
                      kSamsungHdrMark, kSamsungHdrSpace,
                      kSamsungBitMark, kSamsungOneSpace,
                      kSamsungBitMark, kSamsungZeroSpace,
                      kSamsungBitMark, kSamsungHdrSpace, False)
  if not used:
     return False
     
  offset += used
  # Data (Block #2)
  
  data2 = 0
  if not matchGeneric(results.rawbuf + offset, data2,
                    results.rawlen - offset, nbits - 16,
                    0, 0,
                    kSamsungBitMark, kSamsungOneSpace,
                    kSamsungBitMark, kSamsungZeroSpace,
                    kSamsungBitMark, kSamsungMinGap, True):
                     return False
  data <<= nbits - 16
  data += data2

  # Success
  results.bits = nbits
  results.value = data
  results.decode_type = SAMSUNG36
  results.command = data & ((1 << (nbits - 16)) - 1)
  results.address = data >> (nbits - 16)
  return True



# Decode the supplied Samsung A/C message.
#
# Args:
#   results: Ptr to the data to decode and where to store the decode result.
#   nbits:   The number of data bits to expect. Typically kSamsungAcBits
#   strict:  Flag indicating if we should perform strict matching.
# Returns:
#   boolean: True if it can decode it, False if it can't.
#
# Status: Stable / Known to be working.
#
# Ref:
#   https:#github.com/crankyoldgit/IRremoteESP8266/issues/505
def decodeSamsungAC(results, nbits, strict):
  if results.rawlen < 2 * nbits + kHeader * 3 + kFooter * 2 - 1:
    return False  # Can't possibly be a valid Samsung A/C message.
  if nbits != kSamsungAcBits and nbits != kSamsungAcExtendedBits:
   return False

  offset = kStartOffset + 1

  # Message Header
  if not matchMark(results.rawbuf[offset], kSamsungAcBitMark):
     return False
  offset += 1
  
  if not matchSpace(results.rawbuf[offset], kSamsungAcHdrSpace):
   return False
   
   
  # Section(s)
  pos = 0
  
  while pos <= (nbits / 8) - kSamsungACSectionLength:
    # Section Header + Section Data (7 bytes) + Section Footer
    used = matchGeneric(results.rawbuf + offset, results.state + pos,
                        results.rawlen - offset, kSamsungACSectionLength * 8,
                        kSamsungAcSectionMark, kSamsungAcSectionSpace,
                        kSamsungAcBitMark, kSamsungAcOneSpace,
                        kSamsungAcBitMark, kSamsungAcZeroSpace,
                        kSamsungAcBitMark, kSamsungAcSectionGap,
                        pos + kSamsungACSectionLength >= nbits / 8,
                        _tolerance, 0, False)
                        
     pos += kSamsungACSectionLength
     
     
    if not used:
       return False
       
    offset += used
    
   
  # Compliance
  # Is the signature correct?

  if results.state[0] != 0x02 or results.state[2] != 0x0F:
     return False
  if strict:
    # Is the checksum valid?
    if not validChecksum(results.state, nbits / 8):
      return False
  
  
  # Success
  results.decode_type = SAMSUNG_AC
  results.bits = nbits
  # No need to record the state as we stored it as we decoded it.
  # As we use result.state, we don't record value, address, or command as it
  # is a union data type.
  return True
  
 
