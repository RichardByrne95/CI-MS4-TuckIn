$(document).ready(() => {
    // Referenced Stripe documentation
    const stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
    const clientSecret = $("#id_client_secret").text().slice(1, -1);
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

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
    const card = elements.create("card", { style: style });
    card.mount("#card-element");

    // Handle card errors
    card.on('change', (event) => {
        const displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // Realtime Stripe validation errors
    card.addEventListener('change', (event) => {
        const errorDiv = $("#card-errors");
        if (event.error) {
            const html = `
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
    const form = document.getElementById("payment-form");
    form.addEventListener("submit", (e) => {
        // Prevent posting so that the below code can be executed
        e.preventDefault();
        // Disable card and submit button to prevent multiple submissions
        card.update({ "disabled": true });
        $("#submit-button").attr("disabled", true);
        // Fade form and loading overlay
        $("#payment-form").fadeToggle(100);
        $("#loading-overlay").fadeToggle(100);

        // Get additional form details and cache them to payment intent
        const url = '/checkout/cache_checkout_data/';
        const saveInfo = Boolean($("#save-info").attr('checked'));
        const csrfMiddlewareToken = $("input[name='csrfmiddlewaretoken']").val();
        const postData = {
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
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                        address: {
                            line1: $.trim(form.address_1.value),
                            line2: $.trim(form.address_2.value),
                            city: $.trim(form.city.value),
                            postal_code: $.trim(form.postcode.value),
                        }
                    }
                },
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.address_1.value),
                        line2: $.trim(form.address_2.value),
                        city: $.trim(form.city.value),
                        postal_code: $.trim(form.postcode.value),
                    }
                }
            }).then((result) => {
                if (result.error) {
                    // If error, display error to customer
                    const errorDiv = $("#card-errors");
                    const html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);

                    // Fade form and loading overlay
                    $("#payment-form").fadeToggle(100);
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
        });
    });
});