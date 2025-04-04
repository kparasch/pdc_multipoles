import numpy as np
import matplotlib.pyplot as plt
import argparse
import pendulum
import pandas as pd

from xaux import ProtectFile

import xPIV
import piv_filemanager as pfm
import pathlib

plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = [9,5]
plt.rcParams['figure.autolayout'] = True
plt.close('all')



parser = argparse.ArgumentParser()
parser.add_argument('--order', nargs='?', type=int, default=None)
parser.add_argument('--KL', nargs='?', type=float, default=0)
parser.add_argument('--skew', action='store_true')
parser.add_argument('--plot', action='store_true')
args = parser.parse_args()

version='4.3.1'
kstr = 'ksl' if args.skew else 'knl'
fname = pathlib.Path(f'PDCseptum_multipole_DA_MA_{kstr}{args.order}.parquet')
rms_dk1 = 1e-3
delta = 0.5e-2

dx = 0.5
x_max = 15
dy = 0.3
y_max = 4
ddelta = 0.5e-2
delta_max = 6e-2
n_turns = 100
####

## setup xsuite model
line = xPIV.get_petra_iv(version=version, rms_dk1=rms_dk1)

if args.order is not None:
    if args.skew:
        line['pdcseptum_mpoles'].ksl[args.order] = args.KL
    else:
        line['pdcseptum_mpoles'].knl[args.order] = args.KL
###############################################

#### Dynamic and Momentum aperture 
x_grid_da, da = xPIV.get_DA(line, delta=delta, n_turns=n_turns,
                        dx=dx, x_max=x_max, dy=dy, y_max=y_max)
            
x_grid_ma, ma = xPIV.get_MA(line, ddelta=ddelta, delta_max=delta_max,
                    dx=dx, x_max=x_max, n_turns=n_turns)
da_area = np.sum(da*1e3)*dx
ma_area = np.sum(ma)*dx

if args.plot:
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    ax3.plot(x_grid_da*1e3, da*1e3, '-')
    ax3.set_xlabel('x [mm]')
    ax3.set_ylabel('y [mm]')

    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
    ax4.plot(x_grid_ma*1e3, ma*100, '-')
    ax4.set_xlabel('x [mm]')
    ax4.set_ylabel('δ [%]')
##############################################

new_row = {'x_DA' : x_grid_da, 'DA' : da, 'DA_area' : da_area,
             'x_MA' : x_grid_ma, 'MA' : ma, 'MA_area' : ma_area,
             'delta' : delta, 'version' : version, 'rms_dk1' : rms_dk1,
             'dx' : dx, 'x_max' : x_max, 'dy' : dy, 'y_max' : y_max,
             'ddelta' : ddelta,  'delta_max' : delta_max,
             'order' : args.order, 'KL' : args.KL, 'skew' : args.skew,
             'n_turns' : n_turns, 'timestamp' : pendulum.now().timestamp()
             }

with ProtectFile(fname, 'r+', wait=1) as pf:
    if not fname.exists():
        df = pd.DataFrame(columns=new_row.keys())
    else:
        df = pd.read_parquet(fname)
    df.loc[len(df)] = new_row.values()
    df.to_parquet(fname)

if args.plot:
    plt.show()