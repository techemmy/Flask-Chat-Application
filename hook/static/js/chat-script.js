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

	// if (!(localStorage.getItem('username'))){
	// 	alert("LogOut and LogIn to fix error.")
	// 	location.reload();
	// }

	// load last active channel on page reload
	if (localStorage.getItem('activeTab')){
		let activeTab = localStorage.getItem('activeTab');
		let activeId = localStorage.getItem('id')
		// TODO!possiblities:
		if(activeTab.slice(0,1) === '#'){
			socket.emit('joinChannel', {'name': activeTab, 'id': activeId});	
		}else{
			socket.emit('joinDM', {'name': activeTab, 'id': activeId,
			            'room': localStorage.getItem('dm_room')});
		};
	};
	
	// gets channels detail from server on channel's click
	document.querySelectorAll('.channel').forEach((channel) => {
		channel.onclick = () => {
			// Get channel name & id
			const name = channel.innerHTML;
			const id = channel.dataset.get;
			localStorage.setItem('activeTab', name);
			localStorage.setItem('id', id)
			socket.emit('joinChannel', {'name': name, 'id': id});
		};
	});

	// gets dm detail from server on dm's click
	document.querySelectorAll('.dm').forEach((dm) => {
		dm.onclick = () => {
			// Get channel name & id
			const name = dm.innerHTML;
			const id = dm.dataset.get;
			const room = dm.dataset.room;
			localStorage.setItem('activeTab', name);
			localStorage.setItem('id', id)
			localStorage.setItem('dm_room', room)
			console.log(name, id)
			socket.emit('joinDM', {'name': name, 'id': id, 'room': room});
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
	addListenerMulti(send_btn, "click keydown", () => {
		send_btn.style.visibility = 'hidden';
		const msg = msg_box.value;
		msg_box.value = '';
		// to ensure message is not an empty string
		if(!(msg.trim() === '')){
			const activeTab = document.querySelector('.active-tab').innerHTML;
			if (activeTab.slice(0,1) === '#'){
				socket.emit('sendMessageToChannel', {'message': msg,
				            'room': document.querySelector('.active-tab').innerText});
			}
			if (activeTab.slice(0,1) !== '#'){
				socket.emit('sendMessageToDm', {'message': msg,
				            'dm_name': document.querySelector('.active-tab').innerText,
				             'dm_room': localStorage.getItem('dm_room')});
			}
		};
	});

	// show message on channel load
	socket.on('MessagesDelivered', (data) => {
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

			document.querySelector('#add-new-form').onsubmit = addNewObject;
    	};
    });
});


// ----------------- FUNCTIONS ------------------- //

function addListenerMulti(element, eventNames, listener) {
	// adds multiple events listeners
  var events = eventNames.split(' ');
  for (var i=0, iLen=events.length; i<iLen; i++) {
    element.addEventListener(events[i], listener, false);
  }
};


function addNewObject(){
	// initialize AJAX request
	const request = new XMLHttpRequest();

	const name = document.querySelector('#add-new-field').value;
	const type = document.querySelector('#add-new-field').dataset.type;
	$('#add-temp').modal('hide');
	document.querySelector('#add-new-field').value = '';

	request.open('POST', '/chat/add-obj');

	// callback function on completion of request
	request.onload = () => {

		// extract json data from response
		const data = JSON.parse(request.responseText);
		console.log(data);

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
	const msg_gutter = document.querySelector('.msg-gutter');
	 msg_gutter.innerHTML = '';
	 document.querySelector('.active-tab').innerHTML = localStorage.getItem('activeTab');
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
  		msgName.style.fontWeight = 'bold';

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

  		msg_gutter.append(msgContainer);
  		msg_gutter.scrollTop = msg_gutter.scrollHeight;
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

	const msg_gutter = document.querySelector('.msg-gutter');

	msg_gutter.append(msgContainer);
	msg_gutter.scrollTop = msg_gutter.scrollHeight;
};
