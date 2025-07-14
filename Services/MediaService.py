import os
from config import media_dirts, download_dirt
from telethon.tl.types import Message
import database.requests as rq
import mimetypes
import os


def get_file_extension(msg: Message) -> str | None:
    if msg.document:
        if msg.document.attributes:
            for attr in msg.document.attributes:
                if hasattr(attr, 'file_name'):
                    _, ext = os.path.splitext(attr.file_name)
                    if ext:
                        return ext.lower()
        # Если имя не найдено, пробуем по mime-type
        mime_type = msg.document.mime_type
        if mime_type:
            ext = mimetypes.guess_extension(mime_type)
            if ext:
                return ext
        return '.bin'
    elif msg.photo:
        return '.jpg'  # всегда JPG
    elif msg.sticker:
        mime = msg.document.mime_type
        if mime == 'application/x-tgsticker':
            return '.tgs'
        elif mime == 'video/webm':
            return '.webm'
        else:
            return '.webp'
    elif msg.gif:
        return '.mp4'  # gif пересылается как сжатое mp4
    elif msg.audio:
        mime = msg.document.mime_type
        return mimetypes.guess_extension(mime) or '.mp3'
    elif msg.video:
        mime = msg.document.mime_type
        return mimetypes.guess_extension(mime) or '.mp4'
    return None

MEDIA_TYPES = [ #Список кортежей с lambda
    ('photo', lambda m: m.photo),
    ('video', lambda m: m.video),
    ('audio', lambda m: m.audio),
    ('sticker', lambda m: m.sticker),
    ('animation', lambda m: m.gif),
    ('document', lambda m: m.document),
]
'''
def bild_path(channel_name, message_id):
    return os.path.join(download_dir, channel_name, f'photo_{message_id}.jpg')

async def download_photo(message, path):
    await message.download_media(file=path)
    return path

async def save_to_db(message, path):
    try:
        await rq.add_photo(
            media_type = "photo",
            file_path=path,
            message_id = message.id
        )
    except Exception as e:
        print(f"Exception: {e}")
'''


#----------------------------------PHOTO--------------------------------------------
async def save_media(channel_name, message, new_message_id):
    media_type = next((name for name, check in MEDIA_TYPES if check(message)), None)
    if media_type is not None:
        file_path = os.path.join(download_dirt, channel_name, media_dirts[media_type], f'{message.id}.{get_file_extension(message)}')
        try:
            await message.download_media(file=file_path)
            await rq.add_photo(
                media_type=media_type,
                file_path = file_path.decode('utf-8') if isinstance(file_path, bytes) else str(file_path),
                message_db_id=new_message_id #сохраняем айди записи в бд
            )

        except Exception as e:
            print(f"Exception: {e}")