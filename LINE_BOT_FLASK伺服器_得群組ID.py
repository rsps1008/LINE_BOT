from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage

app = Flask(__name__)

# 替換成你自己的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = '0fQrbKQK1LPXEK+57aDRVXOhnOMq...'
LINE_CHANNEL_SECRET = '7597fd4...'


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == "group":
        group_id = event.source.group_id
        print(f"接收到來自群組的訊息，Group ID 是：{group_id}")
        # 你也可以用這行來回覆 Group ID
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"你的群組 ID 是：{group_id}")
        )


if __name__ == "__main__":
    app.run(port=5000)
