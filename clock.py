from apscheduler.schedulers.blocking import BlockingScheduler
import twitter-listener

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    num_tweets_to_grab = 100
    retweet_count = 500
    twit = TwitterMain(num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()
