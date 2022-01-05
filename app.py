import re
import json
from flask import render_template

import time
import requests

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from mongodb_function import *


app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi('YQJ26AsjvoDBTkuqYbP6281pZAH9r4t/cug2ksK4kzlKr3A8q6IqpqlMCzedNCnc7H7MXMKsMFJD4zneB28tcxmnPyr349Qzcure6uMZ1kToizonoFKqt2Xo4kul/K5yv+tHMIOVjgwNF4vt31P1wAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('25ab4833a4b0be3cddc433b35d4291b7')

#============================================

# @app.route("/heroku_wake_up")
# def heroku_wake_up():
#     return "Heroku Wake Up!"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/arduino_test", methods=['GET'])
def test():
    v = request.values['input_value']
    v1 = request.values['input_value1']
    line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66',TextMessage(text='偵測到食品有腐壞的跡象，請處理腐壞的相關食品!\n參數:' + v + ',' + v1))
    return 'values={},{}'.format(v, v1)

@app.route("/img_post", methods=['POST'])
def post():

    return 'success!'

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print(json.loads(body))
    print(type(body))
    print(type(json.loads(body)))
    print(json.loads(body)['events'][0]['message']['text'])
    print(type(json.loads(body)['events'][0]['message']['text']))
    # load data
    write_one_data(json.loads(body))
    print('=========date alarm========')
    date_adv()
    print('=========date alarm========')
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
    if msg == '圖片':
        image_message = ImageSendMessage(
            original_content_url='https://cdn.discordapp.com/attachments/756823911768916019/883613032935198722/image0.jpg',
            preview_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883627319581888512/image0.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    elif msg == '選單':
        template_btnmsg = TemplateSendMessage(      #選單按鈕最多4個
            alt_text='此為選單介紹,看不到',  # 此介紹給開發者看的,使用者看不到
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn.discordapp.com/attachments/756823911768916019/883627319581888512/image0.jpg',
                title='指令選單',
                text='點選下方按鈕以了解使用方式',
                actions=[
                    MessageAction(
                        label='保存食品',
                        text='保存食品'
                    ),
                    MessageAction(
                        label='查看保存食品資訊',
                        text='已保存食品資訊'
                    ),
                    MessageAction(
                        label='處理食品',
                        text='處理食品'
                    ),
                    MessageAction(
                        label='查詢指定日期資訊',
                        text='查詢指定日期資訊'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, template_btnmsg)

    elif msg == '保存食品':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請依照格式以記錄食品到期資訊。\n例如:2020-01-05 鮮奶'))

    elif msg == '處理食品':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='若已處理完指定的食品請依照格式以刪除食品資訊。\n例如:已處理2020-01-05 鮮奶'))

    elif msg == '更多資訊':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='此機器人為了有效方便管理食品，只接收與指令有關的訊息，相關功能可點擊指令清單圖示以了解使用方式。\n另外食品到期前三日以及到期日，會主動提醒並且呈現食品資訊'))

    elif msg == '查詢指定日期資訊':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請依照格式以查看指定到期日之資訊。\n例如:查看2020-01-05'))

    elif re.match('\d\d\d\d-\d\d-\d\d \w', msg):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='成功紀錄食品資訊!'))

    # MongoDB操作
    # elif msg == '@讀取':
    #     datas = read_many_datas()
    #     datas_len = len(datas)
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'資料數量，一共{datas_len}條'))


    elif msg == '已保存食品資訊':
        datas = read_chat_records()
        print(type(datas))
        text_list = []
        for data in datas:
            if re.match('\d\d\d\d-\d\d-\d\d', data):
                text_list.append(data)
        text_list.sort()
        data_text = '\n'.join(text_list)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='以下為您目前所存放的食品到期資訊:\n' + data_text + '\n\n想查詢指定到期日的話，可於指令選單中點選查詢指定日期資訊'))

    elif re.match('已處理\d\d\d\d-\d\d-\d\d \w', msg):
        deletion = delete_one_data(msg)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=deletion))

    elif re.match('查看\d\d\d\d-\d\d-\d\d',msg):
        ck = date_check(msg)
        if ck != 0:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您所查詢的' + msg[2:] + '到期的食品資續如下:\n' + ck ))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='您所查詢的日期資訊有誤，請重新檢查是否有此日期之資訊!'))

    # elif msg == '@刪除':
    #     text = delete_all_data()
    #     message = TextSendMessage(text=text)
    #     line_bot_api.reply_message(event.reply_token, message)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='以上發送的訊息無法執行有效的指令，請重新發送正確的訊息'))




import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
