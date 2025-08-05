from config_data.config import Config, load_config


config: Config = load_config()

channels = config.private

chats = {
    '23plus': channels.channel_1,
    '23minus': channels.channel_2,
    'second': channels.channel_3,
    'dagestan': channels.channel_4,
    'kazakh': channels.channel_5,
    'special': [channels.channel_1, channels.channel_2, channels.channel_3, channels.channel_4, channels.channel_5]
}

chats_title = {
    channels.channel_1: 'Тут все невесты от 23 лет',
    channels.channel_2: 'Приватный канал до 23 лет',
    channels.channel_3: 'Готовы пойти Второй Женой',
    channels.channel_4: 'Дагестан невесты',
    channels.channel_5: 'Невесты из Казахстана и Кыргызстана',
}