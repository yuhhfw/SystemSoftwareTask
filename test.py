from multiprocessing import Process
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from todoserver import PORT, API, V1, EVENT, StoppableServer, RequestHandler
import json
import pytest

# ref https://github.com/malony0/pbl.TODOServer/blob/master/test_server.py

URL = "http://localhost:"+str(PORT)+'/'+API+'/'+V1+'/'+EVENT
headers = {"Content-Type" : "application/json",}

def f():
    with UpdateServer(('', PORT), RequestHandler) as server:
        server.serve_forever()
        return server

def test_all():
    p = Process(target=f, args=())
    p.start()
    POST_valid()
    POST_invalid()
    GET_all()
    GET_id_valid()
    GET_id_invalid()
    p.terminate()
    p.join()


## POST
def POST_valid():
    valid_data = {"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}
    req = Request(URL, json.dumps(valid_data).encode(), headers)
    with urlopen(req) as res:
        body = json.load(res)
        assert res.getcode() == 200
        assert body["status"] == "success"
        assert body["message"] == "registered"
        return
    assert False

def POST_invalid():
    invalid_data = {"deadline": "2019/06/11T14:00:00", "title": "レポート提出", "memo": ""}
    req = Request(URL, json.dumps(invalid_data).encode(), headers)
    try:
        urlopen(req)
    except HTTPError as e:
        assert e.code == 400
        return
    except URLError as e:
        pass
    assert False

### GET
def GET_all():
    req = Request(URL)
    with urlopen(req) as res:
        body = json.load(res)
        assert res.getcode() == 200
        assert type(body["events"]) == list

def GET_id_valid():
    # idによるevent取得
    body = json.load(urlopen(Request(URL)))
    maxId = len(body["events"])-1
    if (maxId < 1):
        # 最低1つイベントを発生
        valid_data = {"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}
        req = Request(URL, json.dumps(valid_data).encode(), headers)
        with urlopen(req) as res:
        assert res.getcode() == 200
        valid_data = {"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}
        req = Request(URL, json.dumps(valid_data).encode(), headers)
        with urlopen(req) as res:
        assert res.getcode() == 200
        body = json.load(urlopen(Request(URL)))
        maxId = len(body["events"])-1
    
    # test
    minReq = URL + '/' + str(0)
    maxReq = URL + '/' + str(maxId)
    with urlopen(minReq) as res:
        body = json.load(res)
        assert res.getcode() == 200
        assert type(body) == dict
    with urlopen(maxReq) as res:
        body = json.load(res)
        assert res.getcode() == 200
        assert type(body) == dict

def GET_id_invalid():
    # event数取得
    maxId = -1
    
    # test
    minReq = URL + '/' + str(-1)
    maxReq = URL + '/' + str(maxId)
    try:
        res = urlopen(minReq)
    except HTTPError as e:
        assert e.code == 404
    else:
        assert False

    try:
        res = urlopen(maxReq)
    except HTTPError as e:
        assert e.code == 404
    else:
        assert False    