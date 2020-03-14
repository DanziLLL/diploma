import schedule
from models.session_tokens import SessionTokens


def create_cron():
    schedule.every(1).minutes.do(SessionTokens.remove_expired_tokens())
