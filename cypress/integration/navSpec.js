describe('Desktop Nav Tests', () => {
    it('contains no broken desktop nav links', () => {
        cy.visit('/');
        cy.get('.navbar-nav li:first-child a').should('have.attr', 'href').and('include', '/');
        cy.get('.navbar-nav li:nth-child(2) a').should('have.attr', 'href').and('include', '/accounts/login/');
        cy.get('.navbar-nav li:nth-child(3) a').should('have.attr', 'href').and('include', '/accounts/signup/');
        cy.get('.navbar-nav li:nth-child(4) a').should('have.attr', 'href').and('include', '/help/');
    });

    it('returns relevant results upon using search function', () => {
        cy.visit('/');
        cy.get('#searchbar').type('burger', { force: true });
        cy.get('#desktop-search-button').click({ force: true });
        cy.url().should('contain', '/restaurants/?q=burger');
        cy.get('.card-title').first().invoke('html').should('eq', "McDoogle's®");
    });

});

describe('Mobile Nav Tests', () => {
    it('opens and closes mobile sidebar as expected', () => {
        cy.viewport(402, 828);
        cy.get('.navbar-toggler').click({ force: true });
        cy.get('#sidebar-nav').should('have.class', 'open-nav');
        cy.get('#sidebar-close').click({ force: true });
        cy.get('#sidebar-nav').should('have.class', 'close-nav');
    });

    it('contain no broken mobile nav links', () => {
        cy.viewport(402, 828);
        cy.get('.navbar-toggler').click({ force: true }).wait(500);
        cy.get('#sidebar-nav').find('li:first-child a').should('have.attr', 'href').and('include', '/');
        cy.get('#sidebar-nav').find('li:nth-child(2) a').should('have.attr', 'href').and('include', '/accounts/login/');
        cy.get('#sidebar-nav').find('li:nth-child(3) a').should('have.attr', 'href').and('include', '/accounts/signup/');
        cy.get('#sidebar-nav').find('li:nth-child(4) a').should('have.attr', 'href').and('include', '/help/');
    });

    it('displays the number of food items in the bag on mobile bag icon', () => {
        cy.viewport(402, 828);
        cy.visit('/restaurants/1/');
        cy.get('a.food-item-card-body').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.get('.fa-stack-1x').invoke('html').should('exist').then((numberOfBagItems) => {
            cy.wrap(numberOfBagItems).should('contain', '1');
        });
    });
});