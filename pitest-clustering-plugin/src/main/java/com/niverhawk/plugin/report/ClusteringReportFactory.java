package com.niverhawk.plugin.report;

import com.niverhawk.plugin.PluginService;
import org.pitest.mutationtest.ListenerArguments;
import org.pitest.mutationtest.MutationResultListener;
import org.pitest.mutationtest.MutationResultListenerFactory;

import java.io.IOException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Properties;

public class ClusteringReportFactory implements MutationResultListenerFactory {
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
            outFile = clusterDir.resolve("score.txt").toAbsolutePath().toString();
            String file = clusterDir.resolve("cluster.csv").toAbsolutePath().toString();
            mutants = service.parseClusteredMutants(file);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
        return new ClusteringReportListener(outFile, mutants, service);
    }

    @Override
    public String name() {
        return "CLUSTERINGREPORT";
    }

    @Override
    public String description() {
        return "Plugin for calculating weighed mutation score.";
    }

}
