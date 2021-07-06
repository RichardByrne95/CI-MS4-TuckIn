describe('All Restaurants Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/restaurants/');
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/');
    });

    it('brings the user back to the homepage when change/set location link is clicked', () => {
        cy.get('.change-location > a').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/');
    });

    // Sorting
    it('sorts restaurants correctly by chosen key', () => {
        // Highest Rated - Desktop
        cy.visit('/restaurants/');
        cy.get('.desktop-sort-button').click({ force: true });
        cy.get('#highest-rated-desktop').click({ force: true });
        cy.url().should('include', '?sort=rating_high');
        // Delivery Cost - Desktop
        cy.get('.desktop-sort-button').click({ force: true });
        cy.get('#delivery-cost-desktop').click({ force: true });
        cy.url().should('include', '?sort=delivery_cost');
        // Highest Rated - Mobile
        cy.viewport('iphone-x');
        cy.get('.mobile-sort-button').click({ force: true });
        cy.get('#highest-rated-mobile').click({ force: true });
        cy.url().should('include', '?sort=rating_high');
        // Delivery Cost - Mobile
        cy.get('.mobile-sort-button').click({ force: true });
        cy.get('#delivery-cost-mobile').click({ force: true });
        cy.url().should('include', '?sort=delivery_cost');
        cy.viewport(1000, 660);
    });

    // Cuisine Links
    it('successfully loads relevant url based on cuisine selected', () => {
        // All
        cy.visit('/restaurants/');
        cy.get('.restaurant-cuisine > a[href="/restaurants/"]').click({ force: true });
        cy.url().should('include', 'restaurants').should('equal', 'http://127.0.0.1:8000/restaurants/');
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