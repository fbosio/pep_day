import logging
import os
from random import choice
from datetime import datetime
from telegram.ext import Updater, CommandHandler

import pep


class PepUpdater(Updater):
    def __init__(self, token):
        super().__init__(token=token, use_context=True)

        self.urls = pep.urls()

        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        stop_handler = CommandHandler('stop', self.stop)
        self.dispatcher.add_handler(stop_handler)

        easter_egg_handler = CommandHandler('http', self.easter_egg)
        self.dispatcher.add_handler(easter_egg_handler)

    def start(self, update, context):
        chat_id = update.effective_chat.id
        job = context.job_queue.run_daily(self._send_pep,
                                          datetime.now().time(),
                                          context=chat_id)
        job.run(context.dispatcher)

        if 'job' in context.chat_data:
            context.chat_data['job'].schedule_removal()
        context.chat_data['job'] = job

    def stop(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=('Stopped, no more PEPs for you!\n'
                                       'You can /start me again, whenever you '
                                       'want.'))

        context.chat_data['job'].schedule_removal()

    def easter_egg(self, update, context):
        context.bot.send_voice(chat_id=update.effective_chat.id,
                               voice=open('https.ogg', 'rb'))


    def _send_pep(self, context):
        chat_id = context.job.context
        context.bot.send_message(chat_id, text=('Hi! Here is your daily PEP.\n'
                                                f'{choice(self.urls)}'))


logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ.get('TOKEN')
print(TOKEN)
PORT = int(os.environ.get('PORT', '8443'))

updater = PepUpdater(TOKEN)
updater.start_polling()
