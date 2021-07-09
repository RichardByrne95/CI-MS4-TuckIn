describe('Footer Links Tests', () => {
    // Footer
    it('contains no broken footer links', () => {
        cy.visit('/');
        cy.get('#list-your-restaurant-link').should('have.attr', 'href').and('contain', 'links/list_your_restaurant');
        cy.get('#instagram-link').should('have.attr', 'href').and('contain', 'https://www.instagram.com');
        cy.get('#facebook-link').should('have.attr', 'href').and('contain', 'https://www.facebook.com');
        cy.get('#twitter-link').should('have.attr', 'href').and('contain', 'https://twitter.com');
        cy.get('#cookies-policy-link').should('have.attr', 'href').and('contain', '/links/cookies_policy/');
        cy.get('#privacy-policy-link').should('have.attr', 'href').and('contain', '/links/privacy_policy/');
    });
});

describe('Help Tests', () => {
    // Help
    it('successfully loads', () => {
        cy.visit('/links/help/');
        cy.url().should('equal', 'http://127.0.0.1:8000/links/help/');
    });

    it('contains valid hyperlink to email the business', () => {
        cy.visit('/links/help/');
        cy.get('#help-email-link').should('have.attr', 'href').and('contain', 'mailto:help@tuckin.ie');
    });

});

describe('List Your Restaurant Tests', () => {
    // List Your Restaurant
    it('successfully loads', () => {
        cy.visit('/links/list_your_restaurant/');
        cy.url().should('equal', 'http://127.0.0.1:8000/links/list_your_restaurant/');
    });
    
    it('correctly submits valid form and displays confirmation message', () => {
        
    });

});

describe('Policies Tests', () => {
    // Policies
    it('successfully loads', () => {
        cy.visit('/links/cookies_policy/');
        cy.url().should('equal', 'http://127.0.0.1:8000/links/cookies_policy/');
        cy.visit('/links/privacy_policy/');
        cy.url().should('equal', 'http://127.0.0.1:8000/links/privacy_policy/');
    });
});