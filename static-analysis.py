import os
import json
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def read_measures(repository_name, version, abc, npm, npa, wmc, coa, cda, size, complexity):
    magn = []
    pub_met = []
    pub_att = []
    wmc_val = []
    hal_val = []
    loc_val = []
    cyc_val = []
    coa_val = []
    cda_val = []
    for filename in glob.iglob("data/" + repository_name + "/" + version + '/**/*.json', recursive=True):
        with open(filename, "r") as file:
            jsonData = json.load(file)
            magn.append(float(jsonData["metrics"]["abc"]["magnitude"]))
            pub_met.append(float(jsonData["metrics"]["npm"]["total"]))
            pub_att.append(float(jsonData["metrics"]["npa"]["total"]))
            coa_val.append(float(jsonData["metrics"]["npm"]["average"] or 0))
            cda_val.append(float(jsonData["metrics"]["npa"]["average"] or 0))
            wmc_val.append(float(jsonData["metrics"]["wmc"]["wmc"]))
            hal_val.append(float(jsonData["metrics"]["halstead"]["estimated_program_length"]))
            loc_val.append(float(jsonData["metrics"]["loc"]["ploc"]))
            cyc_val.append(float(jsonData["metrics"]["cyclomatic"]["sum"]))

            # print(os.path.basename(jsonData["name"]))
            # print(jsonData["metrics"]["abc"]["magnitude"])
    magn = [float(x) for x in magn]
    pub_met = [float(x) for x in pub_met]
    pub_att = [float(x) for x in pub_att]
    wmc_val = [float(x) for x in wmc_val]
    # print(magn)
    abc.append( [min(magn), max(magn), sum(magn)/len(magn), sum(magn)] )
    npm.append( [min(pub_met), max(pub_met), sum(pub_met)/len(pub_met), sum(pub_met)] )
    npa.append( [min(pub_att), max(pub_att), sum(pub_att)/len(pub_att), sum(pub_att)] )
    cda.append( [min(cda_val), max(cda_val), sum(cda_val)/len(cda_val), sum(cda_val)] )
    coa.append( [min(coa_val), max(coa_val), sum(coa_val)/len(coa_val), sum(coa_val)] )
    wmc.append( [min(wmc_val), max(wmc_val), sum(wmc_val)/len(wmc_val), sum(wmc_val)] )
    size.append( [sum(magn), sum(hal_val), sum(loc_val), sum(cyc_val)] )
    print( [sum(magn), sum(hal_val), sum(loc_val), sum(cyc_val)] )
    complexity.append( [sum(wmc_val), sum(cyc_val)] )
    # print(abc)
    return


def plot_measures(repositories, versions, abc, title, y_name, file):
    V_axis = []
    Y_axis=[]
    for i in range(0, len(repositories)):
        V_axis.append([repositories[i] + "_sum", repositories[i] + "_min", repositories[i] + "_max", repositories[i] + "_avg"])
        Y_axis.append([abc[i][3], abc[i][0], abc[i][1], abc[i][2]])
    min_y=float("inf")
    max_y=0
    for y in Y_axis:
        for value in y:
            min_y=min(min_y,value)
            max_y=max(max_y,value)
    plt.rcParams.update({'font.size': 24})
    figure(figsize=(42,22), dpi=80)
    for i in range(0,len(repositories)):
        bar=plt.barh(V_axis[i], Y_axis[i], 0.66, label = repositories[i])
        plt.bar_label(bar,padding=5)

    plt.xticks(get_ticks(Y_axis),rotation=45)
    plt.xlim(min_y)
    plt.xlabel("Repositories",loc='left',labelpad = 10, fontsize=24)
    plt.ylabel(y_name,loc='bottom',labelpad = 10, fontsize=24)
    plt.title(title)
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()

    #figure(figsize=(16, 10), dpi=80)
    #plt.subplots_adjust(top=0.92, bottom=0.28)
    #plt.rcParams.update({'font.size': 14})
    #plt.xticks(rotation='vertical')
    #plt.xlabel("Repositories")
    #plt.ylabel(y_name)
    #plt.title(title)
    #for i in range(0, len(repositories)):
    #    x = np.array([repositories[i] + "_sum", repositories[i] + "_min", repositories[i] + "_max", repositories[i] + "_avg"])
    #    y = np.array([abc[i][3], abc[i][0], abc[i][1], abc[i][2]])
    #    plt.bar(x, y, 0.5, label=repositories[i] + " " + versions[i])
    #plt.legend()
    #plt.savefig("./graphs/static-analysis/" + file)
    return


def print_bar_plot(x,vec,img_path,title): 
    V_axis = []
    X_axis = np.arange(len(x))
    Y_axis=[]
    for v in x:
        V_axis.append([v+'_AVG_CYC',v+'_MAX_CYC',v+'_MIN_CYC',v+'_AVG_COG',v+'_MAX_COG',v+'_MIN_COG'])
    min_y=float("inf")
    max_y=0
    for rows in vec:
        Y_axis.append([rows[0],rows[2],rows[4],rows[1],rows[3],rows[5]])
    for y in Y_axis:
        for value in y:
            min_y=min(min_y,value)
            max_y=max(max_y,value)
    plt.rcParams.update({'font.size': 18})
    figure(figsize=(36,30), dpi=80)
    for i in range(0,len(x)):
        bar=plt.barh(V_axis[i], Y_axis[i], 0.6, label = x[i])
        plt.bar_label(bar,padding=5,fontweight='bold')

    plt.xticks(get_ticks(Y_axis),rotation=45)
    plt.xlim(min_y)
    plt.xlabel("projects",loc='left',labelpad = 10,fontweight='bold',fontsize=22)
    plt.ylabel("Complexity",loc='bottom',labelpad = 10,fontweight='bold',fontsize=22)
    plt.title(title)
    plt.legend()
    plt.savefig(img_path)
    plt.cla()
    return


def plot_size_measures(repositories, versions, val, title, y_name, file):
    #figure(figsize=(16, 10), dpi=80)
    #plt.subplots_adjust(top=0.92, bottom=0.28)
    #plt.rcParams.update({'font.size': 14})
    #plt.xticks(rotation='vertical')
    #plt.xlabel("Repositories")
    #plt.ylabel(y_name)
    #plt.title(title)
    #for i in range(0, len(repositories)):
    #    x = np.array([repositories[i] + "_abc", repositories[i] + "_hal", repositories[i] + "_ploc", repositories[i] + "_cyc"])
    #    y = np.array([val[i][0], val[i][1], val[i][2], val[i][3]])
    #    plt.bar(x, y, 0.5, label=repositories[i] + " " + versions[i])
    #plt.legend()
    #plt.savefig("./graphs/static-analysis/" + file)

    V_axis = []
    Y_axis=[]
    for i in range(0, len(repositories)):
        V_axis.append([repositories[i] + "_cyc", repositories[i] + "_ploc", repositories[i] + "_hal", repositories[i] + "_abc"])
        Y_axis.append([val[i][3], val[i][2], val[i][1], val[i][0]])
    min_y=float("inf")
    max_y=0
    for y in Y_axis:
        for value in y:
            min_y=min(min_y,value)
            max_y=max(max_y,value)
    plt.rcParams.update({'font.size': 24})
    figure(figsize=(42,22), dpi=80)
    for i in range(0,len(repositories)):
        bar=plt.barh(V_axis[i], Y_axis[i], 0.66, label = repositories[i])
        plt.bar_label(bar,padding=5)

    plt.xticks(get_ticks(Y_axis),rotation=45)
    plt.xlim(min_y)
    plt.xlabel("Repositories",loc='left',labelpad = 10, fontsize=24)
    plt.ylabel(y_name,loc='bottom',labelpad = 10, fontsize=24)
    plt.title(title)
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()


    return

def plot_complexity_measures(repositories, versions, val, title, y_name, file):
    V_axis = []
    Y_axis=[]
    for i in range(0, len(repositories)):
        V_axis.append([repositories[i] + "_cyc", repositories[i] + "_wmc"])
        Y_axis.append([val[i][1], val[i][0]])
    min_y=float("inf")
    max_y=0
    for y in Y_axis:
        for value in y:
            min_y=min(min_y,value)
            max_y=max(max_y,value)
    plt.rcParams.update({'font.size': 24})
    figure(figsize=(42,20), dpi=80)
    for i in range(0,len(repositories)):
        bar=plt.barh(V_axis[i], Y_axis[i], 0.66, label = repositories[i])
        plt.bar_label(bar,padding=5)

    plt.xticks(get_ticks(Y_axis),rotation=45)
    plt.xlim(min_y)
    plt.xlabel("Repositories",loc='left',labelpad = 10, fontsize=24)
    plt.ylabel(y_name,loc='bottom',labelpad = 10, fontsize=24)
    plt.title(title)
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def static_analysis():
    repos = ["FastCSV", "java-jwt", "jsoup", "Java-WebSocket"]
    versions = ["v2.2.0", "4.0.0", "jsoup-1.15.2", "v1.5.3"]
    abc = []
    npm = []
    npa = []
    wmc = []
    coa = []
    cda = []
    size = []
    complexity = []
    for i in range(len(repos)):
        read_measures(repos[i], versions[i], abc, npm, npa, wmc, coa, cda, size, complexity)
    plot_measures(repos, versions, abc, "ABC", "Magnitude", "abc-static-analysis.png")
    plot_measures(repos, versions, npm, "NPM", "Number of public methods", "npm-static-analysis.png")
    plot_measures(repos, versions, npa, "NPA", "Number of public attributes", "npa-static-analysis.png")
    plot_measures(repos, versions, coa, "COA", "Class Operation Accessibility", "coa-static-analysis.png")
    plot_measures(repos, versions, cda, "CDA", "Class Data Accessibility", "cda-static-analysis.png")
    plot_measures(repos, versions, wmc, "WMC", "Weighted methods per class", "wmc-static-analysis.png")
    plot_size_measures(repos, versions, size, "Size measures", "Values", "size-metrics-comparison.png")
    plot_complexity_measures(repos, versions, complexity, "Complexity measures", "Values", "complexity-metrics-comparison.png")
    return

def get_ticks(Y_axis):
    vec=[y for ys in Y_axis for y in ys]
    ymin= min(vec)
    ymax= max(vec)
    npv=np.linspace(ymin,ymax,30)
    return npv

static_analysis()