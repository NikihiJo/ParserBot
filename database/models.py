from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Media_info(Base):
    __tablename__ = 'medias_info'
    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str] = mapped_column(String(15))
    file_path: Mapped[str] = mapped_column(String(50))
    message_db_id: Mapped[int] = mapped_column(ForeignKey("messages_info.id"))

class MessageInfo(Base):
    __tablename__ = "messages_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column()
    channel_name: Mapped[str] = mapped_column(String(30))
    date: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(String)
    text_len: Mapped[int] = mapped_column()
    media: Mapped[bool] = mapped_column()
    has_emoji: Mapped[bool] = mapped_column()
    views: Mapped[int] = mapped_column()
    forwards: Mapped[int] = mapped_column()
    reactions: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
