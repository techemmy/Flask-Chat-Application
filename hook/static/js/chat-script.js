console.log("Javascript (chat-script) connected.")

document.addEventListener('DOMContentLoaded', () => {
	// Connect to Websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/chat');

	// When connected
	socket.on('connect', () => {
		console.log("Connecting script...");
		socket.emit('connected', {'data': 'I\'m connected!'});
	});
});
