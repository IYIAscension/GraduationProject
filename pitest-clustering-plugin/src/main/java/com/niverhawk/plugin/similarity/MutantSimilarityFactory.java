package com.niverhawk.plugin.similarity;

import org.pitest.mutationtest.build.InterceptorParameters;
import org.pitest.mutationtest.build.MutationInterceptor;
import org.pitest.mutationtest.build.MutationInterceptorFactory;
import org.pitest.plugin.Feature;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;

public class MutantSimilarityFactory implements MutationInterceptorFactory {
    @Override
    public MutationInterceptor createInterceptor(InterceptorParameters params) {

        FileSystem fileSystem = FileSystems.getDefault();
        String outFile = null;
        try {
            final String outDir = params.data().getReportDir();
            final Path classDir = fileSystem.getPath(outDir);
            Path clusterDir = classDir.resolve("clustering");
            Files.createDirectories(clusterDir);
            outFile = clusterDir.resolve("distance.csv").toAbsolutePath().toString();
            FileWriter csvWriter = new FileWriter(outFile, false);
            csvWriter.append("id");
            csvWriter.append(",");
            csvWriter.append("distance");
            csvWriter.append("\n");
            csvWriter.flush();
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        return new MutantSimilarityInterceptor(outFile);
    }

    @Override
    public Feature provides() {
        return Feature.named("SIMILARITY")
                .withDescription("Calculates mutants Leventshtein distance from original")
                .withOnByDefault(false);
    }

    @Override
    public String description() {
        return "Mutant similarity plugin";
    }
}

