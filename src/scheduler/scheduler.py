from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from src.core import settings
from .jobs import cache_exchange_rates

     
async def start_scheduler():
   scheduler = AsyncIOScheduler()
   
   scheduler.add_job(func=cache_exchange_rates, trigger='interval', 
                     hours=1, next_run_time=datetime.now())
   
   scheduler.start()