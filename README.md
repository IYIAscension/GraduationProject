
# Mutation testing: "Clustered" and "Contextual Predictive" approaches analysed

## File/folder explanations:
* Graphs: Contains the graphs that were used in the thesis. Most were made in PowerBI. Time Analysis graphs were made by timingsToGraphs.ipynb
* Pitest-Clustering-Plugin: Imported from [Basarat's work](https://github.com/Rbasarat/thesis-mutation-testing/), slightly tweaked. User guide below.
* Projects: Imported from [Basarat's work](https://github.com/Rbasarat/thesis-mutation-testing/). Used for chapter 4 and 5 in my thesis. Time analysis required raw projects and are therefore only saved locally.
* Tables: Tables fed to PowerBI, created by outputsToTables.py.
* Theis: Contains submitted thesis in .tex form with files necessary for compilation. Also contains thesis in .pdf form.
* Timings: Contains tables made for chapter 3, the time analysis. Files were written by cmtTimeAnalysis.ipynb
* cmtImprovement.ipynb: Code for chapter 4. Made to calculate the impact more rigorous pre-processing and center selection has on the precision of [CMT](https://github.com/Rbasarat/thesis-mutation-testing/)
* cpmt.ipynb: Code for chapter 5, implements Contextual Predictive Mutation Testing and calculates the precision of original and 3-projects training variant.
* cpmt3DClustering.ipynb: Variant of cpmt.ipynb which clusters 1D features using 3D clustering algorithms, reasoning discussed in chapter 5.
* cpmtClusterSelection.ipynb: Variant of cpmt.ipynb which replaces the sampleSelector() function with that of CMT(Center Selection variant).
* cpmtClusterSelection.ipynbWeighted: Not discussed in thesis. Variant of cpmtClusterSelection, but with changes to the pkScoreTransformer() function. In this version, the similarity of mutants is taken into account for pk-score calculations.
* nmt.ipynb: Only mentioned in thesis. Implements new algorithm: "Network Mutation Testing". More detailed explanation given inside file.
* outputsToTables: Used to create the tables in "Tables" folder. Not intended for public use, messy code. Does contain Central Limit Theorem/Mann-Whitney U test.
* timingsToGraphs.ipynb: Used to create the graphs for the time analysis seen in "Graphs" folder.

## Pitest-Clustering-Plugin user guide:
Original contained following features:

* Similarity: calculates the Levenshtein distance between each mutation and the original class it was based on.
* Characteristics: Gathers various characteristics of the mutation.
* Clustering: Reads a csv of mutation - cluster pairs from a certain folder, picks only 1 mutation of each cluster at random and executes all picked mutations.
* Report: Consists of two scripts, one which reports the final status of each mutant and the number of tests it has undergone and one which reports the number of clusters killed with the clustering plugin and the total amount of clusters.

We removed the Similarity feature, because in its current state, it is too time consuming to be useful. We also updated the pom.xml to use junit5, to use it with current-day projects.

Below is how to use each feature. Make sure to use `mvn install` inside pitest-clustering-plugin directory. The pom.xml of the project must contain the code given below the feature usage explanations for all features to work. If you have yet to compile a projects test, use "mvn test-compile ...". If you want verbose output, use -verbose flag. 

* Characteristics: "mvn -Drat.skip=true -Dfeatures=+characteristics org.pitest:pitest-maven:mutationCoverage"
* Clustering: "mvn -Drat.skip=true -Dfeatures=+cluster org.pitest:pitest-maven:mutationCoverage". Requires "cluster.csv" in "project folder"/target/pit-reports/clustering with cluster ID, mutant ID pairs. cmtTimeAnalysis.ipynb produces this.
* Report: ON BY DEFAULT, to remove: remove `<outputFormat>MUTANTKILLEDREPORT</outputFormat>` and `<outputFormat>CLUSTERINGREPORT</outputFormat>` from code below.

Inside `<project><build><pluginManagement><plugins>`:
```
        <plugin>
          <groupId>org.pitest</groupId>
          <artifactId>pitest-maven</artifactId>
          <version>1.9.8</version>
          <dependencies>
            <dependency>
              <groupId>org.pitest</groupId>
              <artifactId>pitest-junit5-plugin</artifactId>
              <version>LATEST</version>
            </dependency>
            <dependency>
              <groupId>com.niverhawk</groupId>
              <artifactId>pitest-clustering-plugin</artifactId>
              <version>1.0-SNAPSHOT</version>
            </dependency>
          </dependencies>
          <configuration>
            <outputFormats>
               <outputFormat>MUTANTKILLEDREPORT</outputFormat>
               <outputFormat>CLUSTERINGREPORT</outputFormat>
              <outputFormat>HTML</outputFormat>
              <outputFormat>XML</outputFormat>
              <outputFormat>CSV</outputFormat>
            </outputFormats>
            <exportLineCoverage>true</exportLineCoverage>
            <mutators>
              <mutator>ALL</mutator>
            </mutators>
            <threads>6</threads>
          </configuration>
        </plugin>
```
Inside `<project><dependencies>`:
```
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
```

[Pitest advanced guide](https://pitest.org/quickstart/advanced/)
