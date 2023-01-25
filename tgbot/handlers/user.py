from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text



import json

async def user_start(message: Message):
    pass





def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")

