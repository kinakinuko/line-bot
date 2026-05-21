{\rtf1\ansi\ansicpg932\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
from flask import Flask, request\
from linebot import LineBotApi, WebhookHandler\
from linebot.models import MessageEvent, TextMessage, TextSendMessage\
\
app = Flask(__name__)\
\
# \uc0\u12373 \u12387 \u12365 \u35211 \u12388 \u12369 \u12383 \u12300 2\u12388 \u12398 \u37749 \u12301 \u12434 \u12371 \u12371 \u12391 \u35501 \u12415 \u36796 \u12415 \u12414 \u12377 \
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))\
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))\
\
# LINE\uc0\u12363 \u12425 \u12513 \u12483 \u12475 \u12540 \u12472 \u12364 \u23626 \u12367 \u12300 \u36890 \u12426 \u36947 \u12301 \
@app.route("/callback", methods=['POST'])\
def callback():\
    body = request.get_data(as_text=True)\
    signature = request.headers.get('X-Line-Signature')\
    handler.handle(body, signature)\
    return 'OK'\
\
# \uc0\u12513 \u12483 \u12475 \u12540 \u12472 \u12434 \u21463 \u20449 \u12375 \u12383 \u12392 \u12365 \u12398 \u20966 \u29702 \
@handler.add(MessageEvent, message=TextMessage)\
def handle_message(event):\
    user_text = event.message.text  # \uc0\u24066 \u24029 \u12373 \u12435 \u12364 \u36865 \u12387 \u12383 \u25991 \u23383 \
    \
    # \uc0\u36820 \u20107 \u12398 \u25991 \u31456 \u65288 \u8251 \u12371 \u12371 \u12434 \u24460 \u12363 \u12425 \u22825 \u27671 \u12398 \u35336 \u31639 \u12394 \u12393 \u12395 \u26360 \u12365 \u25563 \u12360 \u12414 \u12377 \u65281 \u65289 \
    reply_text = f"\uc0\u12300 \{user_text\}\u12301 \u12391 \u12377 \u12397 \u65281 \u25215 \u30693 \u12356 \u12383 \u12375 \u12414 \u12375 \u12383 \u12290 "\
    \
    # LINE\uc0\u12395 \u12362 \u36820 \u20107 \u12434 \u36865 \u12426 \u36820 \u12377 \
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))\
\
if __name__ == "__main__":\
    app.run(host="0.0.0.0", port=5000)}