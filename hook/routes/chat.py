from flask import (Blueprint, render_template, session, request,
                   jsonify, redirect, url_for)
from hook.routes.auth import login_required
from flask_socketio import emit, join_room
from .. import socketio
from ..models import Channel, User, Message, Dm
from sqlalchemy.orm.exc import NoResultFound


chat = Blueprint('chat', __name__)


@chat.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    usr_obj = session.get('user')
    try:
        user = User.query.filter_by(username=usr_obj.username).one()
    except Exception:
        return redirect(url_for('auth.login'))
    context = {
        'channels': Channel.query.all(),
        'dms': user.get_dm()
    }
    return render_template('main/chat.html', context=context)


def _process_info(name, n_type):
    try:
        if n_type == 'channel':
            # checks if channel doesn't exists and adds it to the DB
            if not Channel.query.filter_by(channel_name=name).all():
                new_channel = Channel(name)
                new_channel.save()
                return None, new_channel
            else:
                return 'Error', 'Channel already exists!'

        elif n_type == 'DM':
            # gets user to add as DM objects from DB
            user_to_add_id = User.query.filter_by(username=name).one().id

            # gets current user id
            current_user_id = session.get('user').id

            # checks if user to add to DM is valid
            if user_to_add_id:
                # creates new DM object and save if no error raised
                dm = Dm(current_user_id, user_to_add_id)
                return None, dm, current_user_id
        else:
            return 'Error', 'Invalid Input... Contact Developer for help.'

    except ValueError as e:
        return 'Error', e.args[0]

    except NoResultFound:
        return 'Error', 'User doesn\'t exists'


@chat.route('add-obj', methods=['POST'])
def add_new_obj():
    name = request.form.get('name')
    new_type = request.form.get('type')

    # scrutinze name and returns error if name is invalid
    if name.strip(' ') == '':
        return jsonify({'success': False, 'error': 'Invalid input.'})

    name = name.strip().replace(' ', '_')

    if new_type == 'channel':
        new_channel = _process_info(name, new_type)

        # checks for error
        if new_channel[0] == 'Error':
            # return error if channel already exists
            return jsonify({'success': False, 'error': new_channel[1]})

        # return success
        return jsonify({'name': new_channel[1].channel_name,
                        'success': True, 'error': 'null'})
    elif new_type == 'DM':
        new_dm = _process_info(name, new_type)

        # checks for error
        if new_dm[0] == 'Error':
            # return error if processing DM wasn't successful
            return jsonify({'success': False, 'error': new_dm[1]})

        return jsonify({'name': new_dm[1].get_name(new_dm[2]),
                        'success': True, 'error': 'null'})
    else:
        return jsonify({'success': False, 'error': 'Invalid request.\
                        Contact Developer for more info.'})


# -------------------------------- SOCKETS CODES ------------------------------
# =============================================================================

@socketio.on('connected', namespace='/chat')
def connected(data):
    """ confirm connection of sockets """
    print(data['data'])
    emit('setLocalStorage', {'name': session.get('user').username})


@socketio.on('joinChannel', namespace='/chat')
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
            timestamp = ' ' + str(time.date()) + ' | ' + \
                        str(time.strftime('%H:%M'))
            messages.append([user.username, timestamp, message.message])
        try:
            # enter channel as a room
            join_room(channel_name)
            room = join_room(channel_name)
            # return details to script
            emit('MessagesDelivered', {"messages": messages,
                 "user": current_user}, room=room)
        except Exception as e:
            raise e
            emit('Error', {'error': 'Couldn\'t join channel'},
                 broadcast=False)
    else:
        emit('Error', {'error': 'Channel does not exists'},
             broadcast=False)


@socketio.on('sendMessageToChannel', namespace='/chat')
def send_message_to_channel(data):
    # sends message to channel
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
            timestamp = ' ' + str(time.date()) + ' | ' + \
                        str(time.strftime('%H:%M'))
            msg = new_message.message
            message_info = [user_name, timestamp, msg]
            room = channel_name

            emit('broadcastMessage', {'message': message_info}, room=room)
        except Exception:
            emit('Error', {'error': 'Error sending message.'})
    else:
        emit('Error', {'error': 'Invalid message'}, broadcast=False)


@socketio.on('joinDM', namespace='/chat')
def get_dm_details(data):
    """ Check for existence of dm and get
        the details of the dm including the
        - dm's name
          - dm's messages   """
    dm_name = data['name']
    dm_id = data['id']
    channel_room = data['room']

    current_user = session.get('user')
    # confirm existence of channel
    dm = Dm.query.get(dm_id)
    # on existence get channel messages
    if dm.get_name(current_user.id) == dm_name:  # check if the channel exists
        message_objects = dm.messages.all()
        messages = []
        for message in message_objects:
            user = User.query.get_or_404(message.user_id,
                                         description="User not found.")
            time = message.timestamp
            timestamp = ' ' + str(time.date()) + ' | ' + \
                        str(time.strftime('%H:%M'))
            messages.append([user.username, timestamp, message.message])
        try:
            # enter dm as a room
            join_room(channel_room)
            room = join_room(channel_room)
            # return details to script
            emit('MessagesDelivered', {"messages": messages,
                 "user": current_user.username}, room=room)
        except Exception:
            emit('Error', {'error': 'Couldn\'t join channel'},
                 broadcast=False)

    else:
        emit('Error', {'error': 'Channel does not exists'},
             broadcast=False)


@socketio.on('sendMessageToDm', namespace='/chat')
def send_message_to_dm(data):
    # sends message to dm
    message = data['message']
    dm_name = data['dm_name']
    dm_room = data['dm_room']

    user = session.get('user')
    other_user = User.query.filter_by(username=dm_name).one()
    if other_user and user:
        dm1 = Dm.query.filter_by(user_one=user.id,
                                 user_two=other_user.id).first()
        dm2 = Dm.query.filter_by(user_one=other_user.id,
                                 user_two=user.id).first()
        if dm1:
            DM = dm1
        elif dm2:
            DM = dm2
        else:
            # return error
            emit('Error', {'error': 'DM does not exists'}, broadcast=False)
    else:
        emit('Error', {'error': 'Invalid message'}, broadcast=False)

    # ensure the message exists
    if message and DM:
        print("Message", message, "DM", DM)
        try:
            # add the message
            new_message = Message(message)
            new_message.user_id = user.id
            new_message.dm_id = DM.id
            new_message.save()

            # add user info
            user_name = User.query.filter_by(id=user.id).one().username
            time = new_message.timestamp
            timestamp = ' ' + str(time.date()) + ' | ' + \
                        str(time.strftime('%H:%M'))
            msg = new_message.message
            message_info = [user_name, timestamp, msg]
            room = dm_room

            emit('broadcastMessage', {'message': message_info}, room=room)
        except Exception:
            emit('Error', {'error': 'Error sending message.'})
