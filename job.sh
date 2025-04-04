#!/bin/bash
#SBATCH --time=0-24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=petra4
#SBATCH --job-name=pdc_multipoles
#SBATCH -o outputs/slurm-%j.out
#SBATCH -e outputs/slurm-%j.err


order=$1
KL=$2
skew=$3

unset LD_PRELOAD                     # useful on max-display nodes, harmless on others
source /etc/profile.d/modules.sh     # make the module command available

source /data/dust/user/parascho/miniforge3/bin/activate base

pdc=/data/dust/user/parascho/001_pdc_multipoles

python $pdc/001_dynamic_aperture.py --folder simulations --order $order --KL $KL $skew


