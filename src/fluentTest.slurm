#!/bin/bash
#SBATCH --job-name=binger_batch_19_mesh_9
#SBATCH --ntasks=94
#SBATCH --mem=470gb
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=94
#SBATCH --time=24:00:00
#SBATCH --partition=standard
#SBATCH --account=achilli
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zbinger@email.arizona.edu

# SLURM Inherits your environment. cd $SLURM_SUBMIT_DIR not needed
pwd; hostname; date
 
module load ansys/20.1
fluent 3ddp -meshing -g -t16 -i /groups/achilli/EPRI/batch_19/journalFiles/test9.jou > /groups/achilli/EPRI/batch_19/reports/mesh_9.out
