from apscheduler.schedulers.background import BackgroundScheduler
from models.tokens.session_tokens import SessionTokens
from models.tokens.registration_tokens import RegistrationTokens


def create_cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=SessionTokens.remove_expired_tokens, trigger="interval", seconds=60)
    scheduler.add_job(func=RegistrationTokens.remove_expired_tokens, trigger="interval", seconds=60)
    return scheduler
