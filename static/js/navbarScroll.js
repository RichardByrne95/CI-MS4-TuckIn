$(document).ready(() => {
    // Referenced https://www.w3schools.com/howto/howto_js_navbar_slide.asp
    // Change navbar based on scroll position
    window.onscroll = () => {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            $("header").addClass("block-colour").removeClass("transparent-gradient");
            $(".navbar").addClass("navbar-light navbar-block-colour").removeClass("navbar-dark");
            $(".navbar-toggler").addClass("navbar-toggler-block-colour");
            $(".navbar-brand").addClass("navbar-brand-block-colour");
            $(".search-icon").addClass("search-icon-block-colour");
            $(".nav-link").addClass("nav-link-colour");
            $(".fa-shopping-bag").addClass("fa-shopping-bag-block-colour");
            $(".fa-stack-1x").addClass("text-white").removeClass("text-dark");
            $(".fa-stack-2x").addClass("text-dark").removeClass("text-white");
        } else {
            $("header").removeClass("block-colour").addClass("transparent-gradient");
            $(".navbar").removeClass("navbar-light navbar-block-colour").addClass("navbar-dark");
            $(".navbar-toggler").removeClass("navbar-toggler-block-colour");
            $(".navbar-brand").removeClass("navbar-brand-block-colour");
            $(".search-icon").removeClass("search-icon-block-colour");
            $(".nav-link").removeClass("nav-link-colour");
            $(".fa-shopping-bag").removeClass("fa-shopping-bag-block-colour");
            $(".fa-stack-1x").removeClass("text-white").addClass("text-dark");
            $(".fa-stack-2x").removeClass("text-dark").addClass("text-white");
        }
    };
});