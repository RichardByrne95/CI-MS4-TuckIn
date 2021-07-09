describe('Checkout Address Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.url().should('equal', 'http://127.0.0.1:8000/checkout/address/');
    });

    // Functionality and Validity
    it('saves any address details that are inputted/changed', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click().wait(100);
        cy.get('.continue-checkout-button').click();
        cy.get('input[name=full_name]').invoke('val').should('contain', 'testy test');
        cy.get('input[name=email]').invoke('val').should('contain', 'testy@test.com');
        cy.get('input[name=phone_number').invoke('val').should('contain', '0871568498');
        cy.get('input[name=address_1').invoke('val').should('contain', '123 testland road');
        cy.get('input[name=city]').invoke('val').should('contain', 'Dublin');
    });

    it('does not allow user to change city', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('#id_city').should('have.attr', 'readonly');
    });

    it('displays validation error if user tries to submit form without required fields', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-address').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('equal', 'http://127.0.0.1:8000/checkout/address/');
    });

    it("displays validation error if user tries to submit field that doesn't meet specifications", () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=phone_number]').type('t45tcvD$"d*!?').then($el => $el[0].checkValidity()).should('be.false');
    });

    it('bring the user back to the bag upon clicking the adjust order link', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('a#adjust-order-button').click();
        cy.url().should('equal', 'http://127.0.0.1:8000/bag/');
    });

    it('returns user to all restaurants page and displays warning if trying to access checkout payment with no food', () => {
        cy.visit('/checkout/address/');
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/');
        cy.get('.toast-header > strong').should('contain', 'Warning!');
        cy.get('.toast-body > p').should('contain', 'You have no food in your basket.');
    });
});