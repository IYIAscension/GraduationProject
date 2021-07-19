import sys

import matplotlib.pyplot as plt
import pandas

if __name__ == "__main__":

    directory = sys.argv[1]
    projects = ['google-auto-service', 'scribejava-core', 'google-auto-factory', 'google-auto-common',
                'google-auto-value', 'gson', 'commons-io', 'commons-cli', 'commons-text', 'commonc-codec',
                'commons-csv', 'commons-lang', 'jfreechart', 'jodatime', 'zxing', ]
    reductions = [0.25, 0.5, 0.75]
    seeds = [66304, 16389, 14706, 91254, 49890, 86054, 55284, 77324, 36147, 13506, 73920, 80157, 43981, 75358, 33399,
             56134, 13388, 81617, 90957, 52113, 20428, 26482, 56340, 31018, 32067, 13067, 8339, 49008, 125894, 68282, ]
    csv_path = directory + "/fcm_no_distance"

    results_df = pandas.DataFrame(columns=['project', 'clusters', 'score', 'acc_avg', 'acc_min', 'acc_max'])
    tmp = pandas.DataFrame(columns=["project", 'seed', "clusters", "score", "acc_avg", "acc_min", "acc_max"])
    boxplot_df = pandas.DataFrame()
    for seed in seeds:
        data = pandas.read_csv(csv_path + "/" + str(seed) + ".csv",
                               names=["project", 'seed', "clusters", "score", "acc_avg", "acc_min", "acc_max"],
                               skiprows=1)
        tmp = tmp.append(data)

    for project in projects:
        cur = tmp[tmp['project'] == project]
        cur.reset_index(inplace=True)
        boxplot_df[project] = cur['score']


    bp = boxplot_df.boxplot(column=projects,figsize=(9, 7))

    plt.ylabel("mutation score %")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    # bp.get_figure().savefig("boxplots/fcm_no_distance/"+project+".png")
    bp.get_figure().savefig("boxplots/fcm_summary/fcm_no_distance.png")

