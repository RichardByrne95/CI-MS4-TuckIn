describe('Home Page/Index Test', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/');
        cy.url().should('include', '/');
    });

    // Address Tests
    it('should disable find button when new user visits site', () => {
        cy.get('button.find-button').should('be.disabled');
    });

    it('should enable find button upon a valid address being entered or selected', () => {
        cy.get('input#address').type('22 Shelbourne Road', { force: true });
        cy.get('input#address').focus();
        cy.get('.pac-item').first().click();
        cy.get('button.find-button').should('not.be.disabled');
    });

    it('should disable find button if input is empty', () => {
        cy.get('input#address').clear({ force: true });
        cy.get('button.find-button').should('be.disabled', { force: true });
    });

    it('should return to homepage and display error if "Dublin" is not in address', () => {
        cy.get('input#address').clear({ force: true }).type('Cork', { force: true }).get('input#address').focus();
        cy.get('.pac-item').first().click();
        cy.wait(1000);
        cy.get('#address-finder').submit();
        cy.wait(1000);
        cy.url().should('equal', 'http://127.0.0.1:8000/');
        cy.get('.toast').should('have.class', 'show');
        cy.get('.toast-header').children('strong').should('contain', 'Error');
        cy.get('.toast-body').children().should('contain', 'Address not found within Dublin, please try again');
    });
});