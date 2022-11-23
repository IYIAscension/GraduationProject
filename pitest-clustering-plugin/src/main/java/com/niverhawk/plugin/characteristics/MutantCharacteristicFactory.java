package com.niverhawk.plugin.characteristics;

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

public class MutantCharacteristicFactory implements MutationInterceptorFactory {

    @Override
    public MutationInterceptor createInterceptor(InterceptorParameters params) {

        FileSystem fileSystem = FileSystems.getDefault();
        String outFile = null;
        // TODO: set headers for csv.
        try {
            final String outDir = params.data().getReportDir();
            final Path classDir = fileSystem.getPath(outDir);
            Path clusterDir = classDir.resolve("clustering");
            Files.createDirectories(clusterDir);
            outFile = clusterDir.resolve("characteristics.csv").toAbsolutePath().toString();
            FileWriter csvWriter = new FileWriter(outFile, false);
            String header = "id,mutOperator,opcode,returnType,localVarsCount,isInTryCatch,isInFinalBlock,className,methodName,blockNumber,lineNumber,numTests\n";
            csvWriter.append(header);
            csvWriter.flush();
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        return new MutantCharacteristicInterceptor(outFile);
    }

    @Override
    public Feature provides() {
        return Feature.named("CHARACTERISTICS")
                .withDescription("Gathers characteristics from mutants and writes them to file.")
                .withOnByDefault(false);
    }

    @Override
    public String description() {
        return "Mutant similarity plugin";
    }


}
