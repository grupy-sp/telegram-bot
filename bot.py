#!/usr/bin/env python3

"""Bot do Grupy-SP."""


from __future__ import print_function

import os
import sys
import logging
import logging.config
from locale import setlocale, LC_ALL

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

from events import get_events

# check python version
if sys.version_info.major != 3 or sys.version_info.minor < 6:
    print('Esse programa so funciona com python 3.6 ou mais recente')
    sys.exit()

# config stuff
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

load_dotenv()

setlocale(LC_ALL, 'pt_BR.UTF-8')


def start(update, context):
    """Echo some info"""

    user_username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    user_name = update.message.from_user['first_name']
    logger.info(f'Usuário: {user_id} {user_username} - /start')
    update.message.reply_text(f'Olá, {user_name}!')


def eventos(update, context, q=5):
    """Get the events on meetup website and send on chat"""

    user_username = update.message.from_user['username']
    user_id = update.message.from_user['id']
    if q == 1:
        logger.info(f'Usuário: {user_id} {user_username} - /evento')
    else:
        logger.info(f'Usuário: {user_id} {user_username} - /eventos')

    events = get_events()
    qtd = len(events)

    if qtd == 0:
        update.message.reply_text('Não há nenhum evento registrado no Meetup!')
    else:
        update.message.reply_text('Próximos eventos:\n')
        for i in range(qtd):
            event = events[i]

            msg = ((
                f"[{event['title']}]({event['url']})",
                event['date'].strftime('Dia %d de %B de %Y, às %H:%M'),
                '\n',
            ))

            update.message.reply_text(
                '\n'.join(msg),
                disable_web_page_preview=False,
                parse_mode='Markdown',
            )

            """
            This snipet would be used to send the location
            However I couldn't get the location on the events listing page
            One ideia is to get the individual event page

            update.message.reply_venue(
                latitude=lat, longitude=lon, title=location, address=address
            )
            """
        update.message.reply_text('#evento #Meetup')


def evento(bot, update):
    eventos(bot, update, 1)


if __name__ == '__main__':
    # instantiate the telegram bot inner works
    updater = Updater(os.environ['TELEGRAM_TOKEN'], use_context=True)

    # add functions that can be called from telegram chat
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('eventos', eventos))
    updater.dispatcher.add_handler(CommandHandler('evento', evento))

    # start loop that listen to chat
    updater.start_polling()
    updater.idle()
