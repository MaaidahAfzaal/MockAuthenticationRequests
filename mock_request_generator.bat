@echo off
set FLASK_APP=app.py
set FLASK_ENV=development
start http://127.0.0.1:5000/
flask run