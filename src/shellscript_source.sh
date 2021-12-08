#!/bin/sh
d1=( 0.6412 0.8607 0.8992 0.5793 0.3129 0.3094 0.9773 0.9451 0.3945 0.564 )
dsub=( 0.3621 0.3665 0.3755 0.7429 0.6099 0.4702 0.5363 0.4354 0.6866 0.6978 )
ltot=( 4.8993 3.4494 3.9348 3.2986 4.3192 4.2484 2.8226 3.3132 4.4004 3.2425 )
lsub=( 0.6319 0.4797 0.6722 0.4022 0.5892 0.5975 0.2776 0.5391 0.676 0.7639 )
angle=( 68.9765 39.1408 40.0216 45.318 44.3777 25.0587 55.1926 21.2823 42.4889 28.8725 )
compfac=( 1.3471 1.1947 1.0361 1.3296 1.1882 1.2328 1.3481 1.3383 1.4524 1.2826 )

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
    sed -i "218s#.*#DS.Script.doFileExport('/groups/achilli/EPRI/batch_19/assets/mesh_${i}.msh')#" /groups/achilli/EPRI/batch_19/meshGen/boundaryNaming3.js
	echo "Generating mesh_${i}.msh"
    runwb2 -X -R "/groups/achilli/EPRI/batch_19/meshGen/meshJournal.wbjn"
	i=$((i+1))
done
echo "Done"