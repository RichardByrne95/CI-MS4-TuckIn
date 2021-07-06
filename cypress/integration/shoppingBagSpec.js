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
        
    });
    
    it('deletes food from cart upon pressing the delete button', () => {
        
    });

    it('redirects user to restaurant associated with food in cart upon pressing back to restaurant button', () => {
        
    });

    it('redirect user to checkout address page upon pressing secure checkout button', () => {
        
    });

    it('should update prices in realtime as user adjusts quantities', () => {
        
    });

    it('displays error message if trying to add food to cart from a different restaurant', () => {
        
    });
});