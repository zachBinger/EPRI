#!/bin/sh
d1=( 0.9609 0.7803 0.8051 0.414 0.8908 0.8137 0.5541 0.9233 0.5469 0.747 )
dsub=( 0.6353 0.2859 0.493 0.6482 0.4971 0.4293 0.2138 0.2488 0.5217 0.6753 )
ltot=( 4.6155 4.8232 4.772 3.1031 3.3487 4.4728 4.3746 4.1242 3.871 3.386 )
lsub=( 0.3817 0.2902 0.7498 0.5443 0.3211 0.7882 0.2898 0.4681 0.5518 0.3065 )
angle=( 26.2048 54.213 58.4526 27.6451 38.9812 44.7853 39.9573 59.9749 37.8381 63.5678 )
compfac=( 1.2423 1.1671 1.4084 1.3724 1.4069 1.463 1.1961 1.1255 1.0819 1.3185 )

unset SLURM_GTIDS
module load ansys/20.1
echo "Start"
i=0
while [ $i -lt 10 ]
do
    sed -i "12s#.*#var D_1 = ${d1[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "13s#.*#var D_subFrac = ${dsub[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "14s#.*#var L_Total = ${ltot[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "15s#.*#var L_subFrac = ${lsub[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "16s#.*#var D2 = ${lsub[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "17s#.*#var angle = ${angle[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js
    sed -i "18s#.*#var compFactor = ${compfac[$i]}#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/Parameterized.js

	# Change mesh name in meshScript.js last line
    sed -i "171s#.*#DS.Script.doFileExport('/groups/achilli/EPRI/batch_1/assets/mesh_${i}.msh')#" /groups/achilli/EPRI2021/scripts/meshScripts/batch1/boundaryNaming3.js
	echo "Generating mesh_${i}.msh"
    runwb2 -X -R "/groups/achilli/EPRI2021/scripts/meshScripts/batch1/meshJournal.wbjn"
	i=$((i+1))
done

echo "Done" 