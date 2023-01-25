from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import *
from tgbot.misc.states import FSMAdmin
from create_bot import bot, config

import os
import random


user_id = config.tg_bot.users

async def admin_start_msg(message: Message):
    text = 'Главное меню'
    kb = admin_main_menu_kb()
    await FSMAdmin.home.set()
    await message.answer(text, reply_markup=kb)


async def admin_start_clb(callback: CallbackQuery):
    text = 'Главное меню'
    kb = admin_main_menu_kb()
    await FSMAdmin.home.set()
    await callback.message.answer(text, reply_markup=kb)
    # await bot.answer_callback_query(callback.id, cache_time=10)


async def admin_edit(callback: CallbackQuery):
    admin_id = callback.from_user.id
    doc_path = f'{os.getcwd()}/templates/template.txt'
    text = 'Отредактируй файл'
    kb = home_kb()
    await FSMAdmin.edit.set()
    await bot.send_document(chat_id=admin_id, document=open(doc_path, 'rb'), caption=' '.join(text), reply_markup=kb)
    # await bot.answer_callback_query(callback.id, cache_time=10)


async def template_doc(message: Message):
    text = 'Шаблон обновлён'
    kb = home_kb()
    file_id = message['document']['file_id']
    await bot.download_file_by_id(file_id, f'{os.getcwd()}/templates/template.txt')
    await message.answer(text, reply_markup=kb)


async def send_message(callback: CallbackQuery):
    file_path = f'{os.getcwd()}/templates/template.txt'
    with open(file_path, 'r') as file:
        file_text = file.read()
        msg_list = file_text.split('###$%$###')[2:]
    msg = random.choice(msg_list)
    kb = signal_kb()
    try:
        await bot.send_message(user_id, msg)
        await callback.message.answer(msg, reply_markup=kb)
    except Exception as ex:
        await callback.message.answer(f'Ошибка отправки {ex}', reply_markup=kb)
    # await bot.answer_callback_query(callback.id)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_msg, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(template_doc, content_types=['document'], state='*', is_admin=True)

    dp.register_callback_query_handler(admin_start_clb, lambda x: x.data == 'home', state='*', is_admin=True)
    dp.register_callback_query_handler(send_message, lambda x: x.data == 'signal', state='*', is_admin=True)
    dp.register_callback_query_handler(admin_edit, lambda x: x.data == 'edit', state='*', is_admin=True)


