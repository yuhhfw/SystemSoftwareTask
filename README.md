# SystemSoftwareTask

レポート課題: TODO管理サービス用のHTTPサーバを作成
pytest作成は断念
エラーが直らない
---

## 概要

- TODO イベントを POST で登録，GET で取得できる HTTP サーバを作成する．
- POST，GET ともに，データは JSON でやりとりする．（API 仕様は以下に示す）
- TODO イベントはメインメモリ上に保持するだけで良い．
- サーバプログラムの記述言語，フレームワーク等は自由．
- github.com の自分のアカウント上にソースコードを置き，Circle CI により自動テストを行う．
- 自動テストには正常系の GET，POST のテストを含めよ．
- ローカルホスト及びポートは8080

## API仕様

### イベント登録

```
# イベント登録 API request
POST /api/v1/event
{"deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}

# イベント登録 API response
200 OK
{"status": "success", "message": "registered", "id": 1}

400 Bad Request
{"status": "failure", "message": "invalid date format"}
```

### イベント取得

```
# イベント全取得 API request
GET /api/v1/event

#イベント全取得 API response
200 OK
{"events": [
    {"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""},
    ...
]}
```

```
#イベント1件取得 API request
GET /api/v1/event/${id}

#イベント1件取得 API response
200 OK
{"id": 1, "deadline": "2019-06-11T14:00:00+09:00", "title": "レポート提出", "memo": ""}

404 Not Found
```