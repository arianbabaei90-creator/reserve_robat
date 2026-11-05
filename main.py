import asyncio

import os
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

import database



from middleware import mymidleware

from handlers import router

load_dotenv()

TOKEN=os.getenv("TOKEN")



async def main():

    bot=Bot(TOKEN)

    dp=Dispatcher()

    await database.init()

    dp.message.middleware(mymidleware())
    dp.callback_query.middleware(mymidleware())

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())