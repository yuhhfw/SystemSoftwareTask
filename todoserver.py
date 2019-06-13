#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

API = "api";
V1 = "v1";
EVENT = "event";
DEADLINE = "deadline";
TITLE = "title";
MEMO = "memo";
STATUS = "status";
SUCCESS = "success";
FAILURE = "failure";
MESSAGE = "message";
REGGISTERED = "registered";
INVALID_DATE_FORMAT = "invalid date format";
INVALID_EVENT_FORMAT = "invalid event format";
ID = "id";
EVENTS = "events";
event_data = {EVENTS: []}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]

        #返すやつの設定
        if len(path_elements) > 3:
            try:
                id = int(path_elements[3])
                events = event_data[EVENTS]
                if id < 0 or len(events) <= id:
                    self.send_response(404)
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.end_headers()
                    if events[id] != None:
                        js_response = json.dumps(events[id])
                        self.wfile.write('{}\n'.format(js_response).encode('utf-8'))
            # intじゃなかったとか
            except ValueError as e:
                print(e)
                self.send_response(400)
                self.end_headers()
        else:
            # id指定なし
            self.send_response(200)
            self.end_headers()
            if event_data != None:
                js_response = json.dumps(event_data)
                self.wfile.write('{}\n'.format(js_response).encode('utf-8'))
        return


    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_elements = parsed_path.path.split('/')[1:]
        response = {}
        if len(path_elements) < 3:
            self.send_response(404)
            self.end_headers()
            return
        else:
            if path_elements[:3] == [API, V1, EVENT]:
                pass
            else:
                print("koko")
                self.send_response(404)
                self.end_headers()
            return

        # 入力部
        try:
            content_len = int(self.headers.get('content-length'))
            event = json.loads(self.rfile.read(content_len).decode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            return

        # 内容チェック
        if (DEADLINE or TITLE or MEMO) in event.keys():
            # if iso_to_jstdt(event[DEADLINE]) == None:
            if not "{0:%Y-%m-%dT%H:%M:%S%z}".format.match(event[DEADLINE]):
                # 日付入力ミス
                response = {STATUS: FAILURE, MESSAGE: INVALID_DATE_FORMAT}
                self.send_response(200)
                self.end_headers()
                if response != None:
                    js_response = json.dumps(response)
                    self.wfile.write('{}\n'.format(js_response).encode('utf-8'))
                    self.send_response(response)
            else:
                # 入力成功
               id = len(event_data[EVENTS])
               event[ID] = id
               event_data[EVENTS].append(event)
               response = {STATUS: SUCCESS, MESSAGE: REGGISTERED, ID: id}
               self.send_response(200)
               self.end_headers()
               if response != None:
                    js_response = json.dumps(response)
                    self.wfile.write('{}\n'.format(js_response).encode('utf-8'))
        else:
            # 入力ミス
            response = {STATUS: FAILURE, MESSAGE: INVALID_EVENT_FORMAT}
            self.send_response(200)
            self.end_headers()
            if response != None:
                js_response = json.dumps(response)
                self.wfile.write('{}\n'.format(js_response).encode('utf-8'))
        return

class UpdateServer(HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()


def main():
    with UpdateServer(('', 8080), RequestHandler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
