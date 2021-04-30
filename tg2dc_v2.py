import requests as req
# External Library
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CallbackContext

TG_TOKEN:str = ''
# The webhook url that copy from client
DC_WEBHOOK:str = ""

def forward2dc(update: Update, _: CallbackContext) -> None:
    # You can check and edit the message at here
    content = update.message.text
    print("Message:\n",content)
    payload = {'content': content}
    response = req.post(DC_WEBHOOK+"?wait=true",json=payload)

def main():
    print("-"*40)
    updater = Updater(TG_TOKEN)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, forward2dc))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
   main()