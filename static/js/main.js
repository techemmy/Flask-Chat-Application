document.addEventListener('DOMContentLoaded', () => {
    window.onload = () => {
        $('#signup').modal('show');
    }
    document.querySelector('.signup').onclick = () => {
        $('#signup').modal('show');
    };
});


let menuButton = document.querySelector(".menu__button");
let menuWrap = document.querySelector(".menu-wrap");

menuButton.addEventListener("click", () => {
    console.log("clicked")
    toggleMenu();
    // clearInterval(toggleTimer);
});

let toggleMenu = () => {
    menuWrap.classList.toggle("open");
};

// let toggleTimer = setInterval(() => {
//     toggleMenu();
// }, 2000);