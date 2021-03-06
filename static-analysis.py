import os
import json
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def read_measures(repository_name, version, abc, npm, npa, wmc, coa, cda, size):
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

            print(os.path.basename(jsonData["name"]))
            print(jsonData["metrics"]["abc"]["magnitude"])
    magn = [float(x) for x in magn]
    pub_met = [float(x) for x in pub_met]
    pub_att = [float(x) for x in pub_att]
    wmc_val = [float(x) for x in wmc_val]
    print(magn)
    abc.append( [min(magn), max(magn), sum(magn)/len(magn), sum(magn)] )
    npm.append( [min(pub_met), max(pub_met), sum(pub_met)/len(pub_met), sum(pub_met)] )
    npa.append( [min(pub_att), max(pub_att), sum(pub_att)/len(pub_att), sum(pub_att)] )
    cda.append( [min(cda_val), max(cda_val), sum(cda_val)/len(cda_val), sum(cda_val)] )
    coa.append( [min(coa_val), max(coa_val), sum(coa_val)/len(coa_val), sum(coa_val)] )
    wmc.append( [min(wmc_val), max(wmc_val), sum(wmc_val)/len(wmc_val), sum(wmc_val)] )
    size.append( [sum(magn), sum(hal_val), sum(loc_val), sum(cyc_val)] )
    print(abc)
    return


def plot_measures(repositories, versions, abc, title, y_name, file):
    figure(figsize=(16, 10), dpi=80)
    plt.subplots_adjust(top=0.92, bottom=0.28)
    plt.rcParams.update({'font.size': 14})
    plt.xticks(rotation='vertical')
    plt.xlabel("Repositories")
    plt.ylabel(y_name)
    plt.title(title)
    for i in range(0, len(repositories)):
        x = np.array([repositories[i] + "_sum", repositories[i] + "_min", repositories[i] + "_max", repositories[i] + "_avg"])
        y = np.array([abc[i][3], abc[i][0], abc[i][1], abc[i][2]])
        plt.bar(x, y, 0.5, label=repositories[i] + " " + versions[i])
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    return

def plot_size_measures(repositories, versions, val, title, y_name, file):
    figure(figsize=(16, 10), dpi=80)
    plt.subplots_adjust(top=0.92, bottom=0.28)
    plt.rcParams.update({'font.size': 14})
    plt.xticks(rotation='vertical')
    plt.xlabel("Repositories")
    plt.ylabel(y_name)
    plt.title(title)
    for i in range(0, len(repositories)):
        x = np.array([repositories[i] + "_abc", repositories[i] + "_hal", repositories[i] + "_ploc", repositories[i] + "_cyc"])
        y = np.array([val[i][0], val[i][1], val[i][2], val[i][3]])
        plt.bar(x, y, 0.5, label=repositories[i] + " " + versions[i])
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
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
    for i in range(len(repos)):
        read_measures(repos[i], versions[i], abc, npm, npa, wmc, coa, cda, size)
    plot_measures(repos, versions, abc, "ABC", "Magnitude", "abc-static-analysis.png")
    plot_measures(repos, versions, npm, "NPM", "Number of public methods", "npm-static-analysis.png")
    plot_measures(repos, versions, npa, "NPA", "Number of public attributes", "npa-static-analysis.png")
    plot_measures(repos, versions, coa, "COA", "Class Operation Accessibility", "coa-static-analysis.png")
    plot_measures(repos, versions, cda, "CDA", "Class Data Accessibility", "cda-static-analysis.png")
    plot_measures(repos, versions, wmc, "WMC", "Weighted methods per class", "wmc-static-analysis.png")
    plot_size_measures(repos, versions, size, "Size measures", "Values", "size-metrics-comparison.png")
    return

static_analysis()
