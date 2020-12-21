from hook import create_app, socketio
from hook.models import User, Channel, Message, Dm, db

app = create_app(debug=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Channel=Channel, Message=Message, Dm=Dm)


if __name__ == '__main__':
    socketio.run(app)
