$(document).ready(() => {
    // Update grand total and bag total
    function updateGrandAndBagTotals() {
        let grandTotalElement = $(".bag-grand-total > strong");
        let bagTotalElement = $(".bag-total > strong");
        let deliveryCost = $(".bag-delivery").contents().text().split(" ").pop().split("€").pop();
        deliveryCost = parseFloat(deliveryCost);
        let allSubtotals = $(".subtotal").contents().text().split("€");
        allSubtotals.shift();
        let bagTotal = 0.00;
        for (i = 0; i < allSubtotals.length; i++) {
            bagTotal += parseFloat(allSubtotals[i]);
        }
        bagTotalElement.html(`Bag Total: €${bagTotal.toFixed(2)}`);
        let grandTotal = bagTotal + deliveryCost;
        grandTotalElement.html(`Grand Total: €${grandTotal.toFixed(2)}`);
    }

    // Update food subtotal on quantity change
    function updateSubtotal(element) {
        let thisFoodQty = $(element).parent().siblings(".qty-input").val();
        let thisFoodPrice = $(element).parents(".qty-form").siblings(".food-price").children().html();
        thisFoodPrice = thisFoodPrice.split("€").pop();
        let calcFoodSubtotal = `€${(parseFloat(thisFoodPrice) * parseInt(thisFoodQty)).toFixed(2)}`;
        $(element).parents(".qty-form").siblings(".food-subtotal").children(".subtotal").html(calcFoodSubtotal);
        updateGrandAndBagTotals();
    }

    // Update food subtotal on quantity increment
    $(".increment-qty").on("click", function () {
        updateSubtotal(this);
    });

    // Update food subtotal on quantity decrement
    $(".decrement-qty").on("click", function () {
        updateSubtotal(this);
    });
});