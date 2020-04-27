let page = document.querySelector(".page");
let toggle_menu = document.querySelector(".menu_toggle");
let content = document.querySelector(".content");

toggle_menu.addEventListener("click", () => {
  page.classList.toggle("shazam");
});
content.addEventListener("click", () => {
  page.classList.remove("shazam");
});
