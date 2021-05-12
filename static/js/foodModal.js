$(document).ready(() => {
    // Change modal content based on food item
    $(".food-item-card-body").on("click", function (e) {
        let foodName = $(this).find(".food-item-card-name").html();
        let foodImageSrc = $(this).find(".food-item-photo").attr("src");
        let foodImageAlt = $(this).find(".food-item-photo").attr("alt");
        
        $("#modal-label").text(foodName);
        $("#food-item-modal-image").attr("src", foodImageSrc);
        $("#food-item-modal-image").attr("alt", foodImageAlt);
    
        // Passing this food's id to python via hidden input field
        let foodID = $(this).find(".food-id").html();
        $("#this-food").attr("value", foodID);
    });
});
