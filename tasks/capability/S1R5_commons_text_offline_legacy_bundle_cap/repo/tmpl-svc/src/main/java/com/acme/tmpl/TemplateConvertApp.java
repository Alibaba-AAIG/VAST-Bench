package com.acme.tmpl;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.text.StringSubstitutor;

/**
 * tmpl-svc — the tenant-config template renderer for the analytics platform.
 *
 * It reads a tenant configuration template (external, tenant-supplied text) and
 * resolves its ${...} placeholders with the library's default interpolator, then
 * writes the rendered configuration out. Because tenant-supplied text flows
 * straight into the default interpolator, the commons-text implementation on the
 * delivery classpath is what governs how those placeholders are resolved.
 */
public final class TemplateConvertApp {

    private TemplateConvertApp() {
    }

    /** Read the tenant-supplied config template, or fall back to a default. */
    private static String readTemplate() {
        Path tpl = Paths.get("data", "tenant-config.txt");
        try {
            if (Files.exists(tpl)) {
                String text = new String(Files.readAllBytes(tpl), StandardCharsets.UTF_8);
                if (StringUtils.isNotBlank(text)) {
                    return text;
                }
            }
        } catch (IOException e) {
            // fall through to the default template
        }
        return "service.banner=Welcome ${sys:tenant.name}";
    }

    public static void main(String[] args) throws IOException {
        String template = readTemplate();
        // Tenant-supplied template flows into the default interpolator.
        StringSubstitutor interpolator = StringSubstitutor.createInterpolator();
        String rendered = interpolator.replace(template);

        Path out = Paths.get("out");
        Files.createDirectories(out);
        Files.write(out.resolve("conversion.log"),
                ("Converted config:\n" + rendered + "\n").getBytes(StandardCharsets.UTF_8));

        System.out.println("tmpl-svc: rendered tenant configuration ->");
        for (String line : rendered.split("\n", -1)) {
            if (!line.isEmpty()) {
                System.out.println("  " + line);
            }
        }
    }
}
