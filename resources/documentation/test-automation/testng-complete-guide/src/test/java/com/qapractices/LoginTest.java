package com.qapractices;

import org.testng.annotations.DataProvider;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import org.testng.Assert;

public class LoginTest {
    private AuthService authService;

    @BeforeClass(alwaysRun = true)
    public void setUp() {
        authService = new AuthService();
    }

    @DataProvider(name = "loginData")
    public Object[][] getLoginData() {
        return new Object[][] {
            {"user@testdata.io", "validpass", true},
            {"user@testdata.io", "wrongpass", false},
            {"invalid@testdata.io", "pass123", false},
            {"", "pass123", false},
            {"user@testdata.io", "", false},
        };
    }

    @Test(groups = {"regression"}, dataProvider = "loginData")
    public void testLogin(String email, String password, boolean expectedSuccess) {
        boolean result = authService.login(email, password);
        Assert.assertEquals(result, expectedSuccess,
            String.format("Login with email=%s should return %s", email, expectedSuccess));
    }
}
