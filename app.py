import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, g, redirect
import pymongo
import json

app = Flask(__name__);

ws_list = [];
user_list = [];

def myprint(obj):
	open("out.txt", "a").write(str(obj) + '\n');

@app.route('/')
def index():
	return render_template('index.html');

@app.route('/echo')
def echo():
	myprint("test")
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		ws_list.append(websock);
		myprint("test")
		while True:
			message = websock.receive();
			if not message:
				break;
			jsonData = json.loads(message);
			myprint(jsonData);
			if jsonData["type"] == "web":
				login(jsonData, websock);
			else:
				chat(jsonData);
				#for user in ws_list:
				#	user.send(message);
	return "nadeko";

def login(jsonData, websock):
	myprint(jsonData["id"] + " " + jsonData["pass"]);
	db_find = g.db.users.find_one({"id":jsonData["id"], "pass":jsonData["pass"]});
	myprint(db_find);
	if db_find is None:	
		return;
	user_list.append((jsonData["id"], websock));
	myprint(user_list);

def chat(jsonData):
	myprint(jsonData);
	from_user = jsonData["from"];
	to_user = jsonData["to"];
	message = jsonData["text"];
	for user in user_list:
		myprint(user);
		if user[0] == to_user:
			myprint(user);
			user[1].send(message);
	return;

@app.before_request
def before_request():
	g.conn = pymongo.Connection()
	g.db = g.conn["chat_db"]

@app.teardown_request
def teardown_request(exception):
	g.conn.close()

if __name__ == '__main__':
	app.debug = True
	server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
	server.serve_forever();
