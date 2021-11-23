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
deployPath = localDir + '/deploy/'
dataPath = deployPath + '/data/'
meshPath = deployPath + '/assets/'
jouPath = deployPath + '/journalFiles/'
slurmPath = deployPath + '/slurmFiles/'
reportPath = localDir + '/reports/'
sourcePath = localDir + '/src/'

iterations = 100
numberofplanes = 4
samplePlanes = list(range(1,numberofplanes+1))
samplingPlanes= ['vPlane'+str(x) for x in samplePlanes]

df = pd.read_csv(reportPath+'progressReport.csv')
paramDF = pd.read_csv(reportPath+'testParams200.csv')
paramsPerBatch = 10
df['Batch'] = df['Batch']-1

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

def getUnitCellLen(a):
    ang = math.cos(math.radians(a))
    return ang

angles = list(map(getUnitCellLen,paramDF['angle'].values))
unitCellLens = 2*(paramDF['L_Total'].values/1000)*list(map(getUnitCellLen,paramDF['angle'].values))

def writeSlurmFiles(batch,m):
    cores = 4
    hrs = 1
    mem = cores*5

    str1 = "#SBATCH --job-name=binger_"
    str2_front = "fluent 3ddp -meshing -g -t"+str(cores)+" -i "+HPCDir+"batch_"+str(batch)+"/journalFiles"
    str2_back = " > "+HPCDir+"batch_"+str(batch)+"/reports/"

    my_file = open(sourcePath+"fluentTest.slurm", "r")
    string_list = my_file.readlines()
    my_file.close()

    string_list[1] = str1+"batch_"+str(batch)+"_mesh_"+str(m)+ "\n"
    string_list[2] = "#SBATCH --ntasks="+ str(cores)+ "\n"
    string_list[3] = "#SBATCH --mem="+ str(mem)+ "gb\n"
    string_list[5] = "#SBATCH --ntasks-per-node="+ str(cores)+ "\n"
    string_list[6] = "#SBATCH --time="+str(hrs)+":00:00\n"
    string_list[16] = str2_front+"/test"+str(m)+".jou" + str2_back + "mesh_" +str(m)+ ".out" + "\n"

    my_file = open(sourcePath+"fluentTest.slurm", "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()
    
def addExp(b,m,d,v):
    batchNum = b
    denStrings = ['water-di', 'water-35g', 'water-70g', 'water-120g']
    # str3 = "/report surface-integrals area-weighted-avg inlet vPlane1 vPlane2 vPlane3 vPlane4 vPlane5 vPlane6 vPlane7 outlet , pressure yes "+HPCDir+"batch_"+str(batchNum)+"/data/pressure/"
    str3 = "/report surface-integrals area-weighted-avg inlet "+" ".join(samplingPlanes)+" outlet , pressure yes "+HPCDir+"batch_"+str(batchNum)+"/data/pressure/"
    str4_front = '/define b-c fluid fluid yes '
    str4_back =' no no no no 0 no 0 no 0 no 0 no 0 no 1 no yes no no no'
    str5_front = '/define b-c velocity-inlet inlet no no yes yes no '
    str5_back = ' no 0 , , , , ,'
    reportStr = "/report summary y "+HPCDir+"/batch_"+str(batchNum)+"/reports/expReport_"+str(m)+".sum\n"
    residualStr = "/plot residuals-set plot-to-file "+HPCDir+"batch_"+str(batchNum)+"/data/residuals_"+str(m)+".dat\n"
    exportStr = "/file export ensight-gold "+HPCDir+"batch_"+str(batchNum)+"/data/exp_"+str(m)+" pressure velocity-magnitude x-velocity y-velocity z-velocity x-wall-shear y-wall-shear z-wall-shear vorticity-mag dp-dx density helicity viscosity-lam strain-rate-mag q y fluid , , , \n"

    stringList = []
    stringList.append(str4_front+denStrings[d-1]+str4_back+'\n')
    for idx, vel in enumerate(v):
            stringList.append(str5_front+str(v[idx])+str5_back+'\n')
            stringList.append(';initialize'+'\n')
            stringList.append('/solve initialize initialize-flow yes'+'\n')
            stringList.append(';solve'+'\n')
            stringList.append('/solve iterate '+str(iterations)+'\n')
            stringList.append(str3+"mesh_"+str(m)+"_density"+str(d)+"_"+str(vel)[0]+str(vel)[2:]+".srp\n")
            stringList.append(reportStr)
            stringList.append('/solve iterate 1'+'\n')
            stringList.append(residualStr)
            stringList.append(exportStr)
            stringList.append(';'+'\n')
            stringList.append(';'+'\n')
            stringList.append(';'+'\n')

    return stringList     

def writeJouDirs(batch,m, df):
    str1 = "/file read-mesh "+HPCDir+"batch_"+str(batch)+"/assets/"
    # str1 = "/file read-mesh /groups/achilli/EPRI2021/meshes/scriptedMeshes/batch"+str(batch)+"/"
    str2 = "/surface plane-point-n-normal vPlane"
    
    my_file = open(sourcePath+"test0.jou", "r")
    string_list = my_file.readlines()
    my_file.close()
    string_list[35:] = []

    string_list[1] = str1+"mesh_"+str(m)+".msh"+"\n"

    unitCellLen = unitCellLens[(10*(batch-1))+m]
    planeStrings = string_list[15:23]
    newPlaneStrings = []
    for idx, plane in enumerate(samplingPlanes):
        newPlaneStrings.append(str2+str(idx+1)+" 0 0 "+str(round(unitCellLen*(idx+1)-unitCellLen/2,6))+" 0 0 1\n")
    string_list[15:23] = newPlaneStrings

    densities = df.loc[(df['Batch'] == batch) & (df['Mesh #'] == m)]['Density'].unique()
    newStrings = []
    for den in densities:
        newStrings = newStrings + addExp(batch, m, den, df.loc[(df['Batch'] == batch) & (df['Mesh #'] == batch) & (df['Density'] == den)]['Velocity'].values)
    
    string_list = string_list + newStrings

    string_list.append('/report/system/proc-stats\n')
    string_list.append('/report system time-stats\n')
    string_list.append('/parallel timer usage\n')
    string_list.append('/exit yes\n')

    my_file = open(sourcePath+"test0Auto.jou", "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()
    
def makeBatch(batchNum):
    if "batch_"+str(batchNum) not in listdir(deployPath):
        batchPath = deployPath+"batch_"+str(batchNum) + '/'
        os.mkdir(batchPath)
        os.mkdir(batchPath+'data/')
        os.mkdir(batchPath+'data/pressure')
        os.mkdir(batchPath+'data/flow')
        os.mkdir(batchPath+'data/raw')
        os.mkdir(batchPath+'data/residuals')
        os.mkdir(batchPath+'assets/')
        os.mkdir(batchPath+'journalFiles/')
        os.mkdir(batchPath+'slurmFiles/')
        os.mkdir(batchPath+'reports/')
        os.mkdir(batchPath+'meshGen/')

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

    my_file = open('/Users/zacharybinger/EPRI/src/meshJournal.wbjn', "w")
    new_file_contents = "".join(string_list)

    my_file.write(new_file_contents)
    my_file.close()

# for idx, bat in enumerate(df['Batch'].unique()):
for idx, bat in enumerate(range(20)):
    makeBatch(bat)
    writeString(bat, '/Users/zacharybinger/EPRI/src/shellscript_source.sh', p)
    writeJouFile(bat)

    shutil.copyfile(sourcePath+"meshJournal.wbjn", deployPath+"batch_"+str(bat)+"/meshGen/meshJournal.wbjn")
    shutil.copyfile(sourcePath+"shellscript_source.sh", deployPath+"batch_"+str(bat)+"/meshGen/shellscript_source.sh")
    shutil.copyfile(sourcePath+"Parameterized.js", deployPath+"batch_"+str(bat)+"/meshGen/Parameterized.js")
    shutil.copyfile(sourcePath+"boundaryNaming3.js", deployPath+"batch_"+str(bat)+"/meshGen/boundaryNaming3.js")

    # for idx2, mesh in enumerate(df.loc[(df['Batch'] == bat)]['Mesh #'].unique()):
    for idx2, mesh in enumerate(range(10)):
        writeJouDirs(bat,mesh, df)
        writeSlurmFiles(bat,mesh)
        shutil.copyfile(sourcePath+"test0Auto.jou", deployPath+"batch_"+str(bat)+"/journalFiles/test"+str(mesh)+".jou")
        shutil.copyfile(sourcePath+"fluentTest.slurm", deployPath+"batch_"+str(bat)+"/slurmFiles/fluentTest"+str(mesh)+".slurm")
