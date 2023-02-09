# This file was made for personal use, using it is not recommended.
# It was used to create tables from raw cell outputs of CMT/CPMT.
# These tables were used to create tables that were fed
# to powerBI to create the graphs in Adam's thesis.

import numpy as np
import os
import sys
from ast import literal_eval
from scipy.stats import mannwhitneyu


# Source: tutorialspoint.com/file-searching-using-python
def find_files(filename, search_path):
   result = []

    # Walking top-down from the root
   for root, _, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result


cmtProjects = ["google-auto-common", "scribejava-core", "google-auto-factory", "commons-csv",
                "commons-cli", "google-auto-value", "gson", "commons-io","commons-text", "commons-codec", ]
cpmtProjects = ["commons-text", "commons-codec", "google-auto-common", "scribejava-core", "google-auto-factory", "commons-csv",
                "commons-cli", "google-auto-value", "gson", "commons-io", ]


# Boxplot tables for all methods of CMT, for all reductions.
# Requires cmtImprovement output in "cmtImprovementOutput.txt".
precisions = [[[[] for _ in range(len(cpmtProjects))] for _ in range(4)] for _ in range(3)]
reductions = ["05", "025", "01"]
with open(os.path.join(sys.path[0], "cmtImprovementOutput.txt"), "r") as inputF:
    for i in range(len(reductions)):
        outputF = open(os.path.join(sys.path[0], "tables/cmt/" + "cmt" + reductions[i] + "FirstBoxPlotTable.txt"), "w")
        outputF.write("project, method, run, precision\n")
        for x, project in enumerate(cmtProjects[:5]):
            inputF.readline()
            for run, val in enumerate(literal_eval(inputF.readline().split("= ")[-1])[i]):
                outputF.write("{}, orig, {}, {:.1f}\n".format(project, run, val * 100))
                precisions[i][0][x].append(val * 100)
            val = literal_eval(inputF.readline().split("= ")[-1])[i] * 100
            outputF.write("{}, cs, 0, {:.1f}\n".format(project, val))
            precisions[i][1][x].append(val)
            for run, val in enumerate(literal_eval(inputF.readline().split("= ")[-1])[i]):
                precisions[i][2][x].append(val * 100)
                outputF.write("{}, pp, {}, {:.1f}\n".format(project, run, val * 100))
            val = literal_eval(inputF.readline().split("= ")[-1])[i] * 100
            outputF.write("{}, cs+pp, 0, {:.1f}\n".format(project, val))
            precisions[i][3][x].append(val)
        outputF.close()
        outputF = open(os.path.join(sys.path[0], "tables/cmt/" + "cmt" + reductions[i] + "SecondBoxPlotTable.txt"), "w")
        outputF.write("project, method, run, precision\n")
        for x, project in enumerate(cmtProjects[5:]):
            inputF.readline()
            for run, val in enumerate(literal_eval(inputF.readline().split("= ")[-1])[i]):
                outputF.write("{}, orig, {}, {:.1f}\n".format(project, run, val * 100))
                precisions[i][0][x+5].append(val * 100)
            val = literal_eval(inputF.readline().split("= ")[-1])[i] * 100
            outputF.write("{}, cs, 0, {:.1f}\n".format(project, val))
            precisions[i][1][x+5].append(val)
            for run, val in enumerate(literal_eval(inputF.readline().split("= ")[-1])[i]):
                precisions[i][2][x+5].append(val * 100)
                outputF.write("{}, pp, {}, {:.1f}\n".format(project, run, val * 100))
            val = literal_eval(inputF.readline().split("= ")[-1])[i] * 100
            outputF.write("{}, cs+pp, 0, {:.1f}\n".format(project, val))
            precisions[i][3][x+5].append(val)
        outputF.close()

        inputF.seek(0)


# Calculates the heatmap value for given samples with given significance test's p-value.
alpha = 0.05
def heatMapVal(sample1, sample2, pvalue):
    if pvalue < alpha:
        pvalue = 2
    else:
        pvalue = 1
    if np.mean(sample1) > np.mean(sample2):
        pvalue = -pvalue
    return pvalue


# Calculates the heatmap value for given sample and fixed number with Central Limit Theory.
def compareFixed(randomResults, fixedResult):
    randomMean = np.mean(randomResults)
    randomStd = np.std(randomResults)
    z5 = -1.64
    z95 = 1.64
    if randomMean > fixedResult:
        if randomMean + randomStd/30**0.5 * z5 > fixedResult:
            return -2
        return -1
    if randomMean < fixedResult:
        if randomMean + randomStd/30**0.5 * z95 < fixedResult:
            return 2
        return 1


# These code blocks were used for heatmap comparisons between CMT methods.
with open(os.path.join(sys.path[0], "tables/cmt/" + "cmtPP-HMtable.txt"), "w") as pValueFile:
    pValueFile.write("project, 0.1, 0.25, 0.5\n")
    for x, project in enumerate(cmtProjects):
        _, pvalue1 = mannwhitneyu(precisions[2][0][x], precisions[2][2][x])
        _, pvalue2 = mannwhitneyu(precisions[1][0][x], precisions[1][2][x])
        _, pvalue3 = mannwhitneyu(precisions[0][0][x], precisions[0][2][x])
        pvalue1 = heatMapVal(precisions[2][0][x], precisions[2][2][x], pvalue1)
        pvalue2 = heatMapVal(precisions[1][0][x], precisions[1][2][x], pvalue2)
        pvalue3 = heatMapVal(precisions[0][0][x], precisions[0][2][x], pvalue3)
        pValueFile.write("{}, {:.2f}, {:.2f}, {:.2f}\n".format(project, pvalue1, pvalue2, pvalue3))

with open(os.path.join(sys.path[0], "tables/cmt/" + "cmtCSPP-HMtable.txt"), "w") as pValueFile:
    pValueFile.write("project, 0.1, 0.25, 0.5\n")
    for x, project in enumerate(cmtProjects):
        pvalue1 = compareFixed(precisions[2][0][x], precisions[2][3][x][0])
        pvalue2 = compareFixed(precisions[1][0][x], precisions[1][3][x][0])
        pvalue3 = compareFixed(precisions[0][0][x], precisions[0][3][x][0])
        pValueFile.write("{}, {:.2f}, {:.2f}, {:.2f}\n".format(project, pvalue1, pvalue2, pvalue3))

with open(os.path.join(sys.path[0], "tables/cmt/" + "cmtCS-HMtable.txt"), "w") as pValueFile:
    pValueFile.write("project, 0.1, 0.25, 0.5\n")
    for x, project in enumerate(cmtProjects):
        pvalue1 = compareFixed(precisions[2][0][x], precisions[2][1][x][0])
        pvalue2 = compareFixed(precisions[1][0][x], precisions[1][1][x][0])
        pvalue3 = compareFixed(precisions[0][0][x], precisions[0][1][x][0])
        pValueFile.write("{}, {:.2f}, {:.2f}, {:.2f}\n".format(project, pvalue1, pvalue2, pvalue3))

with open(os.path.join(sys.path[0], "tables/cmt/" + "cmtAllHeatmap.txt"), "w") as pValueFile:
    pValueFile.write("method, 0.1, 0.25, 0.5\n")
    pValueFile.write("CS, {:.2f}, {:.2f}, {:.2f}\n".format(heatMapVal([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][1] for val in sublist], mannwhitneyu([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][1] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][1] for val in sublist], mannwhitneyu([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][1] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][1] for val in sublist], mannwhitneyu([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][1] for val in sublist])[1])))
    pValueFile.write("CSPP, {:.2f}, {:.2f}, {:.2f}\n".format(heatMapVal([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][3] for val in sublist], mannwhitneyu([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][3] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][3] for val in sublist], mannwhitneyu([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][3] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][3] for val in sublist], mannwhitneyu([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][3] for val in sublist])[1])))
    pValueFile.write("PP, {:.2f}, {:.2f}, {:.2f}\n".format(heatMapVal([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][2] for val in sublist], mannwhitneyu([val for sublist in precisions[2][0] for val in sublist], [val for sublist in precisions[2][2] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][2] for val in sublist], mannwhitneyu([val for sublist in precisions[1][0] for val in sublist], [val for sublist in precisions[1][2] for val in sublist])[1]),
                                                            heatMapVal([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][2] for val in sublist], mannwhitneyu([val for sublist in precisions[0][0] for val in sublist], [val for sublist in precisions[0][2] for val in sublist])[1])))


# These code blocks were used for boxplots of precisions/reductions/timings for all reported CPMT methods.
# Required files from here are files with raw cell outputs of corresponding CPMT version:
# "CPMTOutput.txt", "cpmt3ProjectOutput.txt", "cpmtClusterSelectionOutput.txt", cpmt3DClusteringOutput.txt".
cmtPrecisions = precisions
precisions = [[[] for _ in range(len(cpmtProjects))] for _ in range(4)]
reductions = [[[] for _ in range(len(cpmtProjects))] for _ in range(4)]
timings = [[[] for _ in range(len(cpmtProjects))] for _ in range(4)]

def arrayFiller(inputF, index, seeds):
    for _ in range(seeds):
        for i in range(len(cpmtProjects)):
            redFound = 0
            timingFound = 0
            while True:
                line = inputF.readline()
                if timingFound == 1:
                    precisions[index][i].append(float(line.split()[-1]) * 100)
                    timingFound = 0
                    break
                elif redFound == 1:
                    timings[index][i].append(float(line.split()[-2]))
                    timingFound = 1
                    redFound = 0
                elif "reduction =" in line:
                    reductions[index][i].append(float(line.split()[-1]))
                    redFound = 1

with open(os.path.join(sys.path[0], "CPMTOutput.txt"), "r") as cpmtInputF:
    arrayFiller(cpmtInputF, 0, 30)

with open(os.path.join(sys.path[0], "cpmt3ProjectOutput.txt"), "r") as cpmt3ProjectInputF:
    arrayFiller(cpmt3ProjectInputF, 1, 30)

with open(os.path.join(sys.path[0], "cpmtClusterSelectionOutput.txt"), "r") as cpmtClusterSelectionInputF:
    arrayFiller(cpmtClusterSelectionInputF, 2, 1)

with open(os.path.join(sys.path[0], "cpmt3DClusteringOutput.txt"), "r") as cpmt3DClusInputF:
    arrayFiller(cpmt3DClusInputF, 3, 30)

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtPrecisionsFirstBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, precision\n"))
    for i, project in enumerate(cpmtProjects[:5]):
        outputF.write("{}, cs, 0, {:.1f}\n".format(project, precisions[2][i][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.1f}\n".format(project, x, precisions[0][i][x]))
            outputF.write("{}, 3-Proj, {}, {:.1f}\n".format(project, x, precisions[1][i][x]))
            outputF.write("{}, 3D-Clus, {}, {:.1f}\n".format(project, x, precisions[3][i][x]))

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtPrecisionsSecondBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, precision\n"))
    for i, project in enumerate(cpmtProjects[5:]):
        outputF.write("{}, cs, 0, {:.1f}\n".format(project, precisions[2][i+5][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.1f}\n".format(project, x, precisions[0][i+5][x]))
            outputF.write("{}, 3-Proj, {}, {:.1f}\n".format(project, x, precisions[1][i+5][x]))
            outputF.write("{}, 3D-Clus, {}, {:.1f}\n".format(project, x, precisions[3][i+5][x]))

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtTimingsFirstBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, timing\n"))
    for i, project in enumerate(cpmtProjects[:5]):
        outputF.write("{}, cs, 0, {:.1f}\n".format(project, timings[2][i][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.1f}\n".format(project, x, timings[0][i][x]))
            outputF.write("{}, 3-Proj, {}, {:.1f}\n".format(project, x, timings[1][i][x]))
            outputF.write("{}, 3D-Clus, {}, {:.1f}\n".format(project, x, timings[3][i][x]))

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtTimingsSecondBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, timing\n"))
    for i, project in enumerate(cpmtProjects[5:]):
        outputF.write("{}, cs, 0, {:.1f}\n".format(project, timings[2][i+5][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.1f}\n".format(project, x, timings[0][i+5][x]))
            outputF.write("{}, 3-Proj, {}, {:.1f}\n".format(project, x, timings[1][i+5][x]))
            outputF.write("{}, 3D-Clus, {}, {:.1f}\n".format(project, x, timings[3][i+5][x]))

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtReductionsFirstBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, reduction\n"))
    for i, project in enumerate(cpmtProjects[:5]):
        outputF.write("{}, cs, 0, {:.3f}\n".format(project, reductions[2][i][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.3f}\n".format(project, x, reductions[0][i][x]))
            outputF.write("{}, 3-Proj, {}, {:.3f}\n".format(project, x, reductions[1][i][x]))
            outputF.write("{}, 3D-Clus, {}, {:.3f}\n".format(project, x, reductions[3][i][x]))

with open(os.path.join(sys.path[0], "tables/cpmt/cpmtReductionsSecondBoxPlotTable.txt"), "w") as outputF:
    outputF.write(("project, method, run, reduction\n"))
    for i, project in enumerate(cpmtProjects[5:]):
        outputF.write("{}, cs, 0, {:.3f}\n".format(project,  reductions[2][i+5][0]))
        for x in range(30):
            outputF.write("{}, orig, {}, {:.3f}\n".format(project, x,  reductions[0][i+5][x]))
            outputF.write("{}, 3-Proj, {}, {:.3f}\n".format(project, x,  reductions[1][i+5][x]))
            outputF.write("{}, 3D-Clus, {}, {:.3f}\n".format(project, x,  reductions[3][i+5][x]))


# This was used for a heatmap comparison between CPMT (orig) and CMT (w/ better pre-processing).
with open(os.path.join(sys.path[0], "tables/cpmt/" + "CPMTvsCMT.txt"), "w") as pValueFile:
    pValueFile.write("project, result\n")
    for x, project in enumerate(cmtProjects):
        _, pvalue = mannwhitneyu(cmtPrecisions[2][2][x], precisions[0][x])
        pvalue = heatMapVal(cmtPrecisions[2][2][x], precisions[0][x], pvalue3)
        pValueFile.write("{}, {:.2f}\n".format(project, pvalue))
    pValueFile.write("average, {:.2f}\n".format(heatMapVal([val for sublist in cmtPrecisions[2][2] for val in sublist], [val for sublist in precisions[0] for val in sublist], mannwhitneyu([val for sublist in cmtPrecisions[2][2] for val in sublist], [val for sublist in precisions[0] for val in sublist])[1])))
