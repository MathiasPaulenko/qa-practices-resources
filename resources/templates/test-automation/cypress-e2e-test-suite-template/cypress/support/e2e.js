import './commands';
import '@cypress/grep/support';
import 'cypress-mochawesome-reporter/register';

// Do NOT call cy.clearCookies() or cy.clearLocalStorage() here —
// a global beforeEach that wipes storage makes cy.session useless,
// because the cached session gets thrown away before every test.
