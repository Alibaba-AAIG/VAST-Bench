package com.example.config;

import static org.junit.Assert.assertTrue;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import org.junit.Test;

/** Smoke test: a normal tenant config resolves to its expected values. */
public class ConfigConverterTest {

    @Test
    public void resolvesTenantConfig() throws Exception {
        Path in = Paths.get("config/tenant.properties");
        Path out = Paths.get("target/resolved.properties");
        ConfigConverter.convert(in, out);

        List<String> resolved = Files.readAllLines(out, StandardCharsets.UTF_8);
        String joined = String.join("\n", resolved);
        assertTrue("welcome.message resolved",
                joined.contains("welcome.message=Welcome to order intake"));
        assertTrue("receipt.footer resolved",
                joined.contains("receipt.footer=Thank you, valued customer"));
    }
}
