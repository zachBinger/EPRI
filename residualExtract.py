import matplotlib.pyplot as plt

def getResiduals(resFile):
    my_file = open(resFile, "r")
    txt = my_file.read()
    my_file.close()
    sec = txt.split('((')
    resDict = dict()
    keys = []
    for i in range(1,len(sec)):
        title = sec[i].split(')')[0]
        key = title.split('"')[1]
        keys.append(key)
        data = sec[i].split(')')[1]
        keyData = []
        for j in range(1,int(data.split('\n')[-2].split('\t')[0])+1):
            datapoint = data.split('\n')[j].split('\t')[1]
            keyData.append(float(datapoint))

        resDict[keys[i-1]] = keyData
    return resDict

def plotResiduals(res):
    plotColors = ['k','b','g','r','c','m']
    fig, ax = plt.subplots(figsize=(8, 6.5))

    for idx, key in enumerate(list(res.keys())):
        ax.plot(res[key], color=plotColors[idx], label=key)

    ax.set_xlabel('Iterations', fontsize=20)
    ax.set_ylabel('Residual', fontsize=20)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)

    plt.legend(fontsize=10, frameon=False, loc='upper right')
    plt.yscale('log')
    plt.show()
    return fig


def compareResiduals(res):
    plotColors = ['k','b','g','r','c','m']
    fig, ax = plt.subplots(figsize=(8, 6.5))

    for idx, key in enumerate(list(res.keys())):
        ax.plot(res[key]['continuity'], color=plotColors[idx], label=key)

    ax.set_xlabel('Iterations', fontsize=20)
    ax.set_ylabel('Residual', fontsize=20)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)

    plt.legend(fontsize=10, frameon=False, loc='upper right')
    plt.yscale('log')
    plt.show()
    return fig

def getSimQuality(res):
    return res["continuity"][-1],res["x-velocity"][-1],res["y-velocity"][-1],res["z-velocity"][-1]
residuals = dict()
residuals['komega_coupled'] = getResiduals('/Users/zacharybinger/EPRI/residuals_komega_coupled.dat')
residuals['komega_simple'] = getResiduals('/Users/zacharybinger/EPRI/residuals_komega_simple.dat')
residuals['kepsilon_coupled'] = getResiduals('/Users/zacharybinger/EPRI/residuals_kepsilon_coupled.dat')
residuals['laminar_coupled'] = getResiduals('/Users/zacharybinger/EPRI/residuals_laminar_coupled.dat')
residuals['laminar_simple'] = getResiduals('/Users/zacharybinger/EPRI/residuals_laminar_simple.dat')

print(list(residuals.keys()))
# print(list(residuals.keys())[0])
# plotResiduals(residuals)
compareResiduals(residuals)
# cRes, xRes,yRes,zRes = getSimQuality(residuals['komega_coupled'])

# print(cRes, xRes,yRes,zRes) 
