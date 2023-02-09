package com.niverhawk.plugin.report;

import com.niverhawk.plugin.PluginService;
import org.pitest.mutationtest.ClassMutationResults;
import org.pitest.mutationtest.MutationResult;
import org.pitest.mutationtest.MutationResultListener;

import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

public class ClusteringReportListener implements MutationResultListener {

    private final String outputFile;
    private final HashMap<String, Integer> mutants;
    private final PluginService service;
    int killed;
    int total;

    public ClusteringReportListener(String outputFile, HashMap<String, Integer> mutants, PluginService service) {
        this.outputFile = outputFile;
        this.mutants = mutants;
        this.service = service;
    }

    @Override
    public void runStart() {
        this.killed = 0;
        this.total = 0;
    }

    @Override
    public void handleMutationResult(ClassMutationResults classMutationResults) {

        for (MutationResult mutantResult : classMutationResults.getMutations()) {
            int weight = this.mutants.get(this.service.getMutantIdAsString(mutantResult.getDetails()));
            if (mutantResult.getStatus().isDetected()) {
                if (mutants.get(this.service.getMutantIdAsString(mutantResult.getDetails())) != null) {
                    killed += weight;
                }
            }
        }
        this.total += classMutationResults.getMutations().size();
    }

    @Override
    public void runEnd() {
        try {
            System.out.printf("Clusters killed: %d, Total Clusters: %d", this.killed, this.total);
            if (this.outputFile != null) {
                FileWriter writer = new FileWriter(this.outputFile, true);
                writer.append(String.format("Clusters killed: %d, Total Clusters: %d", this.killed, this.total));
                writer.append("\n");
                writer.flush();
                writer.close();
            } else {
                System.err.println("Could not read/create results file");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
