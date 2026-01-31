from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker 
from sqlalchemy.orm import DeclarativeBase
import os
DB_URL = "sqlite+aiosqlite:///./hospetal.db"
engine = create_async_engine(DB_URL , echo=True)
LocalSesion = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with LocalSesion() as session:
        yield session
        

Media_dir = "media"
os.makedirs(Media_dir,exist_ok=True)