package com.cartify.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * Cart page object for Cartify checkout.
 */
public class CartPage extends BasePage {
    private static final By CART_ITEMS = By.cssSelector("[data-testid='cart-item']");
    private static final By CHECKOUT_BUTTON = By.cssSelector("[data-testid='checkout-button']");
    private static final By EMPTY_CART_MESSAGE = By.cssSelector("[data-testid='empty-cart']");

    public CartPage(WebDriver driver) {
        super(driver);
    }

    public int getCartItemCount() {
        return driver.findElements(CART_ITEMS).size();
    }

    public void proceedToCheckout() {
        click(CHECKOUT_BUTTON);
    }

    public boolean isEmpty() {
        return driver.findElements(EMPTY_CART_MESSAGE).size() > 0;
    }
}
