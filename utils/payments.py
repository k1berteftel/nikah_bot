import asyncio
import hashlib
import random
from urllib import parse
from aiohttp import ClientSession

from aiogram import Bot
from yookassa import Payment, Configuration, Payout
from yookassa.payment import PaymentResponse

from utils.text_utils import get_form_text
from database.action_data_class import DataInteraction
from config_data.config import Config, load_config


config: Config = load_config()


merchant_login = config.robokassa.merchant_login
merchant_password_1 = config.robokassa.merchant_password_1
merchant_password_2 = config.robokassa.merchant_password_2


def _calculate_signature(out_sum: str, inv_id: str, password: str, **kwargs) -> str:
    base_parts = [merchant_login]
    base_parts.append(out_sum)
    base_parts.append(inv_id)
    base_parts.append(password)

    if kwargs:
        user_params = {k: v for k, v in kwargs.items()
                       if k not in ['out_sum', 'inv_id', 'password']}
        if user_params:
            sorted_params = sorted(user_params.items(), key=lambda x: x[0])
            for key, value in sorted_params:
                normalized_key = key if key.startswith("Shp_") else f"Shp_{key}"
                normalized_value = str(value)
                base_parts.append(f"{normalized_key}={normalized_value}")

    base_string = ":".join(base_parts)
    print(base_string)
    return hashlib.md5(base_string.encode('utf-8')).hexdigest()


def get_robokassa_url(
    cost: float,
    user_id: int,
    order_id: int
) -> dict:
    url = 'https://auth.robokassa.ru/Merchant/Index.aspx'
    number = random.randint(1, 1000000)
    signature = _calculate_signature(
        str(cost),
        str(number),
        merchant_password_1,
        Shp_userId=user_id,
        Shp_orderId=order_id
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'SignatureValue': signature,
        'InvId': number,
        'Shp_userId': str(user_id),
        'Shp_orderId': str(order_id)
    }
    return {
        'url': f'{url}?{parse.urlencode(data)}',
    }


#print(get_robokassa_url(float(15), 8005178596, 8043))


def check_signature_result(
    inv_id: int,  # invoice number
    cost: float,  # cost of goods, RU
    received_signature: hex,  # SignatureValue
    user_id: str,
    order_id: str
) -> bool:
    signature = _calculate_signature(str(cost), str(inv_id), merchant_password_2, Shp_userId=user_id, Shp_orderId=order_id)
    if signature.lower() == received_signature.lower():
        return True
    return False


async def get_oxa_payment_data(amount: int | float):
    usdt_rub = await _get_usdt_rub()
    amount = round(amount / (usdt_rub), 2)
    url = 'https://api.oxapay.com/v1/payment/invoice'
    headers = {
        'merchant_api_key': config.oxapay.api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'amount': float(amount),
        'mixed_payment': False
    }
    async with ClientSession() as session:
        async with session.post(url, json=data, headers=headers, ssl=False) as resp:
            if resp.status != 200:
                print(await resp.json())
                print(resp.status)
            data = await resp.json()
            print(data)
            print(type(data['status']), data['status'])
            if data['status'] == 429:
                print('status', data['status'])
                return await get_oxa_payment_data(amount)
    return {
        'url': data['data']['payment_url'],
        'id': data['data']['track_id']
    }


async def check_oxa_payment(track_id: str, counter: int = 1) -> bool:
    url = 'https://api.oxapay.com/v1/payment/' + track_id
    headers = {
        'merchant_api_key': config.oxapay.api_key,
        'Content-Type': 'application/json'
    }
    async with ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as resp:
            if resp.status != 200:
                print('oxa check error', await resp.json())
                return False
            try:
                data = await resp.json()
            except Exception:
                if counter >= 5:
                    return False
                return await check_oxa_payment(track_id, counter+1)
    if data['data']['status'] == 'paid':
        return True
    return False


async def _get_usdt_rub() -> float:
    url = 'https://open.er-api.com/v6/latest/USD'
    async with ClientSession() as session:
        async with session.get(url, ssl=False) as res:
            data = await res.json()
            rub = data['rates']['RUB']
    return float(rub)
