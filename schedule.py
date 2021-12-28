from apscheduler.schedulers.blocking import BlockingScheduler
from linebot.models import TextMessage
from mongodb_function import *
import datetime

from app import line_bot_api

import requests

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=17, minute=23)
def timed_job():
    date = date_alarm()
    d = str(datetime.date.today())
    if len(date) !=0:
        line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66', TextMessage(text='您所存放的\n' + date + '\n已於今日' + d + '到期!'))



# @sched.scheduled_job('cron', minute='*/25')
# def scheduled_job():
#     url = "https://testmessaging.herokuapp.com/"
#     res = requests.get(url)
#
#     if res.status_code == 200:
#         print('喚醒成功')
#     else:
#         print('喚醒失敗')


sched.start()