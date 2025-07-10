from contextlib import asynccontextmanager
from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core import settings
from .models import Base


class Database:
    def __init__(self): 
        self.async_engine = create_async_engine(url=settings.database_dsn, echo=False)
        self.async_session_maker = async_sessionmaker(bind=self.async_engine)

    async def init_models(self):
        async with self.async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session_maker() as session:
            yield session
            
    async def _execute_with_result(self, session: AsyncSession, statement: Any, fetch: str) -> Any:
        result = await session.execute(statement=statement)
        
        if fetch == 'one':
            return result.scalar()
        
        if fetch == 'all':
            return result.scalars().all()
    
    async def _execute_without_result(self, session: AsyncSession, statement: Any) -> Any:
        await session.execute(statement=statement)
        await session.commit()
        
    async def execute(self, statement: Any, fetch: str = None) -> Any:
        async with self.get_session() as session:
            if fetch:
                return await self._execute_with_result(session=session, statement=statement, fetch=fetch)
            
            return await self._execute_without_result(session=session, statement=statement)
        