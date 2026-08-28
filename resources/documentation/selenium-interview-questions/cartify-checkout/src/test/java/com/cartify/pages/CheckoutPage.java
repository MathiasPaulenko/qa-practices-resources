package com.cartify.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Checkout page object for Cartify.
 * Handles shipping address form and order confirmation.
 */
public class CheckoutPage extends BasePage {
    private static final By FULL_NAME_FIELD = By.cssSelector("[data-testid='full-name']");
    private static final By ADDRESS_FIELD = By.cssSelector("[data-testid='address']");
    private static final By CITY_FIELD = By.cssSelector("[data-testid='city']");
    private static final By ZIP_FIELD = By.cssSelector("[data-testid='zip']");
    private static final By CONTINUE_BUTTON = By.cssSelector("[data-testid='continue-to-payment']");
    private static final By ORDER_CONFIRMATION = By.cssSelector("[data-testid='order-confirmation']");

    public CheckoutPage(WebDriver driver) {
        super(driver);
    }

    public void fillShippingAddress(String fullName, String address, String city, String zip) {
        type(FULL_NAME_FIELD, fullName);
        type(ADDRESS_FIELD, address);
        type(CITY_FIELD, city);
        type(ZIP_FIELD, zip);
        click(CONTINUE_BUTTON);
    }

    public boolean isOrderConfirmed() {
        return driver.findElements(ORDER_CONFIRMATION).size() > 0;
    }
}
