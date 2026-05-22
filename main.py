import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

#気象庁のデータ取得
import requests
url = "https://api.open-meteo.com/v1/forecast?latitude=34.6938&longitude=135.5011&daily=temperature_2m_max,wind_speed_10m_max&hourly=temperature_2m,relative_humidity_2m,precipitation&timezone=Asia%2FTokyo&forecast_days=3"

def get_forecast_summary():
    response = requests.get(url)
    data = response.json()
    
    # 1. 今日の最高気温 (dailyの0番目)
    max_temp = data['daily']['temperature_2m_max'][0]
    
    # 2. 今日の最大風速 (dailyの0番目)
    max_wind = data['daily']['wind_speed_10m_max'][0]
    
    # 3. 今日の夜21時の気温 (hourlyリストの21番目)
    night_temp = data['hourly']['temperature_2m'][21]
    
    return {
        "max": max_temp,
        "wind": max_wind,
        "night": night_temp
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
    reply_text = f"【大阪の予報】\n最高気温: {res['max']}℃\n夜21時の気温: {res['night']}℃\n最大風速: {res['wind']} km/h"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
