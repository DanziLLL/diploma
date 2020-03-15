from apscheduler.schedulers.background import BackgroundScheduler
from models.session_tokens import SessionTokens


def create_cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=SessionTokens.remove_expired_tokens, trigger="interval", seconds=60)
    return scheduler
