#!/bin/sh

_mydir="`pwd`"

for file in "$_mydir/"*.slurm ;
do
    sbatch ${file}
done