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
parser.add_argument('--scale', nargs='?', type=float, default=1)
parser.add_argument('--folder', nargs='?', type=str, default='./')
parser.add_argument('--plot', action='store_true')
args = parser.parse_args()

version='4.3.1'
fname = pathlib.Path(args.folder) / pathlib.Path(f'PDCseptum_multipole_specifications_DA_MA.parquet')
rms_dk1 = 1e-3
delta = 0.5e-2

dx = 0.5
x_max = 15
dy = 0.3
y_max = 4
ddelta = 0.5e-2
delta_max = 6e-2
n_turns = 2000
####

## setup xsuite model
line = xPIV.get_petra_iv(version=version, rms_dk1=rms_dk1)

line['pdcseptum_mpoles'].knl[2] = 1e-1
line['pdcseptum_mpoles'].knl[3] = 1e1
line['pdcseptum_mpoles'].knl[4] = 1e4
line['pdcseptum_mpoles'].knl[5] = 1e6
line['pdcseptum_mpoles'].knl[6] = 1e10
line['pdcseptum_mpoles'].knl[7] = 1e13
line['pdcseptum_mpoles'].knl[8] = 1e16
line['pdcseptum_mpoles'].knl[9] = 1e19
line['pdcseptum_mpoles'].knl[10] = 1e22
line['pdcseptum_mpoles'].knl[11] = 1e25
line['pdcseptum_mpoles'].knl[12] = 1e28
line['pdcseptum_mpoles'].knl[13] = 1e32
line['pdcseptum_mpoles'].knl[14] = 1e35
line['pdcseptum_mpoles'].knl[15] = 1e38
line['pdcseptum_mpoles'].knl[16] = 1e42
line['pdcseptum_mpoles'].knl[17] = 1e45
line['pdcseptum_mpoles'].knl[18] = 1e48
line['pdcseptum_mpoles'].knl[19] = 1e51

line['pdcseptum_mpoles'].ksl[2] = 1e-1
line['pdcseptum_mpoles'].ksl[3] = 1e1
line['pdcseptum_mpoles'].ksl[4] = 1e4
line['pdcseptum_mpoles'].ksl[5] = 1e7
line['pdcseptum_mpoles'].ksl[6] = 1e10
line['pdcseptum_mpoles'].ksl[7] = 1e13
line['pdcseptum_mpoles'].ksl[8] = 1e16
line['pdcseptum_mpoles'].ksl[9] = 1e19
line['pdcseptum_mpoles'].ksl[10] = 1e22
line['pdcseptum_mpoles'].ksl[11] = 1e25
line['pdcseptum_mpoles'].ksl[12] = 1e28
line['pdcseptum_mpoles'].ksl[13] = 1e32
line['pdcseptum_mpoles'].ksl[14] = 1e35
line['pdcseptum_mpoles'].ksl[15] = 1e38
line['pdcseptum_mpoles'].ksl[16] = 1e41
line['pdcseptum_mpoles'].ksl[17] = 1e45
line['pdcseptum_mpoles'].ksl[18] = 1e48
line['pdcseptum_mpoles'].ksl[19] = 1e51

for ii in range(2, 20):
    line['pdcseptum_mpoles'].knl[ii] *= args.scale
    line['pdcseptum_mpoles'].ksl[ii] *= args.scale
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
             'skew' : args.scale,
             'n_turns' : n_turns, 'timestamp' : pendulum.now().timestamp()
             }

with ProtectFile(fname, 'rb+', wait=1) as pf:
    df = pd.read_parquet(pf)
    df.loc[len(df)] = new_row.values()
    pf.seek(0)
    df.to_parquet(pf)

if args.plot:
    plt.show()
