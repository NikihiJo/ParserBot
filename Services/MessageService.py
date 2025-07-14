import database.requests as rq
from telethon.tl.types import Message
from Services.ReactionService import reactions_to_json

async def save_message_to_db(message: Message, channel_name: str) -> int | None:
    try:
        new_message_id = await rq.add_message(
            sender_id = str(message.peer_id.channel_id),
            message_id=message.id,
            channel_name = channel_name,
            date = message.date.isoformat(),
            text = message.message,
            text_len=len(message.message),
            media = message.media is not None,
            #-------------Emoji------------------------------------------------------------------------
            has_emoji = (len(message.reactions.results) != 0 if message.reactions is not None else False), #защита от блокировки реакций
            # -------------------------------------------------------------------------------------
            views = message.views,
            forwards = message.forwards,
            # -------------Emoji------------------------------------------------------------------------
            reactions = (reactions_to_json(message.reactions) if message.reactions is not None else '') #защита от блокировки реакций
            # -------------------------------------------------------------------------------------
        )
        if message.media is not None:
            return new_message_id
        else:
            return None
    except Exception as e:
        print(f"Exception: {e}")

