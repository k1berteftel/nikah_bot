from typing import Optional
from pydantic import BaseModel
from cachetools import TTLCache

from aiogram import Bot
from fastapi import APIRouter, Request, HTTPException, status
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.process_payment import execute_rate
from database.action_data_class import DataInteraction
from utils.payments import check_signature_result


ALLOWED_IPS: list[str] = [
    "185.59.216.65",
    "185.59.217.65"
]


class PaymentNotification(BaseModel):
    OutSum: float
    InvId: int
    Fee: Optional[float] = None
    EMail: Optional[str] = None
    SignatureValue: str
    PaymentMethod: str
    Shp_userId: str
    Shp_orderId: str


router = APIRouter()


@router.post("/payment")
async def payment_notification(payment: PaymentNotification, response: Request):
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
    if not check_signature_result(payment.InvId, payment.OutSum, PaymentNotification.SignatureValue):
        return "bad sign"
    answer = f'OK{payment.InvId}'
    user_id = int(payment.Shp_userId)
    order_id = int(payment.Shp_orderId)
    order_data = order_storage.get(order_id)
    await execute_rate(user_id, bot, session, scheduler, order_data)
    return answer

