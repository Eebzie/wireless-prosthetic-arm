window.addEventListener("load", () => {
    document.body.classList.remove("preload");
});

// Nav Bar Open/Close
document.addEventListener("DOMContentLoaded", () => {
const nav = document.querySelector(".nav");

    document.querySelector("#btnNav").addEventListener("click", () =>{
        nav.classList.add("nav--open");
    });

    document.querySelector(".nav-overlay").addEventListener("click", () =>{
        nav.classList.remove("nav--open");
    });
});

// Chart Resizing for Window Size Change
const myCanvas = document.getElementById("canvas"); 
const updateCanvas = () => ({width: window.innerWidth, height: window.innerHeight}) 
updateCanvas();
window.addEventListener("resize", updateCanvas());

// Dark Mode Toggle
function dark_mode_toggle() {
    document.body.classList.toggle("light");
    document.body.classList.toggle("dark");
 }