console.log("Javascript (chat-script) connected.")

document.addEventListener('DOMContentLoaded', () => {
	// Connect to Websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/chat');

	// When connected
	socket.on('connect', () => {
		console.log("Connecting script...");
		socket.emit('connected', {'data': 'I\'m connected!'});
	});

	socket.on('setLocalStorage', (data) => {
		localStorage.setItem('username', data.name);
	});

	if (!(localStorage.getItem('username'))){
		window.reload();
	}

	// load last active channel on page reload
	if (localStorage.getItem('activeChannel')){
		let channelName = localStorage.getItem('activeChannel');
		let channelId = localStorage.getItem('id')
		socket.emit('getChannelDetails', {'name': channelName, 'id': channelId});
	};
	
	// gets channels detail from server on channel's click
	document.querySelectorAll('.channel').forEach((channel) => {
		channel.onclick = () => {
			// Get channel name & id
			const name = channel.innerHTML;
			const id = channel.dataset.get;
			localStorage.setItem('activeChannel', name);
			localStorage.setItem('id', id)
			socket.emit('getChannelDetails', {'name': name, 'id': id});
		};
	});

	// send message
	const msg_box = document.querySelector('#send-message');
	const send_btn = document.querySelector('#send_btn');
	msg_box.onkeyup = () => {
		if(((msg_box.value).trim()).length > 0){
			send_btn.style.visibility = 'visible';
		}else{
			send_btn.style.visibility = 'hidden';
		}
	};
	send_btn.onkeydown = () => {
		send_btn.style.visibility = 'hidden';
		const msg = msg_box.value;
		msg_box.value = '';
		// to ensure message is not an empty string
		if(!(msg.trim() === '')){
			socket.emit('sendMessageToChannel', {'message': msg, 'room': document.querySelector('.active-channel').innerText});
		};
	};

	// show message on channel load
	socket.on('channelMessagesDelivered', (data) => {
		showMessage(data);
	});

	// append message to room(channel, DM)
	socket.on('broadcastMessage', (data) => {
		broadcastMessage(data);
	})

	// ----------------ERROR HANDLER-----------------
	socket.on('Error', (data) => {
		alert(data.error)
	});

});


document.addEventListener('DOMContentLoaded', () => {
	// initializes function for adding new object (channel, DM)
    var addNew = document.querySelectorAll('.add-new').forEach((addNew) => {
    	addNew.onclick = () => {
    		const type = addNew.dataset.type;
    		document.querySelector('.modal-dialog .modal-title').innerHTML = `Add New ${type}`;
    		document.querySelector('#add-new-field').dataset.type = type;
    		$('#add-temp').modal('show');

    		console.log(document.querySelector('#add-new-field'));

			document.querySelector('#add-new-form').onsubmit = addNewObject;
    	};
    });
});


// ----------------- FUNCTIONS ------------------- //


function addNewObject(){
	// initialize AJAX request
	const request = new XMLHttpRequest();

	const name = document.querySelector('#add-new-field').value;
	const type = document.querySelector('#add-new-field').dataset.type;
	$('#add-temp').modal('hide');
	document.querySelector('#add-new-field').value = '';

	request.open('POST', '/chat/add-new-obj');

	// callback function on completion of request
	request.onload = () => {

		// extract json data from response
		const data = JSON.parse(request.responseText);

		// add channel
		if (data.success){
			const name = `${data.name}`;
			console.log(name);
		} else {
			alert(data.error);
		}
	}

	// add data to send with request
	const data = new FormData();
	data.append('name', name)
	data.append('type', type)

	// send request
	request.send(data);
	return false;
};


function showMessage(data) {
	 document.querySelector('.msg-gutter').innerHTML = '';
	 document.querySelector('.active-channel').innerHTML = localStorage.getItem('activeChannel');
	// loop to add message to the message gutter
	for(i=0; i < data.messages.length; i++){
		message = data.messages[i]

		let msgContainer = document.createElement('div');
		msgContainer.className = 'msg-container';
  		if (data.user === message[0]){
  			msgContainer.style.justifyContent = 'flex-end';
  		};

  		let msgInfo = document.createElement('div');
  		msgInfo.className = 'msg-info';

  		let msgPic = document.createElement('div');
  		msgPic.className = 'msg-pic';

  		let msgImg = document.createElement('img');
  		msgImg.src = '../static/assets/msg-img.png';
  		msgImg.alt = 'user-image';
  		msgImg.className = 'msg-img';

  		let msgCont = document.createElement('div');
  		msgCont.className = 'msg-cont';

  		let msgName = document.createElement('span');
  		msgName.className = 'msg-name';
  		msgName.innerHTML = `${message[0]}`;

  		let msgTime = document.createElement('span');
  		msgTime.className = 'msg-time';
  		msgTime.innerHTML = `${message[1]}`;

  		let msgMsg = document.createElement('p');
  		msgMsg.className = 'msg-msg';
  		msgMsg.innerHTML = `${message[2]}`;

  		msgPic.append(msgImg);
  		msgCont.append(msgName);
  		msgCont.append(msgTime);
  		msgCont.append(msgMsg);
  		msgInfo.append(msgPic);
  		msgInfo.append(msgCont);
  		msgContainer.append(msgInfo);

  		document.querySelector('.msg-gutter').append(msgContainer);
	}
};

function broadcastMessage(data){
	// loop to add message to the message gutter
	message = data.message;

	let msgContainer = document.createElement('div');
	msgContainer.className = 'msg-container';
	if (localStorage.getItem('username') === message[0]){
		msgContainer.style.justifyContent = 'flex-end';
	};

	let msgInfo = document.createElement('div');
	msgInfo.className = 'msg-info';

	let msgPic = document.createElement('div');
	msgPic.className = 'msg-pic';

	let msgImg = document.createElement('img');
	msgImg.src = '../static/assets/msg-img.png';
	msgImg.alt = 'user-image';
	msgImg.className = 'msg-img';

	let msgCont = document.createElement('div');
	msgCont.className = 'msg-cont';

	let msgName = document.createElement('span');
	msgName.className = 'msg-name';
	msgName.innerHTML = `${message[0]}`;

	let msgTime = document.createElement('span');
	msgTime.className = 'msg-time';
	msgTime.innerHTML = `${message[1]}`;

	let msgMsg = document.createElement('p');
	msgMsg.className = 'msg-msg';
	msgMsg.innerHTML = `${message[2]}`;

	msgPic.append(msgImg);
	msgCont.append(msgName);
	msgCont.append(msgTime);
	msgCont.append(msgMsg);
	msgInfo.append(msgPic);
	msgInfo.append(msgCont);
	msgContainer.append(msgInfo);

	document.querySelector('.msg-gutter').append(msgContainer);
};
