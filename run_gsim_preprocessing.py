import numpy as np
import pandas as pd
import glob

# import packages
import glob
from pathlib import Path
import os
import numpy as np
from datetime import datetime
from datetime import timedelta
import pandas as pd
import calendar
import geopandas as gpd
import cartopy
import matplotlib.pyplot as plt
import math
from pathos.threading import ThreadPool as Pool
from scipy.optimize import least_squares
import sklearn
from sklearn.linear_model import LinearRegression
from scipy.stats import gaussian_kde
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

from f_preprocess_discharge import *


work_dir=Path('/scratch/fransjevanoors/global_sr')
#work_dir=Path('/tudelft.net/staff-umbrella/LSM root zone/global_sr')
data_dir=Path(f'{work_dir}/data')
out_dir = Path(f"{work_dir}/output")

print(work_dir)
print(out_dir)
print(data_dir)

# get list of all catchment ids available in the GSIM yearly discharge timeseries data
# gsim_id_list_up = []
# gsim_id_list_lo = []
# for filepath in glob.iglob(f'{data_dir}/GSIM_data/GSIM_indices/TIMESERIES/yearly/*'):
#     f = os.path.split(filepath)[1] # remove full path
#     f = f[:-5] # remove .year extension
#     fl = f.lower()
#     gsim_id_list_up.append(f)
#     gsim_id_list_lo.append(fl)
# print(gsim_id_list_lo)
# np.savetxt(f'{out_dir}/gsim/gsim_catch_id_list_up.txt',gsim_id_list_up,fmt='%s')
# np.savetxt(f'{out_dir}/gsim/gsim_catch_id_list_lo.txt',gsim_id_list_lo,fmt='%s')

gsim_id_list_lo = np.loadtxt(f'{out_dir}/gsim/gsim_catch_id_list_lo.txt',dtype=str) 
gsim_id_list_lo = gsim_id_list_lo[:]

# check catchments that are not processed yet
gsim_id_list_lo_done = []
for filepath in glob.iglob(f'{out_dir}/gsim/timeseries/*'):
    f = os.path.split(filepath)[1] # remove full path
    f = f[:-4] # remove .csv extension
    gsim_id_list_lo_done.append(f)

dif_list=list(set(gsim_id_list_lo)-set(gsim_id_list_lo_done))
print(len(dif_list))
gsim_id_list_lo=dif_list

# define folder with discharge timeseries data
fol_in = f'{data_dir}/GSIM_data/GSIM_indices/TIMESERIES/yearly/'

# define output folder
fol_out = f'{out_dir}/gsim/'

catch_list = gsim_id_list_lo
fol_in_list = [fol_in] * len(catch_list)
fol_out_list = [fol_out] * len(catch_list)

run_function_parallel(catch_list,fol_in_list,fol_out_list)
print('done')
