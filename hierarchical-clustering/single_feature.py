import random
import sys

import pandas
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from pathlib import Path

# Set this so we can render dendograms.
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


def export_mutants(labels, csv_data, export_dir):
    f = open(export_dir + "/target/pit-reports/clustering/cluster.csv", "w")
    f.write("id,distance,weight\n")
    cluster = {}
    for i in range(0, len(labels)):
        # Select one random mutant from this cluster
        if labels[i] not in cluster:
            cluster[labels[i]] = [i]
        else:
            cluster[labels[i]].append(i)

    for key, value in cluster.items():
        if len(value) < 1:
            print("Error no mutants found in cluster")
        mutant = csv_data.loc[random.choice(value)]
        f.write("{},{},{}\n".format(mutant.id, mutant.distance, len(value)))


if __name__ == "__main__":
    reduction = int(sys.argv[1])
    directory = sys.argv[2]
    csvFile = Path(directory + "/target/pit-reports/clustering/distance.csv")
    if int(reduction) < 2:
        sys.exit('Need at least 2 clusters.')
    if not csvFile.is_file():
        sys.exit("distance.csv not found.")

    data = pandas.read_csv(csvFile,
                           names=["id", "distance"],
                           skiprows=1)

    X = np.array([[i] for i in data.distance.tolist()])
    clustering = AgglomerativeClustering(distance_threshold=None, n_clusters=int(len(data) / reduction), linkage="ward",
                                         compute_distances=True, memory='D:/repos/clustering/cache')
    clustering = clustering.fit(X)
    # export_mutants(clustering.labels_, data, directory)

    # plt.figure(figsize=(25, 10))
    # plt.title("Hierarchical Clustering Dendrogram (truncated)")
    # plt.xlabel("sample index or (cluster size)")
    # plt.ylabel("distance")
    # fancy_dendrogram(
    #     calc_linkage_matrix(clustering),
    #     truncate_mode="lastp",
    #     p=96,
    #     leaf_rotation=90.,
    #     leaf_font_size=12.,
    #     show_contracted=True,
    #     annotate_above=10,  # useful in small plots so annotations don"t overlap
    #     # max_d=500 # Show this if we want a cutoff line
    # )
    # plt.show()
