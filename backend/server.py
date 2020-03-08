#!/usr/bin/env python

from flask import Flask, request
from flask_cors import CORS
import sender
import db
import receiver

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'API Middleware'


@app.route('/login')
def do_login():
    username = request.args.get('username')
    password = request.args.get('password')

    s = sender.Sender('login')
    s.sendtoRabbitMq({'username': username, 'password': password})

    rec = receiver.Receiver('login')
    r = rec.getMessages()

    if r == False:
        return '{"status":"error","message":"Username or password not found"}'
    return '{"status":"ok","message":"'+str(r)+'"}'


@app.route('/registration')
def do_registration():
    UserName = request.args.get('username')
    Email = request.args.get('email')
    Password = request.args.get('password')
    Address = request.args.get('address')
    ContactNo = request.args.get('contactNo')

    # Send this data to RabbitMQ
    s = sender.Sender('registration')
    s.sendtoRabbitMq({'UserName': UserName, 'Email': Email,
                      'Password': Password, 'Address': Address, 'ContactNo': ContactNo})

    rec = receiver.Receiver('registration')
    r = rec.getMessages()
    if r == False:
        return '{"status":"error","message":"This user may already exists"}'
    return '{"status":"ok","message":"User has been registered!"}'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
