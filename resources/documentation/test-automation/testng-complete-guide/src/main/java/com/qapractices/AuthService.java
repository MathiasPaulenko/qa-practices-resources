package com.qapractices;

public class AuthService {

    private static final String VALID_EMAIL = "user@testdata.io";
    private static final String VALID_PASSWORD = "validpass";

    public boolean login(String email, String password) {
        if (email == null || password == null || email.isEmpty() || password.isEmpty()) {
            return false;
        }
        return VALID_EMAIL.equals(email) && VALID_PASSWORD.equals(password);
    }
}
