describe('Shopping Bag Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/bag/');
        cy.url().should('eq', 'http://127.0.0.1:8000/bag/');
    });

    // Functionality Tests
    it('displays warning and button to browse restaurants if no food in cart', () => {
        cy.visit('/bag/');
        cy.get('.bag-contents > p').should('contain', "Looks like you haven't added any food to your order yet...");
        cy.get('.browse-restaurants-btn').should('exist');
        cy.get('form.table-responsive').should('not.exist');
    });

    it('directs user to all restaurants page upon pressing "browse restaurants" button', () => {
        cy.visit('/bag/');
        cy.get('.browse-restaurants-btn').click({ force: true });
        cy.url().should('eq', 'http://127.0.0.1:8000/restaurants/');
    });

    it('should adjust food quantity upon proceeding with checkout', () => {
        // Putting food into bag
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        cy.get('form.table-responsive').should('exist');
        // Adjusting to random quantity
        cy.get('.qty-input').invoke('val').then((qtyOriginal) => {
            let count = 0;
            let randomQty = Math.round(Math.random() * 14);
            while (count < randomQty) {
                cy.get('.increment-qty').click({ force: true }).wait(50);
                count++;
            }
            // Proceeding with checkout
            cy.get('.qty-input').invoke('val').should('not.be', qtyOriginal).then((qtyNew) => {
                cy.get('.continue-checkout-button').click();
                cy.url().should('eq', 'http://127.0.0.1:8000/checkout/address/');
                cy.get('input[name=full_name]').type('testy test');
                cy.get('input[name=email]').type('testy@test.com');
                cy.get('input[name=phone_number]').type('0871568498');
                cy.get('input[name=address_1]').type('123 testland road');
                cy.get('.continue-checkout-button').click().wait(100);
                cy.get('.continue-checkout-button').click();
                cy.get('.food-qty').invoke('html').should('eq', `Qty: ${parseFloat(randomQty) + 1}`);
            });
        });
    });

    it("doesn't allow quantity selector to go above 15 or below 1", () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        // Check above 15
        let count = 0;
        while (count < 20) {
            cy.get('.increment-qty').click({ force: true }).wait(50);
            count++;
        }
        cy.get('.qty-input').invoke('val').should('eq', '15');
        // Check below 1
        cy.reload();
        cy.get('.qty-input').invoke('val').should('eq', '1');
        count = 0;
        while (count < 5) {
            cy.get('.decrement-qty').click({ force: true }).wait(50);
            count++;
        }
        cy.get('.qty-input').invoke('val').should('eq', '1');
    });
    
    it('deletes food from cart upon pressing the delete button', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        cy.get('.fa-trash-alt').parent().click({ force: true }).wait(500);
        cy.get('.bag-contents > p').should('contain', "Looks like you haven't added any food to your order yet...");
        cy.get('.browse-restaurants-btn').should('exist');
        cy.get('form.table-responsive').should('not.exist');
        cy.get('.toast-header').should('contain', 'Alert!');
        cy.get('.toast-body > .row > .col > p').should('contain', 'has been removed from your order');
    });

    it('redirects user to restaurant associated with food in cart upon pressing back to restaurant button', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        cy.get('#back-to-restaurant-btn').click({ force: true });
        cy.url().should('eq', 'http://127.0.0.1:8000/restaurants/1/');
    });

    it('redirect user to checkout address page upon pressing secure checkout button with valid bag', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        cy.get('.continue-checkout-button').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/address/');
    });

    it('should update prices in realtime as user adjusts quantities', () => {
        // Putting food into bag
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/bag/');
        cy.get('form.table-responsive').should('exist');
        // Adjusting quantity
        cy.get('.qty-input').invoke('html').then((originalQty) => {
            cy.get('.food-price > p').invoke('html').then((originalPrice) => {
                originalPrice = originalPrice.replace('€', '');
                cy.get('p.subtotal').invoke('html').then((originalSubtotal) => {
                    cy.get('.increment-qty').click({ force: true });
                    cy.get('p.subtotal').should('contain', `€${originalPrice * 2}`);
                    cy.get('.bag-total > strong').should('contain', `€${originalPrice * 2}`);
                    cy.get('.bag-delivery').invoke('html').then((deliveryCharge) => {
                        deliveryCharge = deliveryCharge.replace('Delivery: €', '');
                        cy.get('.bag-grand-total > strong').should('contain', `€${(originalPrice * 2) + parseFloat(deliveryCharge)}`);
                    });
                });
            });
        });
    });

    it('displays error message if trying to add food to cart from a different restaurant', () => {
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/restaurants/2/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.get('.toast-header').should('contain', 'Error');
        cy.get('.toast-body > p').should('contain', 'There is already food from another restaurant in your cart.');
    });
});