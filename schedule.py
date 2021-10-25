from apscheduler.schedulers.blocking import BlockingScheduler
from linebot.models import TextMessage

from app import line_bot_api

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    line_bot_api.push_message('U4ee7f6b303c39a750a7638d340149b66', TextMessage(text='測試成功!'))

sched.start()