import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

app = Flask(__name__);

@app.route('/')
def index():
	return render_template('index.html');


@app.route('/echo')
def echo():
	if request.environ.get('wsgi.websocket'):
		global websock;
		websock = request.environ['wsgi.websocket'];
		while True:
			global message;
			message = websock.receive();
			if message is None:
				break;
			websock.send(message);
			websock.send(message);
		
	return;

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler);
	server.serve_forever();
