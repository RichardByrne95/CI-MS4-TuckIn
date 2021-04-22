// From Stripe documentation
let stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
let clientSecret = $("#id_client_secret").text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();
let cardElement = $("#card-element")

const style =  {
    base: {
        color: "#000",
        fontFamily: "'Inter', sans-serif",
        fontSmoothing: "antialiased",
        fontSize: "1.3rem",
        "::placeholder": {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#dc3545",
        iconColor: '#dc3545',
    }
};

let card = elements.create("card", {style: style});
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
});