describe('Home Page/Index Tests', () => {
    // Page Load Test
    it('successfully loads', () => {
        cy.visit('/');
        cy.url().should('eq', 'http://127.0.0.1:8000/');
    });

    // Address Tests
    it('disables find button when new user visits site', () => {
        cy.get('#address-finder').then(form => form[0].checkValidity()).should('be.false');
        cy.get('button.find-button').should('be.disabled');
    });

    it('enables find button upon a valid address being entered or selected', () => {
        cy.get('input#address').type('65 Merrion Square', { force: true }).focus();
        cy.get('.pac-item').first().click();
        cy.get('#address-finder').then(form => form[0].checkValidity()).should('be.true');
        cy.get('button.find-button').should('not.be.disabled');
    });

    it('disables find button if input is empty', () => {
        cy.get('input#address').clear({ force: true });
        cy.get('#address-finder').then(form => form[0].checkValidity()).should('be.false');
        cy.get('button.find-button').should('be.disabled', { force: true });
    });

    it('returns to homepage and display error if "Dublin" is not in address', () => {
        cy.get('input#address').clear({ force: true }).type('Cork', { force: true }).get('input#address').focus();
        cy.get('.pac-item').first().click();
        cy.get('#address-finder').submit();
        cy.url().should('equal', 'http://127.0.0.1:8000/');
        cy.get('.toast').should('have.class', 'show');
        cy.get('.toast-header').children('strong').should('contain', 'Error');
        cy.get('.toast-body').children().should('contain', 'Address not found within Dublin, please try again');
    });

    it('redirects to all restaurants page and display "Dublin" as address if no address inputted and cuisine selected', () => {
        cy.get('i.fa-pizza-slice').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=pizza');
        cy.get('h4.nearby-restaurants').should('contain', 'delivering in Dublin');
        cy.get('.change-location > a').should('contain', 'set location');
    });

    it('redirects to all restaurants page and display valid address on page if valid address', () => {
        cy.visit('/');
        cy.get('input#address').clear({ force: true }).type('65 Merrion Square', { force: true }).focus();
        cy.get('.pac-item').first().click();
        cy.get('#address-finder').then(form => form[0].checkValidity()).should('be.true');
        cy.get('#address-finder').submit();
        cy.url().should('equal', 'http://127.0.0.1:8000/restaurants/');
        cy.get('h4.nearby-restaurants').should('contain', 'delivering to 65 Merrion Square');
        cy.get('.change-location > a').should('contain', 'change location');
    });

    it('creates session cookie upon submitting valid address', () => {
        cy.visit('/');
        cy.get('input#address').clear({ force: true }).type('65 Merrion Square', { force: true }).focus();
        cy.get('.pac-item').first().click();
        cy.get('#address-finder').then(form => form[0].checkValidity()).should('be.true');
        cy.get('#address-finder').submit();
        cy.getCookie('sessionid').should('exist');
    });

    // Cuisine Links
    it('successfully loads relevant url based on cuisine selected', () => {
        // Pizza
        cy.visit('/');
        cy.get('i.fa-pizza-slice').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=pizza');
        // American
        cy.visit('/');
        cy.get('i.fa-hamburger').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=american');
        // Indian
        cy.visit('/');
        cy.get('i.fa-pepper-hot').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=indian');
        // Seafood
        cy.visit('/');
        cy.get('i.fa-fish').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=seafood');
        // Vegetarian
        cy.visit('/');
        cy.get('i.fa-egg').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=vegetarian');
        // Vegan
        cy.visit('/');
        cy.get('i.fa-carrot').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=vegan');
        // Chicken
        cy.visit('/');
        cy.get('i.fa-drumstick-bite').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=chicken');
        // Treats
        cy.visit('/');
        cy.get('i.fa-cookie').click();
        cy.url().should('include', 'restaurants').should('contain', 'cuisine=treats');
    });
});