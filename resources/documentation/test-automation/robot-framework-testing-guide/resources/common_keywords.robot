*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${BASE_URL}/login    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains Element    id=email    timeout=10s

Close Application
    Close Browser

Take Screenshot On Failure
    Capture Page Screenshot    ${OUTPUTDIR}/screenshots/${TEST_NAME}.png

Navigate To Login Page
    Go To    ${BASE_URL}/login
    Wait Until Page Contains Element    id=email    timeout=10s

Login To Application
    [Arguments]    ${email}    ${password}
    Input Text    id=email    ${email}
    Input Text    id=password    ${password}
    Click Button    id=login-button

Verify User Is Logged In
    [Arguments]    ${expected_name}
    Wait Until Page Contains    Welcome, ${expected_name}    timeout=10s
    Page Should Contain    Dashboard

Verify Error Message
    [Arguments]    ${expected_error}
    Wait Until Page Contains    ${expected_error}    timeout=10s
    Page Should Contain    ${expected_error}
