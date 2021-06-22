import sys

import pandas

if __name__ == "__main__":
    clusters = pandas.read_csv("D:/Dropbox/UVA/thesis/experiment_results/commons-csv/clustering/clusters.csv",
                               names=["id", "cluster_id"],
                               skiprows=1)
    killed = pandas.read_csv("D:/Dropbox/UVA/thesis/experiment_results/commons-csv/clustering/killed.csv",
                             names=["id", "killed","numTests"],
                             skiprows=1)

    cluster_ids = clusters['cluster_id'].unique()
    for i in range(0, len(cluster_ids)):
        curr_cluster_id = cluster_ids[i]
        single_cluster = clusters[clusters['cluster_id'] == curr_cluster_id]
        first_mutant = single_cluster.iloc[0].id
        first_mutant_status = killed[killed['id'] == first_mutant].iloc[0].killed
        for j in range(1, len(single_cluster)):
            cur_mutant = single_cluster.iloc[j].id
            if len(killed[killed['id'] == cur_mutant]) != 1:
                print("panick2")
            cur_mutant_status = killed[killed['id'] == cur_mutant].iloc[0].killed
            if cur_mutant_status != first_mutant_status:
                print("PANIK")
