from flask import Blueprint, render_template, session, request, jsonify
from hook.routes.auth import login_required
from flask_socketio import emit, join_room
from .. import socketio
from ..models import Channel, User

chat = Blueprint('chat', __name__)


@chat.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    context = {
    	'channels': Channel.query.all()
    }
    return render_template('main/chat.html', context=context)


@chat.route('/add-channel', methods=['POST'])
def add_new_channel():
    channel_name = request.form.get('channel_name')
    channel_name = channel_name.strip()
    if channel_name:
	    if not Channel.query.filter_by(channel_name=channel_name).all():
		    new_channel = Channel(channel_name)
		    new_channel.save()

		    return jsonify({'channel_name': new_channel.channel_name, 'success': True,
		                    'error': 'null'})
	    else:
	    	return jsonify({'success': False, 'error': 'Channel already exists!'})
    else:
        return jsonify({'success': False, 'error': 'Invalid input.'})


# ============== SOCKETS CODES =================

@socketio.on('connected', namespace='/chat')
def connected(data):
	""" confirm connection of sockets """
	print(data['data'])


@socketio.on('getChannelDetails', namespace='/chat')
def get_channel_details(data):
	""" Check for existence of channels and get
	    the details of the channels including the
	    - channel's name
	    - channel's messages   """
	channel_name = data['name'][1:]  # excluding the '#' symbol
	channel_id = data['id']

	current_user = session.get('user').username # check for alignment of message in script
	# confirm existence of channel
	channel = Channel.query.get(channel_id)
	# on existence get channel messages
	if channel.channel_name == channel_name:
		message_objects = channel.messages.all()
		messages = []
		for message in message_objects:
			user = User.query.get_or_404(message.user_id,
				                         description="User not found.")
			time = message.timestamp
			timestamp = ' ' + str(time.date()) + ' | ' + str(time.strftime('%H:%M'))
			messages.append([user.username, timestamp,
			                 message.message])
	else:
		emit('ChannelDoesNotExist', {'error': 'Channel does not exists'},
			 broadcast=False)
	# enter channel as a room
	room = join_room(channel_name)
	join_room(channel_name)
	# return details to script
	emit('channelMessagesDelivered', {"messages": messages,
	     "user": current_user}, room=room)
