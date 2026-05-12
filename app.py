from flask import Flask, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>정보 확인</title>
</head>
<body style="font-family:sans-serif;text-align:center;padding-top:50px;">

<h1>접속 정보를 확인하는 중...</h1>

<script>
(async () => {

    const data = {
        브라우저: navigator.userAgent,
        언어: navigator.language,
        운영체제: navigator.platform,

        화면크기: {
            가로: screen.width,
            세로: screen.height
        },

        인터넷상태: navigator.onLine ? "온라인" : "오프라인",

        시간대: Intl.DateTimeFormat().resolvedOptions().timeZone,

        접속시간: new Date().toLocaleString()
    };

    await fetch('/collect', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    document.body.innerHTML = "<h1>완료!</h1>";

})();
</script>

</body>
</html>
"""

@app.route("/")
def index():

    info = {
        "접속 시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IP 주소": request.headers.get("X-Forwarded-For", request.remote_addr),
        "접속 방식": request.method,
        "접속 경로": request.path,
        "브라우저": str(request.user_agent),
    }

    print("\n===== 서버 정보 =====")
    print(json.dumps(info, indent=4, ensure_ascii=False))

    return PAGE


@app.route("/collect", methods=["POST"])
def collect():

    print("\n===== 기기 정보 =====")
    print(json.dumps(request.get_json(), indent=4, ensure_ascii=False))

    return jsonify({"결과": "성공"})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
  
