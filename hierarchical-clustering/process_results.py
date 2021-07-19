import sys

import pandas

# this is so we can render big dendogram

sys.setrecursionlimit(100000)

if __name__ == "__main__":

    directory = sys.argv[1]
    skipped = ['zxing', 'commons-lang', 'jodatime', 'jfreechart', ]
    projects = ['google-auto-service', 'google-auto-common', 'scribejava-core', 'google-auto-factory', 'commons-csv',
                'commons-cli', 'google-auto-value', 'gson', 'commons-io', 'commons-text', 'commonc-codec', ]
    reductions = [0.25, 0.5, 0.75]
    results_df = pandas.DataFrame(columns=['project', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max', ])
    avg_df = pandas.DataFrame(columns=['project', 'reduction', 'score'])
    for project in projects:
        data = pandas.read_csv(directory + "/no_distance/results_exp_no_distance_" + project + ".csv",
                               names=['seed','reduction','score','acc_avg','acc_min','acc_max'],
                               skiprows=1)
    data = pandas.read_csv(directory + "/no_distance/results_exp_no_distance_" + "project" + ".csv",
                           names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max'],
                           skiprows=1)
    # for reduction in reductions:
    curData = data[data['reduction'] == 0.50]
    for index, row in curData.iterrows():
        print("{},{}".format(row.seed, row.score))
        # avg_df = avg_df.append(
        #     {'project': project, 'reduction': reduction, 'score': score_diff},
    #         ignore_index=True)
    # avg_df = avg_df.sort_values('reduction')
    # avg_df.to_csv(directory + "/no_distance" + "/results_no_distance_seed_diff.csv", sep=',',
    #                       index=False, )
    # for reduction in reductions:
    #
    #     cvs_path = directory + "/no_distance"
    #     for project in projects:
    #         data = pandas.read_csv(cvs_path + "/results_exp_no_distance_" + project + ".csv",
    #                                names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max', ],
    #                                skiprows=1)
    #         sorted = data[data['reduction'] == reduction]
    #         results_df = results_df.append(
    #             {'project': project, 'reduction': reduction, 'score': sorted['score'].mean(),
    #              'acc_avg': sorted['acc_avg'].mean(), 'acc_min': sorted['acc_min'].mean(),
    #              'acc_max': sorted['acc_max'].mean()},
    #             ignore_index=True)
    # results_df = results_df.sort_values('project')
    # results_df.to_csv(directory + "/no_distance" + "/results_no_distance_avg.csv", sep=',',
    #                       index=False, )
