package com.niverhawk.plugin;

import org.pitest.mutationtest.engine.MutationDetails;

public class Feature {

    public String id;
    public String mutOperator;
    public int opcode;
    public int lineNumber;
    public int blockNumber;
    public int metInstrIdx;
    public int numTests;
    public String returnType;
    public int localVarsCount;
    public int isInTryCatch;
    public boolean isInFinalBlock;
    public String className;
    public String methodName;


    public Feature(MutationDetails details, int opcode, String returnType, int localVarsCount, int tryCatchBlocks) {
        // get mutator name
        String mutator = details.getMutator();
        String mutOperator = (mutator.substring(mutator.lastIndexOf(".") + 1));

        this.id = details.getId().toString().replaceAll(",", "");
        this.mutOperator = mutOperator;
        this.opcode = opcode;
        this.metInstrIdx = details.getFirstIndex();
        this.numTests = details.getTestsInOrder().size();
        this.returnType = returnType;
        this.localVarsCount = localVarsCount;
        this.isInTryCatch = tryCatchBlocks;
        this.isInFinalBlock = details.isInFinallyBlock();
        this.className = details.getClassName().asJavaName();
        this.methodName = details.getMethod().name();
        this.blockNumber = details.getBlock();
        this.lineNumber = details.getClassLine().getLineNumber();

    }


}
