import os
from dotenv import load_dotenv
from hook import create_app, socketio
from hook.models import User, Channel, Message, Dm, db

app = create_app(debug=False)

# load configurations from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Channel=Channel, Message=Message, Dm=Dm)

@app.cli.command()
def create_db():
    db.create_all()
    print("DB CREATED...")

@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    socketio.run(app)
