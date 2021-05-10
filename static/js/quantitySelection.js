$(document).ready(() => {
    // Decrement Quantity
    $(".decrement-qty").on("click", function () {
        // Get
        let thisFood = $(this).parent().siblings(".qty-input");
        let currentVal = thisFood.val();
        let newVal = Number(currentVal) - 1;
        // Prevent user from going below 1
        if (newVal < 1) {
            thisFood.val(1)
        } else {
            thisFood.val(newVal)
        }
    });

    // Increment Quantity
    $(".increment-qty").on("click", function () {
        // Get values
        let thisFood = $(this).parent().siblings(".qty-input")
        let currentVal = thisFood.val()
        let newVal = Number(currentVal) + 1
        // Prevent user from going above 15
        if (newVal > 15) {
            thisFood.val(15)
        } else {
            thisFood.val(newVal)
        }
    });
});