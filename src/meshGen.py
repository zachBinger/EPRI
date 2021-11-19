import os
import math
from os import listdir
from os.path import isfile, join
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HPCDir = '/groups/achilli/EPRI/'
localDir = os.getcwd()
# os.chdir(path)

batch = 1

deployPath = localDir + '/deploy/'
dataPath = deployPath + '/data/'
meshPath = deployPath + '/assets/'
jouPath = deployPath + '/journalFiles/'
slurmPath = deployPath + '/slurmFiles/'
reportPath = localDir + '/reports/'
sourcePath = localDir + '/src/'

df = pd.read_csv(reportPath+'progressReport.csv')
paramDF = pd.read_csv(reportPath+'testParams200.csv')

# if "testDir" in listdir(mypath):
#     shutil.rmtree('testDir')

# os.mkdir("testDir")
# mypath = mypath+"/testDir"
# os.chdir(mypath)

# onlyDirs = [f for f in listdir(mypath)if isdir(join(mypath, f))]
# onlyFiles = [f for f in listdir(mypath)if isfile(join(mypath, f))]

paramsPerBatch = 10
# numOfMeshes = len(df['Mesh #'])
# numOfBatches = int(numOfMeshes/paramsPerBatch)

# desiredDirs = ["batch"+str(group+1) for group in range(numOfBatches)]

P1 = paramDF['D_1'].tolist()
P2 = paramDF['D_subFrac'].tolist()
P3 = paramDF['L_Total'].tolist()
P4 = paramDF['L_subFrac'].tolist()
P5 = paramDF['angle'].tolist()
P6 = paramDF['compFactor'].tolist()

P1 = [round(num, 4) for num in P1]
P2 = [round(num, 4) for num in P2]
P3 = [round(num, 4) for num in P3]
P4 = [round(num, 4) for num in P4]
P5 = [round(num, 4) for num in P5]
P6 = [round(num, 4) for num in P6]

p = [P1,P2,P3,P4,P5,P6]

def writeString(batch, batchDir, params, paramsPerBatch = paramsPerBatch):
    str1 = "d1=( "
    str2 = "dsub=( "
    str3 = "ltot=( "
    str4 = "lsub=( "
    str5 = "angle=( "
    str6 = "compfac=( "

    for idx in range(paramsPerBatch):
        str1 = str1+str(params[0][idx+paramsPerBatch*batch])+" "
        str2 = str2+str(params[1][idx+paramsPerBatch*batch])+" "
        str3 = str3+str(params[2][idx+paramsPerBatch*batch])+" "
        str4 = str4+str(params[3][idx+paramsPerBatch*batch])+" "
        str5 = str5+str(params[4][idx+paramsPerBatch*batch])+" "
        str6 = str6+str(params[5][idx+paramsPerBatch*batch])+" "

    str1 = str1+")\n"
    str2 = str2+")\n"
    str3 = str3+")\n"
    str4 = str4+")\n"
    str5 = str5+")\n"
    str6 = str6+")\n"

    params = [str1,str2,str3,str4,str5,str6]

    my_file = open(batchDir, "r")
    string_list = my_file.readlines()
    my_file.close()

    for idx in range(len(params)):
        string_list[idx+1] = params[idx]

    for idx in range(7):
        string_list[14] = '    sed -i "12s#.*#var D_1 = ${d1[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[15] = '    sed -i "13s#.*#var D_subFrac = ${dsub[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[16] = '    sed -i "14s#.*#var L_Total = ${ltot[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[17] = '    sed -i "15s#.*#var L_subFrac = ${lsub[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[18] = '    sed -i "16s#.*#var D2 = ${lsub[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[19] = '    sed -i "17s#.*#var angle = ${angle[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[20] = '    sed -i "18s#.*#var compFactor = ${compfac[$i]}#" '+HPCDir+'batch_'+str(batch)+'/meshGen/Parameterized.js\n'
        string_list[23] = '    sed -i "218s#.*#DS.Script.doFileExport('+"'"+HPCDir+"batch_"+str(batch)+"/assets/mesh_${i}.msh')#"+'" '+ HPCDir+'batch_'+str(batch)+'/meshGen/boundaryNaming3.js\n'
        string_list[25] = '    runwb2 -X -R "/groups/achilli/EPRI/batch_'+str(batch)+'/meshGen/meshJournal.wbjn"\n'
    my_file = open(batchDir, "w")
    new_file_contents = "".join(string_list)

    my_file.write(new_file_contents)
    my_file.close()

    return

def writeJouFile(batch):
    str1 = 'DSscript = open("'+HPCDir+'batch_'
    str2 = '/meshGen/Parameterized.js", "r")'
    str3 = '/meshGen/boundaryNaming3.js", "r")'

    my_file = open('/Users/zacharybinger/EPRI/src/meshJournal.wbjn', "r")
    string_list = my_file.readlines()
    my_file.close()

    string_list[8] = str1 + str(batch) + str2 +"\n"
    string_list[20] = str1 + str(batch) + str3+"\n"

    print(string_list[8])
    print(string_list[20])
    my_file = open('/Users/zacharybinger/EPRI/src/meshJournal.wbjn', "w")
    new_file_contents = "".join(string_list)

    my_file.write(new_file_contents)
    my_file.close()

writeJouFile(0)
# writeString(0, '/Users/zacharybinger/EPRI/src/shellscript_source.sh', p)