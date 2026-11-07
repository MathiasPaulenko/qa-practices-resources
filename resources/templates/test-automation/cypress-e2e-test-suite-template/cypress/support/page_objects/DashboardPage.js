class DashboardPage {
  visit() {
    cy.visit('/dashboard');
    return this;
  }

  getWelcomeText() {
    return cy.getByTestId('welcome-text');
  }

  navigateTo(section) {
    cy.getByTestId(`nav-${section}`).click();
    return this;
  }

  getNotificationCount() {
    return cy.getByTestId('notification-badge');
  }

  search(query) {
    cy.getByTestId('global-search').clear().type(`${query}{enter}`);
    return this;
  }

  openUserMenu() {
    cy.getByTestId('user-menu').click();
    return this;
  }

  logout() {
    this.openUserMenu();
    cy.getByTestId('logout-button').click();
    return this;
  }

  isLoaded() {
    cy.getByTestId('welcome-text').should('be.visible');
    return this;
  }
}

export default DashboardPage;
