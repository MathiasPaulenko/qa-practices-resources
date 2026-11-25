*** Settings ***
Library    ../libraries/CustomLibrary.py

*** Test Cases ***
Validate API Response
    ${status}    Get API Response    https://api.example.com/health    # Placeholder: replace with your API URL
    Should Be Equal As Integers    ${status}    200

Validate API Data
    ${response}    Post API Data    https://api.example.com/users    {"name": "Jane"}
    Validate JSON Field    ${response}    name    Jane
