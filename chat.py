from flask import Blueprint, render_template, session
from auth import login_required

bp = Blueprint('chat', __name__)


@bp.route('/')
@login_required
def index():
    """ chat page if user is logged in """
    return render_template('main/chat.html')
