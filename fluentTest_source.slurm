#!/bin/bash
#SBATCH --job-name=bingerFluentTest_mesh0
#SBATCH --ntasks=48
#SBATCH --mem=240gb
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=48         
#SBATCH --time=36:00:00   
#SBATCH --partition=standard
#SBATCH --account=achilli  
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zbinger@email.arizona.edu

# SLURM Inherits your environment. cd $SLURM_SUBMIT_DIR not needed
pwd; hostname; date
 
module load ansys/20.1
fluent 3ddp -meshing -g -t48 -i /groups/achilli/EPRI2021/scripts/fluentScripts/test1/test2.jou > /groups/achilli/EPRI2021/data/outputFiles/meshTests/mesh0.out

