import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

app = Flask(__name__);

ws_list = set();

@app.route('/')
def index():
	return render_template('index.html');


@app.route('/echo')
def echo():
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		ws_list.add(websock);
		while True:
			message = websock.receive();
			if message is None:
				break;
			for user in ws_list:
				user.send(message);
	return;

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
	server.serve_forever();
