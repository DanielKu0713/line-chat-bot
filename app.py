from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage

app = Flask(__name__)

# 請填入你的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭
    signature = request.headers['X-Line-Signature']
    
    # 獲取請求的 body
    body = request.get_data(as_text=True)
    
    try:
        # 驗證簽名
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆用戶發送的消息
    reply_message = TextSendMessage(text=f"你說：{event.message.text}")
    line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
