import os
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template

import datetime
import locale
import json, hashlib

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
		broadcast('{"type":"userNum", "data":"' + str(len(wss)) + '"}');
		while True:
			message = websock.receive();

			if message is None:
				wss.remove(websock);
				broadcast('{"type":"userNum", "data":"' + str(len(wss)) + '"}');
				break;
			else:
				try :
					postedDataJson = json.loads(message);
				except:
					emsg = "<p>ERROR : Sorry but we can't accept your message. (E0)</p>";
					senderr(emsg, websock);
					continue;
				if (postedDataJson['type'] == 'post'):
					if 'msg' not in postedDataJson :
						continue;
					if postedDataJson['msg'] == '' :
						emsg = "<p>ERROR : Sorry but you must write comment.</p>";
						senderr(emsg, websock);
						continue;
					if 'script' in postedDataJson['msg'].lower() :
						emsg = "<p>ERROR : Sorry but we can't accept your message. (E1)</p>";
						senderr(emsg, websock);
						continue;

					handlename = '';
					if 'name' in postedDataJson :
						if '@' in postedDataJson['name'] or '<' in postedDataJson['name'] or '>' in postedDataJson['name']:
							emsg = "<p>ERROR : Sorry but you can't use '@' or '<' or '>' in your handlename.</p>";
							senderr(emsg, websock);
							continue;

						handlename = 'from:' + postedDataJson['name'];

						if 'id' in postedDataJson :
							m = hashlib.md5();
							try:
								m.update(postedDataJson['id']);
								handlename = handlename + '@' + m.hexdigest();
							except:
								emsg = "<p>ERROR : Sorry but we can't accept your hash id.</p>";
								senderr(emsg, websock);
								continue;

					postNo += 1;
					d = datetime.datetime.today();

					cont = "<p>" + postedDataJson['msg'] + "</p>" + "<small>" + d.strftime("%Y-%m-%d %H:%M:%S") + " " + handlename + "</small>" + "<small>PostNo : " + str(postNo) + "</small>";
					broadcast('{"type":"msg", "data":"' + cont + '"}');
	return;

def senderr(emsg, sock):
	sock.send('{"type":"err", "data":"' + emsg + '"}');

def broadcast(msg):
	global wss;
	for ws in wss:
		ws.send(msg);

if __name__ == '__main__':
	server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler);
	server.serve_forever();
