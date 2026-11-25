*** Settings ***
Resource    ../resources/common_keywords.robot
Test Template    Login Should Fail

*** Variables ***
${BASE_URL}   https://example.com    # Placeholder: replace with your app URL
${BROWSER}    Chrome

*** Test Cases ***
Invalid Email       invalid@email.com    validpass    Invalid credentials
Invalid Password    jane@example.com     wrongpass    Invalid credentials
Empty Email         ${EMPTY}             validpass    Email is required
Empty Password      jane@example.com     ${EMPTY}     Password is required

*** Keywords ***
Login Should Fail
    [Arguments]    ${email}    ${password}    ${expected_error}
    Navigate To Login Page
    Login To Application    ${email}    ${password}
    Verify Error Message    ${expected_error}
