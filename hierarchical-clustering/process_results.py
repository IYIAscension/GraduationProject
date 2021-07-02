import sys

import pandas

# this is so we can render big dendogram

sys.setrecursionlimit(100000)

if __name__ == "__main__":

    directory = sys.argv[1]
    skipped = ['zxing', 'commons-lang', 'jodatime', 'jfreechart', ]
    projects = ['google-auto-service', 'google-auto-common', 'scribejava-core', 'google-auto-factory', 'commons-csv',
                'commons-cli', 'google-auto-value', 'gson', 'commons-io', 'commons-text', 'commonc-codec', ]
    results_df = pandas.DataFrame(columns=['project', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max', ])
    cvs_path = directory + "/full"
    for project in projects:
        data = pandas.read_csv(cvs_path + "/full" + "/results_exp_full_" + project + ".csv",
                               names=['seed', 'reduction', 'score', 'acc_avg', 'acc_min', 'acc_max', ],
                               skiprows=1)

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
