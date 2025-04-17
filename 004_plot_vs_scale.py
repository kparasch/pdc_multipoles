import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pathlib
import argparse


plt.rcParams['font.size'] = 12
# plt.rcParams['font.family'] = 'Nimbus Roman'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = [9,5]

parser = argparse.ArgumentParser()
parser.add_argument('--folder', nargs='?', type=str, default='./simulations')
args = parser.parse_args()


fname = pathlib.Path(args.folder) / pathlib.Path(f'PDCseptum_multipole_specifications_DA_MA.parquet')
df = pd.read_parquet(fname)

df.sort_values(by='scale', inplace=True)
xlabel = f'Scaling factor'

fig1 = plt.figure()
ax1 = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212)
ax1.plot(df['scale'].values, df['DA_area'], 'o-')
ax2.plot(df['scale'].values, df['MA_area'], 'o-')
ax2.set_xlabel(xlabel)
ax1.set_ylabel('DA area [mm$^2$]')
ax2.set_ylabel('MA area [mm]')


i0 = np.where(df.scale == 0)[0][0]
i1 = np.where(df.scale == 1)[0][0]
fig2 = plt.figure()
ax3 = fig2.add_subplot(111)
ax3.plot(df.iloc[i0]['x_DA']*1e3, df.iloc[i0]['DA']*1e3, 'o-', label='no multipoles')
ax3.plot(df.iloc[i1]['x_DA']*1e3, df.iloc[i1]['DA']*1e3, 'o-', label='specification')
ax3.set_xlabel('x [mm]')
ax3.set_ylabel('y [mm]')
ax3.legend()

fig3 = plt.figure()
ax4 = fig3.add_subplot(111)
ax4.plot(df.iloc[i0]['x_MA']*1e3, df.iloc[i0]['MA']*1e2, 'o-', label='no multipoles')
ax4.plot(df.iloc[i1]['x_MA']*1e3, df.iloc[i1]['MA']*1e2, 'o-', label='specification')
ax4.set_xlabel('x [mm]')
ax4.set_ylabel('δ [%]')
ax4.legend()



for ax in ax1, ax2, ax3, ax4:
    #ax.set_yscale('log')
    #ax.set_xscale('symlog')
    ax.grid()
plt.show()
