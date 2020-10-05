from flask import Blueprint, render_template, session, request, jsonify
from hook.routes.auth import login_required
from flask_socketio import emit, join_room
from .. import socketio
from ..models import Channel, User, Message, db


chat = Blueprint('chat', __name__)


@chat.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    context = {
    	'channels': Channel.query.all()
    }
    return render_template('main/chat.html', context=context)


def _process_info(name, n_type):
    if n_type == 'channel':
        if not Channel.query.filter_by(channel_name=name).all():
            new_channel = Channel(name)
            new_channel.save()
            return new_channel
        else:
        	return ('Error', 'Channel already exists!')
    elif n_type == 'DM':
    	pass
    else:
    	return None


@chat.route('/add-new-obj', methods=['POST'])
def add_new_obj():
	name = request.form.get('name')
	new_type = request.form.get('type')

	if new_type == 'channel':
		name = name.strip()
		if name:
			new_channel = _process_info(name, new_type)
			# check foor error
			if new_channel[0] == 'Error':
				# return error if channel already exists
				return jsonify({'success': False, 'error': new_channel[1]})
            # return success
			return jsonify({'name': new_channel.channel_name, 'success': True,
                            'error': 'null'})
		else:
			# return invalid input
			return jsonify({'success': False, 'error': 'Invalid input.'})
	elif new_type == 'DM':
		return jsonify({'name': 'ME', 'success': True,
			'error': 'null'})
	else:
		pass

# ------------- SOCKETS CODES --------------

@socketio.on('connected', namespace='/chat')
def connected(data):
	""" confirm connection of sockets """
	print(data['data'])
	emit('setLocalStorage', {'name': session.get('user').username})


@socketio.on('getChannelDetails', namespace='/chat')
def get_channel_details(data):
	""" Check for existence of channels and get
	    the details of the channels including the
	    - channel's name
	    - channel's messages   """
	channel_name = data['name'][1:]  # excluding the '#' symbol
	channel_id = data['id']

	current_user = session.get('user').username
	# confirm existence of channel
	channel = Channel.query.get(channel_id)
	# on existence get channel messages
	if channel.channel_name == channel_name:  # check if the channel exists
		message_objects = channel.messages.all()
		messages = []
		for message in message_objects:
			user = User.query.get_or_404(message.user_id,
				                         description="User not found.")
			time = message.timestamp
			timestamp = ' ' + str(time.date()) + ' | ' + str(time.strftime('%H:%M'))
			messages.append([user.username, timestamp,
			                 message.message])
		try:
			# enter channel as a room
			join_room(channel_name)
			room = join_room(channel_name)
			# return details to script
			emit('channelMessagesDelivered', {"messages": messages,
			     "user": current_user}, room=room)
		except Exception:
			emit('Error', {'error': 'Couldn\'t join channel'},
		          broadcast=False)

	else:
		emit('Error', {'error': 'Channel does not exists'},
			 broadcast=False)

@socketio.on('sendMessageToChannel', namespace='/chat')
def send_message_to_channel(data):
	message = data['message']
	channel_name = data['room'][1:]

	# ensure valid message
	if message:
		try:
			user = session.get('user')
			channel = Channel.query.filter_by(channel_name=channel_name).one()
			new_message = Message(message)
			new_message.user_id = user.id
			new_message.channel_id = channel.id
			new_message.save()
			# add user info
			user_name = User.query.filter_by(id=user.id).one().username
			time = new_message.timestamp
			timestamp = ' ' + str(time.date()) + ' | ' + str(time.strftime('%H:%M'))
			msg = new_message.message
			message_info = [user_name, timestamp, msg]
			room = channel_name
			
			emit('broadcastMessage', {'message': message_info}, room=room)
		except Exception:
			emit('Error', {'error': 'Error sending message.'})
	else:
		print("Pssd..")

