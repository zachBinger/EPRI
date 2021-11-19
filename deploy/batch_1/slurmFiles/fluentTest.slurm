#!/bin/bash
#SBATCH --job-name=binger_batch_1_mesh_1
#SBATCH --ntasks=28
#SBATCH --mem=140gb
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28     
#SBATCH --time=12:00:00   
#SBATCH --partition=standard
#SBATCH --account=achilli
#SBATCH --mail-type=ALL
#SBATCH --mail-user=zbinger@email.arizona.edu

# SLURM Inherits your environment. cd $SLURM_SUBMIT_DIR not needed
pwd; hostname; date
 
module load ansys/20.1
fluent 3ddp -meshing -g -t28 -i /groups/achilli/EPRI/batch_1/journalFiles/test1.jou > /groups/achilli/EPRI/batch_1/reports/mesh_1.out
