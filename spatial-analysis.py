import json
import glob
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def read_measures(repository_name, version, abc, npm, npa, wmc, size, compl, met, att):
    abc_mag = []
    npm_tot = []
    npa_tot = []
    wmc_tot = []
    hal_epl = []
    loc_ploc = []
    cyc_sum = []
    npm_avg = []
    npa_avg = []
    npn_tot_met = []
    npa_tot_att = []

    for filename in glob.iglob("data/" + repository_name + "/" + version + "/**/*java.json", recursive=True):
        with open(filename, "r") as file:
            jsonData = json.load(file)
            abc_mag.append(float(jsonData["metrics"]["abc"]["magnitude"]))
            wmc_tot.append(float(jsonData["metrics"]["wmc"]["total"]))
            npm_tot.append(float(jsonData["metrics"]["npm"]["total"]))
            npa_tot.append(float(jsonData["metrics"]["npa"]["total"]))
            npm_avg.append(float(jsonData["metrics"]["npm"]["average"] or 0))
            npa_avg.append(float(jsonData["metrics"]["npa"]["average"] or 0))
            npn_tot_met.append(float(jsonData["metrics"]["npm"]["total_methods"]))
            npa_tot_att.append(float(jsonData["metrics"]["npa"]["total_attributes"]))
            hal_epl.append(float(jsonData["metrics"]["halstead"]["estimated_program_length"]))
            loc_ploc.append(float(jsonData["metrics"]["loc"]["ploc"]))
            cyc_sum.append(float(jsonData["metrics"]["cyclomatic"]["sum"]))

    abc.append([sum(abc_mag), max(abc_mag), sum(abc_mag)/len(abc_mag)])
    wmc.append([sum(wmc_tot), max(wmc_tot), sum(wmc_tot)/len(wmc_tot)])
    npm.append([sum(npm_tot), max(npm_tot), sum(npm_tot)/len(npm_tot)])
    npa.append([sum(npa_tot), max(npa_tot), sum(npa_tot)/len(npa_tot)])
    size.append([sum(abc_mag), sum(hal_epl), sum(loc_ploc), sum(cyc_sum)])
    compl.append([sum(wmc_tot), sum(cyc_sum)])
    met.append([sum(npm_tot), sum(npn_tot_met)])
    att.append([sum(npa_tot), sum(npa_tot_att)])
    return

def plot_cumulative_measures(repositories, values, legend_loc, title, file, abc = False):
    x = []
    y = []
    for i in range(0, len(repositories)):
        x.append([round(values[i][2], 2), round(values[i][1], 2), round(values[i][0], 2)])
        y.append([repositories[i] + "_avg", repositories[i] + "_max", repositories[i] + "_sum"])

    font_size = 30
    #figure(figsize=(50, 26), dpi=80)
    plt.rcParams.update({"font.size": font_size})
    figure, axis = plt.subplots(3, 1)
    figure.set_size_inches(23, 28) #20-28
    titles = ["Sum", "Maximum", "Average"]

    for j in range(3):
        for i in range(0,len(repositories)):
            bar = axis[j].barh(y[i][2-j], x[i][2-j], 0.5, label=repositories[i])
            if abc == True or j == 2:
                axis[j].bar_label(bar, padding=5, fmt="%0.2f", fontweight="bold")
            else:
                axis[j].bar_label(bar, padding=5, fontweight="bold")
        axis[j].margins(x=0.2)
        axis[j].set_xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
        axis[j].set_ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
        axis[j].set_title(title + " - " + titles[j])
        # remove legend?
        #axis[j].legend(loc=legend_loc)
        axis[j].set_ylim([-0.75, 3.75])

    #plt.xticks(rotation=45)
    plt.tight_layout(h_pad=2)
    plt.savefig("./spatial-analysis/" + file)
    plt.cla()
    return

def plot_size_measures(repositories, val, title, file):
    x = []
    y = []
    for i in range(0, len(repositories)):
        x.append([val[i][3], val[i][2], float(round(val[i][1], 2)), float(round(val[i][0], 2))])
        y.append([repositories[i] + "_cyc", repositories[i] + "_ploc", repositories[i] + "_hal", repositories[i] + "_abc"])

    font_size = 30
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(33, 18), dpi=80)

    for i in range(0,len(repositories)):
        bar = plt.barh(y[i], x[i], 0.66, label=repositories[i])
        plt.bar_label(bar, padding=5, fmt="%0.2f", fontweight="bold")

    plt.margins(x=0.13)
    #plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left",labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    plt.legend(loc="lower right",)
    plt.tight_layout()
    plt.savefig("./spatial-analysis/" + file)
    plt.cla()
    return

def plot_complexity_measures(repositories, val, title, file):
    x = []
    y = []
    for i in range(0, len(repositories)):
        y.append([repositories[i] + "_cyc", repositories[i] + "_wmc"])
        x.append([val[i][1], val[i][0]])

    font_size = 30
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(24, 16), dpi=80)

    for i in range(0,len(repositories)):
        bar = plt.barh(y[i], x[i], 0.66, label=repositories[i])
        plt.bar_label(bar, padding=5, fontweight="bold")

    plt.margins(x=0.13)
    #plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    ax = plt.gca()
    ax.set_ylim([-1, 8])
    plt.legend()
    plt.tight_layout()
    plt.savefig("./spatial-analysis/" + file)
    plt.cla()
    return

def plot_visibility_measures(repositories, values, title, file):
    x = []
    y1 = []
    y2 = []
    for i in range(0, len(repositories)):
        y1.append([values[i][1]])
        y2.append([values[i][0]])
        x.append([repositories[i]])

    font_size = 30
    name = title.split()[-1]
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(18, 36), dpi=80)

    for i in range(0, len(repositories)):
        bar1 = plt.bar(x[i], y1[i], 0.5, color="#1f77b4", label = "Non-Public " + name)
        bar2 = plt.bar(x[i], y2[i], 0.5, color="#d62728", label = "Public " + name)
        plt.text(i, (values[i][1] - values[i][0]) / 2 + values[i][0], str(int(values[i][1] - values[i][0])), color="snow", va="center_baseline", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold")
        if values[i][0] != 0:
            plt.text(i, values[i][0] / 2, str(int(values[i][0])), color="snow", va="center_baseline", ha="center", fontweight="bold")
            #plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold")

    plt.margins(x=0.15)
    #plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper left", prop={"size": font_size})
    plt.tight_layout()
    plt.savefig("./spatial-analysis/" + file)
    plt.cla()
    return

def plot_visibility_percentages(repositories, values, title, file):
    x = []
    y1 = []
    y2 = []
    for i in range(0, len(repositories)):
        y1.append([100])
        y2.append([round(values[i][0] / values[i][1] * 100, 2)])
        x.append([repositories[i]])

    font_size = 30
    name = title.split()[-1]
    plt.rcParams.update({"font.size": font_size})
    #plt.rcParams["figure.autolayout"] = True
    figure(figsize=(22, 16), dpi=80)

    for i in range(0, len(repositories)):
        bar1 = plt.bar(x[i], y1[i], 0.5, color="#1f77b4", label = "Non-Public " + name)
        bar2 = plt.bar(x[i], y2[i], 0.5, color="#d62728", label = "Public " + name)
        #plt.bar_label(bar1, padding=5, fontweight="bold", fmt="%.0f%%")
        if values[i][0] == 0:
            plt.text(i, (100 - y2[i][0]) / 2 + y2[i][0], str(int(100.0)) + "%", color="snow", va="center_baseline", ha="center", fontweight="bold")
        else:
            plt.text(i, (100 - y2[i][0]) / 2 + y2[i][0], "{:.2f}".format(100 - y2[i][0]) + "%", color="snow", va="center_baseline", ha="center", fontweight="bold")
        if values[i][0] != 0:
            plt.text(i, y2[i][0] / 2, "{:.2f}".format(y2[i][0]) + "%", color="snow", va="center_baseline", ha="center", fontweight="bold")
            #plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold", fmt="%.2f%%")

    plt.margins(x=0.15)
    #plt.xticks(rotation=45)
    plt.xlabel("Percentage Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    ax = plt.gca()
    ax.set_ylim([0, 120])
    handles, labels = ax.get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper right", prop={"size": font_size})
    plt.tight_layout()
    plt.savefig("./spatial-analysis/" + file)
    plt.cla()
    return

def spatial_analysis():
    repos = ["FastCSV", "Java-WebSocket", "spring-kafka", "mockito"]
    versions = ["v2.2.0", "v1.5.3", "v2.9.0", "v4.7.0"]

    abc = []
    npm = []
    npa = []
    wmc = []
    size = []
    compl = []
    met = []
    att = []

    for i in range(len(repos)):
        read_measures(repos[i], versions[i], abc, npm, npa, wmc, size, compl, met, att)

    plot_cumulative_measures(repos, abc, "lower right", "ABC - Magnitude", "cumulative-measures-abc.svg", True)
    plot_cumulative_measures(repos, wmc, "lower right", "WMC - Weighted Methods per Class", "cumulative-measures-wmc.svg")
    plot_cumulative_measures(repos, npm, "lower right", "NPM - Number of Public Methods", "cumulative-measures-npm.svg")
    plot_cumulative_measures(repos, npa, "lower right", "NPA - Number of Public Attributes", "cumulative-measures-npa.svg")
    plot_visibility_measures(repos, met, "NPM - Number of Public Methods", "visibility-measures-npm.svg")
    plot_visibility_measures(repos, att, "NPA - Number of Public Attributes", "visibility-measures-npa.svg")
    plot_visibility_percentages(repos, met, "NPM - Number of Public Methods", "visibility-percentages-npm.svg")
    plot_visibility_percentages(repos, att, "NPA - Number of Public Attributes", "visibility-percentages-npa.svg")
    plot_complexity_measures(repos, compl, "Complexity measures", "metric-comparisons-complexity.svg")
    plot_size_measures(repos, size, "Size measures", "metric-comparisons-size.svg")
    return

spatial_analysis()