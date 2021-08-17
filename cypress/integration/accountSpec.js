// Required to access Stripe card input element which is within a nested iframe html document - Referenced https://www.cypress.io/blog/2020/02/12/working-with-iframes-in-cypress/
const getIframeDocument = (iframeSelector) => {
    return cy.get(iframeSelector).its('0.contentDocument').should('exist');
};
const getIframeBody = (iframeSelector) => {
    return getIframeDocument(iframeSelector).its('body').should('not.be.undefined').then(cy.wrap);
};

describe('Register Tests', () => {
    it('successfully loads', () => {
        cy.visit('/accounts/signup/');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    it('directs user to sign in page upon clicking the link to sign in', () => {
        cy.visit('/accounts/signup/');
        cy.get('#sign-in-link').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/login/');
    });

    it('displays validation errors if empty form is submitted', () => {
        cy.visit('/accounts/signup/');
        cy.get('#sign-up-button').click({ force: true });
        cy.get('#signup_form').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    it("displays validation errors if invalid email address is submitted", () => {
        cy.visit('/accounts/signup/');
        cy.get('#id_email').type('test123@com');
        cy.get('#id_password1').type('tuckinms4');
        cy.get('#id_password2').type('tuckinms4');
        cy.get('#sign-up-button').click({ force: true });
        cy.get('#signup_form').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    it("displays validation errors if passwords don't match", () => {
        cy.visit('/accounts/signup/');
        cy.get('#id_email').type('test123@test.com');
        cy.get('#id_password1').type('tuckinms4');
        cy.get('#id_password2').type('TUCKINMS4');
        cy.get('#sign-up-button').click({ force: true });
        cy.get('#signup_form').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    it('redirects user to email confirmation page upon successful submission of registration form', () => {
        cy.visit('/accounts/signup/');
        cy.get('#id_email').type('test123@test.com');
        cy.get('#id_password1').type('tuckinms4');
        cy.get('#id_password2').type('tuckinms4');
        cy.get('#sign-up-button').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/confirm-email/');
    });

    it('displays error to user upon attempting to sign up using credentials belonging to another account', () => {
        cy.visit('/accounts/signup/');
        cy.get('#id_email').type('test123@test.com');
        cy.get('#id_password1').type('tuckinms4');
        cy.get('#id_password2').type('tuckinms4');
        cy.get('#sign-up-button').click({ force: true });
        cy.get('#signup_form').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });
});

describe('Login Tests', () => {
    it('successfully loads', () => {
        cy.visit('/accounts/login/');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/login/');
    });

    it('redirects user to "sign up" page upon clicking "sign up" link', () => {
        cy.visit('/accounts/login/');
        cy.get('#sign-up-link').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    it('redirects user to correct "forgot password" url', () => {
        cy.visit('/accounts/login/');
        cy.get('#forgot-password-link').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/password/reset/');
    });

    // Due to needing to verify account via email, a pre-verified test account is used for this test
    it('redirects user to "all restaurants" page if sign in successful', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/');
    });
});

describe('Profile Tests', () => {
    it('successfully loads', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/');
        cy.url().should('equal', 'http://127.0.0.1:8000/profiles/');
    });

    it('should not allow users to change email or city', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/');
        cy.get('input[name=email]').should('have.attr', 'readonly');
        cy.get('input[name=default_city]').should('have.attr', 'readonly');
    });

    it('rejects submission of an invalid form', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/');
        cy.get('#id_full_name').clear({ force: true }).type('abcd', { force: true });
        cy.get('.save-changes-button').click({ force: true});
        cy.get('#account-details-form').then($el => $el[0].checkValidity()).should('be.false');
    });

    it('correctly saves info on form submit', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/');
        cy.get('#id_default_address_1').clear({ force: true }).type('123 Test Road');
        cy.get('#id_default_address_2').clear({ force: true }).type('Testlandia');
        cy.get('#id_default_phone_number').clear({ force: true }).type('12345678');
        cy.get('.save-changes-button').click({ force: true}).wait(4000);
        cy.get('#id_default_address_1').invoke('val').should('contain', '123 Test Road');
        cy.get('#id_default_address_2').invoke('val').should('contain', 'Testlandia');
        cy.get('#id_default_phone_number').invoke('val').should('contain', '12345678');
    });

});

describe('Order History', () => {
    it('successfully loads', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/customer_order_history/');
        cy.url().should('equal', 'http://127.0.0.1:8000/profiles/customer_order_history/');
    });

    it("displays an info message to a user that hasn't placed any orders", () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/profiles/customer_order_history/');
        cy.get('.no-orders p').should('contain', "Looks like you haven't ordered anything yet!");
    });

    it('redirects user to restaurant when clicking on restaurant logo', () => {
        // Setup account
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        // Create order
        cy.visit('/restaurants/1/');
        cy.get('a.food-item-card-body').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').clear({ force: true }).type('testy test');
        cy.get('input[name=phone_number]').clear({ force: true }).type('0871568498');
        cy.get('input[name=address_1]').clear({ force: true }).type('123 testland road');
        cy.get('input[name=address_2]').clear({ force: true }).type('Testlandia');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        getIframeBody('#card-element iframe').find('.CardNumberField-input-wrapper > span > input').type('424242424242424242424242424');
        cy.get('#submit-button').click().wait(4000);
        cy.url().should('contain', 'order_confirmation').wait(300);
        // Validation
        cy.visit('/profiles/customer_order_history/');
        cy.get('.restaurant-logo').first().click({ force: true });
        cy.url().should('contain', '/restaurants/1/');
    });

    it('redirects user to order confirmation page with correct message if user clicks on order text', () => {
        // Setup account
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        // Create order
        cy.visit('/restaurants/1/');
        cy.get('a.food-item-card-body').first().click({ force: true });
        cy.get('#add-to-basket-btn').wait(300).click({ force: true });
        cy.visit('/checkout/address/');
        cy.get('input[name=full_name]').clear({ force: true }).type('testy test');
        cy.get('input[name=phone_number]').clear({ force: true }).type('0871568498');
        cy.get('input[name=address_1]').clear({ force: true }).type('123 testland road');
        cy.get('input[name=address_2]').clear({ force: true }).type('Testlandia');
        cy.get('.continue-checkout-button').click();
        cy.get('#delivery-time-select').select('11:45 p.m.');
        cy.get('.continue-checkout-button').click();
        getIframeBody('#card-element iframe').find('.CardNumberField-input-wrapper > span > input').type('424242424242424242424242424');
        cy.get('#submit-button').click().wait(4000);
        // Validation
        cy.visit('/profiles/customer_order_history/');
        cy.get('.restaurant-address-container').first().click({ force: true });
        cy.url().should('contain', 'profiles/customer_order_history/');
    });

    it('adds all food, quantities and additional messages to order, then redirects to cart upon pressing the order again button', () => {
        // Setup account
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        // Create order
        cy.visit('/restaurants/1/');
        cy.get('a.food-item-card-body').first().click({ force: true });
        cy.get('#modal-label').invoke('html').then((foodName) => {
            cy.get('#add-to-basket-btn').wait(300).click({ force: true });
            cy.visit('/checkout/address/');
            cy.get('input[name=full_name]').clear({ force: true }).type('testy test');
            cy.get('input[name=phone_number]').clear({ force: true }).type('0871568498');
            cy.get('input[name=address_1]').clear({ force: true }).type('123 testland road');
            cy.get('.continue-checkout-button').click();
            cy.get('#delivery-time-select').select('11:45 p.m.');
            cy.get('.continue-checkout-button').click();
            getIframeBody('#card-element iframe').find('.CardNumberField-input-wrapper > span > input').type('424242424242424242424242424');
            cy.get('#submit-button').click();
            // Validation
            cy.visit('/profiles/customer_order_history/');
            cy.get('.order-again-btn').first().click({ force: true });
            cy.get('.bag-food-name strong').invoke('html').should('equal', foodName);
        });
    });
});

describe('Logout Tests', () => {
    it('successfully loads', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/accounts/logout/');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/logout/');
    });

    it('successfully sign a user out of their account', () => {
        cy.visit('/accounts/login/');
        cy.get('#id_login').type('test@test.com');
        cy.get('#id_password').type('9r9cYMd3B56cSY@');
        cy.get('button.primaryAction[type=submit]').click({ force: true });
        cy.visit('/accounts/logout/');
        cy.get('#log-out-button').click({ force: true }).wait(500);
        cy.visit('/profiles/').wait(500);
        cy.url().should('contain', '/accounts/login/');
    });
});