"""Stand-in for Fortran module clm_varcon, written by recast-clm.

Not a translation: the module is a stub under the clm frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

RPI = np.float64('3.141592654')  # clm_varcon.f90:17
TFRZ = np.float64('273.15')  # clm_varcon.f90:21
SB = np.float64('5.67e-08')  # clm_varcon.f90:22
GRAV = np.float64('9.80665')  # clm_varcon.f90:23
VKC = np.float64('0.4')  # clm_varcon.f90:24
DENH2O = np.float64('1000.')  # clm_varcon.f90:25
DENICE = np.float64('917.')  # clm_varcon.f90:26
TKWAT = np.float64('0.57')  # clm_varcon.f90:27
TKICE = np.float64('2.29')  # clm_varcon.f90:28
TKAIR = np.float64('0.023')  # clm_varcon.f90:29
HFUS = np.float64('0.3337e6')  # clm_varcon.f90:30
HVAP = np.float64('2.5010e6')  # clm_varcon.f90:31
HSUB = np.float64('2.8347e6')  # clm_varcon.f90:32
CPICE = np.float64('2.11727e3')  # clm_varcon.f90:33
CPLIQ = np.float64('4.188e3')  # clm_varcon.f90:34
THK_BEDROCK = np.float64('3.0')  # clm_varcon.f90:38
CSOL_BEDROCK = np.float64('2.0e6')  # clm_varcon.f90:39
ZMIN_BEDROCK = np.float64('0.4')  # clm_varcon.f90:40
SPVAL = np.float64('1.e36')  # clm_varcon.f90:44
ISPVAL = (-9999)  # clm_varcon.f90:45

rpi = RPI
tfrz = TFRZ
sb = SB
grav = GRAV
vkc = VKC
denh2o = DENH2O
denice = DENICE
tkwat = TKWAT
tkice = TKICE
tkair = TKAIR
hfus = HFUS
hvap = HVAP
hsub = HSUB
cpice = CPICE
cpliq = CPLIQ
thk_bedrock = THK_BEDROCK
csol_bedrock = CSOL_BEDROCK
zmin_bedrock = ZMIN_BEDROCK
spval = SPVAL
ispval = ISPVAL

