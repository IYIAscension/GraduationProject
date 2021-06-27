package com.niverhawk.plugin.report;

import com.niverhawk.plugin.PluginService;
import org.pitest.mutationtest.ListenerArguments;
import org.pitest.mutationtest.MutationResultListener;
import org.pitest.mutationtest.MutationResultListenerFactory;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Properties;

public class MutantKilledReportFactory implements MutationResultListenerFactory {
    @Override
    public MutationResultListener getListener(Properties properties, ListenerArguments listenerArguments) {
        PluginService service = new PluginService();
        FileSystem fileSystem = FileSystems.getDefault();
        String outFile = null;
        HashMap<String, Integer> mutants = new HashMap<>();
        try {
            final String outDir = listenerArguments.data().getReportDir();
            final Path classDir = fileSystem.getPath(outDir);
            Path clusterDir = classDir.resolve("clustering");
            Files.createDirectories(clusterDir);
            outFile = clusterDir.resolve("killed.csv").toAbsolutePath().toString();
            FileWriter csvWriter = new FileWriter(outFile, false);
            csvWriter.append("id,killed,numTests\n");
            csvWriter.flush();
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
        return new MutantKilledReportListener(outFile);
    }

    @Override
    public String name() {
        return "MUTANTKILLEDREPORT";
    }

    @Override
    public String description() {
        return "Plugin for extracting results of mutants.";
    }

}
