package com.cartify.utils;

import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Retry analyzer for flaky tests.
 * Max 2 retries per test. Logs each retry attempt.
 */
public class RetryAnalyzer implements IRetryAnalyzer {
    private static final Logger logger = LogManager.getLogger(RetryAnalyzer.class);
    private static final int MAX_RETRY_COUNT = 2;
    private int retryCount = 0;

    @Override
    public boolean retry(ITestResult result) {
        if (retryCount < MAX_RETRY_COUNT) {
            retryCount++;
            logger.warn("Retrying test {} (attempt {}/{})", result.getName(), retryCount, MAX_RETRY_COUNT);
            return true;
        }
        return false;
    }
}
