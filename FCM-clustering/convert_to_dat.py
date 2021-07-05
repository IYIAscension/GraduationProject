import pandas as pd
from sklearn.preprocessing import LabelEncoder

if __name__ == '__main__':
    projects = ['google-auto-service', 'google-auto-common',
                'scribejava-core', 'google-auto-factory', 'commons-csv', 'commons-cli', 'google-auto-value', 'gson',
                'commons-io', 'commons-text', 'commonc-codec', 'jodatime', 'commons-lang', 'zxing', 'jfreechart', ]

    for project in projects:
        DataFrame = pd.read_csv(
            "D:/Dropbox/UVA/thesis/experiment_results/" + project + "/clustering/characteristic_complete.csv",
            names=["id", "mutOperator", "opcode", "returnType",
                   "localVarsCount", "isInTryCatch", "isInFinalBlock",
                   "className", "methodName", "blockNumber", "lineNumber",
                   "distance", "killed", "numTests"],
            skiprows=1)

        del DataFrame['killed']

        # define ordinal encoding
        encoder = LabelEncoder()
        DataFrame = DataFrame[["id", "mutOperator", "opcode", "returnType",
                               "localVarsCount", "isInTryCatch", "isInFinalBlock", "className", "methodName",
                               "blockNumber", "lineNumber", "distance", "numTests"]]
        for col in ["mutOperator", "returnType", "className", "methodName", "id"]:
            DataFrame[col] = encoder.fit_transform(DataFrame[col])

        DataFrame.to_csv("C:/Users/rasja/Documents/MATLAB/data/" + project.replace("-","_") + ".dat", sep=' ',
                         index=False, header=False)
