"""Stand-in for Fortran module mlclm_varctl, written by recast-clm.

Not a translation: the module is a stub under the clm frontend. Its
initialized entities are resolved from the source tree; framework
calls are answered the way a standalone run answers them."""

import numpy as np  # noqa: F401


class _Record:
    """A module variable of derived type: components are set by whoever
    drives the translation (the flat adapters, a harness)."""

    def __init__(self, **fields):
        self.__dict__.update(fields)

GS_TYPE = 2  # MLclm_varctl.f90:18
GSPOT_TYPE = 1  # MLclm_varctl.f90:19
GS_SOLVER = 2  # MLclm_varctl.f90:20
COLIM_TYPE = 1  # MLclm_varctl.f90:21
ACCLIM_TYPE = 1  # MLclm_varctl.f90:22
KN_VAL = (-np.float64('999.'))  # MLclm_varctl.f90:23
TURB_TYPE = 1  # MLclm_varctl.f90:27
SPARSE_CANOPY_TYPE = 1  # MLclm_varctl.f90:28
HF_EXTENSION_TYPE = 2  # MLclm_varctl.f90:29
FLUX_PROFILE_TYPE = 1  # MLclm_varctl.f90:30
GB_TYPE = 3  # MLclm_varctl.f90:31
LIGHT_TYPE = 2  # MLclm_varctl.f90:35
LEAF_OPTICS_TYPE = 0  # MLclm_varctl.f90:36
LONGWAVE_TYPE = 1  # MLclm_varctl.f90:37
DTIME_ML = np.float64('300.')  # MLclm_varctl.f90:41
RUNGE_KUTTA_TYPE = 41  # MLclm_varctl.f90:45
NRK = ((RUNGE_KUTTA_TYPE // 10))  # MLclm_varctl.f90:49
DZ_TALL = np.float64('0.5')  # MLclm_varctl.f90:53
DZ_SHORT = np.float64('0.1')  # MLclm_varctl.f90:54
DZ_PARAM = np.float64('2.')  # MLclm_varctl.f90:55
NLAYER_ABOVE = 0  # MLclm_varctl.f90:59
NLAYER_WITHIN = 0  # MLclm_varctl.f90:60
MLCAN_TO_CLM = 0  # MLclm_varctl.f90:64
ISPVAL = (-9999)  # clm_varcon.f90:45
ML_VERT_INIT = ISPVAL  # MLclm_varctl.f90:65
MET_TYPE = 3  # constant_overrides (namelist); was: 3
DPAI_MIN = np.float64(0.01)  # constant_overrides (namelist); was: np.float64(0.01)
PFTCON_VAL = 1  # constant_overrides (namelist); was: 1

gs_type = GS_TYPE
gspot_type = GSPOT_TYPE
gs_solver = GS_SOLVER
colim_type = COLIM_TYPE
acclim_type = ACCLIM_TYPE
kn_val = KN_VAL
turb_type = TURB_TYPE
sparse_canopy_type = SPARSE_CANOPY_TYPE
hf_extension_type = HF_EXTENSION_TYPE
flux_profile_type = FLUX_PROFILE_TYPE
gb_type = GB_TYPE
light_type = LIGHT_TYPE
leaf_optics_type = LEAF_OPTICS_TYPE
longwave_type = LONGWAVE_TYPE
dtime_ml = DTIME_ML
runge_kutta_type = RUNGE_KUTTA_TYPE
nrk = NRK
dz_tall = DZ_TALL
dz_short = DZ_SHORT
dz_param = DZ_PARAM
nlayer_above = NLAYER_ABOVE
nlayer_within = NLAYER_WITHIN
mlcan_to_clm = MLCAN_TO_CLM
ispval = ISPVAL
ml_vert_init = ML_VERT_INIT
met_type = MET_TYPE
dpai_min = DPAI_MIN
pftcon_val = PFTCON_VAL

