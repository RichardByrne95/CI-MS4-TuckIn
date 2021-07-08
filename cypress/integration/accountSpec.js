describe('Account System Tests', () => {
    // Register
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/accounts/signup/');
        cy.url().should('equal', 'http://127.0.0.1:8000/accounts/signup/');
    });

    // Functionality and Validation Tests
    it('directs user to sign in page upon clicking the link to sign in', () => {
        cy.visit('/accounts/signup/');
        cy.get('#sign-in-link').click({ force: true });
        cy.url().should('eq', 'http://127.0.0.1:8000/accounts/login/');
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
        cy.url().should('eq', 'http://127.0.0.1:8000/accounts/confirm-email/');
    });

    it('displays error to user upon attempting to sign up using credentials belonging to another account', () => {
        cy.visit('/accounts/signup/');
        cy.get('#id_email').type('test123@test.com');
        cy.get('#id_password1').type('tuckinms4');
        cy.get('#id_password2').type('tuckinms4');
        cy.get('#sign-up-button').click({ force: true });
        cy.get('#signup_form').then($el => $el[0].checkValidity()).should('be.false');
        cy.url().should('eq', 'http://127.0.0.1:8000/accounts/signup/');
    });
});