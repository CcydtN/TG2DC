import asyncio
import sys
# External Library
import discord
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor

# Copy channel id by enable “Developer Mode” from "setting" -> "Advance"
# Right click on the channel anc click "copy id".
DC_CHANNEL_ID:int = 0

DC_TOKEN:str = 'Your Discord Bot ID'
TG_TOKEN:str = 'Your Telegram Bot ID'

class custom_DC_client(discord.Client):
    def __init__(self, *args, **kwargs):
        # pass the varible to the parent object
        super().__init__(*args, **kwargs)
        # new varible storing the channel targeted
        self.reciving_channel = None

    async def on_ready(self):
        self.reciving_channel = self.get_channel(DC_CHANNEL_ID)
        if not self.reciving_channel:
            print("Channel Not Found")
            sys.exit()
        print("The message is sending to:")
        print("\tChannel:\t", self.reciving_channel)
        print("\tGuild:\t\t", self.reciving_channel.guild)
    
    async def forward_message(self,message):
        await self.reciving_channel.send(message)

loop = asyncio.new_event_loop()
dc = custom_DC_client(loop=loop)

tg_bot = Bot(TG_TOKEN,loop=loop)
tg = Dispatcher(tg_bot,loop=loop)
tg_exec = Executor(tg, skip_updates=True,loop=loop)

@tg.message_handler()
async def handle(message: types.Message):
    # You can check and edit the message at here
    print("Message:\n",message.md_text)
    await dc.forward_message(message.md_text)

def main():
    print("-"*40)

    # This part is a combined verison of `dc.run()`(from `discord.py`) and `excutor.start_polling`(from `aiogram`)
    # Running them sepratly will cause blocking
    tg_exec._prepare_polling()
    try:
        loop.run_until_complete(dc.login(DC_TOKEN))
        loop.create_task(dc.connect())

        loop.run_until_complete(tg_exec._startup_polling())
        loop.create_task(tg_exec.dispatcher.start_polling())

        print("-"*40)
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
            loop.run_until_complete(dc.close())
            loop.run_until_complete(tg_exec._shutdown_polling())
    finally:
        print("-"*40)

if __name__ == '__main__':
   main()