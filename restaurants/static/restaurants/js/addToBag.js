$(document).ready(() => {
    let foodModalForm = $("#food-modal-form");
    let addToBasketButton = $("#add-to-basket-btn");
    foodModalForm.on("submit", () => {
        addToBasketButton.prop('disabled', true);
    });
});