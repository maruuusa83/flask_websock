import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import datetime
import locale

app = Flask(__name__);

wss = [];
postNo = 1;

@app.route('/')
def index():
	return render_template('index.html');


@app.route('/echo')
def echo():
	global wss;
	global postNo;
	if request.environ.get('wsgi.websocket'):
		websock = request.environ['wsgi.websocket'];
		wss.append(websock);
		for ws in wss:
			ws.send('{"type":"userNum", "data":"' + str(len(wss)) + '"}');
		while True:
			message = websock.receive();
			postNo += 1;
			if message is None:
				wss.remove(websock);
				num = 1;
				for ws in wss:
					ws.send('{"type":"userNum", "data":"' + str(len(wss)) + '"}');
				break;
			for ws in wss:
				d = datetime.datetime.today();
				cont = "<p>" + message + "</p>" + "<small>" + " PostNo:" + str(postNo) + "  Date:" + d.strftime("%Y-%m-%d %H:%M:%S") + "</small>";
				ws.send('{"type":"msg", "data":"' + cont + '"}');
		
	return;

def broadcast(msg):
	global wss;
	for ws in wss:
		ws.send(msg);

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler);
	server.serve_forever();
