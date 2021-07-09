describe('Restaurant Menu Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/restaurants/1/');
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/1/');
    });

    // Add to Cart Tests
    it('shows and hides add to cart modal based on user interaction', () => {
        // Show
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#food-item-modal').should('have.class', 'show').and('have.css', 'display', 'block');
        // Hide - x
        cy.get('button.btn-close').wait(300).click({ force: true });
        cy.get('#food-item-modal').should('not.have.class', 'show').and('have.css', 'display', 'none');
        // Hide - click outside modal
        cy.get('a#food-item-card-link').first().wait(300).click({ force: true });
        cy.get('.modal').wait(500).click({ force: true });
        cy.get('#food-item-modal').should('not.have.class', 'show').and('have.css', 'display', 'none');
    });

    it('successfully adds a food to the cart', () => {
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.get('.toast').should('have.class', 'show');
        cy.get('.toast-header > strong').should('contain', 'Success!');
        cy.get('.toast-body > .row > .col > p').should('contain', 'Added', 'to your cart');
    });

    it('displays error message when food already in cart and user tries to add food from another restaurant to cart', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/restaurants/2/');
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/2/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.get('.toast').should('have.class', 'show');
        cy.get('.toast-header > strong').should('contain', 'Error');
        cy.get('.toast-body > p').should('contain', 'There is already food from another restaurant in your cart.');
    });

    it('correctly adds the chosen quantity of the food to the order', () => {
        // Add 1 to cart
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('input.qty-input').invoke('val').then((qty) => {
            cy.get('#add-to-basket-btn').wait(300).click({ force: true });
            cy.get('.bag-food-quantity').should('have.text', `Qty: ${qty}`);
        });
        // Add random amount more to cart (max 14 more)
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('input.qty-input').clear().type(Math.round(Math.random() * 14)).invoke('val').then((qty) => {
            cy.get('#add-to-basket-btn').wait(300).click({ force: true });
            cy.get('.bag-food-quantity').should('have.text', `Qty: ${parseFloat(qty) + 1}`);
        });
    });

    it('redirects to cart to review order when secure checkout button is pressed', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.get('#mini-bag-checkout-btn').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/bag/');
    });
});