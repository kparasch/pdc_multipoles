import pandas as pd
import matplotlib.pyplot as plt

import pathlib
import argparse


plt.rcParams['font.size'] = 12
# plt.rcParams['font.family'] = 'Nimbus Roman'
plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = [9,5]

parser = argparse.ArgumentParser()
parser.add_argument('--order', nargs='?', type=int, default=None)
parser.add_argument('--folder', nargs='?', type=str, default='./simulations')
parser.add_argument('--skew', action='store_true')
args = parser.parse_args()

korder = args.order - 1

kstr = 'ksl' if args.skew else 'knl'
fname = pathlib.Path(args.folder) / pathlib.Path(f'PDCseptum_multipole_DA_MA_{kstr}{korder}.parquet')
df = pd.read_parquet(fname)

df.sort_values(by='KL', inplace=True)
if args.skew:
    xlabel = f'$KsL_{korder}$'
else:
    xlabel = f'$KnL_{korder}$'

fig1 = plt.figure()
ax1 = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212)
ax1.plot(df['KL'].values, df['DA_area'], 'o-')
ax2.plot(df['KL'].values, df['MA_area'], 'o-')
ax2.set_xlabel(xlabel)
ax1.set_ylabel('DA area [mm$^2$]')
ax2.set_ylabel('MA area [mm]')

for ax in ax1, ax2:
    #ax.set_yscale('log')
    ax.set_xscale('symlog')
    ax.grid()

plt.show()
