import pandas as pd
import pathlib
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--order', nargs='?', type=int, default=None)
parser.add_argument('--folder', nargs='?', type=str, default='./')
parser.add_argument('--skew', action='store_true')
args = parser.parse_args()

kstr = 'ksl' if args.skew else 'knl'
fname = pathlib.Path(args.folder) / pathlib.Path( f'PDCseptum_multipole_DA_MA_{kstr}{args.order}.parquet')

columns = ['x_DA', 'DA', 'DA_area', 'x_MA', 'MA', 'MA_area',
           'delta', 'version', 'rms_dk1', 'dx', 'x_max', 'dy',
           'y_max', 'ddelta', 'delta_max', 'order', 'KL', 'skew',
           'n_turns', 'timestamp']

df = pd.DataFrame(columns=columns)
df.to_parquet(fname)