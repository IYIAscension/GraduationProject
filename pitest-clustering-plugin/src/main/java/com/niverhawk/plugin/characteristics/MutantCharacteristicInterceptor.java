package com.niverhawk.plugin.characteristics;

import com.niverhawk.plugin.Feature;
import org.objectweb.asm.tree.AbstractInsnNode;
import org.pitest.bytecode.analysis.ClassTree;
import org.pitest.bytecode.analysis.MethodTree;
import org.pitest.mutationtest.build.InterceptorType;
import org.pitest.mutationtest.build.MutationInterceptor;
import org.pitest.mutationtest.engine.Mutater;
import org.pitest.mutationtest.engine.MutationDetails;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;


public class MutantCharacteristicInterceptor implements MutationInterceptor {

    private ClassTree classTree;
    FileWriter csvWriter;
    private final String outFilePath;

    public MutantCharacteristicInterceptor(String outFilePath) {
        this.outFilePath = outFilePath;
    }

    @Override
    public InterceptorType type() {
        return InterceptorType.REPORT;
    }

    @Override
    public void begin(ClassTree classTree) {
        this.classTree = classTree;
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
    public Collection<MutationDetails> intercept(Collection<MutationDetails> collection, Mutater mutater) {
        try {
            for (MutationDetails details : collection) {
                int opcode = 0;
                String returnType = "none";
                int localVars = 0;
                int tryCatchBlocks = 0;
                // Find method of this mutant
                for (MethodTree methodTree : classTree.methods()) {
                    if (methodTree.asLocation().equals(details.getId().getLocation())) {
                        AbstractInsnNode instruction = methodTree.instruction(details.getInstructionIndex());

                        // Determine return type
                        String signature = methodTree.rawNode().signature;
                        if (signature != null) {
                            int i = signature.lastIndexOf(")") + 1;
                            returnType = (signature.substring(i, i + 1));
                        }
                        localVars = methodTree.rawNode().localVariables.size();
                        opcode = instruction.getOpcode();
                        tryCatchBlocks = methodTree.rawNode().tryCatchBlocks.size();
                    }
                }
                Feature record = new Feature(details, opcode, returnType, localVars, tryCatchBlocks);

                csvWriter.append(buildCsvRecord(record));
                csvWriter.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return collection;
    }

    @Override
    public void end() {
        try {
            csvWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private String buildCsvRecord(Feature feature) {

        return String.format("%s,%s,%d,%s,%d,%d,%d,%s,%s,%d,%d\n",
                feature.id,
                feature.mutOperator,
                feature.opcode,
                feature.returnType,
                feature.localVarsCount,
                feature.isInTryCatch > 0 ? 0 : 1,
                feature.isInFinalBlock ? 0 : 1,
                feature.className,
                feature.methodName,
                feature.blockNumber,
                feature.lineNumber
        );
    }
}
