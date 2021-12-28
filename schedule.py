from apscheduler.schedulers.blocking import BlockingScheduler
from linebot.models import TextMessage
from mongodb_function import *
import datetime

from app import line_bot_api

import requests

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18, minute=35)
def timed_job():
    date = date_alarm()
    adv_date = date_adv()
    d = str(datetime.date.today())
    d1 = str(datetime.date.today() + datetime.timedelta(days=2))
    if len(adv_date) != 0:
        line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66',TextMessage(text='您所存放的\n' + date + '\n再過2日於' + d1 + '到期!'))
    if len(date) !=0:
        line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66', TextMessage(text='您所存放的\n' + date + '\n已於今日' + d + '到期!\n請處理完食品後，於選單點選處理食品輸入已處理完的食品資訊'))



@sched.scheduled_job('cron', minute='*/25')
def scheduled_job():
    url = "https://testmessaging.herokuapp.com/"
    res = requests.get(url)

    if res.status_code == 200:
        print('喚醒成功')
    else:
        print('喚醒失敗')


sched.start()