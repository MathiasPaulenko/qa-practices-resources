package com.cartify.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;

/**
 * Payment page object for Cartify.
 * Handles the third-party payment iframe with FluentWait for variable load times.
 */
public class PaymentPage extends BasePage {
    private static final By PAYMENT_IFRAME = By.cssSelector("[data-testid='payment-iframe']");
    private static final By CARD_NUMBER = By.cssSelector("[data-testid='card-number']");
    private static final By CARD_EXPIRY = By.cssSelector("[data-testid='card-expiry']");
    private static final By CARD_CVV = By.cssSelector("[data-testid='card-cvv']");
    private static final By PAY_BUTTON = By.cssSelector("[data-testid='pay-button']");
    private static final By PAYMENT_SUCCESS = By.cssSelector("[data-testid='payment-success']");

    public PaymentPage(WebDriver driver) {
        super(driver);
    }

    public void switchToPaymentIframe() {
        wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(PAYMENT_IFRAME));
    }

    public void enterPaymentDetails(String cardNumber, String expiry, String cvv) {
        type(CARD_NUMBER, cardNumber);
        type(CARD_EXPIRY, expiry);
        type(CARD_CVV, cvv);
    }

    public void clickPay() {
        click(PAY_BUTTON);
    }

    public boolean isPaymentSuccessful() {
        driver.switchTo().defaultContent();
        return driver.findElements(PAYMENT_SUCCESS).size() > 0;
    }
}
