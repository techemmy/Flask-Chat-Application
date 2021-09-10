
window.onload = () => {
    $('#signup').modal('show');
}
var signUpBtn = document.querySelector('#signup-btn');
var loginBtn = document.querySelector('#login-btn')

if (signUpBtn){
	signUpBtn.onclick = () => {
   		$('#signup-modal').modal('show');
	}; 
};

if (loginBtn){
	loginBtn.onclick = () => {
   		$('#login-modal').modal('show');
	}; 
};
