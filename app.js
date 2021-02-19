const navSlide = () => {
    const profileSettings = document.querySelector('.profileSettings');
    const nav = document.querySelector('.nav-links');

    profileSettings.addEventListener('click', () =>{
        nav.classList.toggle('nav-active');
    }
}
navSlide();