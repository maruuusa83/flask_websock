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

class User:
	def append_data(self, jsonData, websock):
		myprint("append called");
		self.user_id = jsonData["id"];
		self.websock = websock;
		return;

	def login(self, jsonData):
		myprint("login called");
		check_user = g.db.users.find_one({"id":jsonData["id"], "pass":jsonData["pass"]});
		if check_user is None:
			myprint(jsonData["id"] + " is NotFound");
			return False;
		return True;

	def tmp(self):
		myprint("tmp");

	def chat(self, jsonData):
		to_user = jsonData["to"];
		message = jsonData["text"];
		myprint(to_user + " " + message);
		for user in user_list:
			if user.user_id == to_user:
				user.websock.send(message);
		return;
	#	send_message(self, to_user, message);

	'''
	def send_message(self, to_user, message):
		myprint(to_user +  message);
		for user in user_list:
			if user.user_id == to_user:
				user.websock.send(message);
		return;		
	'''

@app.route('/echo')
def echo():
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		while True:
		#	myprint("tukareta");
			data = websock.receive();
			user = User();
		#	myprint(data);
		#	user.tmp();
			if not data:
				break;
			jsonData = json.loads(data);
			if jsonData["type"] == "web":
				myprint(jsonData);
				myprint("ws="  + str(websock));
				flag = user.login(jsonData);
				if flag == False:
					continue;
				user.append_data(jsonData, websock);
				user_list.append(user);
				for u in user_list:
					myprint(u.user_id + " " + str(u.websock));
			else:
				user.chat(jsonData);
				#for user in ws_list:
				#	user.send(message);
	return "nadeko";

'''
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
	to_user = jsonData["to"];
	message = jsonData["text"];
	send_message(to_user, message);
	return;

def send_message(to_user, message):
	for user in user_list:
		if user[0] == to_user:
			user[1].send(message);
	return;		
'''

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
