import logging, asyncio
from database.models import async_main
from Services import MediaService, MessageService
from telethon import TelegramClient
from config import bot, client

#----------------------BOT-------------------------------------------

from aiogram import Bot, Dispatcher
from app.handlers import router

dp = Dispatcher()



#-----------------------------------------------------------------
'''
client = TelegramClient(session="my_session",
                        api_id=config.api_id,
                        api_hash=config.api_hash,
                        device_model="Telegram Web 2.2 K",
                        system_version="Windows"
)
'''





async def main():
    await async_main()

    # ----------------------BOT-------------------------------------------
    dp.include_router(router=router)
    await dp.start_polling(bot)
    # ----------------------BOT-------------------------------------------



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

