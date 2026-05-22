import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

#気象庁のデータ取得
import requests
jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"

def get_forecast_summary():
    response = requests.get(jma_url)
    data = response.json()
    
    # 1. きょうの風の予報（一番最初のデータ）
    wind_text = data[0]['timeSeries'][0]['areas'][0]['winds'][0]
    
    # 2. きょうの最高気温（エリアの temps のうち、日中データの位置を指定）
    # 朝のデータでは、1番目に今日の最高気温が入ります
    max_temp = data[0]['timeSeries'][2]['areas'][0]['temps'][1]
    
    # 3. あすの最低気温（翌朝のデータ）
    # 朝のデータでは、2番目に明日の最低気温が入ります
    tomorrow_min = data[0]['timeSeries'][2]['areas'][0]['temps'][2]
    
    return {
        "max": max_temp,
        "wind": wind_text,
        "tomorrow_min": tomorrow_min
    }

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature')
    handler.handle(body, signature)
    return 'OK'

# 4. LINEでメッセージを受け取ったときの処理
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    res = get_forecast_summary()
    reply_text = (
        f"【大阪の朝予報】\n"
        f"☀️きょうの最高気温: {res['max']}℃\n"
        f"🌙あすの最低気温: {res['tomorrow_min']}℃\n"
        f"🍃きょうの風: {res['wind']}")
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
