# book_server.py
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote


class BookStore:
    def __init__(self):
        self.books = {}

    def add(self, title, available=True):
        self.books[title] = available

    def get(self, title):
        if title in self.books:
            return {"title": title, "available": self.books[title]}
        return None

    def clear(self):
        self.books.clear()


store = BookStore()


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence server logs so Behave output stays clean.
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/")

        if len(parts) == 2 and parts[0] == "books":
            title = unquote(parts[1])
            book = store.get(title)

            if book is not None:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(book).encode())
                return

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Book not found"}).encode())
            return

        self.send_response(404)
        self.end_headers()


def make_server(host="127.0.0.1", port=8765):
    return HTTPServer((host, port), RequestHandler)
