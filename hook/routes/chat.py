from flask import Blueprint, render_template
from hook.routes.auth import login_required
# from flask_socketio import emit, join_room, leave_room
from .. import socketio

chat = Blueprint('chat', __name__)

@chat.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    return render_template('main/chat.html')


@socketio.on('connected', namespace='/chat')
def connected(data):
	print("""
		connecting server-side...
		""")
	
	print(data['data'])
