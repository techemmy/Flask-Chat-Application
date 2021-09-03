
window.onload = () => {
    $('#signup').modal('show');
}
var signUpBtn = document.querySelector('#signup_btn');

if (signUpBtn){
	signUpBtn.onclick = () => {
   		$('#signup-modal').modal('show');
	}; 
};
