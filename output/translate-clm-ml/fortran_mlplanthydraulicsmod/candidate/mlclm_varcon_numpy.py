"""Stand-in for Fortran module mlclm_varcon, written by RecastEngine.

Not a translation: the module is a stub under the frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

RGAS = np.float64('8.31446')  # MLclm_varcon.f90:19
MMDRY = (np.float64('28.97') * np.float64('1.e-03'))  # MLclm_varcon.f90:20
MMH2O = (np.float64('18.02') * np.float64('1.e-03'))  # MLclm_varcon.f90:21
CPD = np.float64('1005.')  # MLclm_varcon.f90:22
CPW = np.float64('1846.')  # MLclm_varcon.f90:23
VISC0 = np.float64('13.3e-06')  # MLclm_varcon.f90:24
DH0 = np.float64('18.9e-06')  # MLclm_varcon.f90:25
DV0 = np.float64('21.8e-06')  # MLclm_varcon.f90:26
DC0 = np.float64('13.8e-06')  # MLclm_varcon.f90:27
LAPSE_RATE = np.float64('0.0098')  # MLclm_varcon.f90:28
KC25 = np.float64('404.9')  # MLclm_varcon.f90:35
KCHA = np.float64('79430.')  # MLclm_varcon.f90:36
KO25 = np.float64('278.4')  # MLclm_varcon.f90:37
KOHA = np.float64('36380.')  # MLclm_varcon.f90:38
CP25 = np.float64('42.75')  # MLclm_varcon.f90:39
CPHA = np.float64('37830.')  # MLclm_varcon.f90:40
VCMAXHA_NOACCLIM = np.float64('65330.')  # MLclm_varcon.f90:42
VCMAXHA_ACCLIM = np.float64('72000.')  # MLclm_varcon.f90:43
VCMAXHD_NOACCLIM = np.float64('150000.')  # MLclm_varcon.f90:44
VCMAXHD_ACCLIM = np.float64('200000.')  # MLclm_varcon.f90:45
VCMAXSE_NOACCLIM = np.float64('490.')  # MLclm_varcon.f90:46
SPVAL = np.float64('1.e36')  # clm_varcon.f90:44
VCMAXSE_ACCLIM = SPVAL  # MLclm_varcon.f90:47
JMAXHA_NOACCLIM = np.float64('43540.')  # MLclm_varcon.f90:49
JMAXHA_ACCLIM = np.float64('50000.')  # MLclm_varcon.f90:50
JMAXHD_NOACCLIM = np.float64('150000.')  # MLclm_varcon.f90:51
JMAXHD_ACCLIM = np.float64('200000.')  # MLclm_varcon.f90:52
JMAXSE_NOACCLIM = np.float64('490.')  # MLclm_varcon.f90:53
JMAXSE_ACCLIM = SPVAL  # MLclm_varcon.f90:54
RDHA = np.float64('46390.')  # MLclm_varcon.f90:56
RDHD = np.float64('150000.')  # MLclm_varcon.f90:57
RDSE = np.float64('490.')  # MLclm_varcon.f90:58
JMAX25_TO_VCMAX25_NOACCLIM = np.float64('1.67')  # MLclm_varcon.f90:60
JMAX25_TO_VCMAX25_ACCLIM = SPVAL  # MLclm_varcon.f90:61
RD25_TO_VCMAX25_C3 = np.float64('0.015')  # MLclm_varcon.f90:62
RD25_TO_VCMAX25_C4 = np.float64('0.025')  # MLclm_varcon.f90:63
KP25_TO_VCMAX25_C4 = np.float64('0.02')  # MLclm_varcon.f90:64
PHI_PSII = np.float64('0.70')  # MLclm_varcon.f90:66
THETA_J = np.float64('0.90')  # MLclm_varcon.f90:68
QE_C4 = np.float64('0.05')  # MLclm_varcon.f90:69
COLIM_C3A = np.float64('0.98')  # MLclm_varcon.f90:71
COLIM_C3B = SPVAL  # MLclm_varcon.f90:72
COLIM_C4A = np.float64('0.80')  # MLclm_varcon.f90:73
COLIM_C4B = np.float64('0.95')  # MLclm_varcon.f90:74
DH2O_TO_DCO2 = np.float64('1.6')  # MLclm_varcon.f90:79
RH_MIN_BB = np.float64('0.2')  # MLclm_varcon.f90:80
VPD_MIN_MED = np.float64('100.')  # MLclm_varcon.f90:81
CPBIO = (np.float64('4188.') / np.float64('3.'))  # MLclm_varcon.f90:86
FCARBON = np.float64('0.5')  # MLclm_varcon.f90:87
FWATER = np.float64('0.7')  # MLclm_varcon.f90:88
GB_FACTOR = np.float64('1.5')  # MLclm_varcon.f90:93
DEWMX = np.float64('0.1')  # MLclm_varcon.f90:98
MAXIMUM_LEAF_WETTED_FRACTION = np.float64('0.05')  # MLclm_varcon.f90:99
INTERCEPTION_FRACTION = np.float64('1.0')  # MLclm_varcon.f90:100
FWET_EXPONENT = np.float64('0.67')  # MLclm_varcon.f90:101
CHIL_MIN = (-np.float64('0.4'))  # MLclm_varcon.f90:106
CHIL_MAX = np.float64('0.6')  # MLclm_varcon.f90:107
KB_MAX = np.float64('40.')  # MLclm_varcon.f90:108
J_TO_UMOL = np.float64('4.6')  # MLclm_varcon.f90:109
EMG = np.float64('0.96')  # MLclm_varcon.f90:114
CD = np.float64('0.25')  # MLclm_varcon.f90:119
BETA_NEUTRAL_MAX = np.float64('0.35')  # MLclm_varcon.f90:120
CR = np.float64('0.3')  # MLclm_varcon.f90:121
C2 = np.float64('0.5')  # MLclm_varcon.f90:122
PR0 = np.float64('0.5')  # MLclm_varcon.f90:123
PR1 = np.float64('0.3')  # MLclm_varcon.f90:124
PR2 = np.float64('2.0')  # MLclm_varcon.f90:125
Z0MG = np.float64('0.01')  # MLclm_varcon.f90:126
WIND_FORC_MIN = np.float64('0.5')  # MLclm_varcon.f90:133
LCL_MIN = (-np.float64('2.'))  # MLclm_varcon.f90:134
LCL_MAX = np.float64('1.')  # MLclm_varcon.f90:135
GBH_MIN = np.float64('0.2')  # MLclm_varcon.f90:136
RA_MAX = np.float64('500.')  # MLclm_varcon.f90:137
ETA_MAX = np.float64('20.')  # MLclm_varcon.f90:138
NZ = 276  # MLclm_varcon.f90:145
NL = 41  # MLclm_varcon.f90:145

rgas = RGAS
mmdry = MMDRY
mmh2o = MMH2O
cpd = CPD
cpw = CPW
visc0 = VISC0
dh0 = DH0
dv0 = DV0
dc0 = DC0
lapse_rate = LAPSE_RATE
kc25 = KC25
kcha = KCHA
ko25 = KO25
koha = KOHA
cp25 = CP25
cpha = CPHA
vcmaxha_noacclim = VCMAXHA_NOACCLIM
vcmaxha_acclim = VCMAXHA_ACCLIM
vcmaxhd_noacclim = VCMAXHD_NOACCLIM
vcmaxhd_acclim = VCMAXHD_ACCLIM
vcmaxse_noacclim = VCMAXSE_NOACCLIM
spval = SPVAL
vcmaxse_acclim = VCMAXSE_ACCLIM
jmaxha_noacclim = JMAXHA_NOACCLIM
jmaxha_acclim = JMAXHA_ACCLIM
jmaxhd_noacclim = JMAXHD_NOACCLIM
jmaxhd_acclim = JMAXHD_ACCLIM
jmaxse_noacclim = JMAXSE_NOACCLIM
jmaxse_acclim = JMAXSE_ACCLIM
rdha = RDHA
rdhd = RDHD
rdse = RDSE
jmax25_to_vcmax25_noacclim = JMAX25_TO_VCMAX25_NOACCLIM
jmax25_to_vcmax25_acclim = JMAX25_TO_VCMAX25_ACCLIM
rd25_to_vcmax25_c3 = RD25_TO_VCMAX25_C3
rd25_to_vcmax25_c4 = RD25_TO_VCMAX25_C4
kp25_to_vcmax25_c4 = KP25_TO_VCMAX25_C4
phi_psii = PHI_PSII
theta_j = THETA_J
qe_c4 = QE_C4
colim_c3a = COLIM_C3A
colim_c3b = COLIM_C3B
colim_c4a = COLIM_C4A
colim_c4b = COLIM_C4B
dh2o_to_dco2 = DH2O_TO_DCO2
rh_min_bb = RH_MIN_BB
vpd_min_med = VPD_MIN_MED
cpbio = CPBIO
fcarbon = FCARBON
fwater = FWATER
gb_factor = GB_FACTOR
dewmx = DEWMX
maximum_leaf_wetted_fraction = MAXIMUM_LEAF_WETTED_FRACTION
interception_fraction = INTERCEPTION_FRACTION
fwet_exponent = FWET_EXPONENT
chil_min = CHIL_MIN
chil_max = CHIL_MAX
kb_max = KB_MAX
j_to_umol = J_TO_UMOL
emg = EMG
cd = CD
beta_neutral_max = BETA_NEUTRAL_MAX
cr = CR
c2 = C2
pr0 = PR0
pr1 = PR1
pr2 = PR2
z0mg = Z0MG
wind_forc_min = WIND_FORC_MIN
lcl_min = LCL_MIN
lcl_max = LCL_MAX
gbh_min = GBH_MIN
ra_max = RA_MAX
eta_max = ETA_MAX
nz = NZ
nl = NL

