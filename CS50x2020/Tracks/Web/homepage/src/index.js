let page = document.querySelector(".page");
let toggle_menu = document.querySelector(".menu_toggle");
let content = document.querySelector(".content");

toggle_menu.addEventListener("click", () => {
  page.classList.toggle("shazam");
});
content.addEventListener("click", () => {
  page.classList.remove("shazam");
});

let swiper = new Swiper(".swiper-container", {
  spaceBetween: 30,
  speed: 1500,
  centeredSlides: true,
  autoplay: {
    delay: 3500,
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    dynamicBullets: true,
    waitForTransition: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});
