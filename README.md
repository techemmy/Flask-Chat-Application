# Hook - in development
A Flask chat application that uses sockets with python and javascript.

This full stack application uses only flask | Python on the backend, 
Javascript for front-end and interactiveness.

It uses Postgresql on the backend using flask-sqlalchemy.

It uses flask_socketio to communicate with javascript as well as the
javascript uses the javascript socket script to communicate back and forth.

To run this code on windows, run the run.sh file or copy and paste it in cmd
NOTE: Make sure you change the DATABASE_URL to suit your database url,
	  'username' usually postgres by default
	  'password' the password set for the db or your master password
	  'db' for the name of your db

For those running on Mac or Linux, to run this code check the equivalent
of the commands on google.