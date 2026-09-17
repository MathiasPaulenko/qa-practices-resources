package steps;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;

public class Hooks {

    @Before
    public void setUp() {
        TestContext.reset();
    }

    @After
    public void tearDown() {
        TestContext.reset();
    }

    @Before("@auth")
    public void setUpAuth() {
        TestContext.loginAsTestUser();
    }

    @After
    public void captureScreenshotOnFailure(Scenario scenario) {
        if (scenario.isFailed()) {
            scenario.attach(
                ("Scenario failed: " + scenario.getName()).getBytes(),
                "text/plain",
                "failure-note.txt");
        }
    }
}
