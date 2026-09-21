package com.qapractices;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Same login scenario reported with ExtentReports 5.1.2 + JUnit 5.
 *
 * Run: mvn test
 * Output: build/reports/extent-report.html (single self-contained file)
 */
class ExtentUserTest {

    private static ExtentReports extent;

    @BeforeAll
    static void setupReport() {
        extent = new ExtentReports();
        ExtentSparkReporter spark = new ExtentSparkReporter("build/reports/extent-report.html");
        spark.config().setDocumentTitle("Login Regression");
        spark.config().setReportName("User Authentication Suite");
        extent.attachReporter(spark);
        extent.setSystemInfo("Environment", "staging");
        extent.setSystemInfo("JDK", System.getProperty("java.version"));
    }

    @Test
    void userLogsInWithValidCredentials() {
        ExtentTest test = extent.createTest("User logs in with valid credentials");
        FakeLoginPage page = new FakeLoginPage();

        test.info("Enter valid credentials");
        page.enterCredentials("demo", "s3cret"); // Placeholder: use a test account

        test.info("Submit the form");
        page.submit();

        assertTrue(page.dashboardVisible());
        test.pass("Dashboard rendered for user=demo");
    }

    @Test
    void loginFailsWithLockedAccount() {
        ExtentTest test = extent.createTest("Login fails with a locked account");
        FakeLoginPage page = new FakeLoginPage();

        test.info("Enter credentials for a locked account");
        page.enterCredentials("locked-user", "s3cret");

        test.info("Submit the form");
        page.submit();

        assertFalse(page.dashboardVisible());
        test.pass("Dashboard correctly hidden for locked account");
    }

    @AfterAll
    static void flushReport() {
        extent.flush();
    }

    /** Placeholder page object — replace with your real page or API client. */
    static class FakeLoginPage {
        private String user;
        private boolean submitted;

        void enterCredentials(String user, String password) {
            this.user = user;
        }

        void submit() {
            this.submitted = true;
        }

        boolean dashboardVisible() {
            return submitted && "demo".equals(user);
        }
    }
}
