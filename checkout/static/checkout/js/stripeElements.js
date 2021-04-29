// Referenced Stripe documentation
let stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
let clientSecret = $("#id_client_secret").text().slice(1, -1);
let cardElement = $("#card-element");
let form = $("#payment-form");
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();

const style = {
    base: {
        color: "#000",
        fontFamily: "'Inter', sans-serif",
        fontSmoothing: "antialiased",
        fontSize: "13px",
        "::placeholder": {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#dc3545",
        iconColor: '#dc3545',
    }
};

// Create and place Stripe card element in DOM
let card = elements.create("card", { style: style });
card.mount("#card-element");

// Handle card errors
card.on('change', (event) => {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

// Realtime Stripe validation errors
card.addEventListener('change', (event) => {
    let errorDiv = $("#card-errors");
    if (event.error) {
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>`;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = "";
    }
});

// Handle Checkout Form Submission
$("#submit-button").on("click", (e) => {
    // Prevent posting so that the below code can be executed
    e.preventDefault();
    // Disable card and submit button to prevent multiple submissions
    card.update({ "disabled": true });
    $("#submit-button").attr("disabled", true);
    // Fade form and loading overlay
    form.fadeToggle(100);
    $("#loading-overlay").fadeToggle(100);
    
    // Get additional form details and cache them to payment intent
    let saveInfo = Boolean($("#save-info").attr('checked'));
    let csrfMiddlewareToken = $("input[name='csrfmiddlewaretoken']").val();
    const url = '/checkout/cache_checkout_data/';
    let postData = {
        'csrfmiddlewaretoken': csrfMiddlewareToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    
    // Post additional form details to payment intent metadata
    $.post(url, postData).done(() => {
        // Send card details to Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name),
                    phone_number: $.trim(form.phone_number),
                    email: $.trim(form.email),
                    address: {
                        line1: $.trim(form.address_1),
                        line2: $.trim(form.address_2),
                        city: $.trim(form.city),
                        postcode: $.trim(form.postcode),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name),
                phone_number: $.trim(form.phone_number),
                address: {
                    line1: $.trim(form.address_1),
                    line2: $.trim(form.address_2),
                    city: $.trim(form.city),
                    postcode: $.trim(form.postcode),
                }
            }
        }).then((result) => {
            if (result.error) {
                // If error, show error to customer
                let errorDiv = $("#card-errors");
                let html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
                $(errorDiv).html(html);

                // Fade form and loading overlay
                form.fadeToggle(100);
                $("#loading-overlay").fadeToggle(100);

                // Re-enable card and submit button to allow the user to try again
                card.update({ "disabled": false });
                $("#submit-button").attr("disabled", false);

            } else {
                // If payment has gone through, submit form
                if (result.paymentIntent.status === "succeeded") {
                    form.submit();
                }
            }
        });
    }).fail(() => {
        // Reload page, error displayed via messages
        location.reload();
    })
});