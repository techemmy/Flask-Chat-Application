console.log("Javascript (chat-script) connected.")

document.addEventListener('DOMContentLoaded', () => {
	// Connect to Websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/chat');

	// When connected
	socket.on('connect', () => {
		console.log("Connecting script...");
		socket.emit('connected', {'data': 'I\'m connected!'});
	});
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

	socket.on('channelMessagesDelivered', (data) => {
		broadcastMessage(data);
	});

	socket.on('ChannelDoesNotExist', (data) => {
		alert(data.error)
	});


});


document.addEventListener('DOMContentLoaded', () => {
    const addNew = document.querySelectorAll('.add-new').forEach((addNew) => {
    	addNew.onclick = () => {
    		document.querySelector('.modal-dialog .modal-title').innerHTML = `Add New ${addNew.dataset.type}`;
    		$('#add-temp').modal('show');
    	};
    });

 //    window.onload = () => {
	// 	let channelName = localStorage.getItem('activeChannel');
	// 	let channelId = localStorage.getItem('id')
	// 	console.log(channelName);
	// 	socket.emit('getChannelDetails', {'name': name, 'id': id});
	// }

	document.querySelector('#add-new-form').onsubmit = addNewChannel;
});


// =================== FUNCTIONS =============================== //


function addNewChannel(){
	// initialize AJAX request
	const request = new XMLHttpRequest();
	const channelName = document.querySelector('#add-new-field').value;
	$('#add-temp').modal('hide');
	document.querySelector('#add-new-field').value = '';
	request.open('POST', '/chat/add-channel');

	// callback function on completion of request
	request.onload = () => {

		// extract json data from response
		const data = JSON.parse(request.responseText);

		// add channel
		if (data.success){
			const channel_name = `${data.channel_name}`;
			console.log(channel_name);
		} else {
			alert(data.error);
		}
	}

	// add data to send with request
	const data = new FormData();
	data.append('channel_name', channelName)

	// send request
	request.send(data);
	return false;
};


function broadcastMessage(data) {
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