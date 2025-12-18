import logging
from typing import Optional
from pydantic import BaseModel
from cachetools import TTLCache

from aiogram import Bot
from fastapi import APIRouter, Request, HTTPException, status, Form
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.process_payment import execute_rate
from database.action_data_class import DataInteraction
from utils.payments import check_signature_result


logger = logging.getLogger(__name__)


ALLOWED_IPS: list[str] = [
    "185.59.216.65",
    "185.59.217.65"
]


router = APIRouter()


@router.post("/payment")
async def payment_notification(
        response: Request,
        out_summ: Optional[str] = Form(None, alias='OutSum'),
        OutSum: Optional[str] = Form(None),
        inv_id: Optional[str] = Form(None, alias='InvId'),
        InvId: Optional[str] = Form(None),
        crc: Optional[str] = Form(None, alias='SignatureValue'),
        SignatureValue: Optional[str] = Form(None),
        # PaymentMethod: str = Form(...),
        # Fee: Optional[str] = Form(None),
        # EMail: Optional[str] = Form(None),
        Shp_userId: str = Form(...),
        Shp_orderId: str = Form(...)
):
    client_ip = response.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"IP {client_ip} is not allowed"
        )
    bot: Bot = response.app.state.bot
    session: DataInteraction = response.app.state.session
    scheduler: AsyncIOScheduler = response.app.state.scheduler
    order_storage: TTLCache = response.app.state.order_storage
    # if not check_signature_result(str(InvId), str(OutSum), SignatureValue, user_id=Shp_userId, order_id=Shp_orderId):
    #     logger.info('bab signature')
    #     return "bad sign"
    answer = f'OK{InvId}'
    user_id = int(Shp_userId)
    order_id = int(Shp_orderId)
    order_data = order_storage.get(order_id)
    if not order_data:
        logger.info('no order data in storage')
        return "old order"
    await execute_rate(user_id, bot, session, scheduler, order_data)
    logger.info('success execute rate')
    return answer

