#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


calculate_funcs = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
    'div': lambda x, y: x // y,
}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_query = parse_qs(parsed_path.query)
        path_elements = parsed_path.path.split('/')[1:]

        func_name = path_elements[0]
        if func_name not in calculate_funcs:
            self.send_response(404)
            self.end_headers()
            return

        func = calculate_funcs[func_name]
        try:
            arguments = [int(x) for x in path_elements[1:]]
        except:
            self.send_response(400)
            self.end_headers()
            return

        if len(arguments) != len(func.__code__.co_varnames):
            self.send_response(404)
            self.end_headers()
            return

        try:
            result = func(*arguments)
            self.send_response(200)
            self.end_headers()
            self.wfile.write('{}\n'.format(result).encode('utf-8'))
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
