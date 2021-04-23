# Run python server on a different thread
import http.server
import socketserver
import os
from pathlib import Path


def run_local_server(port=8000):
    path = Path(os.path.dirname(__file__))
    web_dir = os.path.join(path.parent.parent.absolute(), "hosted_stats")
    os.chdir(web_dir)
    socketserver.TCPServer.allow_reuse_address = True  # required for fast reuse !
    """
    Check out :
    https://stackoverflow.com/questions/15260558/python-tcpserver-address-already-in-use-but-i-close-the-server-and-i-use-allow
    """
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("Creating server at port", port)
    httpd.serve_forever()


def main():
    run_local_server(port=8499)


if __name__ == "__main__":
    main()