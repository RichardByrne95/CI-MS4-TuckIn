describe('Checkout Delivery Time Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click().wait(100);
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/time/');
    });

    // Functionality
    it('redirects user to bag with error message if user tries to go directly to page', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/time/');
        cy.url().should('eq', 'http://127.0.0.1:8000/bag/');
    });

    it('displays available delivery times for the restaurant', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click().wait(100);
        cy.get('#delivery-time-select > option').first().should('exist').and('contain', 'p.m.');
    });

    it('successfully adds delivery time to order upon submission', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11 p.m.');
        cy.get('.continue-checkout-button').click();
        cy.get('.delivery-time strong').should('contain', '11 p.m.');
    });

    it('directs user to checkout address page upon pressing edit address button', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#edit-address-button').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/address/');
    });
});