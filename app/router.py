from typing import Optional
from pydantic import BaseModel, Field, validator
from cachetools import TTLCache

from aiogram import Bot
from fastapi import APIRouter, Request, HTTPException, status, Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.process_payment import execute_rate
from database.action_data_class import DataInteraction
from utils.payments import check_signature_result


ALLOWED_IPS: list[str] = [
    "185.59.216.65",
    "185.59.217.65"
]


class PaymentNotification(BaseModel):
    # Основные поля (с альтернативными именами)
    OutSum: float = Field(alias='out_summ')  # Принимаем и out_summ и OutSum
    InvId: int = Field(alias='inv_id')  # Принимаем и inv_id и InvId
    Fee: Optional[float] = None
    EMail: Optional[str] = None
    SignatureValue: str = Field(alias='crc')  # crc это SignatureValue
    PaymentMethod: str
    Shp_userId: str
    Shp_orderId: str

    class Config:
        # Разрешаем автоматическое создание из разных вариантов имен полей
        allow_population_by_field_name = True
        # Разрешаем передачу любых полей (лишние будут проигнорированы)
        extra = 'ignore'

    @validator('OutSum', 'InvId', 'Fee', pre=True)
    def convert_string_to_number(cls, v):
        """Конвертируем строки в числа"""
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                # Убираем возможные пробелы
                v = v.strip()
                if '.' in v:
                    return float(v)
                else:
                    return int(v)
            except ValueError:
                return v
        return v


# Альтернативный вариант, если нужно обрабатывать оба варианта имен полей:
class PaymentNotificationFlex(BaseModel):
    # Приоритет: если есть OutSum - используем его, иначе out_summ
    OutSum: Optional[float] = None
    InvId: Optional[int] = None

    # Резервные поля (alias)
    out_summ: Optional[float] = None
    inv_id: Optional[int] = None

    # Остальные поля
    Fee: Optional[float] = None
    EMail: Optional[str] = None
    SignatureValue: Optional[str] = None
    crc: Optional[str] = None  # Альтернативное имя для SignatureValue
    PaymentMethod: str
    Shp_userId: str
    Shp_orderId: str

    class Config:
        extra = 'ignore'

    @validator('OutSum', 'InvId', 'Fee', 'out_summ', 'inv_id', pre=True)
    def convert_string_to_number(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return float(v) if '.' in v else int(v)
            except ValueError:
                return v
        return v

    @validator('SignatureValue', always=True)
    def set_signature_value(cls, v, values):
        """Берем SignatureValue из crc если основной поле не задано"""
        if v is None and 'crc' in values:
            return values['crc']
        return v

    @validator('OutSum', always=True)
    def set_outsum(cls, v, values):
        """Берем OutSum из out_summ если основной поле не задано"""
        if v is None and 'out_summ' in values:
            return values['out_summ']
        return v

    @validator('InvId', always=True)
    def set_invid(cls, v, values):
        """Берем InvId из inv_id если основной поле не задано"""
        if v is None and 'inv_id' in values:
            return values['inv_id']
        return v


router = APIRouter()


@router.post("/payment")
async def payment_notification(response: Request, payment: PaymentNotification = Depends()):
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
    if not check_signature_result(payment.InvId, payment.OutSum, payment.SignatureValue, user_id=payment.Shp_userId, order_id=payment.Shp_orderId):
        return "bad sign"
    answer = f'OK{payment.InvId}'
    user_id = int(payment.Shp_userId)
    order_id = int(payment.Shp_orderId)
    order_data = order_storage.get(order_id)
    if not order_data:
        return "old order"
    await execute_rate(user_id, bot, session, scheduler, order_data)
    return answer

