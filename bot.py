import asyncio
import logging
import os
import inspect
import pytz
import datetime
from cachetools import TTLCache

import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.router import router
from database.build import PostgresBuild
from database.model import Base
from database.action_data_class import DataInteraction, configurate_tables
from config_data.config import load_config, Config
from handlers.user_handlers import user_router
from handlers.payment_handlers import payment_router
from handlers.admin_router import admin_router
from handlers.join_handlers import join_router
from dialogs import get_dialogs
from middlewares import TransferObjectsMiddleware, RemindMiddleware, OpMiddleware
from utils.start_funcs import stars_schedulers


timezone = pytz.timezone('Europe/Moscow')
datetime.datetime.now(timezone)

module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))


format = '[{asctime}] #{levelname:8} {filename}:' \
         '{lineno} - {name} - {message}'

logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    style='{'
)


logger = logging.getLogger(__name__)

config: Config = load_config()


async def main():
    database = PostgresBuild(config.db.dns)
    #await database.drop_tables(Base)
    #await database.create_tables(Base)
    session = database.session()
    db = DataInteraction(session)

    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.start()

    order_storage = TTLCache(
        maxsize=2000,
        ttl=60 * 20
    )

    #nc, js = await connect_to_nats(servers=config.nats.servers)
    #storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()#storage=storage)

    await configurate_tables(session)
    await stars_schedulers(bot, DataInteraction(session), scheduler)

    # подключаем роутеры
    dp.include_routers(user_router, join_router, payment_router, *get_dialogs())

    # подключаем middleware
    setup_dialogs(dp)

    #order_storage=order_storage

    dp.update.middleware(TransferObjectsMiddleware())
    dp.callback_query.middleware(OpMiddleware())
    dp.update.middleware(RemindMiddleware())

    # запуск
    await bot.delete_webhook(drop_pending_updates=True)

    app = FastAPI()
    app.include_router(router)
    app.state.bot = bot
    app.state.scheduler = scheduler
    app.state.session = db
    app.state.order_storage = order_storage

    uvicorn_config = uvicorn.Config(app, host='0.0.0.0', port=8000, log_level="info")  # ssl_keyfile='ssl/key.pem', ssl_certfile='ssl/cert.pem'
    server = uvicorn.Server(uvicorn_config)

    aiogram_task = asyncio.create_task(dp.start_polling(bot, _session=session, _scheduler=scheduler, order_storage=order_storage))
    uvicorn_task = asyncio.create_task(server.serve())

    logger.info('Bot start polling')

    try:
        await asyncio.gather(aiogram_task, uvicorn_task)
    except Exception as e:
        logger.exception(e)
    finally:
        #await nc.close()
        await server.shutdown()
        logger.info('Connection closed')


if __name__ == "__main__":
    asyncio.run(main())