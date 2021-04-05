// Change modal content based on food item
$(".food-item-card-body").on("click", function () {
    let foodName = $(this).find(".food-item-card-name").html()
    let foodImageSrc = $(this).find(".food-item-photo").attr("src")
    let foodImageAlt = $(this).find(".food-item-photo").attr("alt")

    $("#modal-label").text(foodName)
    $("#food-item-modal-image").attr("src", foodImageSrc)
    $("#food-item-modal-image").attr("alt", foodImageAlt)
});

// Decrement Quantity
$(".decrement-qty").on("click", function () {
    let currentVal = $(".qty-input").val()
    let newVal = Number(currentVal) - 1

    // Prevent user from going below 1
    if (newVal < 1) {
        $(".qty-input").val(1)
    } else {
        $(".qty-input").val(newVal)
    }
});

$(".increment-qty").on("click", function () {
    let currentVal = $(".qty-input").val()
    let newVal = Number(currentVal) + 1
    
    // Prevent user from going above 15
    if (newVal > 15) {
        $(".qty-input").val(15)
    } else {
        $(".qty-input").val(newVal)
    }
});