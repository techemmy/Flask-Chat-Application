from flask import Blueprint, render_template, session
from auth import login_required

chat = Blueprint('chat', __name__)


@chat.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    return render_template('main/chat.html')
