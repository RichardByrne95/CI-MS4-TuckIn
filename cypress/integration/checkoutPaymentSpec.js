// Required to access Stripe card input element which is within a nested iframe html document - Referenced https://www.cypress.io/blog/2020/02/12/working-with-iframes-in-cypress/
const getIframeDocument = (iframeSelector) => {
    return cy.get(iframeSelector).its('0.contentDocument').should('exist');
};
const getIframeBody = (iframeSelector) => {
    return getIframeDocument(iframeSelector).its('body').should('not.be.undefined').then(cy.wrap);
};

describe('Checkout Payment Tests', () => {

    // Page Load Test
    it('successfully loads', () => {
        // Setup
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
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/payment/');
    });

    // // Functionality Tests
    it('successfully submits all order details upon proceeding with checkout', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        getIframeBody('#card-element iframe').find('.CardNumberField-input-wrapper > span > input').type('424242424242424242424242424');
        cy.get('#submit-button').click();
        // // Validation
        cy.get('#order-confirmed-jumbotron > h3').should('contain', '11:45 p.m.');
        cy.get('.food-line-item > strong').should('contain', 'Big Muc');
        cy.get('.food-price').should('contain', '5.99');
        cy.get('.delivery-cost').should('contain', '5.00');
        cy.get('.grand-total').should('contain', '€10.99');
        cy.get('.customer-checkout-address').should('contain', '123 testland road');
        cy.get('.restaurant-checkout-phone').should('contain', '0871568498');
        cy.get('.toast-header > strong').first().should('contain', 'Success!');
        cy.get('.toast-body p').should('contain', 'A confirmation email will be sent to testy@test.com');
    });

    it('does not allow user to change city', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        cy.get('#id_city').should('have.attr', 'readonly');
    });

    it('should not allow user to submit form with invalid fields', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        // Clear name and attempt submit
        cy.get('#id_full_name').clear({ force: true });
        getIframeBody('iframe[allow="payment *"]').find('.CardNumberField-input-wrapper > span > input').type('424242424242424242424242424');
        cy.get('#submit-button').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/payment/');
        cy.get('#payment-form').then($el => $el[0].checkValidity()).should('be.false');
        // Enter invalid phone number and attempt submit
        cy.get('#id_full_name').type('testy test');
        cy.get('#id_phone_number').clear({ force: true }).type('e&$bH5236');
        cy.get('#submit-button').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/checkout/payment/');
        cy.get('#payment-form').then($el => $el[0].checkValidity()).should('be.false');
    });

    it('successfully loads bag upon clicking "adjust order" link', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        // Click link
        cy.get('.order-summary-heading a').click({ force: true });
        cy.url().should('eq', 'http://127.0.0.1:8000/bag/');
    });

    it('accurately displays the amount to be charged beneath the card number input field', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        // Validation
        cy.get('.charge-warning > strong').invoke('html').then((amount) => {
            cy.get('.grand-total-amount').invoke('html').should('eq', amount);
        });
    });

    it('accurately displays the number of items in the order in the order summary heading', () => {
        // Setup
        cy.visit('/restaurants/1/');
        let count = 0;
        while (count < Math.round(Math.random() * 5)) {
            cy.get('a#food-item-card-link').first().click({ force: true });
            cy.get('#add-to-basket-btn').wait(300).click({ force: true });
            count++;
        }
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        // Validation
        cy.get('.order-summary-heading strong').invoke('html').should('eq', `Order summary (${count})`);
    });

    it('directs user to help page upon clicking help link', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        // Validation
        cy.get('#help-link').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/links/help/');
    });

    it('returns to payment page and displays error if issue with card', () => {
        // Setup
        cy.visit('/restaurants/1/');
        cy.get('a#food-item-card-link').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').type('testy test');
        cy.get('input[name=email]').type('testy@test.com');
        cy.get('input[name=phone_number]').type('0871568498');
        cy.get('input[name=address_1]').type('123 testland road');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        getIframeBody('#card-element iframe').find('.CardNumberField-input-wrapper > span > input').type('400000826000317842424242424'); // This is a test card number that displays the 3D secure window, but fails regardless of choice due to 'insufficient funds'.
        cy.get('#submit-button').click().wait(7000); // Give time to 3D secure to render fully
        // Stripe uses 3 nested iframe elements to display the 3D secure payment buttons
        getIframeBody('iframe[allow="payment *"]').find('iframe#challengeFrame').then((iframeContainer) => {
            cy.wrap(iframeContainer).its('0.contentDocument').should('exist').its('body').find('iframe.FullscreenFrame').then((fullscreenFrame) => {
                cy.wrap(fullscreenFrame).its('0.contentDocument').should('exist').its('body').find('#test-source-authorize-3ds').click();
            });
            // Validation
        }).then(() => {
            cy.url().should('eq', 'http://127.0.0.1:8000/checkout/payment/');
            cy.get('#card-errors').should('contain', 'insufficient funds');
        });
    });
});