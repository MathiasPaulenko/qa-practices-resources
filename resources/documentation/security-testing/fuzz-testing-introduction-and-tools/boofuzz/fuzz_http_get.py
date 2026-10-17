"""boofuzz 0.4.2 session: fuzz the request line of an HTTP GET against a target.

Usage:
    pip install -r requirements.txt
    python fuzz_http_get.py <host> <port>
"""
import sys

from boofuzz import (
    Session, Target, TCPSocketConnection,
    s_delim, s_string, s_static, s_get, Request,
)

def build_request() -> Request:
    req = Request("http-get", children=(
        s_string("GET", name="method"),
        s_delim(" "),
        s_string("/index.html", name="uri"),
        s_delim(" "),
        s_static("HTTP/1.1\r\n"),
        s_static("Host: "),
        s_string("target", name="host-header"),
        s_static("\r\n\r\n"),
    ))
    return req

def main() -> None:
    host, port = sys.argv[1], int(sys.argv[2])
    session = Session(
        target=Target(connection=TCPSocketConnection(host, port)),
        sleep_time=0.1,
    )
    session.connect(s_get("http-get"))
    session.fuzz()

if __name__ == "__main__":
    main()
