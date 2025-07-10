import os

from dotenv import load_dotenv
from pydantic import BaseModel


for key in list(os.environ.keys()):
    if key in os.environ:
        del os.environ[key]

load_dotenv(dotenv_path='.env')


class Settings(BaseModel):
    token: str
    database_dsn: str
    news_channel_id: str
    bot_url: str
    news_channel_url: str
    supergroup_id: str
    topic_vpn_id: str
    topic_payments_id: int
    topic_events_id: int
    topic_request_id: int
    referral_lvls: list
    panel_ip: str
    panel_port: int
    panel_username: str
    panel_password: str 
    panel_path: str
    panel_session_id: str
    cryptobot_url: str
    cryptobot_secret_key: str
    yookassa_shop_id: int
    yookassa_secret_key: str

    
settings = Settings(
    token=os.getenv('TOKEN'),
    database_dsn=os.getenv('DATABASE_URL'),
    news_channel_id=os.getenv('NEWS_CHANNEL_ID'),
    news_channel_url=os.getenv('NEWS_CHANNEL_URL'),
    supergroup_id=os.getenv('SUPERGROUP_ID'),
    topic_vpn_id=os.getenv('TOPIC_VPN_ID'),
    topic_payments_id=os.getenv('TOPIC_PAYMENTS_ID'),
    topic_events_id=os.getenv('TOPIC_EVENTS_ID'),
    topic_request_id=os.getenv('TOPIC_REQUEST_ID'),
    bot_url=os.getenv('BOT_URL'),
    referral_lvls=[int(referral_lvl) for referral_lvl in os.getenv('REFERRAL_LVLS').split(',')],
    panel_ip=os.getenv('PANEL_IP'),
    panel_port=os.getenv('PANEL_PORT'),
    panel_username=os.getenv('PANEL_USERNAME'),
    panel_password=os.getenv('PANEL_PASSWORD'),
    panel_path=os.getenv('PANEL_PATH'),
    panel_session_id=os.getenv('PANEL_SESSION_ID'),
    cryptobot_url=os.getenv('CRYPTOBOT_URL'),
    cryptobot_secret_key=os.getenv('CRYPTOBOT_SECRET_KEY'),
    yookassa_shop_id=os.getenv('YOOKASSA_SHOP_ID'),
    yookassa_secret_key=os.getenv('YOOKASSA_SECRET_KEY')
)
