package com.niverhawk.plugin.clustering;

import com.niverhawk.plugin.PluginService;
import org.pitest.bytecode.analysis.ClassTree;
import org.pitest.mutationtest.build.InterceptorType;
import org.pitest.mutationtest.build.MutationInterceptor;
import org.pitest.mutationtest.engine.Mutater;
import org.pitest.mutationtest.engine.MutationDetails;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;


public class MutantClusteringInterceptor implements MutationInterceptor {

    private final HashMap<String, Integer> mutants;
    private final PluginService service;

    public MutantClusteringInterceptor(HashMap<String, Integer> mutants, PluginService service) {
        this.mutants = mutants;
        this.service = service;
    }

    @Override
    public InterceptorType type() {
        return InterceptorType.FILTER;
    }

    @Override
    public void begin(ClassTree clazz) {
        if (this.mutants.isEmpty()) {
            System.err.println("Error parsing mutants");
        }
    }

    @Override
    public Collection<MutationDetails> intercept(Collection<MutationDetails> mutations, Mutater m) {
        final List<MutationDetails> indexable = new ArrayList<>(mutations);

        for (int i = 0; i != indexable.size(); i++) {
            final MutationDetails md = indexable.get(i);
            String details = this.service.getMutantIdAsString(md);
            if (mutants.get(details) == null) {
                mutations.remove(md);
            }
        }
        return mutations;
    }

    @Override
    public void end() {
    }


}
