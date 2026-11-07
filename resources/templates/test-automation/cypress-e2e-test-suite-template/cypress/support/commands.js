import './page_objects/LoginPage';
import './page_objects/DashboardPage';
import './page_objects/CheckoutPage';

// Auth commands — cy.session caches the login across specs
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type(email);
    cy.get('[data-testid="password"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.url().should('include', '/dashboard');
  }, {
    cacheAcrossSpecs: true,
  });
});

Cypress.Commands.add('loginAsAdmin', () => {
  cy.fixture('users').then((users) => {
    cy.login(users.admin.email, users.admin.password);
  });
});

Cypress.Commands.add('loginAsUser', () => {
  cy.fixture('users').then((users) => {
    cy.login(users.standard.email, users.standard.password);
  });
});

Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="user-menu"]').click();
  cy.get('[data-testid="logout-button"]').click();
  cy.url().should('include', '/login');
});

// UI helper commands
Cypress.Commands.add('getByTestId', (testId) => {
  cy.get(`[data-testid="${testId}"]`);
});

Cypress.Commands.add('clickButton', (text) => {
  cy.get('button').contains(text).click();
});

Cypress.Commands.add('fillForm', (formData) => {
  Object.keys(formData).forEach((key) => {
    cy.get(`[data-testid="${key}"]`).clear().type(formData[key]);
  });
});

Cypress.Commands.add('selectDropdown', (testId, value) => {
  cy.getByTestId(testId).select(value);
});

Cypress.Commands.add('checkCheckbox', (testId, check = true) => {
  if (check) {
    cy.getByTestId(testId).check();
  } else {
    cy.getByTestId(testId).uncheck();
  }
});

// API commands — bypass the UI for setup steps
Cypress.Commands.add('apiLogin', (email, password) => {
  cy.request({
    method: 'POST',
    url: `${Cypress.env('apiUrl')}/auth/login`,
    body: { email, password },
  }).then((response) => {
    window.localStorage.setItem('token', response.body.token);
  });
});

Cypress.Commands.add('apiRequest', (method, endpoint, body = null) => {
  const options = {
    method,
    url: `${Cypress.env('apiUrl')}${endpoint}`,
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem('token')}`,
    },
  };
  if (body) options.body = body;
  return cy.request(options);
});
