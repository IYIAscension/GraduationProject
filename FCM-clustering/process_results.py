import sys

import pandas

if __name__ == '__main__':
    directory = sys.argv[1]
    csv_path = directory + "/fcm_full"
    seeds = [
        66304, 16389, 14706, 91254, 49890, 86054, 55284, 77324, 36147, 13506, 73920, 80157, 43981, 75358, 33399, 56134,
        13388, 81617, 90957, 52113, 20428, 26482, 56340, 31018, 32067, 13067, 8339, 49008, 125894, 68282, ]
    projects = ['google-auto-service', 'scribejava-core', 'google-auto-factory', 'google-auto-common', 'google-auto-value','gson', 'commons-io', 'commons-cli',
                 'commons-text','commonc-codec', 'commons-csv','commons-lang',
                'jfreechart', 'jodatime', 'zxing',
                 ]
    results_df = pandas.DataFrame(columns=['project', 'clusters', 'score', 'acc_avg', 'acc_min', 'acc_max'])
    tmp = pandas.DataFrame(columns=["project", 'seed', "clusters", "score", "acc_avg", "acc_min", "acc_max"])
    for seed in seeds:
        data = pandas.read_csv(csv_path + "/" + str(seed) + ".csv",
                               names=["project", 'seed', "clusters", "score", "acc_avg", "acc_min", "acc_max"],
                               skiprows=1)
        tmp = tmp.append(data)

    for project in projects:
        cur = tmp[tmp['project'] == project]

        results_df = results_df.append(
            {'project': project, 'clusters': cur['clusters'].mean(), 'score': cur['score'].mean(),
             'acc_avg': cur['acc_avg'].mean(),
             'acc_min': cur['acc_min'].mean(), 'acc_max': cur['acc_max'].mean()},
            ignore_index=True)
    results_df.to_csv(csv_path + "/avg_result.csv", sep=',',
                      index=False, )
