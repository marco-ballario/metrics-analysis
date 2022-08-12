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

    for filename in glob.iglob("data/" + repository_name + "/" + version + "/**/*.json", recursive=True):
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

def plot_cumulative_measures(repositories, values, legend_loc, title, file):
    x = []
    y = []
    for i in range(0, len(repositories)):
        x.append([values[i][2], values[i][1], values[i][0]])
        y.append([repositories[i] + "_avg", repositories[i] + "_max", repositories[i] + "_sum"])

    font_size = 28
    figure(figsize=(50, 26), dpi=80)
    plt.rcParams.update({"font.size": font_size})

    for i in range(0,len(repositories)):
        bar=plt.barh(y[i], x[i], 0.66, label=repositories[i])
        plt.bar_label(bar, padding=5, fontweight="bold")

    plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    plt.legend(loc=legend_loc)
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def plot_size_measures(repositories, val, title, file):
    x = []
    y = []
    for i in range(0, len(repositories)):
        x.append([val[i][3], val[i][2], val[i][1], val[i][0]])
        y.append([repositories[i] + "_cyc", repositories[i] + "_ploc", repositories[i] + "_hal", repositories[i] + "_abc"])

    font_size = 28
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(50, 26), dpi=80)

    for i in range(0,len(repositories)):
        bar = plt.barh(y[i], x[i], 0.66, label=repositories[i])
        plt.bar_label(bar, padding=5, fontweight="bold")

    plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left",labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def plot_complexity_measures(repositories, val, title, file):
    x = []
    y = []
    for i in range(0, len(repositories)):
        y.append([repositories[i] + "_cyc", repositories[i] + "_wmc"])
        x.append([val[i][1], val[i][0]])

    font_size = 28
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(50, 26), dpi=80)

    for i in range(0,len(repositories)):
        bar = plt.barh(y[i], x[i], 0.66, label=repositories[i])
        plt.bar_label(bar, padding=5, fontweight="bold")

    plt.margins(y=0.1)
    plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    plt.legend()
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def plot_visibility_measures(repositories, values, title, file):
    y = []
    x1 = []
    x2 = []
    for i in range(0, len(repositories)):
        x1.append([values[i][1]])
        x2.append([values[i][0]])
        y.append([repositories[i]])

    font_size = 28
    name = title.split()[-1]
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(50, 26), dpi=80)

    for i in range(0, len(repositories)):
        bar1 = plt.barh(y[i], x1[i], 0.4, color="#1f77b4", label = "Non-Public " + name)
        bar2 = plt.barh(y[i], x2[i], 0.4, color="#d62728", label = "Public " + name)
        plt.text((values[i][1] - values[i][0]) // 2 + values[i][0], i, str(int(values[i][1] - values[i][0])), color="snow", va="center", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold")
        if values[i][0] != 0:
            plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold")

    plt.margins(y=0.2)
    plt.xticks(rotation=45)
    plt.xlabel("Metric Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper right", prop={"size": font_size})
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def plot_visibility_percentages(repositories, values, title, file):
    y = []
    x1 = []
    x2 = []
    for i in range(0, len(repositories)):
        x1.append([100])
        x2.append([values[i][0] / values[i][1] * 100])
        y.append([repositories[i]])

    font_size = 28
    name = title.split()[-1]
    plt.rcParams.update({"font.size": font_size})
    figure(figsize=(50, 26), dpi=80)

    for i in range(0, len(repositories)):
        bar1 = plt.barh(y[i], x1[i], 0.4, color="#1f77b4", label = "Non-Public " + name)
        bar2 = plt.barh(y[i], x2[i], 0.4, color="#d62728", label = "Public " + name)
        plt.text((100 - x2[i][0]) // 2 + x2[i][0], i, "{:.2f}".format(100 - x2[i][0]) + "%", color="snow", va="center", ha="center", fontweight="bold")
        plt.bar_label(bar1, padding=5, fontweight="bold", fmt="%.0f%%")
        if values[i][0] != 0:
            plt.bar_label(bar2, label_type="center", color="snow", fontweight="bold", fmt="%.2f%%")

    plt.margins(y=0.2)
    plt.xticks(rotation=45)
    plt.xlabel("Percentage Values", loc="left", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.ylabel("Repositories", loc="bottom", labelpad = 10, fontweight="bold", fontsize=font_size)
    plt.title(title)
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [1, 0]
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="upper right", prop={"size": font_size})
    plt.savefig("./graphs/static-analysis/" + file)
    plt.cla()
    return

def static_analysis():
    repos = ["FastCSV", "java-jwt", "jsoup", "Java-WebSocket", "spring-kafka"]
    versions = ["v2.2.0", "4.0.0", "jsoup-1.15.2", "v1.5.3", "v2.9.0"]

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

    plot_cumulative_measures(repos, abc, "best", "ABC - Magnitude", "cumulative-measures-abc.png")
    plot_cumulative_measures(repos, wmc, "best", "WMC - Weighted Methods per Class", "cumulative-measures-wmc.png")
    plot_cumulative_measures(repos, npm, "best", "NPM - Number of Public Methods", "cumulative-measures-npm.png")
    plot_cumulative_measures(repos, npa, "lower right", "NPA - Number of Public Attributes", "cumulative-measures-npa.png")
    plot_visibility_measures(repos, met, "NPM - Number of Public Methods", "visibility-measures-npm.png")
    plot_visibility_measures(repos, att, "NPA - Number of Public Attributes", "visibility-measures-npa.png")
    plot_visibility_percentages(repos, met, "NPM - Number of Public Methods", "visibility-percentages-npm.png")
    plot_visibility_percentages(repos, att, "NPA - Number of Public Attributes", "visibility-percentages-npa.png")
    plot_complexity_measures(repos, compl, "Complexity measures", "metric-comparisons-complexity.png")
    plot_size_measures(repos, size, "Size measures", "metric-comparisons-size.png")
    return

static_analysis()