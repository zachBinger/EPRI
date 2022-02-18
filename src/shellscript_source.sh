#!/bin/sh
d1=( 0.4016 0.6434 0.4546 0.39 0.522 0.7852 0.6581 0.7181 0.5836 0.5605 )
dsub=( 0.545 0.4786 0.5623 0.6048 0.7653 0.6432 0.428 0.6628 0.6765 0.7727 )
ltot=( 4.2596 3.6669 3.5864 3.8793 4.2711 4.697 3.1589 3.8629 4.4493 4.868 )
lsub=( 0.6154 0.6208 0.5424 0.2004 0.7853 0.7428 0.2401 0.6407 0.5789 0.5916 )
angle=( 67.1556 61.1994 25.6629 47.3644 46.4261 23.1221 66.3426 22.0357 62.6952 57.2364 )
compfac=( 0.754 0.8436 0.8472 0.8869 0.7455 0.8537 0.9191 0.9899 0.7881 0.7374 )

unset SLURM_GTIDS
module load ansys/20.1
echo "Start"
i=0
while [ $i -lt 10 ]
do
    sed -i "12s#.*#var D_1 = ${d1[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "13s#.*#var D_subFrac = ${dsub[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "14s#.*#var L_Total = ${ltot[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "15s#.*#var L_subFrac = ${lsub[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "16s#.*#var D2 = ${lsub[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "17s#.*#var angle = ${angle[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js
    sed -i "18s#.*#var compFactor = ${compfac[$i]}#" /groups/achilli/EPRI/batch_19/meshGen/Parameterized.js

	# Change mesh name in meshScript.js last line
    sed -i "211s#.*#DS.Script.doFileExport('/groups/achilli/EPRI/batch_19/assets/mesh_${i}.msh')#" /groups/achilli/EPRI/batch_19/meshGen/boundaryNaming3.js
	echo "Generating mesh_${i}.msh"
    runwb2 -X -R "/groups/achilli/EPRI/batch_19/meshGen/meshJournal.wbjn"
	i=$((i+1))
done
echo "Done"