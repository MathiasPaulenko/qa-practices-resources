from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status/200':
            self.send_response(200)
        elif self.path == '/status/404':
            self.send_response(404)
        else:
            self.send_response(500)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def start_server(host='127.0.0.1', port=8765):
    server = HTTPServer((host, port), MockAPIHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def stop_server(server):
    server.shutdown()
