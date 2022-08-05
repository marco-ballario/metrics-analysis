import os
import json
import glob
from importlib_metadata import version
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def read_measures(repository_name, version, max_data, avg_data):
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

    magn = [float(x) for x in magn]
    pub_met = [float(x) for x in pub_met]
    pub_att = [float(x) for x in pub_att]
    wmc_val = [float(x) for x in wmc_val]
    
    max_data.append( [max(magn), max(wmc_val), max(pub_met), max(pub_att), max(coa_val), max(cda_val)] )
    avg_data.append( [sum(magn)/len(magn), sum(wmc_val)/len(wmc_val), sum(pub_met)/len(pub_met), sum(pub_att)/len(pub_att), sum(coa_val)/len(coa_val), sum(cda_val)/len(cda_val)] )
    return

def print_plot(versions,vec,img_path):
    abc=[]
    wmc=[]
    npm=[]
    npa=[]
    coa=[]
    cda=[]
    for rows in vec:
        abc.append(rows[0])
        wmc.append(rows[1])
        npm.append(rows[2])
        npa.append(rows[3])
        coa.append(rows[4])
        cda.append(rows[5])
    plt.rcParams.update({'font.size': 12})
    figure, axis = plt.subplots(3, 2)
    figure.set_size_inches(24, 26)
    axis[0, 0].plot(versions, abc)
    axis[0, 0].scatter(versions, abc, color="r")
    axis[0, 0].set_title("ABC")
    axis[0, 0].set_xlabel('versions')
    axis[0, 1].plot(versions, wmc)
    axis[0, 1].scatter(versions, wmc, color="r")
    axis[0, 1].set_title("WMC")
    axis[0, 1].set_xlabel('versions')
    axis[1, 0].plot(versions, npm)
    axis[1, 0].scatter(versions, npm, color="r")
    axis[1, 0].set_title("NPM")
    axis[1, 0].set_xlabel('versions')
    axis[1, 1].plot(versions, npa)
    axis[1, 1].scatter(versions, npa, color="r")
    axis[1, 1].set_title("NPA")
    axis[1, 1].set_xlabel('versions')
    axis[2, 0].plot(versions, coa)
    axis[2, 0].scatter(versions, coa, color="r")
    axis[2, 0].set_title("COA")
    axis[2, 0].set_xlabel('versions')
    axis[2, 1].plot(versions, cda)
    axis[2, 1].scatter(versions, cda, color="r")
    axis[2, 1].set_title("CDA")
    axis[2, 1].set_xlabel('versions')
    plt.subplots_adjust(wspace=0.2, hspace=0.3)
    plt.savefig(img_path)
    plt.cla()
    return

def time_analysis():
    repos = ["FastCSV", "java-jwt", "jsoup", "Java-WebSocket"]
    versions = [
        ["v1.0.4", "v2.0.0", "v2.1.0", "v2.2.0"],
        ["3.17.0", "3.18.0", "3.18.1", "3.18.2", "3.18.3", "3.19.0", "3.19.1", "3.19.2", "4.0.0-beta.0", "4.0.0"],
        ["jsoup-1.12.2", "jsoup-1.13.1", "jsoup-1.14.1", "jsoup-1.14.2", "jsoup-1.14.3", "jsoup-1.15.1", "jsoup-1.15.2"],
        ["v1.3.1", "v1.3.3", "v1.3.8", "v1.3.9", "v1.4.0", "v1.4.1", "v1.5.0", "v1.5.1", "v1.5.2", "v1.5.3"]
    ]

    for index, repo in enumerate(repos):
        avg= []
        max= []
        print("Generating " + repo + " graphs...")
        for version in versions[index]:
            read_measures(repo, version, max, avg)
            print(repo + " " + version + " data collected!")
        print_plot(versions[index], avg,"./graphs/time-analysis/" + repo + "-avg.png")
        print_plot(versions[index], max,"./graphs/time-analysis/" + repo + "-max.png")
        print(repo + " graphs generated!")

time_analysis()