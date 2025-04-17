import pandas as pd
import pathlib
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--folder', nargs='?', type=str, default='./')
args = parser.parse_args()

fname = pathlib.Path(args.folder) / pathlib.Path( f'PDCseptum_multipole_specifications_DA_MA.parquet')

columns = ['x_DA', 'DA', 'DA_area', 'x_MA', 'MA', 'MA_area',
           'delta', 'version', 'rms_dk1', 'dx', 'x_max', 'dy',
           'y_max', 'ddelta', 'delta_max', 'scale',
           'n_turns', 'timestamp']

df = pd.DataFrame(columns=columns)
df.to_parquet(fname)