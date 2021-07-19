import sys

import matplotlib.pyplot as plt
import pandas

if __name__ == "__main__":

    directory = sys.argv[1]
    projects = ['google-auto-service', 'google-auto-common', 'scribejava-core', 'google-auto-factory', 'commons-csv',
                'commons-cli', 'google-auto-value', 'gson', 'commons-io', 'commons-text', 'commonc-codec', ]
    reductions = [0.25, 0.5, 0.75]
    results_df = pandas.DataFrame()

    for project in projects:
        data = pandas.read_csv(directory + "/no_distance/results_exp_no_distance_" + project + ".csv",
                               names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max'],
                               skiprows=1)
        curData = data[data['reduction'] == 0.25]
        results_df[project] = curData['score']
        bp = results_df.boxplot(column=project, figsize=(9, 7))

        plt.ylabel("mutation score %")
        # plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        bp.get_figure().savefig("boxplots/no_distance_" + str(25) + "/boxplot_" + project + '.png')
# for reduction in reductions:
# for project in projects:
#     data = pandas.read_csv(directory + "/no_distance/results_exp_no_distance_" + project + ".csv",
#                            names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max'],
#                            skiprows=1)
#     curData = data[data['reduction'] == 0.5]
#     results_df[project] = curData['score']
# bp = results_df.boxplot(column=projects, figsize=(10, 11))
#
# plt.ylabel("mutation score %")
# plt.xticks(rotation=45, ha='right')
# plt.figure(figsize=(10, 10))
# plt.show()
# bp.get_figure().savefig('test.png')

# for project in projects:
#     data = pandas.read_csv(directory + "/no_distance/results_exp_no_distance_" + project + ".csv",
#                            names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max'],
#                            skiprows=1)
