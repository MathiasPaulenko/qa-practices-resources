package com.cartify.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Login page object for Cartify checkout.
 * Uses CSS [data-testid] selectors for stability.
 */
public class LoginPage extends BasePage {
    private static final By USERNAME_FIELD = By.cssSelector("[data-testid='username']");
    private static final By PASSWORD_FIELD = By.cssSelector("[data-testid='password']");
    private static final By LOGIN_BUTTON = By.cssSelector("[data-testid='login-button']");
    private static final By ERROR_MESSAGE = By.cssSelector("[data-testid='login-error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public void login(String username, String password) {
        type(USERNAME_FIELD, username);
        type(PASSWORD_FIELD, password);
        click(LOGIN_BUTTON);
    }

    public String getErrorMessage() {
        return waitForVisible(ERROR_MESSAGE).getText();
    }

    public boolean isLoginButtonDisplayed() {
        return driver.findElement(LOGIN_BUTTON).isDisplayed();
    }
}
