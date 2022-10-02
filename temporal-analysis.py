from importlib.util import spec_from_file_location
from importlib_metadata import version
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import glob
import json
import csv
import re
import os

TOP_FILES_NUMBER = 3
TOP_CLASSES_NUMBER = 3

THRESHOLD_ABC = 60
THRESHOLD_WMC = 34
THRESHOLD_NPM = 40
THRESHOLD_NPA = 10
THRESHOLD_COA = 1.0
THRESHOLD_CDA = 1.0

# get the class data
def get_classes(json_data, class_names, class_npm, class_npa, class_coa, class_cda, class_wmc, file_name):
    
    # for each inner space of the provided space
    for space in json_data["spaces"]:
        if space["kind"] == "class" or space["kind"] == "interface":

            # initialize array and save class name
            res = [0, 0, 0, 0, 0, 0, 0]
            class_names.append(str(os.path.join(file_name, space["name"])))
            
            # debug
            print("look inside " + space["name"] + " " + str(space["metrics"]["wmc"]["total"]))

            # compute sums of measures of internal classes
            for s in space["spaces"]:
                count_inner_spaces_measures(s, res)

            # debug
            print("   collected " + str(res[0]))
            print("   measure = " + str(space["metrics"]["wmc"]["total"]) + " - " + str(res[0]))
            
            # compute actual class measure
            # class measure = (class measure + sum of measures of internal classes) - sum of measures of internal classes 
            wmc_val = float(space["metrics"]["wmc"]["total"]) - res[0]
            npm_val = float(space["metrics"]["npm"]["total"]) - res[1]
            npa_val = float(space["metrics"]["npa"]["total"]) - res[2]
            nm_val = float(space["metrics"]["npm"]["total_methods"]) - res[3]
            na_val = float(space["metrics"]["npa"]["total_attributes"]) - res[4]
            coa_val = float(0 if nm_val == 0 else npm_val/nm_val)
            cda_val = float(0 if na_val == 0 else npa_val/na_val)

            # store class measures
            class_wmc.append(wmc_val)
            class_npm.append(npm_val)
            class_npa.append(npa_val)
            class_coa.append(coa_val)
            class_cda.append(cda_val)
            
        # inspect inner spaces of the current space
        get_classes(space, class_names, class_npm, class_npa, class_coa, class_cda, class_wmc, file_name)

    return

# compute sums of measures of internal classes
def count_inner_spaces_measures(root, res):

    # inspect spaces of type class or interface
    if root["kind"] == "class" or root["kind"] == "interface":

        # debug
        print("   |_ " + root["name"] + " " + str(root["metrics"]["wmc"]["total"]))

        # accumulate sums
        res[0] += float(root["metrics"]["wmc"]["total"])
        res[1] += float(root["metrics"]["npm"]["total"])
        res[2] += float(root["metrics"]["npa"]["total"])
        res[3] += float(root["metrics"]["npm"]["total_methods"])
        res[4] += float(root["metrics"]["npa"]["total_attributes"])
        return

    # inspect inner spaces of the current space
    for space in root["spaces"]:
        count_inner_spaces_measures(space, res)
    return

# test class metrics computation
def test_classes(repository_name, version, class_npa_dict, class_npm_dict, class_wmc_dict):

    NPA_JAVA_JWT_CLASS = str(os.path.join("../java-jwt/lib/src/test/java/com/auth0/jwt/JWTVerifierTest.java", "JWTVerifierTest"))
    NPM_JAVA_JWT_CLASS = str(os.path.join("../java-jwt/lib/src/main/java/com/auth0/jwt/TokenUtils.java", "TokenUtils"))
    WMC_JAVA_JWT_CLASS = str(os.path.join("../java-jwt/lib/src/main/java/com/auth0/jwt/JWTVerifier.java", "JWTVerifier"))
    NPA_GSON_CLASS = str(os.path.join("../gson/gson/src/test/java/com/google/gson/GsonTest.java", "GsonTest"))
    NPM_GSON_CLASS = str(os.path.join("../gson/gson/src/test/java/com/google/gson/CommentsTest.java", "CommentsTest"))
    WMC_GSON_CLASS = str(os.path.join("../gson/gson/src/main/java/com/google/gson/JsonNull.java", "JsonNull"))
    NPA_SPRING_KAFKA_CLASS = str(os.path.join("../spring-kafka/spring-kafka-test/src/main/java/org/springframework/kafka/test/core/BrokerAddress.java", "BrokerAddress"))
    NPM_SPRING_KAFKA_CLASS = str(os.path.join("../spring-kafka/spring-kafka-test/src/test/java/org/springframework/kafka/test/utils/KafkaTestUtilsTests.java", "KafkaTestUtilsTests"))
    WMC_SPRING_KAFKA_CLASS = str(os.path.join("../spring-kafka/spring-kafka/src/test/java/org/springframework/kafka/core/KafkaAdminTests.java", "KafkaAdminTests"))
    NPA_MOCKITO_CLASS = str(os.path.join("../mockito/src/test/java/org/mockitoutil/ClassLoadersTest.java", "ClassLoadersTest"))
    NPM_MOCKITO_CLASS = str(os.path.join("../mockito/src/main/java/org/mockito/Mockito.java", "Mockito"))
    WMC_MOCKITO_CLASS = str(os.path.join("../mockito/src/test/java/org/mockitoutil/TestBase.java", "TestBase"))

    if repository_name == "java-jwt":
        if version == "3.16.0":
            assert class_npa_dict[NPA_JAVA_JWT_CLASS] == 1
        if version == "3.17.0":
            assert class_npm_dict[NPM_JAVA_JWT_CLASS] == 0
        if version == "3.18.0":
            assert class_wmc_dict[WMC_JAVA_JWT_CLASS] == 57
    if repository_name == "gson":
        if version == "gson-parent-2.8.2":
            assert class_npa_dict[NPA_GSON_CLASS] == 0
        if version == "gson-parent-2.8.3":
            assert class_npm_dict[NPM_GSON_CLASS] == 1
        if version == "gson-parent-2.8.4":
            assert class_wmc_dict[WMC_GSON_CLASS] == 5
    if repository_name == "spring-kafka":
        if version == "v2.8.0":
            assert class_npa_dict[NPA_SPRING_KAFKA_CLASS] == 1
        if version == "v2.8.1":
            assert class_npm_dict[NPM_SPRING_KAFKA_CLASS] == 2
        if version == "v2.8.2":
            assert class_wmc_dict[WMC_SPRING_KAFKA_CLASS] == 13
    if repository_name == "mockito":
        if version == "v4.1.0":
            assert class_npa_dict[NPA_MOCKITO_CLASS] == 2
        if version == "v4.2.0":
            assert class_npm_dict[NPM_MOCKITO_CLASS] == 52
        if version == "v4.3.0":
            assert class_wmc_dict[WMC_MOCKITO_CLASS] == 15

def read_measures(repository_name, version, top_data, max_data, avg_data, files, abc, wmc, npm, npa, coa, cda, classes):

    abc_mag = []
    loc_ploc = []
    wmc_tot = []
    cyc_sum = []
    npm_tot = []
    npa_tot = []
    npn_tot_met = []
    npa_tot_att = []
    npm_avg = []
    npa_avg = []

    file_names = []
    class_names = []
    class_npm = []
    class_npa = []
    class_coa = []
    class_cda = []
    class_wmc = []

    file_abc_dict = dict()
    class_wmc_dict = dict()
    class_npm_dict = dict()
    class_npa_dict = dict()

    high_abc_files = []
    high_wmc_values = []
    high_npm_values = []
    high_npa_values = []
    high_coa_values = []
    high_cda_values = []

    # debug
    # npm is not debugged since some source files have enum classes not recognised by RCA
    old_class_wmc = 0
    old_class_npa = 0

    # for each measures file
    for filename in glob.iglob("data/" + repository_name + "/" + version + '/**/*.java.json', recursive=True):
        with open(filename, "r") as file:
            
            json_data = json.load(file)
            file_names.append(json_data["name"])
            abc_mag.append(float(json_data["metrics"]["abc"]["magnitude"]))
            wmc_tot.append(float(json_data["metrics"]["wmc"]["total"]))
            npm_tot.append(float(json_data["metrics"]["npm"]["total"]))
            npa_tot.append(float(json_data["metrics"]["npa"]["total"]))
            npm_avg.append(float(json_data["metrics"]["npm"]["average"] or 0))
            npa_avg.append(float(json_data["metrics"]["npa"]["average"] or 0))
            npn_tot_met.append(float(json_data["metrics"]["npm"]["total_methods"]))
            npa_tot_att.append(float(json_data["metrics"]["npa"]["total_attributes"]))
            loc_ploc.append(float(json_data["metrics"]["loc"]["ploc"]))
            cyc_sum.append(float(json_data["metrics"]["cyclomatic"]["sum"]))

            # get class data
            get_classes(json_data, class_names, class_npm, class_npa, class_coa, class_cda, class_wmc, json_data["name"])

            # debug
            assert len(class_names) == len(class_npm) == len(class_npa) == len(class_coa) == len(class_cda) == len(class_wmc)
            assert sum(class_wmc) - old_class_wmc == float(json_data["metrics"]["wmc"]["total"])
            assert sum(class_npa) - old_class_npa == float(json_data["metrics"]["npa"]["total"])
            old_class_wmc = sum(class_wmc)
            old_class_npa = sum(class_npa)
            
            # threshold abc
            file_abc_dict[json_data["name"]] = float(json_data["metrics"]["abc"]["magnitude"])
            if float(json_data["metrics"]["abc"]["magnitude"]) > THRESHOLD_ABC:
                high_abc_files.append(json_data["name"])
    
    # debug
    assert len(file_names) == len(file_abc_dict)
    assert len(class_names) >= len(file_abc_dict)
    assert len(abc_mag) == len(wmc_tot) == len(loc_ploc) == len(cyc_sum)
    assert len(npm_tot) == len(npa_tot) == len(npm_avg) == len(npa_avg) == len(npn_tot_met) == len(npa_tot_att)
    assert sum(npn_tot_met) >= sum(npm_tot)
    assert sum(npa_tot_att) >= sum(npa_tot)

    # top abc files
    file_abc_sorted = sorted(file_abc_dict.items(), key=lambda x: (-x[1], str(os.path.basename(x[0]))), reverse=False)[:TOP_FILES_NUMBER]
    for t in file_abc_sorted:
        top_data[0].append([repository_name, version, t[0], os.path.basename(t[0]), round(t[1], 2)])
    
    # thresholds wmc, npm and npa
    for i, v in enumerate(class_names):
        class_wmc_dict[v] = class_wmc[i]
        class_npm_dict[v] = class_npm[i]
        class_npa_dict[v] = class_npa[i]

        if class_npm[i] > THRESHOLD_NPM:
            high_npm_values.append(class_npm[i])
        if class_npa[i] > THRESHOLD_NPA:
            high_npa_values.append(class_npa[i])
        if class_coa[i] == THRESHOLD_COA:
            high_coa_values.append(class_coa[i])
        if class_cda[i] == THRESHOLD_CDA:
            high_cda_values.append(class_cda[i])
        if class_wmc[i] > THRESHOLD_WMC:
            high_wmc_values.append(class_wmc[i])

    # test class metrics computation
    test_classes(repository_name, version, class_npa_dict, class_npm_dict, class_wmc_dict)

    # top wmc, npm and npa classes
    class_wmc_sorted = sorted(class_wmc_dict.items(), key=lambda x: (-x[1], str(os.path.basename(x[0]))), reverse=False)[:TOP_CLASSES_NUMBER]
    class_npm_sorted = sorted(class_npm_dict.items(), key=lambda x: (-x[1], str(os.path.basename(x[0]))), reverse=False)[:TOP_CLASSES_NUMBER]
    class_npa_sorted = sorted(class_npa_dict.items(), key=lambda x: (-x[1], str(os.path.basename(x[0]))), reverse=False)[:TOP_CLASSES_NUMBER]
    assert len(file_abc_sorted) == len(class_wmc_sorted) == len(class_npm_sorted) == len(class_npa_sorted) == TOP_CLASSES_NUMBER
    for i in range(TOP_CLASSES_NUMBER):
        top_data[1].append([repository_name, version, os.path.dirname(class_wmc_sorted[i][0]), os.path.basename(class_wmc_sorted[i][0]), int(class_wmc_sorted[i][1])])
        top_data[2].append([repository_name, version, os.path.dirname(class_npm_sorted[i][0]), os.path.basename(class_npm_sorted[i][0]), int(class_npm_sorted[i][1])])
        top_data[3].append([repository_name, version, os.path.dirname(class_npa_sorted[i][0]), os.path.basename(class_npa_sorted[i][0]), int(class_npa_sorted[i][1])])

    files.append(len(file_names))
    classes.append(len(class_names))
    abc.append(len(high_abc_files))
    wmc.append(len(high_wmc_values))
    npm.append(len(high_npm_values))
    npa.append(len(high_npa_values))
    coa.append(len(high_coa_values))
    cda.append(len(high_cda_values))

    max_data.append( [max(abc_mag), max(loc_ploc), max(wmc_tot), max(cyc_sum), max(npm_tot), max(npa_tot), max(npn_tot_met), max(npa_tot_att), max(npm_avg), max(npa_avg)] )
    avg_data.append( [sum(abc_mag)/len(abc_mag), sum(loc_ploc)/len(loc_ploc), sum(wmc_tot)/len(wmc_tot), sum(cyc_sum)/len(cyc_sum), sum(npm_tot)/len(npm_tot), sum(npa_tot)/len(npa_tot), sum(npn_tot_met)/len(npn_tot_met), sum(npa_tot_att)/len(npa_tot_att), sum(npm_avg)/len(npm_avg), sum(npa_avg)/len(npa_avg)] )
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
    plt.rcParams.update({'font.size': 24}) #16

    figure, axis = plt.subplots(2, 2)
    figure.set_size_inches(32, 20) #30 - 20

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
    plt.tight_layout()
    plt.savefig(img_path + "-1.svg")
    plt.cla()
    plt.close(figure)

    plt.rcParams.update({'font.size': 20}) # 12

    figure, axis = plt.subplots(3, 2)
    figure.set_size_inches(26, 26) # 24 -26

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
    plt.tight_layout()
    plt.savefig(img_path + "-2.svg")
    plt.cla()
    plt.close(figure)
    return

def plot_threshold_measures(versions, files, values, title, file, label1, label2, label3, threshold, opt=False):
    y = []
    x1 = []
    x2 = []
    for i, v in enumerate(versions):
        versions[i] = re.sub("[a-zA-Z-]", "", versions[i])
    for i in range(0, len(versions)):
        x1.append(files[i])
        x2.append(values[i])
        y.append(str(versions[i]))

    font_size = 28 #28
    plt.rcParams.update({"font.size": font_size})
    fig = figure(figsize=(40, 16), dpi=80) # 50 - 26

    for i in range(0, len(versions)):
        bar1 = plt.bar(y[i], x1[i], 0.5, color="#1f77b4", label = label1 + " With " + label3 + str(threshold))
        bar2 = plt.bar(y[i], x2[i], 0.5, color="#d62728", label = label1 + " With " + label2 + str(threshold))
        plt.text(i, (x1[i] - x2[i]) // 2 + x2[i], str(x1[i] - x2[i]), color="snow", va="center", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold")
        #plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold")
        if x2[i] != 0:
            #values[i] / files[i] * 100
            if x2[i] / x1[i] * 100 >= 5:
                plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold")
            if x2[i] / x1[i] * 100 < 5:
                plt.bar_label(bar2, label_type="edge", color="snow", padding=5, fontweight="bold")


    #plt.margins(y=0.2)
    #plt.xticks(rotation=45)
    yt=plt.yticks()[0].tolist()
    if opt:   
        ###print(yt[-1] - yt[-2])
        yt.append(float(yt[-1] + (yt[-1] - yt[-2])))
        
    ###print(plt.yticks()[0].tolist()) 
    plt.yticks(yt)
    plt.xlabel("Versions", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Number Of " + label1, loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title.replace("?", str(threshold)))
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper left", prop={"size": font_size})
    plt.tight_layout()
    plt.savefig("./temporal-analysis/thresholds/" + file)
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
        x2.append(round(values[i] / files[i] * 100, 2))
        y.append(str(versions[i]))

    font_size = 28 #28
    plt.rcParams.update({"font.size": font_size})
    fig = figure(figsize=(40, 16), dpi=80) # 50 - 26 => 40 - 16 => 44 - 24

    for i in range(0, len(versions)):
        bar1 = plt.bar(y[i], x1[i], 0.5, color="#1f77b4", label = "Percentage Of " + label1 + " With " + label3 + str(threshold))
        bar2 = plt.bar(y[i], x2[i], 0.5, color="#d62728", label = "Percentage Of " + label1 + " With " + label2 + str(threshold))
        if x2[i] == 0:
            plt.text(i, (100 - x2[i]) // 2 + x2[i], str(int(100.0)) + "%", color="snow", va="center", ha="center", fontweight="bold")
        else:
            plt.text(i, (100 - x2[i]) // 2 + x2[i], "{:.2f}".format(100 - x2[i]) + "%", color="snow", va="center", ha="center", fontweight="bold")
        #plt.bar_label(bar1, padding=5, fontweight="bold", fmt="%.0f%%")
        if x2[i] != 0:
            if x2[i] >= 5:
                plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold", fmt="%.2f%%")
            if x2[i] < 5:
                plt.bar_label(bar2, label_type="edge", color="snow", padding=5, fontweight="bold", fmt="%.2f%%")

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
    plt.tight_layout()
    plt.savefig("./temporal-analysis/thresholds/" + file)
    plt.cla()
    plt.close(fig)
    return

def temporal_analysis():
    repos = ["java-jwt", "gson", "spring-kafka", "mockito"]
    versions = [
        ["3.16.0", "3.17.0", "3.18.0", "3.18.1", "3.18.2", "3.18.3", "3.19.0", "3.19.1", "3.19.2", "4.0.0"],
        ["gson-parent-2.8.2", "gson-parent-2.8.3", "gson-parent-2.8.4", "gson-parent-2.8.5", "gson-parent-2.8.6", "gson-parent-2.8.7", "gson-parent-2.8.8", "gson-parent-2.8.9", "gson-parent-2.9.0", "gson-parent-2.9.1"],
        ["v2.8.0", "v2.8.1", "v2.8.2", "v2.8.3", "v2.8.4", "v2.8.5", "v2.8.6", "v2.8.7", "v2.8.8", "v2.9.0"],
        ["v4.1.0", "v4.2.0", "v4.3.0", "v4.3.1", "v4.4.0", "v4.5.0", "v4.5.1", "v4.6.0", "v4.6.1", "v4.7.0"]
    ]
    header = ["repository", "version", "path", "name", "measure"]
    top_metrics = ["abc", "wmc", "npm", "npa"]
    top_data = [[],[],[],[]]

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
            read_measures(repo, version, top_data, max, avg, files, abc, wmc, npm, npa, coa, cda, classes)
            print(repo + " " + version + " data collected!")
        opt = index == 3
        plot_threshold_percentages(versions[index], files, abc, "ABC magnitude files (Threshold = ?) - " + repo, "threshold-percentages-abc-" + repo + ".svg", "Files", "Magnitude >= ", "Magnitude < ", THRESHOLD_ABC)
        plot_threshold_measures(versions[index], files, abc, "ABC magnitude files (Threshold = ?) - " + repo, "threshold-measures-abc-" + repo + ".svg", "Files", "Magnitude >= ", "Magnitude < ", THRESHOLD_ABC, opt)
        plot_threshold_percentages(versions[index], classes, wmc, "WMC classes (Threshold = ?) - " + repo, "threshold-percentages-wmc-" + repo + ".svg", "Classes", "WMC >= ", "WMC < ", THRESHOLD_WMC)
        plot_threshold_measures(versions[index], classes, wmc, "WMC classes (Threshold = ?) - " + repo, "threshold-measures-wmc-" + repo + ".svg", "Classes", "WMC >= ", "WMC < ", THRESHOLD_WMC, opt)
        plot_threshold_percentages(versions[index], classes, npm, "NPM classes (Threshold = ?) - " + repo, "threshold-percentages-npm-" + repo + ".svg", "Classes", "NPM >= ", "NPM < ", THRESHOLD_NPM)
        plot_threshold_measures(versions[index], classes, npm, "NPM classes (Threshold = ?) - " + repo, "threshold-measures-npm-" + repo + ".svg", "Classes", "NPM >= ", "NPM < ", THRESHOLD_NPM, opt)
        plot_threshold_percentages(versions[index], classes, npa, "NPA classes (Threshold = ?) - " + repo, "threshold-percentages-npa-" + repo + ".svg", "Classes", "NPA >= ", "NPA < ", THRESHOLD_NPA)
        plot_threshold_measures(versions[index], classes, npa, "NPA classes (Threshold = ?) - " + repo, "threshold-measures-npa-" + repo + ".svg", "Classes", "NPA >= ", "NPA < ", THRESHOLD_NPA, opt)
        plot_threshold_percentages(versions[index], classes, coa, "COA classes (Threshold = ?) - " + repo, "threshold-percentages-coa-" + repo + ".svg", "Classes", "COA = ", "COA < ", THRESHOLD_COA)
        plot_threshold_measures(versions[index], classes, coa, "COA classes (Threshold = ?) - " + repo, "threshold-measures-coa-" + repo + ".svg", "Classes", "COA = ", "COA < ", THRESHOLD_COA, opt)
        plot_threshold_percentages(versions[index], classes, cda, "CDA classes (Threshold = ?) - " + repo, "threshold-percentages-cda-" + repo + ".svg", "Classes", "CDA = ", "CDA < ", THRESHOLD_CDA)
        plot_threshold_measures(versions[index], classes, cda, "CDA classes (Threshold = ?) - " + repo, "threshold-measures-cda-" + repo + ".svg", "Classes", "CDA = ", "CDA < ", THRESHOLD_CDA, opt)
        print_plot(versions[index], avg,"./temporal-analysis/cumulative/average-measures-" + repo)
        print_plot(versions[index], max,"./temporal-analysis/cumulative/maximum-measures-" + repo)
        print(repo + " graphs generated!")
    
    print("Generating ranking tables...")
    for i, v in enumerate(top_metrics):
        f = open("./temporal-analysis/rankings/top_" + v + "_" + ("files" if i == 0 else "classes") + ".csv", "w")
        csv.writer(f).writerow(header)
        csv.writer(f).writerows(top_data[i])
        f.close()
    print("Ranking tables generated!")

temporal_analysis()