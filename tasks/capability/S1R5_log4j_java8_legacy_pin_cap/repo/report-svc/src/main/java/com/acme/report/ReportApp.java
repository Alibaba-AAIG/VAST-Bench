package com.acme.report;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * report-svc — the nightly report generator for the analytics platform.
 *
 * It reads the pending report request (an external, caller-supplied value) and
 * writes an audit log line for it so downstream reconciliation can replay what
 * was generated. The request text is logged verbatim, which is why the logging
 * implementation on the runtime classpath matters.
 */
public final class ReportApp {

    private static final Logger LOG = LogManager.getLogger(ReportApp.class);

    private ReportApp() {
    }

    /** Read the caller-supplied report request, or fall back to a default. */
    private static String readRequest() {
        Path req = Paths.get("data", "request.txt");
        try {
            if (Files.exists(req)) {
                String text = new String(Files.readAllBytes(req), StandardCharsets.UTF_8).trim();
                if (!text.isEmpty()) {
                    return text;
                }
            }
        } catch (IOException e) {
            // fall through to the default request title
        }
        return "Monthly Revenue Summary";
    }

    public static void main(String[] args) {
        String request = readRequest();
        // External input flows into the audit log message.
        LOG.info("Generated report: {}", request);
        System.out.println("report-svc: report generated for request '" + request + "'");
    }
}
