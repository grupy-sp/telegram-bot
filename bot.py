#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Bot do Grupy-SP."""
import requests
import json
import logging
from locale import setlocale, LC_ALL
from decouple import config
from datetime import datetime
from telegram.ext import Updater, CommandHandler

logging.basicConfig(filename='bot.log', filemode='w', level=logging.INFO)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

telegram_token = config('TELEGRAM_TOKEN')
meetup_key = config('MEETUP_KEY')
meetup_group = config('MEETUP_GROUP')

setlocale(LC_ALL, 'pt_BR.UTF-8')


def start(bot, update):
    user_username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    user_name = update.message.from_user['first_name']
    logging.info(f'Usuário: {user_id} {user_username} - /start')
    update.message.reply_text(f'Olá, {user_name}!')


def eventos(bot, update, q=5):
    global meetup_key, meetup_group

    user_username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    if q == 1:
        logging.info(f'Usuário: {user_id} {user_username} - /evento')
    else:
        logging.info(f'Usuário: {user_id} {user_username} - /eventos')

    url = f'https://api.meetup.com/{meetup_group}/events'
    params = {
        'key': meetup_key,
        'status': 'upcoming',
        'only': 'name,time,venue,link,time',
        'page': q
    }
    r = requests.get(url, params)
    qtd = len(json.loads(r.text))
    if qtd == 0:
        update.message.reply_text('Não há nenhum evento registrado no Meetup!')
    else:
        for i in range(qtd):
            event = json.loads(r.text)[i]
            venue = event['venue']

            location = venue['name']
            address = f'{venue["address_1"]} - {venue["city"]}'
            lat = venue['lat']
            lon = venue['lon']
            title = event['name']
            link = event['link']
            time = datetime.fromtimestamp(
                event['time'] // 1000).strftime('Dia %d de %B de %Y, às %H:%M')

            update.message.reply_text(
                f'[{title}]({link})\n{time}\n\n#evento #Meetup',
                disable_web_page_preview=True,
                parse_mode='Markdown')

            update.message.reply_venue(
                latitude=lat, longitude=lon, title=location, address=address)


def evento(bot, update):
    eventos(bot, update, 1)


updater = Updater(telegram_token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('eventos', eventos))
updater.dispatcher.add_handler(CommandHandler('evento', evento))

updater.start_polling()
updater.idle()
