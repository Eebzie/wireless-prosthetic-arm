window.addEventListener("load", () => {
    document.body.classList.remove("preload");
});

document.addEventListener("DOMContentLoaded", () => {
const nav = document.querySelector(".nav");

    document.querySelector("#btnNav").addEventListener("click", () =>{
        nav.classList.add("nav--open");
    });

    document.querySelector(".nav-overlay").addEventListener("click", () =>{
        nav.classList.remove("nav--open");
    });
});

function dark_mode_toggle() {
    document.body.classList.toggle("light");
    document.body.classList.toggle("dark");
 }