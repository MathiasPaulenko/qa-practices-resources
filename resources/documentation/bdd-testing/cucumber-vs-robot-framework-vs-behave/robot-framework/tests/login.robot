*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://127.0.0.1:8080
${EMAIL}       qa@qapractices.com
${PASSWORD}    ValidPass!2026

*** Test Cases ***
Valid User Logs In And Reaches Dashboard
    Create Session    qapractices    ${BASE_URL}
    ${data}=    Create Dictionary    email=${EMAIL}    password=${PASSWORD}
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${auth}=    POST On Session
    ...    qapractices
    ...    /api/v1/auth/login
    ...    json=${data}
    ...    headers=${headers}
    ...    expected_status=200
    ${token}=    Get From Dictionary    ${auth.json()}    token
    Should Not Be Empty    ${token}
    ${auth_headers}=    Create Dictionary    Authorization=Bearer ${token}
    ${dash}=    GET On Session
    ...    qapractices
    ...    /api/v1/dashboard
    ...    headers=${auth_headers}
    ...    expected_status=200
    Should Contain    ${dash.text}    Welcome to QA Practices
    [Teardown]    Delete All Sessions
