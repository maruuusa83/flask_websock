import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import datetime
import locale

app = Flask(__name__);

@app.route('/')
def index():
	return render_template('index.html');


@app.route('/echo')
def echo():
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		while True:
			message = websock.receive();
			if message is None:
				break;
			websock.send(message);

			d = datetime.datetime.today();
			websock.send(d.strftime("%Y-%m-%d %H:%M:%S"));
		
	return;

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler);
	server.serve_forever();
