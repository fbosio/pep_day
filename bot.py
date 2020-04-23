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

    def start(self, update, context):
        chat_id = update.effective_chat.id
        job = context.job_queue.run_daily(self._send_pep,
                                          datetime.now().time(),
                                          context=chat_id)
        job.run()

        if 'job' in context.chat_data:
            context.chat_data['job'].schedule_removal()
        context.chat_data['job'] = job

    def stop(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=('Stopped, no more PEPs for you!\n'
                                       'You can /start me again, whenever you '
                                       'want.'))

        context.chat_data['job'].schedule_removal()

    def _send_pep(self, context):
        chat_id = context.job.context
        context.bot.send_message(chat_id, text=('Hi! Here is your daily PEP.\n'
                                                f'{choice(self.urls)}'))


logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ.get('TOKEN')
print(TOKEN)
PORT = int(os.environ.get('PORT', '8443'))

updater = PepUpdater(TOKEN)
# updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
# updater.bot.set_webhook('https://pep-day-bot.herokuapp.com/' + TOKEN)
updater.start_polling()
# updater.idle()
