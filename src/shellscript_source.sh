#!/bin/sh
d1=( 0.9374 0.758 0.7106 0.8517 0.6706 0.5144 0.9859 0.7213 0.645 0.6938 )
dsub=( 0.7089 0.787 0.2375 0.5263 0.7528 0.3268 0.3134 0.5599 0.761 0.4174 )
ltot=( 3.6805 3.1616 2.5415 3.6555 3.4731 3.7148 3.019 4.1792 4.0541 2.7494 )
lsub=( 0.7424 0.3274 0.504 0.21 0.6942 0.2966 0.6276 0.6416 0.3103 0.7534 )
angle=( 60.5265 38.4749 66.4436 65.59 21.6201 35.9188 54.8092 47.1441 41.9478 29.7799 )
compfac=( 1.2061 1.0718 1.0345 1.1302 1.1479 1.0024 1.1193 1.1645 1.4325 1.311 )

unset SLURM_GTIDS
module load ansys/20.1
echo "Start"
i=0
while [ $i -lt 10 ]
do
    sed -i "12s#.*#var D_1 = ${d1[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "13s#.*#var D_subFrac = ${dsub[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "14s#.*#var L_Total = ${ltot[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "15s#.*#var L_subFrac = ${lsub[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "16s#.*#var D2 = ${lsub[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "17s#.*#var angle = ${angle[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js
    sed -i "18s#.*#var compFactor = ${compfac[$i]}#" /groups/achilli/EPRI/batch_18/meshGen/Parameterized.js

	# Change mesh name in meshScript.js last line
    sed -i "218s#.*#DS.Script.doFileExport('/groups/achilli/EPRI/batch_18/assets/mesh_${i}.msh')#" /groups/achilli/EPRI/batch_18/meshGen/boundaryNaming3.js
	echo "Generating mesh_${i}.msh"
    runwb2 -X -R "/groups/achilli/EPRI/batch_18/meshGen/meshJournal.wbjn"
	i=$((i+1))
done

echo "Done"