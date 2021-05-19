$(document).ready(() => {
    // Referenced https://www.w3schools.com/howto/howto_js_navbar_slide.asp
    // Change navbar based on scroll position
    window.onscroll = () => {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            $("header").addClass("block-colour").removeClass("transparent-gradient");
            $(".navbar").addClass("navbar-block-colour");
            $(".navbar-brand").addClass("navbar-brand-block-colour");
            $(".search-icon").addClass("search-icon-block-colour");
            $(".nav-link").addClass("nav-link-colour");
            $(".fa-shopping-bag").addClass("fa-shopping-bag-block-colour");
        } else {
            $("header").removeClass("block-colour").addClass("transparent-gradient");
            $(".navbar").removeClass("navbar-block-colour");
            $(".navbar-brand").removeClass("navbar-brand-block-colour");
            $(".search-icon").removeClass("search-icon-block-colour");
            $(".nav-link").removeClass("nav-link-colour");
            $(".fa-shopping-bag").removeClass("fa-shopping-bag-block-colour");
        }
    };
});