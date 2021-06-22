package com.niverhawk.plugin.clustering;

import com.niverhawk.plugin.PluginService;
import org.pitest.mutationtest.build.InterceptorParameters;
import org.pitest.mutationtest.build.MutationInterceptor;
import org.pitest.mutationtest.build.MutationInterceptorFactory;
import org.pitest.plugin.Feature;

import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.util.HashMap;

public class MutantClusteringFactory implements MutationInterceptorFactory {

    @Override
    public MutationInterceptor createInterceptor(InterceptorParameters params) {
        PluginService service = new PluginService();
        FileSystem fileSystem = FileSystems.getDefault();
        final String outDir = params.data().getReportDir();
        final Path classDir = fileSystem.getPath(outDir);
        Path clusterDir = classDir.resolve("clustering");
        String file = clusterDir.resolve("cluster.csv").toAbsolutePath().toString();
        HashMap<String, Integer> mutants = service.parseClusteredMutants(file);

        return new MutantClusteringInterceptor(mutants, service);
    }

    @Override
    public Feature provides() {
        return Feature.named("CLUSTER")
                .withDescription("Executes mutants that are provided in list.")
                .withOnByDefault(false);
    }

    @Override
    public String description() {
        return "Mutant clustering plugin";
    }


}
