import json
import glob
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np


def read_measures(repository_name, sum_list, avg_list, min_list, max_list):
    magnitude = []
    for filename in glob.iglob("data/" + repository_name + '**/**/*.json', recursive=True):
        with open(filename, "r") as file:
            jsonData = json.load(file)
            magnitude.append((float(jsonData["metrics"]["abc"]["magnitude"])))
            print(os.path.basename(jsonData["name"]))
            print(jsonData["metrics"]["abc"]["magnitude"])
    magnitude = [float(x) for x in magnitude]
    print(magnitude)
    min_list.append(min(magnitude))
    max_list.append(max(magnitude))
    avg_list.append(sum(magnitude) / len(magnitude))
    sum_list.append(sum(magnitude))
    print(min_list)
    print(max_list)
    print(avg_list)
    return


def plot_measures(repositories, sum_list, avg_list, min_list, max_list):
    figure(figsize=(16, 10), dpi=80)
    plt.subplots_adjust(top=0.92, bottom=0.28)
    plt.rcParams.update({'font.size': 14})
    plt.xticks(rotation='vertical')
    plt.xlabel("Repositories")
    plt.ylabel("Magnitude")
    plt.title("ABC")
    for i in range(0, len(repositories)):
        x = np.array([repositories[i] + "_sum", repositories[i] + "_min", repositories[i] + "_max", repositories[i] + "_avg"])
        y = np.array([sum_list[i], min_list[i], max_list[i], avg_list[i]])
        plt.bar(x, y, 0.5, label=repositories[i])
    plt.legend()
    plt.savefig("./graphs/static-analysis/abc-static-analysis.png")
    return


def static_analysis():
    repositories = ["Java-WebSocket", "jsoup", "java-jwt", "FastCSV"]
    sum_list = []
    avg_list = []
    min_list = []
    max_list = []
    for repository in repositories:
        read_measures(repository, sum_list, avg_list, min_list, max_list)
    plot_measures(repositories, sum_list, avg_list, min_list, max_list) 
    return


static_analysis()
