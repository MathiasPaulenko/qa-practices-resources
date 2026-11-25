*** Settings ***
Library    SeleniumLibrary
Resource    ../resources/common_keywords.robot
Test Setup    Open Browser    ${URL}    Chrome
Test Teardown    Close Browser

*** Variables ***
${URL}        https://example.com/login    # Placeholder: replace with your app URL
${BASE_URL}   https://example.com
${BROWSER}    Chrome
${EMAIL}      jane@example.com
${PASSWORD}   validpass123

*** Test Cases ***
Login With Valid Credentials
    Input Text    id=email    ${EMAIL}
    Input Text    id=password    ${PASSWORD}
    Click Button    id=login-button
    Wait Until Page Contains    Welcome    timeout=10s
    Page Should Contain    Dashboard

Login With Invalid Credentials
    Input Text    id=email    ${EMAIL}
    Input Text    id=password    wrongpass
    Click Button    id=login-button
    Wait Until Page Contains    Invalid credentials    timeout=10s
    Page Should Contain    Invalid credentials

Login Successfully With User Keywords
    Navigate To Login Page
    Login To Application    jane@example.com    validpass123
    Verify User Is Logged In    Jane
