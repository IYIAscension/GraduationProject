import sys

import pandas
from fcmeans import FCM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


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


if __name__ == '__main__':
    directory = sys.argv[1]
    seed = int(sys.argv[2])
    projects = pandas.read_csv(directory + "/exp2_cluster_size/cluster_sizes.csv",
                               names=["project", "clusters"],
                               skiprows=1)
    dont_use_this = [
        66304, 16389, 14706, 91254, 49890, 86054, 55284, 77324, 36147, 13506, 73920, 80157, 43981, 75358, 33399, 56134,
        13388, 81617, 90957, 52113, 20428, 26482, 56340, 31018, 32067, 13067, 8339, 49008, 125894, 68282, ]

    results_df = pandas.DataFrame(columns=['project', 'seed', 'clusters', 'score', 'acc_avg', 'acc_min', 'acc_max'])
    for row in projects.itertuples():
        print(row.project, seed)
        csv_path = directory + "/" + row.project

        data = pandas.read_csv(csv_path + "/clustering/characteristic_complete.csv",
                               names=["id", "mutOperator", "opcode", "returnType", "localVarsCount", "isInTryCatch",
                                      "isInFinalBlock", "className", "methodName", "blockNumber", "lineNumber",
                                      "distance",
                                      "killed", "numTests", ],
                               skiprows=1)
        del data['killed']
        encoder = LabelEncoder()
        for col in ["mutOperator", "returnType", "className", "methodName", "id"]:
            data[col] = encoder.fit_transform(data[col])

        X_train, X_test = train_test_split(data, test_size=0.20, random_state=seed)

        X = data.values
        fcm = FCM(n_clusters=row.clusters, max_iter=15, random_state=seed, m=2.5)
        fcm.fit(X_train)
        fcm_centers = fcm.centers

        fcm_labels = fcm.predict(X_test)

        data["id"] = encoder.inverse_transform(data["id"])

        export_clusters(fcm_labels, data, csv_path)
        results = calculate_clustered_score(csv_path, seed)
        results_df = results_df.append(
            {'project': row.project, 'seed': seed, 'clusters': row.clusters, 'score': results['score'],
             'acc_avg': results['acc_avg'],
             'acc_min': results['acc_min'], 'acc_max': results['acc_max']},
            ignore_index=True)
        results_df.to_csv(directory + "/fcm_no_distance/" + str(seed) + ".csv", sep=',',
                          index=False, )
