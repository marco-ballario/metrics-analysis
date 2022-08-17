from importlib.util import spec_from_file_location
import os
import json
import glob
from importlib_metadata import version
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re

THRESHOLD_ABC = 60
THRESHOLD_WMC = 34
THRESHOLD_NPM = 40
THRESHOLD_NPA = 0
THRESHOLD_COA = 1.0
THRESHOLD_CDA = 1.0

def get_classes(json_data, classes, classes_npm, classes_npa, classes_coa, classes_cda, classes_wmc):
    class_npm = 0
    class_npa = 0
    class_coa = 0
    class_cda = 0
    for space in json_data["spaces"]:
        if space["kind"] == "class" or space["kind"] == "interface":
            classes.append(space["name"])
            class_npm += float(space["metrics"]["npm"]["total"])
            class_npa += float(space["metrics"]["npa"]["total"])
            class_coa += float(space["metrics"]["npm"]["average"] or 0)
            class_cda += float(space["metrics"]["npa"]["average"] or 0)
            get_classes(space, classes, classes_npm, classes_npa, classes_coa, classes_cda, classes_wmc)
    if json_data["kind"] == "class" or json_data["kind"] == "interface":
        classes_npm.append(float(json_data["metrics"]["npm"]["total"]) - class_npm)
        classes_npa.append(float(json_data["metrics"]["npa"]["total"]) - class_npa)
        classes_coa.append(float(json_data["metrics"]["npm"]["average"] or 0) - class_coa)
        classes_cda.append(float(json_data["metrics"]["npa"]["average"] or 0) - class_cda)
        classes_wmc.append(float(json_data["metrics"]["wmc"]["wmc"]))
    return

def read_measures(repository_name, version, max_data, avg_data, files, abc, wmc, npm, npa, coa, cda, classesx):
    magn = []
    pub_met = []
    pub_att = []
    wmc_val = []
    hal_val = []
    loc_val = []
    cyc_val = []
    coa_val = []
    cda_val = []
    nm_val = []
    na_val = []
    classes = []
    file_names = []
    big_files_names = []
    big_wmc_files_names = []
    big_npm_files_names = []
    big_npa_files_names = []
    big_coa_files_names = []
    big_cda_files_names = []
    npmx = []
    npax = []
    coax = []
    cdax = []
    wmcx = []

    for filename in glob.iglob("data/" + repository_name + "/" + version + '/**/*.java.json', recursive=True):
        with open(filename, "r") as file:
            jsonData = json.load(file)
            print(jsonData["name"])
            magn.append(float(jsonData["metrics"]["abc"]["magnitude"]))
            pub_met.append(float(jsonData["metrics"]["npm"]["total"]))
            pub_att.append(float(jsonData["metrics"]["npa"]["total"]))
            nm_val.append(float(jsonData["metrics"]["npm"]["total_methods"]))
            na_val.append(float(jsonData["metrics"]["npa"]["total_attributes"]))
            coa_val.append(float(jsonData["metrics"]["npm"]["average"] or 0))
            cda_val.append(float(jsonData["metrics"]["npa"]["average"] or 0))
            wmc_val.append(float(jsonData["metrics"]["wmc"]["total"]))
            hal_val.append(float(jsonData["metrics"]["halstead"]["estimated_program_length"]))
            loc_val.append(float(jsonData["metrics"]["loc"]["ploc"]))
            cyc_val.append(float(jsonData["metrics"]["cyclomatic"]["sum"]))
            get_classes(jsonData, classes, npmx, npax, coax, cdax, wmcx)
            file_names.append(jsonData["name"])
            #print(len(classes))
            #print(sum(pub_met))
            #print(sum(npmx))
            #print(len(npmx))
            
            if float(jsonData["metrics"]["abc"]["magnitude"]) > THRESHOLD_ABC:
                big_files_names.append(jsonData["name"])
            #if float(jsonData["metrics"]["wmc"]["total"]) > 34:
                #big_wmc_files_names.append(jsonData["name"])
            
            #if float(jsonData["metrics"]["npa"]["total"]) > 10:
                #big_npa_files_names.append(jsonData["name"])
            #if float(jsonData["metrics"]["npm"]["average"] or 0) >= 1.0:
                #big_coa_files_names.append(jsonData["name"])
            #if float(jsonData["metrics"]["npa"]["average"] or 0) >= 1.0:
                #big_cda_files_names.append(jsonData["name"])
            
    #print(len(classes))
    #print(sum(pub_met))
    #print(sum(npmx))
    #print(len(npmx))
    
    magn = [float(x) for x in magn]
    pub_met = [float(x) for x in pub_met]
    pub_att = [float(x) for x in pub_att]
    wmc_val = [float(x) for x in wmc_val]
    
    #print(npax)
    for i, v in enumerate(classes):
        if npmx[i] > THRESHOLD_NPM:
            big_npm_files_names.append(npmx[i])
        if npax[i] > THRESHOLD_NPA:
            big_npa_files_names.append(npax[i])
        if coax[i] == THRESHOLD_COA:
            big_coa_files_names.append(coax[i])
        if cdax[i] == THRESHOLD_CDA:
            big_cda_files_names.append(cdax[i])
        if wmcx[i] > THRESHOLD_WMC:
            big_wmc_files_names.append(wmcx[i])

    files.append(len(file_names))
    classesx.append(len(classes))
    abc.append(len(big_files_names))
    wmc.append(len(big_wmc_files_names))
    npm.append(len(big_npm_files_names))
    npa.append(len(big_npa_files_names))
    coa.append(len(big_coa_files_names))
    cda.append(len(big_cda_files_names))
    max_data.append( [max(magn), max(loc_val), max(wmc_val), max(cyc_val), max(pub_met), max(pub_att), max(nm_val), max(na_val), max(coa_val), max(cda_val)] )
    avg_data.append( [sum(magn)/len(magn), sum(loc_val)/len(loc_val), sum(wmc_val)/len(wmc_val), sum(cyc_val)/len(cyc_val), sum(pub_met)/len(pub_met), sum(pub_att)/len(pub_att), sum(nm_val)/len(nm_val), sum(na_val)/len(na_val), sum(coa_val)/len(coa_val), sum(cda_val)/len(cda_val)] )
    return

def print_plot(versions,vec,img_path):
    abc=[]
    wmc=[]
    npm=[]
    npa=[]
    coa=[]
    cda=[]
    loc=[]
    cyc=[]
    nm=[]
    na=[]
    for rows in vec:
        abc.append(rows[0])
        loc.append(rows[1])
        wmc.append(rows[2])
        cyc.append(rows[3])
        npm.append(rows[4])
        npa.append(rows[5])
        nm.append(rows[6])
        na.append(rows[7])
        coa.append(rows[8])
        cda.append(rows[9])
    for i, v in enumerate(versions):
        versions[i] = re.sub("[a-zA-Z-]", "", versions[i])
    plt.rcParams.update({'font.size': 16})

    figure, axis = plt.subplots(2, 2)
    figure.set_size_inches(30, 20)

    axis[0, 0].plot(versions, abc)
    axis[0, 0].scatter(versions, abc, color="r")
    axis[0, 0].set_title("ABC")
    axis[0, 0].set_xlabel('versions')

    axis[0, 1].plot(versions, loc)
    axis[0, 1].scatter(versions, loc, color="r")
    axis[0, 1].set_title("PLOC")
    axis[0, 1].set_xlabel('versions')

    axis[1, 0].plot(versions, wmc)
    axis[1, 0].scatter(versions, wmc, color="r")
    axis[1, 0].set_title("WMC")
    axis[1, 0].set_xlabel('versions')

    axis[1, 1].plot(versions, cyc)
    axis[1, 1].scatter(versions, cyc, color="r")
    axis[1, 1].set_title("CC")
    axis[1, 1].set_xlabel('versions')

    plt.subplots_adjust(wspace=0.2, hspace=0.3)
    plt.savefig(img_path + "-1.png")
    plt.cla()
    plt.close(figure)

    plt.rcParams.update({'font.size': 12})

    figure, axis = plt.subplots(3, 2)
    figure.set_size_inches(24, 26)

    axis[0, 0].plot(versions, npm)
    axis[0, 0].scatter(versions, npm, color="r")
    axis[0, 0].set_title("NPM")
    axis[0, 0].set_xlabel('versions')

    axis[0, 1].plot(versions, npa)
    axis[0, 1].scatter(versions, npa, color="r")
    axis[0, 1].set_title("NPA")
    axis[0, 1].set_xlabel('versions')

    axis[1, 0].plot(versions, nm)
    axis[1, 0].scatter(versions, nm, color="r")
    axis[1, 0].set_title("NM")
    axis[1, 0].set_xlabel('versions')

    axis[1, 1].plot(versions, na)
    axis[1, 1].scatter(versions, na, color="r")
    axis[1, 1].set_title("NA")
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
    plt.savefig(img_path + "-2.png")
    plt.cla()
    plt.close(figure)
    return

def plot_threshold_measures(versions, files, values, title, file, label1, label2, label3, threshold):
    y = []
    x1 = []
    x2 = []
    for i, v in enumerate(versions):
        versions[i] = re.sub("[a-zA-Z-]", "", versions[i])
    for i in range(0, len(versions)):
        x1.append(files[i])
        x2.append(values[i])
        y.append(str(versions[i]))

    font_size = 28
    plt.rcParams.update({"font.size": font_size})
    fig = figure(figsize=(50, 26), dpi=80)

    for i in range(0, len(versions)):
        bar1 = plt.bar(y[i], x1[i], 0.5, color="#1f77b4", label = label1 + " With " + label3 + str(threshold))
        bar2 = plt.bar(y[i], x2[i], 0.5, color="#d62728", label = label1 + " With " + label2 + str(threshold))
        plt.text(i, (x1[i] - x2[i]) // 2 + x2[i], str(x1[i] - x2[i]), color="snow", va="center", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold")
        plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold")

    #plt.margins(y=0.2)
    #plt.xticks(rotation=45)
    yt=plt.yticks()[0].tolist()
    plt.yticks(yt)
    plt.xlabel("Versions", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Number Of " + label1, loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title.replace("?", str(threshold)))
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper left", prop={"size": font_size})
    plt.savefig("./graphs/time-analysis/thresholds/" + file)
    plt.cla()
    plt.close(fig)
    return

def plot_threshold_percentages(versions, files, values, title, file, label1, label2, label3, threshold):
    y = []
    x1 = []
    x2 = []
    for i, v in enumerate(versions):
        versions[i] = re.sub("[a-zA-Z-]", "", versions[i])
    for i in range(0, len(versions)):
        x1.append(100)
        x2.append(values[i] / files[i] * 100)
        y.append(str(versions[i]))

    font_size = 28
    plt.rcParams.update({"font.size": font_size})
    fig = figure(figsize=(50, 26), dpi=80)

    for i in range(0, len(versions)):
        bar1 = plt.bar(y[i], x1[i], 0.5, color="#1f77b4", label = "Percentage Of " + label1 + " With " + label3 + str(threshold))
        bar2 = plt.bar(y[i], x2[i], 0.5, color="#d62728", label = "Percentage Of " + label1 + " With " + label2 + str(threshold))
        plt.text(i, (100 - x2[i]) // 2 + x2[i], "{:.2f}".format(100 - x2[i]) + "%", color="snow", va="center", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold", fmt="%.0f%%")
        plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold", fmt="%.2f%%")

    #plt.margins(y=0.2)
    #plt.xticks(rotation=45)
    yt=plt.yticks()[0].tolist()
    plt.yticks(yt)
    plt.xlabel("Versions", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Percentage Of " + label1, loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title.replace("?", str(threshold)))
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper right", prop={"size": font_size})
    plt.savefig("./graphs/time-analysis/thresholds/" + file)
    plt.cla()
    plt.close(fig)
    return

def time_analysis():
    repos = ["java-jwt", "gson", "spring-kafka"]
    versions = [
        ["3.16.0", "3.17.0", "3.18.0", "3.18.1", "3.18.2", "3.18.3", "3.19.0", "3.19.1", "3.19.2", "4.0.0"],
        ["gson-parent-2.8.2", "gson-parent-2.8.3", "gson-parent-2.8.4", "gson-parent-2.8.5", "gson-parent-2.8.6", "gson-parent-2.8.7", "gson-parent-2.8.8", "gson-parent-2.8.9", "gson-parent-2.9.0", "gson-parent-2.9.1"],
        ["v2.8.0", "v2.8.1", "v2.8.2", "v2.8.3", "v2.8.4", "v2.8.5", "v2.8.6", "v2.8.7", "v2.8.8", "v2.9.0"]
    ]

    for index, repo in enumerate(repos):
        avg = []
        max = []
        abc = []
        wmc = []
        npm = []
        npa = []
        coa = []
        cda = []
        files = []
        classes = []
        print("Generating " + repo + " graphs...")
        for version in versions[index]:
            read_measures(repo, version, max, avg, files, abc, wmc, npm, npa, coa, cda, classes)
            print(repo + " " + version + " data collected!")
        plot_threshold_percentages(versions[index], files, abc, "ABC magnitude files (Threshold = ?) - " + repo, "threshold-percentages-abc-" + repo + ".png", "Files", "Magnitude >= ", "Magnitude < ", THRESHOLD_ABC)
        plot_threshold_measures(versions[index], files, abc, "ABC magnitude files (Threshold = ?) - " + repo, "threshold-measures-abc-" + repo + ".png", "Files", "Magnitude >= ", "Magnitude < ", THRESHOLD_ABC)
        plot_threshold_percentages(versions[index], classes, wmc, "WMC classes (Threshold = ?) - " + repo, "threshold-percentages-wmc-" + repo + ".png", "Classes", "WMC >= ", "WMC < ", THRESHOLD_WMC)
        plot_threshold_measures(versions[index], classes, wmc, "WMC classes (Threshold = ?) - " + repo, "threshold-measures-wmc-" + repo + ".png", "Classes", "WMC >= ", "WMC < ", THRESHOLD_WMC)
        plot_threshold_percentages(versions[index], classes, npm, "NPM classes (Threshold = ?) - " + repo, "threshold-percentages-npm-" + repo + ".png", "Classes", "NPM >= ", "NPM < ", THRESHOLD_NPM)
        plot_threshold_measures(versions[index], classes, npm, "NPM classes (Threshold = ?) - " + repo, "threshold-measures-npm-" + repo + ".png", "Classes", "NPM >= ", "NPM < ", THRESHOLD_NPM)
        plot_threshold_percentages(versions[index], classes, npa, "NPA classes (Threshold = ?) - " + repo, "threshold-percentages-npa-" + repo + ".png", "Classes", "NPA >= ", "NPA < ", THRESHOLD_NPA)
        plot_threshold_measures(versions[index], classes, npa, "NPA classes (Threshold = ?) - " + repo, "threshold-measures-npa-" + repo + ".png", "Classes", "NPA >= ", "NPA < ", THRESHOLD_NPA)
        plot_threshold_percentages(versions[index], classes, coa, "COA classes (Threshold = ?) - " + repo, "threshold-percentages-coa-" + repo + ".png", "Classes", "COA >= ", "COA < ", THRESHOLD_COA)
        plot_threshold_measures(versions[index], classes, coa, "COA classes (Threshold = ?) - " + repo, "threshold-measures-coa-" + repo + ".png", "Classes", "COA >= ", "COA < ", THRESHOLD_COA)
        plot_threshold_percentages(versions[index], classes, cda, "CDA classes (Threshold = ?) - " + repo, "threshold-percentages-cda-" + repo + ".png", "Classes", "CDA == ", "CDA < ", THRESHOLD_CDA)
        plot_threshold_measures(versions[index], classes, cda, "CDA classes (Threshold = ?) - " + repo, "threshold-measures-cda-" + repo + ".png", "Classes", "CDA == ", "CDA < ", THRESHOLD_CDA)
        print_plot(versions[index], avg,"./graphs/time-analysis/cumulative/average-measures-" + repo)
        print_plot(versions[index], max,"./graphs/time-analysis/cumulative/maximum-measures-" + repo)
        print(repo + " graphs generated!")

time_analysis()