from dataclasses import dataclass

from environs import Env

'''
    При необходимости конфиг базы данных или других сторонних сервисов
'''


@dataclass
class tg_bot:
    token: str
    admin_ids: list[int]


@dataclass
class DB:
    dns: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class Channels:
    makram: int
    nikah: int


@dataclass
class Private:
    channel_1: int
    channel_2: int
    channel_3: int
    channel_4: int
    channel_5: int


@dataclass
class Yookassa:
    account_id: int
    secret_key: str


@dataclass
class OxaPay:
    api_key: str


@dataclass
class Config:
    bot: tg_bot
    db: DB
    nats: NatsConfig
    channels: Channels
    private: Private
    yookassa: Yookassa
    oxapay: OxaPay


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=tg_bot(
            token=env('token'),
            admin_ids=list(map(int, env.list('admins')))
            ),
        db=DB(
            dns=env('dns')
        ),
        nats=NatsConfig(
            servers=env.list('nats')
        ),
        channels=Channels(
            makram=int(env('makram')),
            nikah=int(env('nikah'))
        ),
        private=Private(
            channel_1=int(env('channel_1')),
            channel_2=int(env('channel_2')),
            channel_3=int(env('channel_3')),
            channel_4=int(env('channel_4')),
            channel_5=int(env('channel_5')),
        ),
        yookassa=Yookassa(
            account_id=int(env('account_id')),
            secret_key=env('secret_key')
        ),
        oxapay=OxaPay(
            api_key=env('oxa_api_key')
        )
    )
