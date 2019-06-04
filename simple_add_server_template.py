#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        if path_elements[0] != 'add':
            self.send_response(404)
            self.end_headers()
            return

        try:
            arguments = [int(x) for x in path_elements[1:]]
        except:
            self.send_response(400)
            self.end_headers()
            return

        if len(arguments) != 2:
            self.send_response(404)
            self.end_headers()
            return

        try:
            # arguments の要素を足してレスポンスするコードを書く
            return
        except Exception as e:
            print(e)
            self.send_response(500)
            self.end_headers()
            return


def main():
    server = HTTPServer(('', 8080), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
