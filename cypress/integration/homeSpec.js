describe('Home Page/Index Test', () => {

    it('successfully loads', () => {
        cy.visit('/');
        cy.url().should('include', '/');
    });

    it('should disable find button when no address has been inputted', () => {
        cy.get('button.find-button').should('be.disabled');
        
    });
})