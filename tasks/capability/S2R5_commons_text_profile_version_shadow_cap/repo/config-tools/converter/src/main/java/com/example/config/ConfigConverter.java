package com.example.config;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.text.StringSubstitutor;

/**
 * Resolves {@code ${...}} interpolation tokens in tenant config files using
 * Commons Text's default interpolator, then writes the resolved config back out.
 *
 * <p>Config values arrive from tenants, so each value's tokens are passed through
 * {@link StringSubstitutor#createInterpolator()} — the default interpolator — as
 * they are.
 */
public final class ConfigConverter {

    private ConfigConverter() {
    }

    /** Resolve every value's {@code ${...}} tokens with the default interpolator. */
    public static List<String> convert(List<String> lines) {
        StringSubstitutor interpolator = StringSubstitutor.createInterpolator();
        List<String> out = new ArrayList<>(lines.size());
        for (String line : lines) {
            int eq = line.indexOf('=');
            if (line.isEmpty() || line.charAt(0) == '#' || eq < 0) {
                out.add(line);
                continue;
            }
            String key = line.substring(0, eq);
            String value = line.substring(eq + 1);
            out.add(key + "=" + interpolator.replace(value));
        }
        return out;
    }

    /** Read {@code in}, resolve tokens, and write the resolved config to {@code out}. */
    public static void convert(Path in, Path out) throws IOException {
        List<String> resolved = convert(Files.readAllLines(in, StandardCharsets.UTF_8));
        if (out.getParent() != null) {
            Files.createDirectories(out.getParent());
        }
        Files.write(out, resolved, StandardCharsets.UTF_8);
    }

    public static void main(String[] args) throws IOException {
        Path in = Paths.get(args.length > 0 ? args[0] : "config/tenant.properties");
        Path out = Paths.get(args.length > 1 ? args[1] : "target/resolved.properties");
        convert(in, out);
        System.out.println("resolved " + in + " -> " + out);
    }
}
