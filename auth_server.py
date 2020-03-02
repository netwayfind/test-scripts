import argparse
import base64

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

class RequestHandler(SimpleHTTPRequestHandler):
    TOKEN = ''
    USERNAME = ''
    PASSWORD = ''
    BASIC_AUTH = ''
    COOKIE = ''

    def do_POST(self):
        try:
            body_len = int(self.headers['Content-Length'])
        except Exception:
            body_len = 0
        if body_len <= 0:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(bytes('unauthorized\n', 'UTF-8'))
            return
        body = self.rfile.read(body_len)
        print(body)
        body = str(body, 'UTF-8')
        if body == 'username=' + self.USERNAME + '&password=' + self.PASSWORD:
            self.send_response(200)
            self.send_header('Set-Cookie', 'session=' + self.COOKIE)
            self.end_headers()
            self.wfile.write(bytes('success login\n', 'UTF-8'))
            return
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes('unauthorized\n', 'UTF-8'))
    
    def do_GET(self):
        try:
            auth_header = self.headers['Authorization']
        except KeyError:
            auth_header = None
        try:
            cookie = self.headers['Cookie']
        except KeyError:
            cookie = None
        if auth_header is None and cookie is None:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Test"')
            self.end_headers()
            self.wfile.write(bytes('unauthorized\n', 'UTF-8'))
            return
        elif auth_header == 'Basic ' + self.BASIC_AUTH:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('success with basic auth\n', 'UTF-8'))
            return
        elif auth_header == 'Bearer ' + self.TOKEN:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('success with bearer token\n', 'UTF-8'))
            return
        elif cookie == 'session=' + self.COOKIE:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('success with cookie\n', 'UTF-8'))
            return
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes('unauthorized\n', 'UTF-8'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port')
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('bearer')
    parser.add_argument('cookie')
    args = parser.parse_args()

    RequestHandler.USERNAME = args.username
    RequestHandler.PASSWORD = args.password
    print('Username: ' + RequestHandler.USERNAME + ', Password: ' + RequestHandler.PASSWORD)
    RequestHandler.BASIC_AUTH = str(base64.b64encode(bytes(args.username + ':' + args.password, 'UTF-8')), 'UTF-8')
    print('Basic auth: ' + RequestHandler.BASIC_AUTH)
    RequestHandler.TOKEN = args.bearer
    print('Bearer token: ' + RequestHandler.TOKEN)
    RequestHandler.COOKIE = args.cookie
    print('Cookie: ' + RequestHandler.COOKIE)
    
    http_server = TCPServer(('', int(args.port)), RequestHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    main()