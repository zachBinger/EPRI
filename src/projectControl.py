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

print(localDir)

df = pd.read_csv(reportPath+'progressReport.csv')
paramDF = pd.read_csv(reportPath+'testParams200.csv')

def getUnitCellLen(a):
    ang = math.cos(math.radians(a))
    return ang

angles = list(map(getUnitCellLen,paramDF['angle'].values))
unitCellLens = 2*(paramDF['L_Total'].values/1000)*list(map(getUnitCellLen,paramDF['angle'].values))

def writeSlurmFiles(batch,m,batchSlurmPath):
    shutil.copyfile(sourcePath+"allRun.sh", batchSlurmPath+"allRun.sh")

    str1 = "#SBATCH --job-name=binger_"
    str2_front = "fluent 3ddp -meshing -g -t28 -i "+HPCDir+"batch_"+str(batch)+"/journalFiles"
    str2_back = " > "+HPCDir+"batch_"+str(batch)+"/reports/"

    my_file = open("/Users/zacharybinger/Desktop/testDir/fluentTest.slurm", "r")
    string_list = my_file.readlines()
    my_file.close()

    string_list[1] = str1+"batch_"+str(batch)+"_mesh_"+str(m)+ "\n"
    string_list[16] = str2_front+"/test"+str(m)+".jou" + str2_back + "mesh_" +str(m)+ ".out" + "\n"

    my_file = open(sourcePath+"fluentTest.slurm", "w")
    new_file_contents = "".join(string_list)
    my_file.write(new_file_contents)
    my_file.close()
    shutil.copyfile(sourcePath+"fluentTest.slurm", batchSlurmPath+"fluentTest.slurm")

def addExp(b,m,d,v):
    batchNum = b
    denStrings = ['water-di', 'water-35g', 'water-70g', 'water-120g']
    str3 = "/report surface-integrals area-weighted-avg inlet vPlane1 vPlane2 vPlane3 vPlane4 vPlane5 vPlane6 vPlane7 outlet , pressure yes "+HPCDir+"batch_"+str(batch)+"/data/pressure/"
    str4_front = '/define b-c fluid fluid yes '
    str4_back =' no no no no 0 no 0 no 0 no 0 no 0 no 1 no yes no no no'
    str5_front = '/define b-c velocity-inlet inlet no no yes yes no '
    str5_back = ' no 0 , , , , ,'
    vels = ["005","015","025","035"]

    stringList = []
    stringList.append(str4_front+denStrings[d-1]+str4_back+'\n')
    for idx, vel in enumerate(v):
            stringList.append(str5_front+str(v[idx])+str5_back+'\n')
            stringList.append(';initialize'+'\n')
            stringList.append('/solve initialize initialize-flow yes'+'\n')
            stringList.append(';solve'+'\n')
            stringList.append('/solve iterate 300'+'\n')
            stringList.append(str3+"mesh_"+str(m)+"_density"+str(d)+"_"+str(vel)[0]+str(vel)[2:]+".srp\n")
            stringList.append(';'+'\n')
            stringList.append(';'+'\n')
            stringList.append(';'+'\n')

    # print(stringList)
    return stringList     

def writeJouDirs(batch,m, df):

    # str1 = "/file read-mesh /groups/achilli/EPRI2021/meshes/scriptedMeshes/batch"+str(batch)+"/"
    str1 = "/file read-mesh "+HPCDir+"batch_"+str(batch)+"/assets/"
    str2 = "/surface plane-point-n-normal vPlane"
    # str3 = "/report surface-integrals area-weighted-avg inlet vPlane1 vPlane2 vPlane3 vPlane4 vPlane5 vPlane6 vPlane7 vPlane8 vPlane9 vPlane10 vPlane11 vPlane12 vPlane13 vPlane14 vPlane15 outlet , pressure yes "+hpcPath+"/pressureTestResults/batch"+str(batch)+"/"
    str3 = "/report surface-integrals area-weighted-avg inlet vPlane1 vPlane2 vPlane3 vPlane4 vPlane5 vPlane6 vPlane7 outlet , pressure yes "+HPCDir+"batch_"+str(batch)+"/data/pressure/"

    denStrings = ['water-di', 'water-35g', 'water-70g', 'water-120g']
    str4_front = '/define b-c fluid fluid yes '
    str4_back =' no no no no 0 no 0 no 0 no 0 no 0 no 1 no yes no no no'
    str5_front = '/define b-c velocity-inlet inlet no no yes yes no '
    str5_back = ' no 0 , , , , ,'
    # vel = ["005","015","025","035"]

    my_file = open(sourcePath+"test0.jou", "r")
    string_list = my_file.readlines()
    my_file.close()
    string_list[35:] = []

    string_list[1] = str1+"mesh_"+str(m)+".msh"+"\n"

    unitCellLen = unitCellLens[(10*(batch-1))+m]
    planeStrings = string_list[15:23]
    newPlaneStrings = []
    for idx, plane in enumerate(planeStrings):
        newPlaneStrings.append(str2+str(idx+1)+" "+str(round(unitCellLen*(idx+1)-unitCellLen/2,6))+" 0 0 1 0 0\n")
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
    
    shutil.copyfile(sourcePath+"test0Auto.jou", deployPath+"batch_"+str(batch)+"/journalFiles/test"+str(m)+".jou")
    # print(deployPath+"batch_"+str(batch)+"/journalFiles/test"+str(m)+".jou")



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

        writeSlurmFiles(batchNum,1,batchPath+'slurmFiles/')



for i in range(2):
    makeBatch(i)
    writeJouDirs(i,1, df)

# print(df.head())

# def getUnitCellLen(a):
#     ang = math.cos(math.radians(a))
#     return ang

# angles = list(map(getUnitCellLen,paramDF['angle'].values))
# unitCellLens = 2*(paramDF['L_Total'].values/1000)*list(map(getUnitCellLen,paramDF['angle'].values))

# def writeSlurmDirs(batch,m):
#     if "batch"+str(batch) not in listdir(slurmPath):
#         os.mkdir(testDirPath+"tests/slurmFiles/batch"+str(batch))
#         shutil.copyfile(testDirPath+"allRun.sh", testDirPath+"tests/slurmFiles/batch"+str(batch)+"/allRun.sh")

#     # str1 = "#SBATCH --job-name=bingerFluentTest_"
#     # str2_front = "fluent 3ddp -meshing -g -t28 -i "+hpcPath+"/journalFiles/batch"+str(batch)
#     # str2_back = " > "+hpcPath+"/outputFiles/batch"

#     # my_file = open("/Users/zacharybinger/Desktop/testDir/fluentTest.slurm", "r")
#     # string_list = my_file.readlines()
#     # my_file.close()

#     # string_list[1] = str1+"batch"+str(batch)+"_mesh"+str(m)+ "\n"
#     # string_list[16] = str2_front+"/test"+str(m)+".jou" + str2_back + str(batch) + "/mesh" +str(m) + "\n"

#     # my_file = open("/Users/zacharybinger/Desktop/testDir/fluentTest.slurm", "w")
#     # new_file_contents = "".join(string_list)
#     # my_file.write(new_file_contents)
#     # my_file.close()