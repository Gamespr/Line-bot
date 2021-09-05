import re

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'YQJ26AsjvoDBTkuqYbP6281pZAH9r4t/cug2ksK4kzlKr3A8q6IqpqlMCzedNCnc7H7MXMKsMFJD4zneB28tcxmnPyr349Qzcure6uMZ1kToizonoFKqt2Xo4kul/K5yv+tHMIOVjgwNF4vt31P1wAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('25ab4833a4b0be3cddc433b35d4291b7')
# Channel ID & push message
line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66', TextMessage(text='測試用指令:\n圖片\n選單\n多重選單'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if re.match('圖片', msg):
        image_message = ImageSendMessage(
            original_content_url='https://cdn.discordapp.com/attachments/756823911768916019/883613032935198722/image0.jpg',
            preview_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883627319581888512/image0.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif re.match('選單', msg):
        template_btnmsg = TemplateSendMessage(      #選單按鈕最多4個
            alt_text='此為選單介紹,看不到',  # 此介紹給開發者看的,使用者看不到
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883627319581888512/image0.jpg',
                title='此為標題',
                text='選單功能 - TemplateSendMessage',
                actions=[
                    PostbackAction(
                        label='偷偷傳資料',
                        display_text='檯面上',
                        data='action=檯面下' #這行才是真的傳送資料
                    ),
                    MessageAction(
                        label='光明正大傳資料',
                        text='這就是資料'
                    ),
                    URIAction(
                        label='網址連結',
                        uri='https://www.youtube.com/watch?v=CJ0Xqx5Wu4M'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_btnmsg)
    elif re.match('多重選單', msg):
        carousel_template_msg = TemplateSendMessage(
            alt_text='介紹部分',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(         #按鈕數量最多三個
                        thumbnail_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883613032935198722/image0.jpg',
                        title='標題部分',
                        text='小簡介',
                        actions=[
                            MessageAction(
                                label='練習內容',
                                text='line bot 多重選單'
                            ),
                            URIAction(
                                label='網址連結',
                                uri='https://www.youtube.com/watch?v=CJ0Xqx5Wu4M'
                            )
                        ]
                    ),
                    CarouselColumn(  # 按鈕數量最多三個
                        thumbnail_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883627319581888512/image0.jpg',
                        title='標題部分',
                        text='小簡介',
                        actions=[
                            MessageAction(
                                label='練習內容',
                                text='line bot 多重選單'
                            ),
                            URIAction(
                                label='網址連結',
                                uri='https://www.youtube.com/watch?v=y4_R2OYZWUc'
                            )
                        ]
                    ),
                    CarouselColumn(  # 按鈕數量最多三個
                        thumbnail_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883985965897633822/image0.jpg',
                        title='標題部分',
                        text='小簡介',
                        actions=[
                            MessageAction(
                                label='練習內容',
                                text='line bot 多重選單'
                            ),
                            URIAction(
                                label='網址連結',
                                uri='https://www.youtube.com/watch?v=Ab8hOwRKXu0'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_msg)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='這是重複訊息 ' + msg))


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
