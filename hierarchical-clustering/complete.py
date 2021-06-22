import os
import subprocess
from pathlib import Path

if __name__ == "__main__":
    cluster_size = [4, 2]
    cluster_command = 'mvn.cmd -U org.pitest:pitest-maven:mutationCoverage -Dfeatures=+CLUSTER'
    cwd = os.getcwd()

    directory = "D:/Dropbox/UVA/thesis/repos/joda-time-2.10.10"

    for i in cluster_size:
        subprocess.call('python single_feature.py ' + str(i) + ' ' + directory)
        os.chdir(directory)
        subprocess.call(cluster_command)
        os.chdir(cwd)
