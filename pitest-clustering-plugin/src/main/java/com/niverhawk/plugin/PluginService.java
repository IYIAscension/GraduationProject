package com.niverhawk.plugin;

import org.pitest.mutationtest.engine.MutationDetails;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;

public class PluginService {

    public String getMutantIdAsString(MutationDetails details) {
        return details.getId().toString().replaceAll(",", "");
    }

    public HashMap<String, Integer> parseClusteredMutants(String filePath) {

        HashMap<String, Integer> result = new HashMap<>();

        try {
            Scanner scanner = new Scanner(new File(filePath));
            // Skip first row.
            scanner.nextLine();
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] id = line.split(",");

                result.put(id[1], Integer.parseInt(id[2]));
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        return result;
    }
}

