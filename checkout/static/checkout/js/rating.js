$(document).ready(() => {
    $(".far").on("mouseenter", (e) => {
        $(e.target).addClass("fas").removeClass("far").prevAll().addClass("fas").removeClass("far");
    });
    $(".far").on("mouseleave", (e) => {
        $(e.target).removeClass("fas").addClass("far").prevAll().removeClass("fas").addClass("far");
    });
});