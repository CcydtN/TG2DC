import requests as req
# External Library
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.executor import Executor

TG_TOKEN:str = ''
# The webhook url that copy from client
DC_WEBHOOK:str = ""

tg_bot = Bot(TG_TOKEN)
tg = Dispatcher(tg_bot)

@tg.message_handler()
async def handle(message: types.Message):
    print("Message:\n",message.md_text)
    # You can check and edit the message at here
    payload = {'content':message.md_text}
    response = req.post(DC_API_URL+"?wait=true",json=payload)
    print(response.json())


def main():
    print("-"*40)
    executor.start_polling(tg, skip_updates=True)

if __name__ == '__main__':
   main()