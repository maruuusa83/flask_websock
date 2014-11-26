import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import datetime
import locale

app = Flask(__name__);

wss = [];

@app.route('/')
def index():
	return render_template('index.html');


@app.route('/echo')
def echo():
	global wss;
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		wss.append(websock);
		while True:
			message = websock.receive();
			if message is None:
				wss.remove(websock);
				break;
			for ws in wss:
				d = datetime.datetime.today();
				cont = "<p>" + message + "</p>" + "<small>" + d.strftime("%Y-%m-%d %H:%M:%S") + "</small>";
				ws.send('{"type":"msg", "data":"' + cont + '"}');
		
	return;

def userNumBroadcast():
	global wss;

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler);
	server.serve_forever();
