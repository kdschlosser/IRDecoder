"""

# Copyright 2019 David Conran


from .IRremoteESP8266 import *
from .ir_Amcor import *
from .ir_Argo import *
from .ir_Coolix import *
from .ir_Daikin import *
from .ir_Fujitsu import *
from .ir_Electra import *
from .ir_Goodweather import *
from .ir_Gree import *
from .ir_Haier import *
from .ir_Hitachi import *
from .ir_Kelvinator import *
from .ir_LG import *
from .ir_Midea import *
from .ir_Mitsubishi import *
from .ir_MitsubishiHeavy import *
from .ir_Neoclima import *
from .ir_Panasonic import *
from .ir_Samsung import *
from .ir_Sharp import *
from .ir_Tcl import *
from .ir_Teco import *
from .ir_Toshiba import *
from .ir_Trotec import *
from .ir_Vestel import *
from .ir_Whirlpool import *

# Constants
int8_t kGpioUnused = -1

# Class
class IRac(object):
    
    def __init__(self, pin, inverted=False, use_modulation=True):
    
    
    @staticmethod
    def isProtocolSupported(protocol):
    
    @staticmethod
    def initState(state, vendor, model, power, mode, degrees, celsius, fan, swingv, swingh, quiet, turbo, econo, light, filter, clean, beep, sleep, clock):
    
    @staticmethod
    def initState(state):
    
    
    def sendAc(self):
    
    def sendAc(self, desired, prev=NULL):
    
    def sendAc(self, vendor, model, power, mode, degrees, celsius, fan, swingv, swingh, quiet, turbo, econo, light, filter, clean, beep, sleep=-1, clock=-1):
    
    @staticmethod
    def cmpStates(a, b):
    
    @staticmethod
    def strToBool(str, def=False):
    
    @staticmethod
    def strToModel(str, def=-1):
    
    @staticmethod
    def strToOpmode(str, def=stdAc.opmode_t.kAuto):
    
    @staticmethod
    def strToFanspeed(str, def=stdAc.fanspeed_t.kAuto):
    
    @staticmethod
    def strToSwingV(str, def=stdAc.swingv_t.kOff):
    
    @staticemthod
    def strToSwingH(str, def=stdAc.swingh_t.kOff):
    
    @staticmethod
    def boolToString(value):
    
    @staticmethod
    def opmodeToString(mode):
    
    @staticmethod
    def fanspeedToString(speed):
    
    @staticmethod
    def swingvToString(swingv):
    
    @staticmethod
    def swinghToString(swingh):

    def getState(self):
    
    def getStatePrev(self):
    
    def hasStateChanged(self):
    
    
  stdAc.state_t next  # The state we want the device to be in after we send.

  self._inverted = False
  self._modulation = False
  stdAc.state_t _prev  # The state we expect the device to currently be in.
  
  
#if SEND_AMCOR
  void amcor(IRAmcorAc *ac,
             bool on, stdAc.opmode_t mode, float degrees,
             stdAc.fanspeed_t fan)
#endif  # SEND_AMCOR
#if SEND_ARGO
  void argo(IRArgoAC *ac,
            bool on, stdAc.opmode_t mode, float degrees,
            stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
            bool turbo, int16_t sleep = -1)
#endif  # SEND_ARGO
#if SEND_COOLIX
  void coolix(IRCoolixAC *ac,
              bool on, stdAc.opmode_t mode, float degrees,
              stdAc.fanspeed_t fan,
              stdAc.swingv_t swingv, stdAc.swingh_t swingh,
              bool turbo, bool light, bool clean,
              int16_t sleep = -1)
#endif  # SEND_COOLIX
#if SEND_DAIKIN
  void daikin(IRDaikinESP *ac,
              bool on, stdAc.opmode_t mode, float degrees,
              stdAc.fanspeed_t fan,
              stdAc.swingv_t swingv, stdAc.swingh_t swingh,
              bool quiet, bool turbo, bool econo,
              bool clean)
#endif  # SEND_DAIKIN
#if SEND_DAIKIN128
  void daikin128(IRDaikin128 *ac,
                 bool on, stdAc.opmode_t mode,
                 float degrees, stdAc.fanspeed_t fan,
                 stdAc.swingv_t swingv,
                 bool quiet, bool turbo, bool light,
                 bool econo, int16_t sleep = -1,
                 int16_t clock = -1)
#endif  # SEND_DAIKIN128
#if SEND_DAIKIN152
  void daikin152(IRDaikin152 *ac,
                 bool on, stdAc.opmode_t mode,
                 float degrees, stdAc.fanspeed_t fan,
                 stdAc.swingv_t swingv,
                 bool quiet, bool turbo, bool econo)
#endif  # SEND_DAIKIN152
#if SEND_DAIKIN160
  void daikin160(IRDaikin160 *ac,
                 bool on, stdAc.opmode_t mode,
                 float degrees, stdAc.fanspeed_t fan,
                 stdAc.swingv_t swingv)
#endif  # SEND_DAIKIN160
#if SEND_DAIKIN176
  void daikin176(IRDaikin176 *ac,
                 bool on, stdAc.opmode_t mode,
                 float degrees, stdAc.fanspeed_t fan,
                 stdAc.swingh_t swingh)
#endif  # SEND_DAIKIN176
#if SEND_DAIKIN2
  void daikin2(IRDaikin2 *ac,
               bool on, stdAc.opmode_t mode,
               float degrees, stdAc.fanspeed_t fan,
               stdAc.swingv_t swingv, stdAc.swingh_t swingh,
               bool quiet, bool turbo, bool light,
               bool econo, bool filter, bool clean,
               bool beep, int16_t sleep = -1,
               int16_t clock = -1)
#endif  # SEND_DAIKIN2
#if SEND_DAIKIN216
void daikin216(IRDaikin216 *ac,
               bool on, stdAc.opmode_t mode,
               float degrees, stdAc.fanspeed_t fan,
               stdAc.swingv_t swingv, stdAc.swingh_t swingh,
               bool quiet, bool turbo)
#endif  # SEND_DAIKIN216
#if SEND_ELECTRA_AC
void electra(IRElectraAc *ac,
             bool on, stdAc.opmode_t mode,
             float degrees, stdAc.fanspeed_t fan,
             stdAc.swingv_t swingv,
             stdAc.swingh_t swingh)
#endif  # SEND_ELECTRA_AC
#if SEND_FUJITSU_AC
  void fujitsu(IRFujitsuAC *ac, fujitsu_ac_remote_model_t model,
               bool on, stdAc.opmode_t mode, float degrees,
               stdAc.fanspeed_t fan,
               stdAc.swingv_t swingv, stdAc.swingh_t swingh,
               bool quiet, bool turbo, bool econo,
               bool filter, bool clean)
#endif  # SEND_FUJITSU_AC
#if SEND_GOODWEATHER
  void goodweather(IRGoodweatherAc *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees,
                   stdAc.fanspeed_t fan,
                   stdAc.swingv_t swingv,
                   bool turbo, bool light,
                   int16_t sleep = -1)
#endif  # SEND_GOODWEATHER
#if SEND_GREE
  void gree(IRGreeAC *ac, gree_ac_remote_model_t model,
            bool on, stdAc.opmode_t mode, float degrees,
            stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
            bool turbo, bool light, bool clean,
            int16_t sleep = -1)
#endif  # SEND_GREE
#if SEND_HAIER_AC
  void haier(IRHaierAC *ac,
             bool on, stdAc.opmode_t mode, float degrees,
             stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
             bool filter, int16_t sleep = -1,
             int16_t clock = -1)
#endif  # SEND_HAIER_AC
#if SEND_HAIER_AC_YRW02
  void haierYrwo2(IRHaierACYRW02 *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv,
                  bool turbo, bool filter,
                  int16_t sleep = -1)
#endif  # SEND_HAIER_AC_YRW02
#if SEND_HITACHI_AC
  void hitachi(IRHitachiAc *ac,
               bool on, stdAc.opmode_t mode,
               float degrees, stdAc.fanspeed_t fan,
               stdAc.swingv_t swingv, stdAc.swingh_t swingh)
#endif  # SEND_HITACHI_AC
#if SEND_HITACHI_AC424
  void hitachi424(IRHitachiAc424 *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv)
#endif  # SEND_HITACHI_AC424
#if SEND_KELVINATOR
  void kelvinator(IRKelvinatorAC *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                  bool quiet, bool turbo, bool light,
                  bool filter, bool clean)
#endif  # SEND_KELVINATOR
#if SEND_LG
  void lg(IRLgAc *ac, lg_ac_remote_model_t model,
          bool on, stdAc.opmode_t mode,
          float degrees, stdAc.fanspeed_t fan)
#endif  # SEND_LG
#if SEND_MIDEA
  void midea(IRMideaAC *ac,
             bool on, stdAc.opmode_t mode, bool celsius,
             float degrees, stdAc.fanspeed_t fan,
             stdAc.swingv_t swingv, int16_t sleep = -1)
#endif  # SEND_MIDEA
#if SEND_MITSUBISHI_AC
  void mitsubishi(IRMitsubishiAC *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees,
                  stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                  stdAc.swingh_t swingh,
                  bool quiet, int16_t clock = -1)
#endif  # SEND_MITSUBISHI_AC
#if SEND_MITSUBISHI112
  void mitsubishi112(IRMitsubishi112 *ac,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv,
                     stdAc.swingh_t swingh,
                     bool quiet)
#endif  # SEND_MITSUBISHI112
#if SEND_MITSUBISHI136
  void mitsubishi136(IRMitsubishi136 *ac,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv, bool quiet)
#endif  # SEND_MITSUBISHI136
#if SEND_MITSUBISHIHEAVY
  void mitsubishiHeavy88(IRMitsubishiHeavy88Ac *ac,
                         bool on, stdAc.opmode_t mode,
                         float degrees, stdAc.fanspeed_t fan,
                         stdAc.swingv_t swingv,
                         stdAc.swingh_t swingh,
                         bool turbo, bool econo, bool clean)
  void mitsubishiHeavy152(IRMitsubishiHeavy152Ac *ac,
                          bool on, stdAc.opmode_t mode,
                          float degrees, stdAc.fanspeed_t fan,
                          stdAc.swingv_t swingv,
                          stdAc.swingh_t swingh,
                          bool quiet, bool turbo, bool econo,
                          bool filter, bool clean,
                          int16_t sleep = -1)
#endif  # SEND_MITSUBISHIHEAVY
#if SEND_NEOCLIMA
  void neoclima(IRNeoclimaAc *ac, bool on, stdAc.opmode_t mode,
                float degrees, stdAc.fanspeed_t fan,
                stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                bool turbo, bool light, bool filter,
                int16_t sleep = -1)
#endif  # SEND_NEOCLIMA
#if SEND_PANASONIC_AC
  void panasonic(IRPanasonicAc *ac, panasonic_ac_remote_model_t model,
                 bool on, stdAc.opmode_t mode, float degrees,
                 stdAc.fanspeed_t fan,
                 stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                 bool quiet, bool turbo, int16_t clock = -1)
#endif  # SEND_PANASONIC_AC
#if SEND_SAMSUNG_AC
  void samsung(IRSamsungAc *ac,
               bool on, stdAc.opmode_t mode, float degrees,
               stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
               bool quiet, bool turbo, bool clean,
               bool beep, bool prevpower = True,
               bool forcepower = True)
#endif  # SEND_SAMSUNG_AC
#if SEND_SHARP_AC
  void sharp(IRSharpAc *ac,
             bool on, stdAc.opmode_t mode,
             float degrees, stdAc.fanspeed_t fan)
#endif  # SEND_SHARP_AC
#if SEND_TCL112AC
  void tcl112(IRTcl112Ac *ac,
              bool on, stdAc.opmode_t mode, float degrees,
              stdAc.fanspeed_t fan,
              stdAc.swingv_t swingv, stdAc.swingh_t swingh,
              bool turbo, bool light, bool econo,
              bool filter)
#endif  # SEND_TCL112AC
#if SEND_TECO
  void teco(IRTecoAc *ac,
            bool on, stdAc.opmode_t mode, float degrees,
            stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
            bool light, int16_t sleep = -1)
#endif  # SEND_TECO
#if SEND_TOSHIBA_AC
  void toshiba(IRToshibaAC *ac,
               bool on, stdAc.opmode_t mode, float degrees,
               stdAc.fanspeed_t fan)
#endif  # SEND_TOSHIBA_AC
#if SEND_TROTEC
  void trotec(IRTrotecESP *ac,
              bool on, stdAc.opmode_t mode, float degrees,
              stdAc.fanspeed_t fan, int16_t sleep = -1)
#endif  # SEND_TROTEC
#if SEND_VESTEL_AC
  void vestel(IRVestelAc *ac,
              bool on, stdAc.opmode_t mode, float degrees,
              stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
              bool turbo, bool filter,
              int16_t sleep = -1, int16_t clock = -1,
              bool sendNormal = True)
#endif  # SEND_VESTEL_AC
#if SEND_WHIRLPOOL_AC
  void whirlpool(IRWhirlpoolAc *ac, whirlpool_ac_remote_model_t model,
                 bool on, stdAc.opmode_t mode, float degrees,
                 stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                 bool turbo, bool light,
                 int16_t sleep = -1, int16_t clock = -1)
#endif  # SEND_WHIRLPOOL_AC
static stdAc.state_t cleanState(stdAc.state_t state)
static stdAc.state_t handleToggles(stdAc.state_t desired,
                                    stdAc.state_t *prev = NULL)
}  # IRac class

namespace IRAcUtils {
  String resultAcToString(decode_results * results)
  bool decodeToState(decode_results *decode, stdAc.state_t *result,
                     stdAc.state_t *prev = NULL)
}  # namespace IRAcUtils
#endif  # IRAC_H_

"""
# Copyright 2019 David Conran

# Provide a universal/standard interface for sending A/C nessages.
# It does not provide complete and maximum granular control but tries
# to off most common functionallity across all supported devices.

from .IRac import *
#ifndef UNIT_TEST
#include <Arduino.h>
#endif
#include <string.h>
#ifndef ARDUINO
#include <string>
#endif
from .IRsend import *
from .IRremoteESP8266 import *
from .IRtext import *
from .IRutils import *
from .ir_Amcor import *
from .ir_Argo import *
from .ir_Coolix import *
from .ir_Daikin import *
from .ir_Electra import *
from .ir_Fujitsu import *
from .ir_Haier import *
from .ir_Hitachi import *
from .ir_Kelvinator import *
from .ir_LG import *
from .ir_Midea import *
from .ir_Mitsubishi import *
from .ir_MitsubishiHeavy import *
from .ir_Neoclima import *
from .ir_Panasonic import *
from .ir_Samsung import *
from .ir_Sharp import *
from .ir_Tcl import *
from .ir_Teco import *
from .ir_Toshiba import *
from .ir_Trotec import *
from .ir_Vestel import *
from .ir_Whirlpool import *

IRac.IRac(pin, bool inverted, bool use_modulation) {
  _pin = pin
  _inverted = inverted
  _modulation = use_modulation
  initState(&next)
  _prev = next
}

void IRac.initState(stdAc.state_t *state,
                     decode_type_t vendor, int16_t model,
                     bool power, stdAc.opmode_t mode,
                     float degrees, bool celsius,
                     stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                     bool quiet, bool turbo, bool econo,
                     bool light, bool filter, bool clean,
                     bool beep, int16_t sleep,
                     int16_t clock) {
  state.protocol = vendor
  state.model = model
  state.power = power
  state.mode = mode
  state.degrees = degrees
  state.celsius = celsius
  state.fanspeed = fan
  state.swingv = swingv
  state.swingh = swingh
  state.quiet = quiet
  state.turbo = turbo
  state.econo = econo
  state.light = light
  state.filter = filter
  state.clean = clean
  state.beep = beep
  state.sleep = sleep
  state.clock = clock
}

void IRac.initState(stdAc.state_t *state) {
  initState(state, decode_type_t.UNKNOWN, -1, False, stdAc.opmode_t.kOff,
            25, True,  # 25 degrees Celsius
            stdAc.fanspeed_t.kAuto, stdAc.swingv_t.kOff,
            stdAc.swingh_t.kOff, False, False, False, False, False, False,
            False, -1, -1)
}

stdAc.state_t IRac.getState(void) { return next }

stdAc.state_t IRac.getStatePrev(void) { return _prev }

# Is the given protocol supported by the IRac class?
bool IRac.isProtocolSupported(decode_type_t protocol) {
  switch (protocol) {
#if SEND_AMCOR
    case decode_type_t.AMCOR:
#endif
#if SEND_ARGO
    case decode_type_t.ARGO:
#endif
#if SEND_COOLIX
    case decode_type_t.COOLIX:
#endif
#if SEND_DAIKIN
    case decode_type_t.DAIKIN:
#endif
#if SEND_DAIKIN128
    case decode_type_t.DAIKIN128:
#endif
#if SEND_DAIKIN152
    case decode_type_t.DAIKIN152:
#endif
#if SEND_DAIKIN160
    case decode_type_t.DAIKIN160:
#endif
#if SEND_DAIKIN176
    case decode_type_t.DAIKIN176:
#endif
#if SEND_DAIKIN2
    case decode_type_t.DAIKIN2:
#endif
#if SEND_DAIKIN216
    case decode_type_t.DAIKIN216:
#endif
#if SEND_ELECTRA_AC
    case decode_type_t.ELECTRA_AC:
#endif
#if SEND_FUJITSU_AC
    case decode_type_t.FUJITSU_AC:
#endif
#if SEND_GOODWEATHER
    case decode_type_t.GOODWEATHER:
#endif
#if SEND_GREE
    case decode_type_t.GREE:
#endif
#if SEND_HAIER_AC
    case decode_type_t.HAIER_AC:
#endif
#if SEND_HAIER_AC_YRW02
    case decode_type_t.HAIER_AC_YRW02:
#endif
#if SEND_HITACHI_AC
    case decode_type_t.HITACHI_AC:
#endif
#if SEND_HITACHI_AC424
    case decode_type_t.HITACHI_AC424:
#endif
#if SEND_KELVINATOR
    case decode_type_t.KELVINATOR:
#endif
#if SEND_LG
    case decode_type_t.LG:
    case decode_type_t.LG2:
#endif
#if SEND_MIDEA
    case decode_type_t.MIDEA:
#endif
#if SEND_MITSUBISHI_AC
    case decode_type_t.MITSUBISHI_AC:
#endif
#if SEND_MITSUBISHI112
    case decode_type_t.MITSUBISHI112:
#endif
#if SEND_MITSUBISHI136
    case decode_type_t.MITSUBISHI136:
#endif
#if SEND_MITSUBISHIHEAVY
    case decode_type_t.MITSUBISHI_HEAVY_88:
    case decode_type_t.MITSUBISHI_HEAVY_152:
#endif
#if SEND_NEOCLIMA
    case decode_type_t.NEOCLIMA:
#endif
#if SEND_PANASONIC_AC
    case decode_type_t.PANASONIC_AC:
#endif
#if SEND_SAMSUNG_AC
    case decode_type_t.SAMSUNG_AC:
#endif
#if SEND_SHARP_AC
    case decode_type_t.SHARP_AC:
#endif
#if SEND_TCL112AC
    case decode_type_t.TCL112AC:
#endif
#if SEND_TECO
    case decode_type_t.TECO:
#endif
#if SEND_TOSHIBA_AC
    case decode_type_t.TOSHIBA_AC:
#endif
#if SEND_TROTEC
    case decode_type_t.TROTEC:
#endif
#if SEND_VESTEL_AC
    case decode_type_t.VESTEL_AC:
#endif
#if SEND_WHIRLPOOL_AC
    case decode_type_t.WHIRLPOOL_AC:
#endif
      return True
    default:
      return False
  }
}

#if SEND_AMCOR
void IRac.amcor(IRAmcorAc *ac,
                bool on, stdAc.opmode_t mode, float degrees,
                stdAc.fanspeed_t fan) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  # No Swing setting available.
  # No Quiet setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Turbo setting available.
  # No Economy setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  ac.send()
}
#endif  # SEND_AMCOR

#if SEND_ARGO
void IRac.argo(IRArgoAC *ac,
                bool on, stdAc.opmode_t mode, float degrees,
                stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                bool turbo, int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setFlap(ac.convertSwingV(swingv))
  # No Quiet setting available.
  # No Light setting available.
  # No Filter setting available.
  ac.setMax(turbo)
  # No Economy setting available.
  # No Clean setting available.
  # No Beep setting available.
  ac.setNight(sleep >= 0)  # Convert to a boolean.
  ac.send()
}
#endif  # SEND_ARGO

#if SEND_COOLIX
void IRac.coolix(IRCoolixAC *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                  bool turbo, bool light, bool clean,
                  int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  if (!on) {
      # after turn off AC no more commands should
      # be accepted
      ac.send()
      return
  }
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  # No Filter setting available.
  # No Beep setting available.
  # No Clock setting available.
  # No Econo setting available.
  # No Quiet setting available.
  if (swingv != stdAc.swingv_t.kOff or swingh != stdAc.swingh_t.kOff) {
    # Swing has a special command that needs to be sent independently.
    ac.setSwing()
    ac.send()
  }
  if (turbo) {
    # Turbo has a special command that needs to be sent independently.
    ac.setTurbo()
    ac.send()
  }
  if (sleep > 0) {
    # Sleep has a special command that needs to be sent independently.
    ac.setSleep()
    ac.send()
  }
  if (light) {
    # Light has a special command that needs to be sent independently.
    ac.setLed()
    ac.send()
  }
  if (clean) {
    # Clean has a special command that needs to be sent independently.
    ac.setClean()
    ac.send()
  }
  ac.send()
}
#endif  # SEND_COOLIX

#if SEND_DAIKIN
void IRac.daikin(IRDaikinESP *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                  bool quiet, bool turbo, bool econo,
                  bool clean) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical((int8_t)swingv >= 0)
  ac.setSwingHorizontal((int8_t)swingh >= 0)
  ac.setQuiet(quiet)
  # No Light setting available.
  # No Filter setting available.
  ac.setPowerful(turbo)
  ac.setEcono(econo)
  ac.setMold(clean)
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_DAIKIN

#if SEND_DAIKIN128
void IRac.daikin128(IRDaikin128 *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv,
                  bool quiet, bool turbo, bool light,
                  bool econo, int16_t sleep, int16_t clock) {
  ac.begin()
  ac.setPowerToggle(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical((int8_t)swingv >= 0)
  # No Horizontal Swing setting avaliable.
  ac.setQuiet(quiet)
  ac.setLightToggle(light ? kDaikin128BitWall : 0)
  # No Filter setting available.
  ac.setPowerful(turbo)
  ac.setEcono(econo)
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep > 0)
  if (clock >= 0) ac.setClock(clock)
  ac.send()
}
#endif  # SEND_DAIKIN128

#if SEND_DAIKIN152
void IRac.daikin152(IRDaikin152 *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv,
                  bool quiet, bool turbo, bool econo) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingV((int8_t)swingv >= 0)
  # No Horizontal Swing setting avaliable.
  ac.setQuiet(quiet)
  # No Light setting available.
  # No Filter setting available.
  ac.setPowerful(turbo)
  ac.setEcono(econo)
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_DAIKIN152

#if SEND_DAIKIN160
void IRac.daikin160(IRDaikin160 *ac,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(ac.convertSwingV(swingv))
  ac.send()
}
#endif  # SEND_DAIKIN160

#if SEND_DAIKIN176
void IRac.daikin176(IRDaikin176 *ac,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingh_t swingh) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingHorizontal(ac.convertSwingH(swingh))
  ac.send()
}
#endif  # SEND_DAIKIN176

#if SEND_DAIKIN2
void IRac.daikin2(IRDaikin2 *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees, stdAc.fanspeed_t fan,
                   stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                   bool quiet, bool turbo, bool light,
                   bool econo, bool filter, bool clean,
                   bool beep, int16_t sleep, int16_t clock) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(ac.convertSwingV(swingv))
  ac.setSwingHorizontal(ac.convertSwingH(swingh))
  ac.setQuiet(quiet)
  ac.setLight(light ? 1 : 3)  # On/High is 1, Off is 3.
  ac.setPowerful(turbo)
  ac.setEcono(econo)
  ac.setPurify(filter)
  ac.setMold(clean)
  ac.setClean(True)  # Hardwire auto clean to be on per request (@sheppy99)
  ac.setBeep(beep ? 2 : 3)  # On/Loud is 2, Off is 3.
  if (sleep > 0) ac.enableSleepTimer(sleep)
  if (clock >= 0) ac.setCurrentTime(clock)
  ac.send()
}
#endif  # SEND_DAIKIN2

#if SEND_DAIKIN216
void IRac.daikin216(IRDaikin216 *ac,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                     bool quiet, bool turbo) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical((int8_t)swingv >= 0)
  ac.setSwingHorizontal((int8_t)swingh >= 0)
  ac.setQuiet(quiet)
  ac.setPowerful(turbo)
  ac.send()
}
#endif  # SEND_DAIKIN216

#if SEND_ELECTRA_AC
void IRac.electra(IRElectraAc *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees, stdAc.fanspeed_t fan,
                   stdAc.swingv_t swingv,
                   stdAc.swingh_t swingh) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingV(swingv != stdAc.swingv_t.kOff)
  ac.setSwingH(swingh != stdAc.swingh_t.kOff)
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Econo setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_ELECTRA_AC

#if SEND_FUJITSU_AC
void IRac.fujitsu(IRFujitsuAC *ac, fujitsu_ac_remote_model_t model,
                   bool on, stdAc.opmode_t mode,
                   float degrees, stdAc.fanspeed_t fan,
                   stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                   bool quiet, bool turbo, bool econo,
                   bool filter, bool clean) {
  ac.begin()
  ac.setModel(model)
  if (on) {
    # Do all special messages (except "Off") first,
    # These need to be sent separately.
    switch (ac.getModel()) {
      # Some functions are only available on some models.
      case fujitsu_ac_remote_model_t.ARREB1E:
        if (turbo) {
          ac.setCmd(kFujitsuAcCmdPowerful)
          # Powerful is a separate command.
          ac.send()
        }
        if (econo) {
          ac.setCmd(kFujitsuAcCmdEcono)
          # Econo is a separate command.
          ac.send()
        }
        break
      default:
        {}
    }
    # Normal operation.
    ac.setMode(ac.convertMode(mode))
    ac.setTemp(degrees)
    ac.setFanSpeed(ac.convertFan(fan))
    swing = kFujitsuAcSwingOff
    if (swingv > stdAc.swingv_t.kOff) swing |= kFujitsuAcSwingVert
    if (swingh > stdAc.swingh_t.kOff) swing |= kFujitsuAcSwingHoriz
    ac.setSwing(swing)
    if (quiet) ac.setFanSpeed(kFujitsuAcFanQuiet)
    # No Light setting available.
    ac.setFilter(filter)
    ac.setClean(clean)
    # No Beep setting available.
    # No Sleep setting available.
    # No Clock setting available.
    ac.on()  # Ref: Issue #860
  } else {
    # Off is special case/message. We don't need to send other messages.
    ac.off()
  }
  ac.send()
}
#endif  # SEND_FUJITSU_AC

#if SEND_GOODWEATHER
void IRac.goodweather(IRGoodweatherAc *ac,
                       bool on, stdAc.opmode_t mode,
                       float degrees,
                       stdAc.fanspeed_t fan,
                       stdAc.swingv_t swingv,
                       bool turbo, bool light,
                       int16_t sleep) {
  ac.begin()
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(swingv == stdAc.swingv_t.kOff ? kGoodweatherSwingOff
                                               : kGoodweatherSwingSlow)
  ac.setTurbo(turbo)
  ac.setLight(light)
  # No Clean setting available.
  ac.setSleep(sleep >= 0)  # Sleep on this A/C is either on or off.
  # No Horizontal Swing setting available.
  # No Econo setting available.
  # No Filter setting available.
  # No Beep setting available.
  # No Quiet setting available.
  # No Clock setting available.
  ac.setPower(on)
  ac.send()
}
#endif  # SEND_GOODWEATHER

#if SEND_GREE
void IRac.gree(IRGreeAC *ac, gree_ac_remote_model_t model,
                bool on, stdAc.opmode_t mode, float degrees,
                stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                bool turbo, bool light, bool clean,
                int16_t sleep) {
  ac.begin()
  ac.setModel(model)
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(swingv == stdAc.swingv_t.kAuto,  # Set auto flag.
                       ac.convertSwingV(swingv))
  ac.setLight(light)
  ac.setTurbo(turbo)
  ac.setXFan(clean)
  ac.setSleep(sleep >= 0)  # Sleep on this A/C is either on or off.
  # No Horizontal Swing setting available.
  # No Econo setting available.
  # No Filter setting available.
  # No Beep setting available.
  # No Quiet setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_GREE

#if SEND_HAIER_AC
void IRac.haier(IRHaierAC *ac,
                 bool on, stdAc.opmode_t mode, float degrees,
                 stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                 bool filter, int16_t sleep, int16_t clock) {
  ac.begin()
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(ac.convertSwingV(swingv))
  # No Horizontal Swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  ac.setHealth(filter)
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep on this A/C is either on or off.
  if (clock >=0) ac.setCurrTime(clock)
  if (on)
    ac.setCommand(kHaierAcCmdOn)
  else
    ac.setCommand(kHaierAcCmdOff)
  ac.send()
}
#endif  # SEND_HAIER_AC

#if SEND_HAIER_AC_YRW02
void IRac.haierYrwo2(IRHaierACYRW02 *ac,
                      bool on, stdAc.opmode_t mode,
                      float degrees, stdAc.fanspeed_t fan,
                      stdAc.swingv_t swingv, bool turbo,
                      bool filter, int16_t sleep) {
  ac.begin()
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(ac.convertSwingV(swingv))
  # No Horizontal Swing setting available.
  # No Quiet setting available.
  ac.setTurbo(turbo)
  # No Light setting available.
  ac.setHealth(filter)
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep on this A/C is either on or off.
  ac.setPower(on)
  ac.send()
}
#endif  # SEND_HAIER_AC_YRW02

#if SEND_HITACHI_AC
void IRac.hitachi(IRHitachiAc *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees, stdAc.fanspeed_t fan,
                   stdAc.swingv_t swingv, stdAc.swingh_t swingh) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(swingv != stdAc.swingv_t.kOff)
  ac.setSwingHorizontal(swingh != stdAc.swingh_t.kOff)
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_HITACHI_AC

#if SEND_HITACHI_AC424
void IRac.hitachi424(IRHitachiAc424 *ac,
                      bool on, stdAc.opmode_t mode,
                      float degrees, stdAc.fanspeed_t fan,
                      stdAc.swingv_t swingv) {
  ac.begin()
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setPower(on)
  # SwingVToggle is special. Needs to be last method called.
  ac.setSwingVToggle(swingv != stdAc.swingv_t.kOff)
  # No Swing(H) setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_HITACHI_AC424

#if SEND_KELVINATOR
void IRac.kelvinator(IRKelvinatorAC *ac,
                      bool on, stdAc.opmode_t mode,
                      float degrees, stdAc.fanspeed_t fan,
                      stdAc.swingv_t swingv,
                      stdAc.swingh_t swingh,
                      bool quiet, bool turbo, bool light,
                      bool filter, bool clean) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan((uint8_t)fan)  # No conversion needed.
  ac.setSwingVertical((int8_t)swingv >= 0)
  ac.setSwingHorizontal((int8_t)swingh >= 0)
  ac.setQuiet(quiet)
  ac.setTurbo(turbo)
  ac.setLight(light)
  ac.setIonFilter(filter)
  ac.setXFan(clean)
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_KELVINATOR

#if SEND_LG
void IRac.lg(IRLgAc *ac, lg_ac_remote_model_t model,
              bool on, stdAc.opmode_t mode,
              float degrees, stdAc.fanspeed_t fan) {
  ac.begin()
  ac.setModel(model)
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  # No Vertical swing setting available.
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_LG

#if SEND_MIDEA
void IRac.midea(IRMideaAC *ac,
                 bool on, stdAc.opmode_t mode, bool celsius,
                 float degrees, stdAc.fanspeed_t fan,
                 stdAc.swingv_t swingv, int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setUseCelsius(celsius)
  ac.setTemp(degrees, celsius)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVToggle(swingv != stdAc.swingv_t.kOff)
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep on this A/C is either on or off.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_MIDEA

#if SEND_MITSUBISHI_AC
void IRac.mitsubishi(IRMitsubishiAC *ac,
                      bool on, stdAc.opmode_t mode,
                      float degrees,
                      stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                      stdAc.swingh_t swingh,
                      bool quiet, int16_t clock) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setVane(ac.convertSwingV(swingv))
  ac.setWideVane(ac.convertSwingH(swingh))
  if (quiet) ac.setFan(kMitsubishiAcFanSilent)
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  if (clock >= 0) ac.setClock(clock / 10)  # Clock is in 10 min increments.
  ac.send()
}
#endif  # SEND_MITSUBISHI_AC

#if SEND_MITSUBISHI112
void IRac.mitsubishi112(IRMitsubishi112 *ac,
                         bool on, stdAc.opmode_t mode,
                         float degrees, stdAc.fanspeed_t fan,
                         stdAc.swingv_t swingv,
                         stdAc.swingh_t swingh,
                         bool quiet) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingV(ac.convertSwingV(swingv))
  ac.setSwingH(ac.convertSwingH(swingh))
  ac.setQuiet(quiet)
  # FIXME - Econo
  # ac.setEcono(econo)
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_MITSUBISHI112

#if SEND_MITSUBISHI136
void IRac.mitsubishi136(IRMitsubishi136 *ac,
                         bool on, stdAc.opmode_t mode,
                         float degrees, stdAc.fanspeed_t fan,
                         stdAc.swingv_t swingv, bool quiet) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingV(ac.convertSwingV(swingv))
  # No Horizontal Swing setting available.
  ac.setQuiet(quiet)
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_MITSUBISHI136

#if SEND_MITSUBISHIHEAVY
void IRac.mitsubishiHeavy88(IRMitsubishiHeavy88Ac *ac,
                             bool on, stdAc.opmode_t mode,
                             float degrees,
                             stdAc.fanspeed_t fan,
                             stdAc.swingv_t swingv,
                             stdAc.swingh_t swingh,
                             bool turbo, bool econo,
                             bool clean) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(ac.convertSwingV(swingv))
  ac.setSwingHorizontal(ac.convertSwingH(swingh))
  # No Quiet setting available.
  ac.setTurbo(turbo)
  # No Light setting available.
  ac.setEcono(econo)
  # No Filter setting available.
  ac.setClean(clean)
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}

void IRac.mitsubishiHeavy152(IRMitsubishiHeavy152Ac *ac,
                              bool on, stdAc.opmode_t mode,
                              float degrees,
                              stdAc.fanspeed_t fan,
                              stdAc.swingv_t swingv,
                              stdAc.swingh_t swingh,
                              bool quiet, bool turbo,
                              bool econo, bool filter,
                              bool clean, int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(ac.convertSwingV(swingv))
  ac.setSwingHorizontal(ac.convertSwingH(swingh))
  ac.setSilent(quiet)
  ac.setTurbo(turbo)
  # No Light setting available.
  ac.setEcono(econo)
  ac.setClean(clean)
  ac.setFilter(filter)
  # No Beep setting available.
  ac.setNight(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_MITSUBISHIHEAVY

#if SEND_NEOCLIMA
void IRac.neoclima(IRNeoclimaAc *ac,
                    bool on, stdAc.opmode_t mode,
                    float degrees, stdAc.fanspeed_t fan,
                    stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                    bool turbo, bool light, bool filter,
                    int16_t sleep) {
  ac.begin()
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingV(swingv != stdAc.swingv_t.kOff)
  ac.setSwingH(swingh != stdAc.swingh_t.kOff)
  # No Quiet setting available.
  ac.setTurbo(turbo)
  ac.setLight(light)
  # No Econo setting available.
  ac.setIon(filter)
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  # No Clock setting available.
  ac.setPower(on)
  ac.send()
}
#endif  # SEND_NEOCLIMA

#if SEND_PANASONIC_AC
void IRac.panasonic(IRPanasonicAc *ac, panasonic_ac_remote_model_t model,
                     bool on, stdAc.opmode_t mode,
                     float degrees, stdAc.fanspeed_t fan,
                     stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                     bool quiet, bool turbo, int16_t clock) {
  ac.begin()
  ac.setModel(model)
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(ac.convertSwingV(swingv))
  ac.setSwingHorizontal(ac.convertSwingH(swingh))
  ac.setQuiet(quiet)
  ac.setPowerful(turbo)
  # No Light setting available.
  # No Econo setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  if (clock >= 0) ac.setClock(clock)
  ac.send()
}
#endif  # SEND_PANASONIC_AC

#if SEND_SAMSUNG_AC
void IRac.samsung(IRSamsungAc *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees,
                   stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                   bool quiet, bool turbo, bool clean,
                   bool beep, bool prevpower,
                   bool forcepower) {
  ac.begin()
  ac.stateReset(forcepower, prevpower)
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(swingv != stdAc.swingv_t.kOff)
  # No Horizontal swing setting available.
  ac.setQuiet(quiet)
  ac.setPowerful(turbo)
  # No Light setting available.
  # No Econo setting available.
  # No Filter setting available.
  ac.setClean(clean)
  ac.setBeep(beep)
  # No Sleep setting available.
  # No Clock setting available.
  # Do setMode() again as it can affect fan speed.
  ac.setMode(ac.convertMode(mode))
  ac.send()
}
#endif  # SEND_SAMSUNG_AC

#if SEND_SHARP_AC
void IRac.sharp(IRSharpAc *ac,
                 bool on, stdAc.opmode_t mode,
                 float degrees, stdAc.fanspeed_t fan) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  # No Vertical swing setting available.
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Econo setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  # Do setMode() again as it can affect fan speed and temp.
  ac.setMode(ac.convertMode(mode))
  ac.send()
}
#endif  # SEND_SHARP_AC

#if SEND_TCL112AC
void IRac.tcl112(IRTcl112Ac *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                  bool turbo, bool light, bool econo,
                  bool filter) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwingVertical(swingv != stdAc.swingv_t.kOff)
  ac.setSwingHorizontal(swingh != stdAc.swingh_t.kOff)
  # No Quiet setting available.
  ac.setTurbo(turbo)
  ac.setLight(light)
  ac.setEcono(econo)
  ac.setHealth(filter)
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_TCL112AC

#if SEND_TECO
void IRac.teco(IRTecoAc *ac,
                bool on, stdAc.opmode_t mode, float degrees,
                stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                bool light, int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(swingv != stdAc.swingv_t.kOff)
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  ac.setLight(light)
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_TECO

#if SEND_TOSHIBA_AC
void IRac.toshiba(IRToshibaAC *ac,
                   bool on, stdAc.opmode_t mode,
                   float degrees, stdAc.fanspeed_t fan) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  # No Vertical swing setting available.
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  # No Sleep setting available.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_TOSHIBA_AC

#if SEND_TROTEC
void IRac.trotec(IRTrotecESP *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees, stdAc.fanspeed_t fan,
                  int16_t sleep) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setSpeed(ac.convertFan(fan))
  # No Vertical swing setting available.
  # No Horizontal swing setting available.
  # No Quiet setting available.
  # No Turbo setting available.
  # No Light setting available.
  # No Filter setting available.
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  # No Clock setting available.
  ac.send()
}
#endif  # SEND_TROTEC

#if SEND_VESTEL_AC
void IRac.vestel(IRVestelAc *ac,
                  bool on, stdAc.opmode_t mode,
                  float degrees,
                  stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                  bool turbo, bool filter, int16_t sleep,
                  int16_t clock, bool sendNormal) {
  ac.begin()
  ac.setPower(on)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(swingv != stdAc.swingv_t.kOff)
  # No Horizontal swing setting available.
  # No Quiet setting available.
  ac.setTurbo(turbo)
  # No Light setting available.
  ac.setIon(filter)
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  if (sendNormal) ac.send()  # Send the normal message.
  if (clock >= 0) {
    ac.setTime(clock)
    ac.send()  # Setting the clock requires a different "timer" message.
  }
}
#endif  # SEND_VESTEL_AC

#if SEND_WHIRLPOOL_AC
void IRac.whirlpool(IRWhirlpoolAc *ac, whirlpool_ac_remote_model_t model,
                     bool on, stdAc.opmode_t mode,
                     float degrees,
                     stdAc.fanspeed_t fan, stdAc.swingv_t swingv,
                     bool turbo, bool light,
                     int16_t sleep, int16_t clock) {
  ac.begin()
  ac.setModel(model)
  ac.setMode(ac.convertMode(mode))
  ac.setTemp(degrees)
  ac.setFan(ac.convertFan(fan))
  ac.setSwing(swingv != stdAc.swingv_t.kOff)
  # No Horizontal swing setting available.
  # No Quiet setting available.
  ac.setSuper(turbo)
  ac.setLight(light)
  # No Filter setting available
  # No Clean setting available.
  # No Beep setting available.
  ac.setSleep(sleep >= 0)  # Sleep is either on/off, so convert to boolean.
  if (clock >= 0) ac.setClock(clock)
  ac.setPowerToggle(on)
  ac.send()
}
#endif  # SEND_WHIRLPOOL_AC

# Create a new state base on the provided state that has been suitably fixed.
# Args:
#   state: The state_t structure describing the desired a/c state.
#
# Returns:
#   A stdAc.state_t with the needed settings.
stdAc.state_t IRac.cleanState(stdAc.state_t state) {
  stdAc.state_t result = state
  # A hack for Home Assistant, it appears to need/want an Off opmode.
  # So enforce the power is off if the mode is also off.
  if (state.mode == stdAc.opmode_t.kOff) result.power = False
  return result
}

# Create a new state base on desired & previous states but handle
# any state changes for options that need to be toggled.
# Args:
#   desired: The state_t structure describing the desired a/c state.
#   prev:    Ptr to the previous state_t structure.
#
# Returns:
#   A stdAc.state_t with the needed settings.
stdAc.state_t IRac.handleToggles(stdAc.state_t desired,
                                   stdAc.state_t *prev) {
  stdAc.state_t result = desired
  # If we've been given a previous state AND the it's the same A/C basically.
  if (prev != NULL and desired.protocol == prev.protocol and
      desired.model == prev.model) {
    # Check if we have to handle toggle settings for specific A/C protocols.
    switch (desired.protocol) {
      case decode_type_t.COOLIX:
        if ((desired.swingv == stdAc.swingv_t.kOff) ^
            (prev.swingv == stdAc.swingv_t.kOff))  # It changed, so toggle.
          result.swingv = stdAc.swingv_t.kAuto
        else
          result.swingv = stdAc.swingv_t.kOff  # No change, so no toggle.
        result.turbo = desired.turbo ^ prev.turbo
        result.light = desired.light ^ prev.light
        result.clean = desired.clean ^ prev.clean
        result.sleep = ((desired.sleep >= 0) ^ (prev.sleep >= 0)) ? 0 : -1
        break
      case decode_type_t.DAIKIN128:
        result.power = desired.power ^ prev.power
        result.light = desired.light ^ prev.light
        break
      case decode_type_t.MIDEA:
      case decode_type_t.HITACHI_AC424:
        if ((desired.swingv == stdAc.swingv_t.kOff) ^
            (prev.swingv == stdAc.swingv_t.kOff))  # It changed, so toggle.
          result.swingv = stdAc.swingv_t.kAuto
        else
          result.swingv = stdAc.swingv_t.kOff  # No change, so no toggle.
        break
      case decode_type_t.WHIRLPOOL_AC:
        result.power = desired.power ^ prev.power
        break
      case decode_type_t.PANASONIC_AC:
        # CKP models use a power mode toggle.
        if (desired.model == panasonic_ac_remote_model_t.kPanasonicCkp)
          result.power = desired.power ^ prev.power
        break
      default:
        {}
    }
  }
  return result
}

# Send A/C message for a given device using common A/C settings.
# Args:
#   vendor:  The type of A/C protocol to use.
#   model:   The specific model of A/C if supported/applicable.
#   on:      Should the unit be powered on? (or in some cases, toggled)
#   mode:    What operating mode should the unit perform? e.g. Cool, Heat etc.
#   degrees: What temperature should the unit be set to?
#   celsius: Use degrees Celsius, otherwise Fahrenheit.
#   fan:     Fan speed.
# The following args are all "if supported" by the underlying A/C classes.
#   swingv:  Control the vertical swing of the vanes.
#   swingh:  Control the horizontal swing of the vanes.
#   quiet:   Set the unit to quiet (fan) operation mode.
#   turbo:   Set the unit to turbo operating mode. e.g. Max fan & cooling etc.
#   econo:   Set the unit to economical operating mode.
#   light:   Turn on the display/LEDs etc.
#   filter:  Turn on any particle/ion/allergy filter etc.
#   clean:   Turn on any settings to reduce mold etc. (Not self-clean mode.)
#   beep:    Control if the unit beeps upon receiving commands.
#   sleep:   Nr. of mins of sleep mode, or use sleep mode. (< 0 means off.)
#   clock:   Nr. of mins past midnight to set the clock to. (< 0 means off.)
# Returns:
#   boolean: True, if accepted/converted/attempted. False, if unsupported.
bool IRac.sendAc(decode_type_t vendor, int16_t model,
                  bool power, stdAc.opmode_t mode,
                  float degrees, bool celsius,
                  stdAc.fanspeed_t fan,
                  stdAc.swingv_t swingv, stdAc.swingh_t swingh,
                  bool quiet, bool turbo, bool econo,
                  bool light, bool filter, bool clean,
                  bool beep, int16_t sleep, int16_t clock) {
  stdAc.state_t to_send
  initState(&to_send, vendor, model, power, mode, degrees, celsius, fan, swingv,
            swingh, quiet, turbo, econo, light, filter, clean, beep, sleep,
            clock)
  return this.sendAc(to_send, &to_send)
}

# Send A/C message for a given device using state_t structures.
# Args:
#   desired: The state_t structure describing the desired new a/c state.
#   prev:    Ptr to the previous state_t structure.
#
# Returns:
#   boolean: True, if accepted/converted/attempted. False, if unsupported.
bool IRac.sendAc(stdAc.state_t desired, stdAc.state_t *prev) {
  # Convert the temp from Fahrenheit to Celsius if we are not in Celsius mode.
  float degC = desired.celsius ? desired.degrees
                               : fahrenheitToCelsius(desired.degrees)
  # special `state_t` that is required to be sent based on that.
  stdAc.state_t send = this.handleToggles(this.cleanState(desired), prev)
  # Per vendor settings & setup.
  switch (send.protocol) {
#if SEND_AMCOR
    case AMCOR:
    {
      IRAmcorAc ac(_pin, _inverted, _modulation)
      amcor(&ac, send.power, send.mode, degC, send.fanspeed)
      break
    }
#endif  # SEND_AMCOR
#if SEND_ARGO
    case ARGO:
    {
      IRArgoAC ac(_pin, _inverted, _modulation)
      argo(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
           send.turbo, send.sleep)
      break
    }
#endif  # SEND_ARGO
#if SEND_COOLIX
    case COOLIX:
    {
      IRCoolixAC ac(_pin, _inverted, _modulation)
      coolix(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
             send.swingh, send.turbo, send.light, send.clean, send.sleep)
      break
    }
#endif  # SEND_COOLIX
#if SEND_DAIKIN
    case DAIKIN:
    {
      IRDaikinESP ac(_pin, _inverted, _modulation)
      daikin(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
             send.swingh, send.quiet, send.turbo, send.econo, send.clean)
      break
    }
#endif  # SEND_DAIKIN
#if SEND_DAIKIN128
    case DAIKIN128:
    {
      IRDaikin128 ac(_pin, _inverted, _modulation)
      daikin128(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                send.quiet, send.turbo, send.light, send.econo, send.sleep,
                send.clock)
      break
    }
#endif  # SEND_DAIKIN2
#if SEND_DAIKIN152
    case DAIKIN152:
    {
      IRDaikin152 ac(_pin, _inverted, _modulation)
      daikin152(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                send.quiet, send.turbo, send.econo)
      break
    }
#endif  # SEND_DAIKIN152
#if SEND_DAIKIN160
    case DAIKIN160:
    {
      IRDaikin160 ac(_pin, _inverted, _modulation)
      daikin160(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv)
      break
    }
#endif  # SEND_DAIKIN160
#if SEND_DAIKIN176
    case DAIKIN176:
    {
      IRDaikin176 ac(_pin, _inverted, _modulation)
      daikin176(&ac, send.power, send.mode, degC, send.fanspeed, send.swingh)
      break
    }
#endif  # SEND_DAIKIN176
#if SEND_DAIKIN2
    case DAIKIN2:
    {
      IRDaikin2 ac(_pin, _inverted, _modulation)
      daikin2(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
              send.swingh, send.quiet, send.turbo, send.light, send.econo,
              send.filter, send.clean, send.beep, send.sleep, send.clock)
      break
    }
#endif  # SEND_DAIKIN2
#if SEND_DAIKIN216
    case DAIKIN216:
    {
      IRDaikin216 ac(_pin, _inverted, _modulation)
      daikin216(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                send.swingh, send.quiet, send.turbo)
      break
    }
#endif  # SEND_DAIKIN216
#if SEND_ELECTRA_AC
    case ELECTRA_AC:
    {
      IRElectraAc ac(_pin, _inverted, _modulation)
      electra(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
              send.swingh)
      break
    }
#endif  # SEND_ELECTRA_AC
#if SEND_FUJITSU_AC
    case FUJITSU_AC:
    {
      IRFujitsuAC ac(_pin, (fujitsu_ac_remote_model_t)send.model, _inverted,
                     _modulation)
      fujitsu(&ac, (fujitsu_ac_remote_model_t)send.model, send.power, send.mode,
              degC, send.fanspeed, send.swingv, send.swingh, send.quiet,
              send.turbo, send.econo, send.filter, send.clean)
      break
    }
#endif  # SEND_FUJITSU_AC
#if SEND_GOODWEATHER
    case GOODWEATHER:
    {
      IRGoodweatherAc ac(_pin, _inverted, _modulation)
      goodweather(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                  send.turbo, send.light, send.sleep)
      break
    }
#endif  # SEND_GOODWEATHER
#if SEND_GREE
    case GREE:
    {
      IRGreeAC ac(_pin, (gree_ac_remote_model_t)send.model, _inverted,
                  _modulation)
      gree(&ac, (gree_ac_remote_model_t)send.model, send.power, send.mode, degC,
           send.fanspeed, send.swingv, send.turbo, send.light, send.clean,
           send.sleep)
      break
    }
#endif  # SEND_GREE
#if SEND_HAIER_AC
    case HAIER_AC:
    {
      IRHaierAC ac(_pin, _inverted, _modulation)
      haier(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
            send.filter, send.sleep, send.clock)
      break
    }
#endif  # SEND_HAIER_AC
#if SEND_HAIER_AC_YRW02
    case HAIER_AC_YRW02:
    {
      IRHaierACYRW02 ac(_pin, _inverted, _modulation)
      haierYrwo2(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                 send.turbo, send.filter, send.sleep)
      break
    }
#endif  # SEND_HAIER_AC_YRW02
#if SEND_HITACHI_AC
    case HITACHI_AC:
    {
      IRHitachiAc ac(_pin, _inverted, _modulation)
      hitachi(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
              send.swingh)
      break
    }
#endif  # SEND_HITACHI_AC
#if SEND_HITACHI_AC424
    case HITACHI_AC424:
    {
      IRHitachiAc424 ac(_pin, _inverted, _modulation)
      hitachi424(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv)
      break
    }
#endif  # SEND_HITACHI_AC424
#if SEND_KELVINATOR
    case KELVINATOR:
    {
      IRKelvinatorAC ac(_pin, _inverted, _modulation)
      kelvinator(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                 send.swingh, send.quiet, send.turbo, send.light, send.filter,
                 send.clean)
      break
    }
#endif  # SEND_KELVINATOR
#if SEND_LG
    case LG:
    case LG2:
    {
      IRLgAc ac(_pin, _inverted, _modulation)
      lg(&ac, (lg_ac_remote_model_t)send.model, send.power, send.mode,
         send.degrees, send.fanspeed)
      break
    }
#endif  # SEND_LG
#if SEND_MIDEA
    case MIDEA:
    {
      IRMideaAC ac(_pin, _inverted, _modulation)
      midea(&ac, send.power, send.mode, send.celsius, send.degrees,
            send.fanspeed, send.swingv, send.sleep)
      break
    }
#endif  # SEND_MIDEA
#if SEND_MITSUBISHI_AC
    case MITSUBISHI_AC:
    {
      IRMitsubishiAC ac(_pin, _inverted, _modulation)
      mitsubishi(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
                 send.swingh, send.quiet, send.clock)
      break
    }
#endif  # SEND_MITSUBISHI_AC
#if SEND_MITSUBISHI112
    case MITSUBISHI112:
    {
      IRMitsubishi112 ac(_pin, _inverted, _modulation)
      mitsubishi112(&ac, send.power, send.mode, degC, send.fanspeed,
                    send.swingv, send.swingh, send.quiet)
      break
    }
#endif  # SEND_MITSUBISHI112
#if SEND_MITSUBISHI136
    case MITSUBISHI136:
    {
      IRMitsubishi136 ac(_pin, _inverted, _modulation)
      mitsubishi136(&ac, send.power, send.mode, degC, send.fanspeed,
                    send.swingv, send.quiet)
      break
    }
#endif  # SEND_MITSUBISHI136
#if SEND_MITSUBISHIHEAVY
    case MITSUBISHI_HEAVY_88:
    {
      IRMitsubishiHeavy88Ac ac(_pin, _inverted, _modulation)
      mitsubishiHeavy88(&ac, send.power, send.mode, degC, send.fanspeed,
                        send.swingv, send.swingh, send.turbo, send.econo,
                        send.clean)
      break
    }
    case MITSUBISHI_HEAVY_152:
    {
      IRMitsubishiHeavy152Ac ac(_pin, _inverted, _modulation)
      mitsubishiHeavy152(&ac, send.power, send.mode, degC, send.fanspeed,
                         send.swingv, send.swingh, send.quiet, send.turbo,
                         send.econo, send.filter, send.clean, send.sleep)
      break
    }
#endif  # SEND_MITSUBISHIHEAVY
#if SEND_NEOCLIMA
    case NEOCLIMA:
    {
      IRNeoclimaAc ac(_pin, _inverted, _modulation)
      neoclima(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
               send.swingh, send.turbo, send.light, send.filter, send.sleep)
      break
    }
#endif  # SEND_NEOCLIMA
#if SEND_PANASONIC_AC
    case PANASONIC_AC:
    {
      IRPanasonicAc ac(_pin, _inverted, _modulation)
      panasonic(&ac, (panasonic_ac_remote_model_t)send.model, send.power,
                send.mode, degC, send.fanspeed, send.swingv, send.swingh,
                send.quiet, send.turbo, send.clock)
      break
    }
#endif  # SEND_PANASONIC_AC
#if SEND_SAMSUNG_AC
    case SAMSUNG_AC:
    {
      IRSamsungAc ac(_pin, _inverted, _modulation)
      samsung(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
              send.quiet, send.turbo, send.clean, send.beep, prev.power)
      break
    }
#endif  # SEND_SAMSUNG_AC
#if SEND_SHARP_AC
    case SHARP_AC:
    {
      IRSharpAc ac(_pin, _inverted, _modulation)
      sharp(&ac, send.power, send.mode, degC, send.fanspeed)
      break
    }
#endif  # SEND_SHARP_AC
#if SEND_TCL112AC
    case TCL112AC:
    {
      IRTcl112Ac ac(_pin, _inverted, _modulation)
      tcl112(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
             send.swingh, send.turbo, send.light, send.econo, send.filter)
      break
    }
#endif  # SEND_TCL112AC
#if SEND_TECO
    case TECO:
    {
      IRTecoAc ac(_pin, _inverted, _modulation)
      teco(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
           send.light, send.sleep)
      break
    }
#endif  # SEND_TECO
#if SEND_TOSHIBA_AC
    case TOSHIBA_AC:
    {
      IRToshibaAC ac(_pin, _inverted, _modulation)
      toshiba(&ac, send.power, send.mode, degC, send.fanspeed)
      break
    }
#endif  # SEND_TOSHIBA_AC
#if SEND_TROTEC
    case TROTEC:
    {
      IRTrotecESP ac(_pin, _inverted, _modulation)
      trotec(&ac, send.power, send.mode, degC, send.fanspeed, send.sleep)
      break
    }
#endif  # SEND_TROTEC
#if SEND_VESTEL_AC
    case VESTEL_AC:
    {
      IRVestelAc ac(_pin, _inverted, _modulation)
      vestel(&ac, send.power, send.mode, degC, send.fanspeed, send.swingv,
             send.turbo, send.filter, send.sleep, send.clock)
      break
    }
#endif  # SEND_VESTEL_AC
#if SEND_WHIRLPOOL_AC
    case WHIRLPOOL_AC:
    {
      IRWhirlpoolAc ac(_pin, _inverted, _modulation)
      whirlpool(&ac, (whirlpool_ac_remote_model_t)send.model, send.power,
                send.mode, degC, send.fanspeed, send.swingv, send.turbo,
                send.light, send.sleep, send.clock)
      break
    }
#endif  # SEND_WHIRLPOOL_AC
    default:
      return False  # Fail, didn't match anything.
  }
  return True  # Success.
}

# Send an A/C message based soley on our internal state.
#
# Returns:
#   boolean: True, if accepted/converted/attempted. False, if unsupported.
bool IRac.sendAc(void) {
  bool success = this.sendAc(next, &_prev)
  _prev = next
  return success
}

# Compare two AirCon states.
# Returns: True if they differ, False if they don't.
# Note: Excludes clock.
bool IRac.cmpStates(stdAc.state_t a, stdAc.state_t b) {
  return a.protocol != b.protocol or a.model != b.model or a.power != b.power or
      a.mode != b.mode or a.degrees != b.degrees or a.celsius != b.celsius or
      a.fanspeed != b.fanspeed or a.swingv != b.swingv or
      a.swingh != b.swingh or a.quiet != b.quiet or a.turbo != b.turbo or
      a.econo != b.econo or a.light != b.light or a.filter != b.filter or
      a.clean != b.clean or a.beep != b.beep or a.sleep != b.sleep
}

bool IRac.hasStateChanged(void) { return cmpStates(next, _prev) }

stdAc.opmode_t IRac.strToOpmode(char *str,
                                stdAc.opmode_t def) {
  if (!strcasecmp(str, kAutoStr) or
      !strcasecmp(str, kAutomaticStr))
    return stdAc.opmode_t.kAuto
  else if (!strcasecmp(str, kOffStr) or
           !strcasecmp(str, kStopStr))
    return stdAc.opmode_t.kOff
  else if (!strcasecmp(str, kCoolStr) or
           !strcasecmp(str, "COOLING"))
    return stdAc.opmode_t.kCool
  else if (!strcasecmp(str, kHeatStr) or
           !strcasecmp(str, "HEATING"))
    return stdAc.opmode_t.kHeat
  else if (!strcasecmp(str, kDryStr) or
           !strcasecmp(str, "DRYING") or
           !strcasecmp(str, "DEHUMIDIFY"))
    return stdAc.opmode_t.kDry
  else if (!strcasecmp(str, kFanStr) or
           !strcasecmp(str, "FANONLY") or
           !strcasecmp(str, kFanOnlyStr))
    return stdAc.opmode_t.kFan
  else
    return def
}

stdAc.fanspeed_t IRac.strToFanspeed(char *str,
                                      stdAc.fanspeed_t def) {
  if (!strcasecmp(str, kAutoStr) or
      !strcasecmp(str, kAutomaticStr))
    return stdAc.fanspeed_t.kAuto
  else if (!strcasecmp(str, kMinStr) or
           !strcasecmp(str, kMinimumStr) or
           !strcasecmp(str, kLowestStr))
    return stdAc.fanspeed_t.kMin
  else if (!strcasecmp(str, kLowStr) or
           !strcasecmp(str, kLoStr))
    return stdAc.fanspeed_t.kLow
  else if (!strcasecmp(str, kMedStr) or
           !strcasecmp(str, kMediumStr) or
           !strcasecmp(str, kMidStr))
    return stdAc.fanspeed_t.kMedium
  else if (!strcasecmp(str, kHighStr) or
           !strcasecmp(str, kHiStr))
    return stdAc.fanspeed_t.kHigh
  else if (!strcasecmp(str, kMaxStr) or
           !strcasecmp(str, kMaximumStr) or
           !strcasecmp(str, kHighestStr))
    return stdAc.fanspeed_t.kMax
  else
    return def
}

stdAc.swingv_t IRac.strToSwingV(char *str,
                                  stdAc.swingv_t def) {
  if (!strcasecmp(str, kAutoStr) or
      !strcasecmp(str, kAutomaticStr) or
      !strcasecmp(str, kOnStr) or
      !strcasecmp(str, kSwingStr))
    return stdAc.swingv_t.kAuto
  else if (!strcasecmp(str, kOffStr) or
           !strcasecmp(str, kStopStr))
    return stdAc.swingv_t.kOff
  else if (!strcasecmp(str, kMinStr) or
           !strcasecmp(str, kMinimumStr) or
           !strcasecmp(str, kLowestStr) or
           !strcasecmp(str, kBottomStr) or
           !strcasecmp(str, kDownStr))
    return stdAc.swingv_t.kLowest
  else if (!strcasecmp(str, kLowStr))
    return stdAc.swingv_t.kLow
  else if (!strcasecmp(str, kMidStr) or
           !strcasecmp(str, kMiddleStr) or
           !strcasecmp(str, kMedStr) or
           !strcasecmp(str, kMediumStr) or
           !strcasecmp(str, kCentreStr))
    return stdAc.swingv_t.kMiddle
  else if (!strcasecmp(str, kHighStr) or
           !strcasecmp(str, kHiStr))
    return stdAc.swingv_t.kHigh
  else if (!strcasecmp(str, kHighestStr) or
           !strcasecmp(str, kMaxStr) or
           !strcasecmp(str, kMaximumStr) or
           !strcasecmp(str, kTopStr) or
           !strcasecmp(str, kUpStr))
    return stdAc.swingv_t.kHighest
  else
    return def
}

stdAc.swingh_t IRac.strToSwingH(char *str,
                                  stdAc.swingh_t def) {
  if (!strcasecmp(str, kAutoStr) or
      !strcasecmp(str, kAutomaticStr) or
      !strcasecmp(str, kOnStr) or !strcasecmp(str, kSwingStr))
    return stdAc.swingh_t.kAuto
  else if (!strcasecmp(str, kOffStr) or
           !strcasecmp(str, kStopStr))
    return stdAc.swingh_t.kOff
  else if (!strcasecmp(str, kLeftMaxStr) or
           !strcasecmp(str, D_STR_LEFT " " D_STR_MAX) or
           !strcasecmp(str, D_STR_MAX D_STR_LEFT) or
           !strcasecmp(str, kMaxLeftStr))
    return stdAc.swingh_t.kLeftMax
  else if (!strcasecmp(str, kLeftStr))
    return stdAc.swingh_t.kLeft
  else if (!strcasecmp(str, kMidStr) or
           !strcasecmp(str, kMiddleStr) or
           !strcasecmp(str, kMedStr) or
           !strcasecmp(str, kMediumStr) or
           !strcasecmp(str, kCentreStr))
    return stdAc.swingh_t.kMiddle
  else if (!strcasecmp(str, kRightStr))
    return stdAc.swingh_t.kRight
  else if (!strcasecmp(str, kRightMaxStr) or
           !strcasecmp(str, D_STR_MAX " " D_STR_RIGHT) or
           !strcasecmp(str, D_STR_MAX D_STR_RIGHT) or
           !strcasecmp(str, kMaxRightStr))
    return stdAc.swingh_t.kRightMax
  else if (!strcasecmp(str, kWideStr))
    return stdAc.swingh_t.kWide
  else
    return def
}

# Assumes str is the model code or an integer >= 1.
int16_t IRac.strToModel(char *str, int16_t def) {
  # Gree
  if (!strcasecmp(str, "YAW1F")) {
    return gree_ac_remote_model_t.YAW1F
  } else if (!strcasecmp(str, "YBOFB")) {
    return gree_ac_remote_model_t.YBOFB
  # Fujitsu A/C models
  } else if (!strcasecmp(str, "ARRAH2E")) {
    return fujitsu_ac_remote_model_t.ARRAH2E
  } else if (!strcasecmp(str, "ARDB1")) {
    return fujitsu_ac_remote_model_t.ARDB1
  } else if (!strcasecmp(str, "ARREB1E")) {
    return fujitsu_ac_remote_model_t.ARREB1E
  } else if (!strcasecmp(str, "ARJW2")) {
    return fujitsu_ac_remote_model_t.ARJW2
  } else if (!strcasecmp(str, "ARRY4")) {
    return fujitsu_ac_remote_model_t.ARRY4
  # Panasonic A/C families
  } else if (!strcasecmp(str, "LKE") or !strcasecmp(str, "PANASONICLKE")) {
    return panasonic_ac_remote_model_t.kPanasonicLke
  } else if (!strcasecmp(str, "NKE") or !strcasecmp(str, "PANASONICNKE")) {
    return panasonic_ac_remote_model_t.kPanasonicNke
  } else if (!strcasecmp(str, "DKE") or !strcasecmp(str, "PANASONICDKE") or
             !strcasecmp(str, "PKR") or !strcasecmp(str, "PANASONICPKR")) {
    return panasonic_ac_remote_model_t.kPanasonicDke
  } else if (!strcasecmp(str, "JKE") or !strcasecmp(str, "PANASONICJKE")) {
    return panasonic_ac_remote_model_t.kPanasonicJke
  } else if (!strcasecmp(str, "CKP") or !strcasecmp(str, "PANASONICCKP")) {
    return panasonic_ac_remote_model_t.kPanasonicCkp
  } else if (!strcasecmp(str, "RKR") or !strcasecmp(str, "PANASONICRKR")) {
    return panasonic_ac_remote_model_t.kPanasonicRkr
  # Whirlpool A/C models
  } else if (!strcasecmp(str, "DG11J13A") or !strcasecmp(str, "DG11J104") or
             !strcasecmp(str, "DG11J1-04")) {
    return whirlpool_ac_remote_model_t.DG11J13A
  } else if (!strcasecmp(str, "DG11J191")) {
    return whirlpool_ac_remote_model_t.DG11J191
  } else {
    int16_t number = atoi(str)
    if (number > 0)
      return number
    else
      return def
  }
}

bool IRac.strToBool(char *str, bool def) {
  if (!strcasecmp(str, kOnStr) or
      !strcasecmp(str, "1") or
      !strcasecmp(str, kYesStr) or
      !strcasecmp(str, kTrueStr))
    return True
  else if (!strcasecmp(str, kOffStr) or
           !strcasecmp(str, "0") or
           !strcasecmp(str, kNoStr) or
           !strcasecmp(str, kFalseStr))
    return False
  else
    return def
}

String IRac.boolToString(bool value) {
  return value ? kOnStr : kOffStr
}

String IRac.opmodeToString(stdAc.opmode_t mode) {
  switch (mode) {
    case stdAc.opmode_t.kOff:
      return kOffStr
    case stdAc.opmode_t.kAuto:
      return kAutoStr
    case stdAc.opmode_t.kCool:
      return kCoolStr
    case stdAc.opmode_t.kHeat:
      return kHeatStr
    case stdAc.opmode_t.kDry:
      return kDryStr
    case stdAc.opmode_t.kFan:
      return kFanOnlyStr
    default:
      return kUnknownStr
  }
}

String IRac.fanspeedToString(stdAc.fanspeed_t speed) {
  switch (speed) {
    case stdAc.fanspeed_t.kAuto:
      return kAutoStr
    case stdAc.fanspeed_t.kMax:
      return kMaxStr
    case stdAc.fanspeed_t.kHigh:
      return kHighStr
    case stdAc.fanspeed_t.kMedium:
      return kMediumStr
    case stdAc.fanspeed_t.kLow:
      return kLowStr
    case stdAc.fanspeed_t.kMin:
      return kMinStr
    default:
      return kUnknownStr
  }
}

String IRac.swingvToString(stdAc.swingv_t swingv) {
  switch (swingv) {
    case stdAc.swingv_t.kOff:
      return kOffStr
    case stdAc.swingv_t.kAuto:
      return kAutoStr
    case stdAc.swingv_t.kHighest:
      return kHighestStr
    case stdAc.swingv_t.kHigh:
      return kHighStr
    case stdAc.swingv_t.kMiddle:
      return kMiddleStr
    case stdAc.swingv_t.kLow:
      return kLowStr
    case stdAc.swingv_t.kLowest:
      return kLowestStr
    default:
      return kUnknownStr
  }
}

String IRac.swinghToString(stdAc.swingh_t swingh) {
  switch (swingh) {
    case stdAc.swingh_t.kOff:
      return kOffStr
    case stdAc.swingh_t.kAuto:
      return kAutoStr
    case stdAc.swingh_t.kLeftMax:
      return kLeftMaxStr
    case stdAc.swingh_t.kLeft:
      return kLeftStr
    case stdAc.swingh_t.kMiddle:
      return kMiddleStr
    case stdAc.swingh_t.kRight:
      return kRightStr
    case stdAc.swingh_t.kRightMax:
      return kRightMaxStr
    case stdAc.swingh_t.kWide:
      return kWideStr
    default:
      return kUnknownStr
  }
}

namespace IRAcUtils {
  # Display the human readable state of an A/C message if we can.
  # Args:
  #   result: A Ptr to the captured `decode_results` that contains an A/C mesg.
  # Returns:
  #   A string with the human description of the A/C message. "" if we can't.
  String resultAcToString(decode_results * result) {
    switch (result.decode_type) {
#if DECODE_AMCOR
      case decode_type_t.AMCOR: {
        IRAmcorAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_AMCOR
#if DECODE_ARGO
      case decode_type_t.ARGO: {
        IRArgoAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_ARGO
#if DECODE_DAIKIN
      case decode_type_t.DAIKIN: {
        IRDaikinESP ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN
#if DECODE_DAIKIN128
      case decode_type_t.DAIKIN128: {
        IRDaikin128 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN128
#if DECODE_DAIKIN152
      case decode_type_t.DAIKIN152: {
        IRDaikin152 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN152
#if DECODE_DAIKIN160
      case decode_type_t.DAIKIN160: {
        IRDaikin160 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN160
#if DECODE_DAIKIN176
      case decode_type_t.DAIKIN176: {
        IRDaikin176 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN160
#if DECODE_DAIKIN2
      case decode_type_t.DAIKIN2: {
        IRDaikin2 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN2
#if DECODE_DAIKIN216
      case decode_type_t.DAIKIN216: {
        IRDaikin216 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_DAIKIN216
#if DECODE_ELECTRA_AC
      case decode_type_t.ELECTRA_AC: {
        IRElectraAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_ELECTRA_AC
#if DECODE_FUJITSU_AC
      case decode_type_t.FUJITSU_AC: {
        IRFujitsuAC ac(0)
        ac.setRaw(result.state, result.bits / 8)
        return ac.toString()
      }
#endif  # DECODE_FUJITSU_AC
#if DECODE_KELVINATOR
      case decode_type_t.KELVINATOR: {
        IRKelvinatorAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_KELVINATOR
#if DECODE_MITSUBISHI_AC
      case decode_type_t.MITSUBISHI_AC: {
        IRMitsubishiAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_MITSUBISHI_AC
#if DECODE_MITSUBISHI112
      case decode_type_t.MITSUBISHI112: {
        IRMitsubishi112 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_MITSUBISHI112
#if DECODE_MITSUBISHI136
      case decode_type_t.MITSUBISHI136: {
        IRMitsubishi136 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_MITSUBISHI136
#if DECODE_MITSUBISHIHEAVY
      case decode_type_t.MITSUBISHI_HEAVY_88: {
        IRMitsubishiHeavy88Ac ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
      case decode_type_t.MITSUBISHI_HEAVY_152: {
        IRMitsubishiHeavy152Ac ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_MITSUBISHIHEAVY
#if DECODE_NEOCLIMA
      case decode_type_t.NEOCLIMA: {
        IRNeoclimaAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_NEOCLIMA
#if DECODE_TOSHIBA_AC
      case decode_type_t.TOSHIBA_AC: {
        IRToshibaAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_TOSHIBA_AC
#if DECODE_TROTEC
      case decode_type_t.TROTEC: {
        IRTrotecESP ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_TROTEC
#if DECODE_GOODWEATHER
      case decode_type_t.GOODWEATHER: {
        IRGoodweatherAc ac(0)
        ac.setRaw(result.value)  # Goodweather uses value instead of state.
        return ac.toString()
      }
#endif  # DECODE_GOODWEATHER
#if DECODE_GREE
      case decode_type_t.GREE: {
        IRGreeAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_GREE
#if DECODE_MIDEA
      case decode_type_t.MIDEA: {
        IRMideaAC ac(0)
        ac.setRaw(result.value)  # Midea uses value instead of state.
        return ac.toString()
      }
#endif  # DECODE_MIDEA
#if DECODE_HAIER_AC
      case decode_type_t.HAIER_AC: {
        IRHaierAC ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_HAIER_AC
#if DECODE_HAIER_AC_YRW02
      case decode_type_t.HAIER_AC_YRW02: {
        IRHaierACYRW02 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_HAIER_AC_YRW02
#if DECODE_SAMSUNG_AC
      case decode_type_t.SAMSUNG_AC: {
        IRSamsungAc ac(0)
        ac.setRaw(result.state, result.bits / 8)
        return ac.toString()
      }
#endif  # DECODE_SAMSUNG_AC
#if DECODE_SHARP_AC
      case decode_type_t.SHARP_AC: {
        IRSharpAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_SHARP_AC
#if DECODE_COOLIX
      case decode_type_t.COOLIX: {
        IRCoolixAC ac(0)
        ac.on()
        ac.setRaw(result.value)  # Coolix uses value instead of state.
        return ac.toString()
      }
#endif  # DECODE_COOLIX
#if DECODE_PANASONIC_AC
      case decode_type_t.PANASONIC_AC: {
        if (result.bits > kPanasonicAcShortBits) {
          IRPanasonicAc ac(0)
          ac.setRaw(result.state)
          return ac.toString()
        }
        return ""
      }
#endif  # DECODE_PANASONIC_AC
#if DECODE_HITACHI_AC
      case decode_type_t.HITACHI_AC: {
        IRHitachiAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_HITACHI_AC
#if DECODE_HITACHI_AC424
      case decode_type_t.HITACHI_AC424: {
        IRHitachiAc424 ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_HITACHI_AC424
#if DECODE_WHIRLPOOL_AC
      case decode_type_t.WHIRLPOOL_AC: {
        IRWhirlpoolAc ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_WHIRLPOOL_AC
#if DECODE_VESTEL_AC
      case decode_type_t.VESTEL_AC: {
        IRVestelAc ac(0)
        ac.setRaw(result.value)  # Like Coolix, use value instead of state.
        return ac.toString()
      }
#endif  # DECODE_VESTEL_AC
#if DECODE_TECO
      case decode_type_t.TECO: {
        IRTecoAc ac(0)
        ac.setRaw(result.value)  # Like Coolix, use value instead of state.
        return ac.toString()
      }
#endif  # DECODE_TECO
#if DECODE_TCL112AC
      case decode_type_t.TCL112AC: {
        IRTcl112Ac ac(0)
        ac.setRaw(result.state)
        return ac.toString()
      }
#endif  # DECODE_TCL112AC
#if DECODE_LG
      case decode_type_t.LG:
      case decode_type_t.LG2: {
        IRLgAc ac(0)
        ac.setRaw(result.value)  # Like Coolix, use value instead of state.
        switch (result.decode_type) {
          case decode_type_t.LG2:
            ac.setModel(lg_ac_remote_model_t.AKB75215403)
            break
          default:
            ac.setModel(lg_ac_remote_model_t.GE6711AR2853M)
        }
        return ac.isValidLgAc() ? ac.toString() : ""
      }
#endif  # DECODE_LG
      default:
        return ""
    }
  }

  # Convert a valid IR A/C remote message that we understand enough into a
  # Common A/C state.
  #
  # Args:
  #   decode: A PTR to a successful raw IR decode object.
  #   result: A PTR to a state structure to store the result in.
  #   prev:   A PTR to a state structure which has the prev. state. (optional)
  # Returns:
  #   A boolean indicating success or failure.
  bool decodeToState(decode_results *decode, stdAc.state_t *result,
                     stdAc.state_t *prev) {
    if (decode == NULL or result == NULL) return False  # Safety check.
    switch (decode.decode_type) {
#if DECODE_AMCOR
      case decode_type_t.AMCOR: {
        IRAmcorAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_AMCOR
#if DECODE_ARGO
      case decode_type_t.ARGO: {
        IRArgoAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_ARGO
#if DECODE_COOLIX
      case decode_type_t.COOLIX: {
        IRCoolixAC ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        *result = ac.toCommon(prev)
        break
      }
#endif  # DECODE_COOLIX
#if DECODE_DAIKIN
      case decode_type_t.DAIKIN: {
        IRDaikinESP ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN
#if DECODE_DAIKIN128
      case decode_type_t.DAIKIN128: {
        IRDaikin128 ac(0)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN128
#if DECODE_DAIKIN152
      case decode_type_t.DAIKIN152: {
        IRDaikin152 ac(0)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN152
#if DECODE_DAIKIN160
      case decode_type_t.DAIKIN160: {
        IRDaikin160 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN160
#if DECODE_DAIKIN176
      case decode_type_t.DAIKIN176: {
        IRDaikin176 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN160
#if DECODE_DAIKIN2
      case decode_type_t.DAIKIN2: {
        IRDaikin2 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN2
#if DECODE_DAIKIN216
      case decode_type_t.DAIKIN216: {
        IRDaikin216 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_DAIKIN216
#if DECODE_ELECTRA_AC
      case decode_type_t.ELECTRA_AC: {
        IRElectraAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_ELECTRA_AC
#if DECODE_FUJITSU_AC
      case decode_type_t.FUJITSU_AC: {
        IRFujitsuAC ac(kGpioUnused)
        ac.setRaw(decode.state, decode.bits / 8)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_FUJITSU_AC
#if DECODE_GOODWEATHER
      case decode_type_t.GOODWEATHER: {
        IRGoodweatherAc ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_GOODWEATHER
#if DECODE_GREE
      case decode_type_t.GREE: {
        IRGreeAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_GREE
#if DECODE_HAIER_AC
      case decode_type_t.HAIER_AC: {
        IRHaierAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_HAIER_AC
#if DECODE_HAIER_AC_YRW02
      case decode_type_t.HAIER_AC_YRW02: {
        IRHaierACYRW02 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_HAIER_AC_YRW02
#if (DECODE_HITACHI_AC or DECODE_HITACHI_AC2)
      case decode_type_t.HITACHI_AC: {
        IRHitachiAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # (DECODE_HITACHI_AC or DECODE_HITACHI_AC2)
#if DECODE_HITACHI_AC424
      case decode_type_t.HITACHI_AC424: {
        IRHitachiAc424 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_HITACHI_AC424
#if DECODE_KELVINATOR
      case decode_type_t.KELVINATOR: {
        IRKelvinatorAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_KELVINATOR
#if DECODE_LG
      case decode_type_t.LG:
      case decode_type_t.LG2: {
        IRLgAc ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        if (!ac.isValidLgAc()) return False
        switch (decode.decode_type) {
          case decode_type_t.LG2:
            ac.setModel(lg_ac_remote_model_t.AKB75215403)
            break
          default:
            ac.setModel(lg_ac_remote_model_t.GE6711AR2853M)
        }
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_LG
#if DECODE_MIDEA
      case decode_type_t.MIDEA: {
        IRMideaAC ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        *result = ac.toCommon(prev)
        break
      }
#endif  # DECODE_MIDEA
#if DECODE_MITSUBISHI_AC
      case decode_type_t.MITSUBISHI_AC: {
        IRMitsubishiAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_MITSUBISHI_AC
#if DECODE_MITSUBISHI112
      case decode_type_t.MITSUBISHI112: {
        IRMitsubishi112 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_MITSUBISHI112
#if DECODE_MITSUBISHI136
      case decode_type_t.MITSUBISHI136: {
        IRMitsubishi136 ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_MITSUBISHI136
#if DECODE_MITSUBISHIHEAVY
      case decode_type_t.MITSUBISHI_HEAVY_88: {
        IRMitsubishiHeavy88Ac ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
      case decode_type_t.MITSUBISHI_HEAVY_152: {
        IRMitsubishiHeavy152Ac ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_MITSUBISHIHEAVY
#if DECODE_NEOCLIMA
      case decode_type_t.NEOCLIMA: {
        IRNeoclimaAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_NEOCLIMA
#if DECODE_PANASONIC_AC
      case decode_type_t.PANASONIC_AC: {
        IRPanasonicAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_PANASONIC_AC
#if DECODE_SAMSUNG_AC
      case decode_type_t.SAMSUNG_AC: {
        IRSamsungAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_SAMSUNG_AC
#if DECODE_SHARP_AC
      case decode_type_t.SHARP_AC: {
        IRSharpAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_SHARP_AC
#if DECODE_TCL112AC
      case decode_type_t.TCL112AC: {
        IRTcl112Ac ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_TCL112AC
#if DECODE_TECO
      case decode_type_t.TECO: {
        IRTecoAc ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_TECO
#if DECODE_TOSHIBA_AC
      case decode_type_t.TOSHIBA_AC: {
        IRToshibaAC ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_TOSHIBA_AC
#if DECODE_TROTEC
      case decode_type_t.TROTEC: {
        IRTrotecESP ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_TROTEC
#if DECODE_VESTEL_AC
      case decode_type_t.VESTEL_AC: {
        IRVestelAc ac(kGpioUnused)
        ac.setRaw(decode.value)  # Uses value instead of state.
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_VESTEL_AC
#if DECODE_WHIRLPOOL_AC
      case decode_type_t.WHIRLPOOL_AC: {
        IRWhirlpoolAc ac(kGpioUnused)
        ac.setRaw(decode.state)
        *result = ac.toCommon()
        break
      }
#endif  # DECODE_WHIRLPOOL_AC
      default:
        return False
    }
    return True
  }
}  # namespace IRAcUtils
