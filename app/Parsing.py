from datetime import datetime

from pyexpat.errors import messages

from Services import MessageService, MediaService
from config import client

group = {
        "grouped_id": None,
        "message_id": None
    }

async def parsing(channel_name: str, offset_date: datetime, limit: int):
    all_messages_during_period = None
    if limit is None:
        all_messages_during_period = client.iter_messages(channel_name, offset_date=offset_date)
    elif offset_date is None:
        all_messages_during_period = client.iter_messages(channel_name, limit=limit)

    if all_messages_during_period is not None:
        async for message in all_messages_during_period:
            if message.grouped_id is None:
                new_message_id = await MessageService.save_message_to_db(message=message, channel_name=channel_name)
                if new_message_id is not None:
                    await MediaService.save_media(channel_name=channel_name, message=message, new_message_id=new_message_id)
            else:
                if group["grouped_id"] == message.grouped_id:
                    await MediaService.save_media(channel_name=channel_name, message=message, new_message_id=new_message_id)
                else:
                    new_message_id = await MessageService.save_message_to_db(message=message, channel_name=channel_name)
                    group["grouped_id"] = message.grouped_id
                    group["message_id"] = new_message_id
                    # если grouped_id != None --- то по-любому есть медиа и new_message_id != None
                    if new_message_id is not None:
                        await MediaService.save_media(channel_name=channel_name, message=message,
                                                      new_message_id=new_message_id)