from sqlite3 import IntegrityError

from database.models import async_session, Media_info, MessageInfo
from sqlalchemy import select, update, delete, BigInteger

async def add_photo(message_db_id: int, file_path: str, media_type: str):
    async with async_session() as session:
        session.add(Media_info(media_type=media_type, file_path=file_path, message_db_id=message_db_id))
        await session.commit()

async def add_message(sender_id: str, message_id: int, channel_name: str, date: str, text: str, text_len: int, media: bool, has_emoji: bool, views: int, forwards: int, reactions: str):
    async with async_session() as session:
        new_message = MessageInfo(
            sender_id=int(sender_id, 16),
            message_id = message_id,
            channel_name=channel_name,
            date=date,
            text=text,
            text_len=text_len,
            media = media,
            has_emoji=has_emoji,
            views=views,
            forwards=forwards,
            reactions=reactions
        )
        session.add(new_message)
        await session.flush() #Метод flush() заставляет SQLAlchemy отправить INSERT-запрос в базу, не коммитя транзакцию.
        await session.commit()
        return new_message.id

