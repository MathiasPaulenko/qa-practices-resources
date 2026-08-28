package com.nexus.utils;

import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.TestExecutionExceptionHandler;

/**
 * Retry analyzer with exponential backoff for rate-limited endpoints.
 * Used with @Tag("flaky") on tests that hit third-party rate limits.
 */
public class RetryAnalyzer implements TestExecutionExceptionHandler {

    private static final int MAX_RETRIES = 3;
    private static final long INITIAL_DELAY_MS = 500;

    @Override
    public void handleTestExecutionException(ExtensionContext context, Throwable throwable) throws Throwable {
        int attempt = 1;
        long delay = INITIAL_DELAY_MS;

        while (attempt <= MAX_RETRIES) {
            System.out.println("Retry " + attempt + "/" + MAX_RETRIES + " for " + context.getDisplayName());
            Thread.sleep(delay);

            try {
                // Re-run the test method
                context.getTestMethod().ifPresent(method -> {
                    try {
                        method.invoke(context.getTestInstance().orElseThrow());
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                });
                return; // Success, don't rethrow
            } catch (Exception e) {
                delay *= 2; // Exponential backoff
                attempt++;
            }
        }

        throw throwable; // All retries exhausted
    }
}
