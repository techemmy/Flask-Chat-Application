console.log("Javascript (chat-script) connected.")

document.addEventListener('DOMContentLoaded', () => {
	// Connect to Websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/chat');

	// When connected
	socket.on('connect', () => {
		console.log("Connecting script...");
		socket.emit('connected', {'data': 'I\'m connected!'});
	});

	// load last active channel on page reload
	if (localStorage.getItem('activeChannel')){
		let channelName = localStorage.getItem('activeChannel');
		let channelId = localStorage.getItem('id')
		console.log(channelName);
		socket.emit('getChannelDetails', {'name': channelName, 'id': channelId});
	};
	
	document.querySelectorAll('.channel').forEach((channel) => {
		// gets channels detail from server on channel's click
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
		showMessage(data);
	});

	// ----------------ERROR HANDLING-----------------
	socket.on('ChannelDoesNotExist', (data) => {
		alert(data.error)
	});

	socket.on('ErrorJoiningChannel', (data) => {
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
  		if(!data.messages){
  			alert("no");
  		}

  		document.querySelector('.msg-gutter').append(msgContainer);
	}
};

// function broadcastMessage(data){
// };
