import math
import random
import sys
import datetime
from pathlib import Path

import numpy as np
import pandas
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
# this is so we can render big dendogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import LabelEncoder

sys.setrecursionlimit(100000)


def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop("max_d", None)
    if max_d and "color_threshold" not in kwargs:
        kwargs["color_threshold"] = max_d
    annotate_above = kwargs.pop("annotate_above", 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get("no_plot", False):
        plt.title("Hierarchical Clustering Dendrogram (truncated)")
        plt.xlabel("sample index or (cluster size)")
        plt.ylabel("distance")
        for i, d, c in zip(ddata["icoord"], ddata["dcoord"], ddata["color_list"]):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, "o", c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords="offset points",
                             va="top", ha="center")
        if max_d:
            plt.axhline(y=max_d, c="k")
    return ddata


def calc_linkage_matrix(model):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    return np.column_stack([model.children_, model.distances_,
                            counts]).astype(float)


def export_clusters(labels, csv_data, export_dir):
    df = pandas.DataFrame(columns=['id', 'cluster_id'])
    for i in range(0, len(labels)):
        df = df.append({'id': csv_data['id'][i], 'cluster_id': labels[i]}, ignore_index=True)

    df.to_csv(export_dir + "/clustering/clusters.csv", sep=',', index=False)
    return df


def calculate_clustered_score(directory, seed):
    killed = pandas.read_csv(directory + "/clustering/killed.csv",
                             names=["id", "killed", " numTests"],
                             skiprows=1)
    clustered = pandas.read_csv(directory + "/clustering/clusters.csv",
                                names=["id", "cluster_id"],
                                skiprows=1)
    df = clustered.merge(killed, on="id")
    acc_min = 1
    acc_max = 0
    acc_total = 0
    killed = 0
    clusters = df['cluster_id'].unique()
    for cluster_id in clusters:
        curr_acc = 0
        tmp = df[df['cluster_id'] == cluster_id]
        cluster_killed = len(tmp[tmp['killed'] == 0])
        cluster_survived = len(tmp[tmp['killed'] == 1])
        # Select x mutant from cluster
        if tmp.sample(random_state=seed).iloc[0]['killed'] == 0:
            killed += len(tmp)
        if cluster_killed > cluster_survived:
            curr_acc += (cluster_killed / len(tmp))
        elif cluster_killed == cluster_survived:
            curr_acc += 0.5
        elif cluster_killed < cluster_survived:
            curr_acc += (cluster_survived / len(tmp))
        # set min/max acc.
        if curr_acc > acc_max:
            acc_max = curr_acc
        if curr_acc < acc_min:
            acc_min = curr_acc

        acc_total += curr_acc
    return {'score': (killed / len(df)), 'acc_avg': (acc_total / len(clusters)), 'acc_min': acc_min,
            'acc_max': acc_max}


def merge_csv_files(directory):
    df_characteristic = pandas.read_csv(directory + "/clustering/characteristics.csv",
                                        names=["id", "mutOperator", "opcode", "returnType",
                                               "localVarsCount",
                                               "isInTryCatch", "isInFinalBlock", "className", "methodName",
                                               "blockNumber",
                                               "lineNumber"],
                                        skiprows=1)
    df_levenshtein = pandas.read_csv(directory + "/clustering/distance.csv",
                                     names=["id", "distance"],
                                     skiprows=1)
    df_numTests = pandas.read_csv(directory + "/clustering/killed.csv",
                                  names=["id", "killed", "numTests"],
                                  skiprows=1)

    df = df_characteristic.merge(df_levenshtein, on="id")
    df2 = df.merge(df_numTests, on="id")
    df2.to_csv(directory + "/clustering/characteristic_complete.csv", sep=',', index=False)
    del df2['killed']
    return df2


if __name__ == "__main__":
    print(datetime.datetime.now())
    directory = sys.argv[1]
    skipped = ['zxing', 'commons-lang', 'jodatime', 'jfreechart', ]
    projects = ['google-auto-service', 'google-auto-common', 'scribejava-core', 'google-auto-factory', 'commons-csv',
                'commons-cli', 'google-auto-value', 'gson', 'commons-io', 'commons-text', 'commonc-codec', ]
    projects1 = ['google-auto-common']
    reductions = [0.25, 0.5, 0.75]

    results_df = pandas.DataFrame(columns=['project', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max'])
    seed = random.randint(0, 99999)
    for project in projects:
        csvPath = directory + "/" + project
        csvFile = Path(csvPath + "/clustering/characteristics.csv")

        if not csvFile.is_file():
            print("characteristics not found: " + project)
            continue

        for reduction in reductions:

            data = merge_csv_files(csvPath)

            # define ordinal encoding
            encoder = LabelEncoder()
            data = data[["id", "mutOperator", "opcode", "returnType",
                         "localVarsCount", "isInTryCatch", "isInFinalBlock", "className", "methodName",
                         "blockNumber", "lineNumber", "distance", "numTests"]]
            # Transform each column.. do id last since we need to inverse that.
            for col in ["mutOperator", "returnType", "className", "methodName", "id"]:
                data[col] = encoder.fit_transform(data[col])

            clustering = AgglomerativeClustering(distance_threshold=None,
                                                 n_clusters=int(math.ceil(len(data) * reduction)),
                                                 linkage="ward",
                                                 compute_distances=True)
            clustering = clustering.fit(data)

            # unlabel id so we can recognize the mutants
            data["id"] = encoder.inverse_transform(data["id"])
            export_clusters(clustering.labels_, data, csvPath)

            results = calculate_clustered_score(csvPath, seed)

            results_df = results_df.append(
                {'project': project, 'reduction': reduction, 'score': results['score'], 'acc_avg': results['acc_avg'],
                 'acc_min': results['acc_min'], 'acc_max': results['acc_max']},
                ignore_index=True)
            results_df.to_csv(directory + "/full" + "/results_exp_full_" + str(seed) + ".csv", sep=',', index=False)

    results_df.to_csv(directory + "/full" + "/results_exp_full_" + str(seed) + ".csv", sep=',', index=False)
    print(datetime.datetime.now())
# plt.title('Hierarchical Clustering Dendrogram (truncated)')
# plt.xlabel('sample index or (cluster size)')
# plt.ylabel('distance')
# dendrogram(
#     calc_linkage_matrix(clustering),
#     truncate_mode='lastp',  # show only the last p merged clusters
#     p=12,  # show only the last p merged clusters
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,  # to get a distribution impression in truncated branches
# )
# plt.show()
