import json
import re
from telethon.tl.types import ReactionEmoji, ReactionCustomEmoji, ReactionPaid

def extract_emojis(text):
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return emoji_pattern.findall(text)
#print(extract_emojis(message.message))

def reactions_to_json(reactions):
    reaction_data = {}

    if reactions:
        for rc in reactions.results:
            reaction = rc.reaction
            if isinstance(reaction, ReactionEmoji):
                key = reaction.emoticon
            elif isinstance(reaction, ReactionCustomEmoji):
                key = f"custom:{reaction.document_id}"
            elif isinstance(reaction, ReactionPaid):
                key = f'paid'
            else:
                key = "unknown"


            reaction_data[key] = rc.count

    return json.dumps(reaction_data)