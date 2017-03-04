import socket, threading, os
from urlparse import urlparse, parse_qs
import handler
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8080           # Arbitrary non-privileged port
STATIC_PATH = "./"

urlMapper = dict()

def getType(path):
    if path.endswith('.js'):
	return 'application/javascript'
    elif path.endswith('.html'):
	return 'text/html'
    elif path.endswith('.css'):
        return 'text/css'
    elif path.endswith('.jpeg'):
        return 'image/jpeg'
    elif path.endswith('.jpg'):
        return 'image/jpeg'
    elif path.endswith('.png'):
        return 'image/png'
    elif path.endswith('.gif'):
        return 'image/gif'
    elif path.endswith('.ttf'):
        return 'application/x-font-ttf'
    elif path.endswith('.woff'):
        return 'application/font-woff'
    elif path.endswith('.woff2'):
        return 'application/font-woff2'
    else:
	return 'text/html'


def response(conn, status, content, res_type):
    if status == 200 :
	res  = 'HTTP/1.0 200 OK\r\nContent-Type: ' + res_type + ';' +'\r\n\r\n' + content
    else:
        res  = 'HTTP/1.0 404 Not Found\r\nContent-Type: text/html;\r\n\r\n'
    conn.sendall(res)
    conn.close()
 


def staticRes(path):
    res = os.path.join(os.getcwd(), path[1:])
    exists = os.path.exists(res)
    print res, exists
    if exists:
        option = "rb"
        if getType(path).startswith("text"):
            option = "r"
        f = open(res, option)
        content = f.read()
	return (True, content)
    return (False, None)
    
    
def router(conn, verb, path, query):
    if path == "/":
        path = "/index.html"
    parsedObj = urlparse(path)
    path = parsedObj.path
    queryFromUrl = parsedObj.query
    if verb == 'get' or verb == 'GET' and queryFromUrl!= '':
        query = queryFromUrl
    res_type = getType(path)
    if path in urlMapper:
        func = urlMapper[path]
        qs = parse_qs(query)
        content = func(verb, path, qs)
        response(conn, 200, content, res_type)
    else:
        (exists, content) = staticRes(path)
        if exists:
            response(conn, 200, content, res_type)
        else:
            response(conn, 404, None, res_type)

def serve(conn):
    data = conn.recv(4096)
    split_data = data.split("\r\n")
    print split_data
    if len(split_data) < 1:
	return;
    #print split_data
    reqLine = split_data[0].split()
    verb = reqLine[0]
    path = reqLine[1]
    protocol = reqLine[2]
    query = split_data[-1]
    router(conn, verb, path, query)


def webServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    handler.register(urlMapper)
    while True:
        conn, addr = s.accept()
        print 'Connected by', addr
        t = threading.Thread(target = serve, args = (conn,))
        t.start()
    s.close()

webServer()
