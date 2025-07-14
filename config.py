from telethon import TelegramClient
from aiogram import Bot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(config["BOT"]["token"])

client = TelegramClient(session="my_session",
                        api_id=config['TelegramClent']['api_id'],
                        api_hash=config['TelegramClent']['api_hash'],
                        device_model=config['TelegramClent']['device_model'],
                        system_version=config['TelegramClent']['system_version']
)



download_dirt="downloads"

media_dirts = {
    'photo': 'media/photos',
    'video': 'media/videos',
    'document': 'media/documents',
    'audio': 'media/audios',
    'sticker': 'media/stickers',
    'animation': 'media/animations'
}
