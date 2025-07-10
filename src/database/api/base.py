from ..base import Database
from ..models import XUIConfigModel

from typing import Any, Optional
from sqlalchemy import select, insert, update


class XUIConfigsAPI:
      def __init__(self, db: Database):
         self.db = db
     
      async def add_config(self, chat_id: int, client_id: str, config_key: str, expires_time: int) -> None:
         statement = insert(XUIConfigModel).values(
            chat_id=chat_id,
            client_id=client_id,
            config_key=config_key,
            expires_time=expires_time
         )

         await self.db.execute(statement=statement)

      async def get_configs(self, **kwargs: Any) -> XUIConfigModel:
         statement = select(XUIConfigModel).filter_by(**kwargs)
        
         return await self.db.execute(statement=statement, fetch='all')