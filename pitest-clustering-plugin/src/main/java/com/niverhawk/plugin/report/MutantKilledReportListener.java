package com.niverhawk.plugin.report;

import com.niverhawk.plugin.PluginService;
import org.pitest.mutationtest.ClassMutationResults;
import org.pitest.mutationtest.MutationResult;
import org.pitest.mutationtest.MutationResultListener;

import java.io.FileWriter;
import java.io.IOException;

public class MutantKilledReportListener implements MutationResultListener {

    private final String outputFile;
    private PluginService pluginService;


    public MutantKilledReportListener(String outputFile) {
        this.outputFile = outputFile;
        this.pluginService = new PluginService();
    }

    @Override
    public void runStart() {
    }

    @Override
    public void handleMutationResult(ClassMutationResults classMutationResults) {

        try {
            for (MutationResult mutantResult : classMutationResults.getMutations()) {
                if (this.outputFile != null) {
                    FileWriter writer = new FileWriter(this.outputFile, true);
                    String id = pluginService.getMutantIdAsString(mutantResult.getDetails());
                    String record = String.format("%s,%d,%d\n",
                            id,
                            mutantResult.getStatus().isDetected() ? 0: 1,
                            mutantResult.getDetails().getTestsInOrder().size());
                    writer.append(record);
                    writer.flush();
                    writer.close();
                } else {
                    System.err.println("Could not read/create results file");
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void runEnd() {

    }
}
