from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text


async def user_start(message: Message):
    await message.answer("Bot started!")





def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")

