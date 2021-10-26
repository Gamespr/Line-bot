from apscheduler.schedulers.blocking import BlockingScheduler
from linebot.models import TextMessage


from app import line_bot_api

import requests

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=14, minute=55)
def timed_job():
    line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66', TextMessage(text='測試成功!'))


@sched.scheduled_job('cron', minute='*/28')
def scheduled_job():
    url = "https://testmessaging.herokuapp.com/"
    res = requests.get(url)

    if res.status_code == 200:
        print('喚醒成功')
    else:
        print('喚醒失敗')


sched.start()