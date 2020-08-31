document.addEventListener('DOMContentLoaded', () => {

	// Connect to Websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
	console.log("Connecting...")
	// When connected
	socket.on('connect', () => {
		console.log("Sockets on...")
	})
})