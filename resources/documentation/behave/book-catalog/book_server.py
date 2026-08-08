# book_server.py
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlparse


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


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Book catalog</title>
</head>
<body>
  <h1>Book catalog</h1>
  <form id="search-form">
    <input type="text" id="title" name="title" placeholder="Title" />
    <button type="submit">Search</button>
  </form>
  <div id="result"></div>
  <script>
    document.getElementById('search-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const res = await fetch('/books/' + encodeURIComponent(title));
      const result = document.getElementById('result');
      if (res.ok) {
        const data = await res.json();
        result.textContent = data.title + ' — ' + (data.available ? 'available' : 'unavailable');
      } else {
        result.textContent = 'Book not found';
      }
    });
  </script>
</body>
</html>
"""


class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
            return

        if path.startswith('/books/'):
            title = unquote(path.split('/books/', 1)[1])
            book = store.get(title)
            if book is not None:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(book).encode())
                return
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Book not found"}).encode())
            return

        self.send_response(404)
        self.end_headers()


def make_server(host='127.0.0.1', port=8765):
    return HTTPServer((host, port), RequestHandler)
