// Referenced https://www.w3schools.com/howto/howto_js_navbar_slide.asp
// Change navbar based on scroll position
window.onscroll = () => {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        $("header").css({"background-image": "none"});
        $(".navbar").css({"background-color": "#fafafa"});
        $(".navbar-brand").css({"color": "orangered"});
        $(".search-icon").css({"color": "#000"});
        $(".nav-link").css({"color": "#00baff"});
        $(".fa-shopping-bag").css({"color": "#00baff"});
    } else {
        $("header").css({"background-image": "linear-gradient(to bottom, rgba(0,0,0,.7)"});
        $(".navbar").css({"background-color": "rgba(0,0,0,0)"});
        $(".navbar-brand").css({"color": "#fafafa"});
        $(".search-icon").css({"color": "#fafafa"});
        $(".nav-link").css({"color": "#fafafa"});
        $(".fa-shopping-bag").css({"color": "#fafafa"});
    }
}