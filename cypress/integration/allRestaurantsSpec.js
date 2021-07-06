describe('All Restaurants Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/restaurants/');
        cy.url().should('include', '/restaurants');
    });

    // Cuisine Links
    it('successfully loads relevant url based on cuisine selected', () => {
        // Pizza
        cy.visit('/restaurants/');
        cy.get('i.fa-pizza-slice').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=pizza');
        // American
        cy.visit('/restaurants/');
        cy.get('i.fa-hamburger').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=american');
        // Indian
        cy.visit('/restaurants/');
        cy.get('i.fa-pepper-hot').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=indian');
        // Seafood
        cy.visit('/restaurants/');
        cy.get('i.fa-fish').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=seafood');
        // Vegetarian
        cy.visit('/restaurants/');
        cy.get('i.fa-egg').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=vegetarian');
        // Vegan
        cy.visit('/restaurants/');
        cy.get('i.fa-carrot').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=vegan');
        // Chicken
        cy.visit('/restaurants/');
        cy.get('i.fa-drumstick-bite').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=chicken');
        // Treats
        cy.visit('/restaurants/');
        cy.get('i.fa-cookie').click({ force: true });
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=treats');
    });
});