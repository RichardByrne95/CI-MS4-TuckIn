$(document).ready(() => {
    // Set stars if order has rating
    const orderRating = $("#order-rating-value").html();
    if (orderRating) {
        $("#" + orderRating)
            .addClass("fas")
            .removeClass("far")
            .prevAll("i")
            .addClass("fas")
            .removeClass("far");
    }

    // Rating Hover Animation
    $(".far").on("mouseenter", (e) => {
        $(e.target).addClass("fas").removeClass("far").prevAll("i").addClass("fas").removeClass("far");
        $(e.target).nextAll().addClass("far").removeClass("fas");
    });
    $(".fas").on("mouseenter", (e) => {
        $(e.target).prevAll().addClass("fas").removeClass("far");
        $(e.target).nextAll().addClass("far").removeClass("fas");
    });
    $(".far, .fas").on("mouseleave", (e) => {
        if (orderRating) {
            $("#" + orderRating)
                .addClass("fas")
                .removeClass("far")
                .prevAll("i")
                .addClass("fas")
                .removeClass("far");
            $("#" + orderRating)
                .nextAll()
                .addClass("far")
                .removeClass("fas");
        } else {
            $(e.target).removeClass("fas").addClass("far").prevAll("i").removeClass("fas").addClass("far");
        }
    });

    // Rating Form Submit
    $(".far, .fas").on("click", (e) => {
        const rating = $(e.target).attr("id");
        $("[name=rating]").attr("value", rating);
        $("#rating-form").submit();
    });
});
