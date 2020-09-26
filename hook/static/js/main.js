document.addEventListener('DOMContentLoaded', () => {
    window.onload = () => {
        $('#signup').modal('show');
    }
    var signUpBtn = document.querySelector('.signup');
    if (signUpBtn){
		signUpBtn.onclick = () => {
       		$('#signup').modal('show');
    	}; 
    };
    
});

let menuButton = document.querySelector(".menu__button");
let menuWrap = document.querySelector(".menu-wrap");

menuButton.addEventListener("click", () => {
    console.log("clicked")
    toggleMenu();
});

let toggleMenu = () => {
    menuWrap.classList.toggle("open");
};

