package com.niverhawk.plugin.similarity;

import org.apache.commons.text.similarity.LevenshteinDistance;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceClassVisitor;
import org.pitest.bytecode.analysis.ClassTree;
import org.pitest.mutationtest.build.InterceptorType;
import org.pitest.mutationtest.build.MutationInterceptor;
import org.pitest.mutationtest.engine.Mutant;
import org.pitest.mutationtest.engine.Mutater;
import org.pitest.mutationtest.engine.MutationDetails;

import java.io.CharArrayWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class MutantSimilarityInterceptor implements MutationInterceptor {

    private String OriginalClassBytesAsString;
    FileWriter csvWriter;
    private final String outFilePath;

    public MutantSimilarityInterceptor(String outFilePath) {
        this.outFilePath = outFilePath;
    }

    @Override
    public InterceptorType type() {
        return InterceptorType.REPORT ;
    }

    @Override
    public void begin(ClassTree clazz) {
        this.OriginalClassBytesAsString = clazz.toString();
        try {
            if (outFilePath != null) {
                csvWriter = new FileWriter(this.outFilePath, true);
            } else {
                System.err.println("Could not read/create CSV file");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Collection<MutationDetails> intercept(Collection<MutationDetails> mutations, Mutater m) {
        final List<MutationDetails> indexable = new ArrayList<>(mutations);

        try {
            for (int i = 0; i != indexable.size(); i++) {
                final MutationDetails md = indexable.get(i);
                final Mutant mutant = m.getMutation(md.getId());

                long startTime = System.currentTimeMillis();
                final String methodName = getMethodNameInByteCode(md);

                // Werid edgecase which affects bytecode
                if (md.getMutator().contains("org.pitest.mutationtest.engine.gregor.mutators.rv.CRCR4Mutator") ||
                        md.getMutator().contains("org.pitest.mutationtest.engine.gregor.mutators.experimental.RemoveSwitchMutator")) {
                    String originalMethod = sanitizeByteCode(this.OriginalClassBytesAsString, md.getMutator());
                    String mutantMethod = getByteCodeAsString(mutant.getBytes());
                    int distance = calculateLevenshteinDistance(originalMethod, mutantMethod);
                    csvWriter.append(buildCsvRecord(distance, md));
                    csvWriter.flush();
                    continue;
                }

                // Remove frame stuff from original class.
                String originalMethod = sanitizeByteCode(getMethodInByteCode(this.OriginalClassBytesAsString, methodName), md.getMutator());
                String mutantMethod = getMethodInByteCode(getByteCodeAsString(mutant.getBytes()), methodName);

                if (originalMethod.equals("") || mutantMethod.equals("")) {
                    System.err.println("Error could not find method");
                }
                // Panick! frames should not be in the mutated bytecode.
                if (mutantMethod.contains("FRAME")) {
                    System.err.println("Found one");
                }

                int distance = calculateLevenshteinDistance(originalMethod, mutantMethod);
                csvWriter.append(buildCsvRecord(distance, md));

                // This should not happen
                if (distance == 0) {
                    System.err.println("ERROR: distance is 0");
                }

                csvWriter.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        mutations.clear();
        return mutations;
    }

    @Override
    public void end() {
        try {
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String getByteCodeAsString(final byte[] source) {
        final ClassReader reader = new ClassReader(source);
        final CharArrayWriter buffer = new CharArrayWriter();
        reader.accept(new TraceClassVisitor(null, new Textifier(), new PrintWriter(
                buffer)), ClassReader.SKIP_FRAMES);
        return buffer.toString();

    }

    private Integer calculateLevenshteinDistance(String originalMethod, String mutantMethod) {
        if (originalMethod.equals("") || mutantMethod.equals("")) return 0;
        LevenshteinDistance distance = new LevenshteinDistance();
        return distance.apply(originalMethod, mutantMethod);
    }

    private String getMethodNameInByteCode(MutationDetails mutantDetails) {
        return mutantDetails.getId().getLocation().getMethodName().name() + mutantDetails.getId().getLocation().getMethodDesc();
    }

    private String getMethodInByteCode(String clazz, String methodName) {
        StringBuilder buf = new StringBuilder(clazz);
        int start = buf.indexOf(" " + methodName);
        int end = buf.indexOf("\n\n", start);
        if (end == -1) end = clazz.length();
        if (start != -1) {
            return buf.substring(start, end);
        }
        return "";
    }

    private String sanitizeByteCode(String originalMethod, String mutator) {
        String[] orignalLines = originalMethod.split("\n");
        ArrayList<String> sanitizedLines = new ArrayList<>();
        for (String orignalLine : orignalLines) {
            if (!orignalLine.contains("FRAME ")) sanitizedLines.add(orignalLine);
        }

        return String.join("\n", sanitizedLines);
    }

    private String buildCsvRecord(int distance, MutationDetails mutant) {
        StringBuilder sb = new StringBuilder();
        sb.append(mutant.getId().toString().replaceAll(",", ""));
        sb.append(",");
        sb.append(distance);
        sb.append("\n");
        return sb.toString();
    }


}
