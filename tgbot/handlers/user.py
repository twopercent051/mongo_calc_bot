from datetime import datetime
from typing import Literal, Optional

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, User

from create_bot import bot
from tgbot.keyboards.inline import UserInline
from tgbot.misc.states import UserFSM
from tgbot.models.mongo import UsersDB
from tgbot.services.converter import converter, rates_db

inline = UserInline()
users_db = UsersDB()


async def start_render(user: User, clb: CallbackQuery = None):
    user_db = users_db.get_user(user_id=user.id)
    if not user_db:
        users_db.create_user(tid=user.id,
                             fname=user.first_name,
                             lname=user.last_name,
                             nname=user.username,
                             ibot=user.is_bot,
                             lang=user.language_code)
    text = "Welcome"
    kb = inline.welcome_kb()
    if clb:
        await clb.message.edit_text(text=text, reply_markup=kb)
    else:
        await bot.send_message(chat_id=user.id, text=text, reply_markup=kb)


async def user_start_msg(message: Message):
    await start_render(user=message.from_user)
    await UserFSM.home.set()


async def user_start_clb(callback: CallbackQuery):
    await start_render(user=callback.from_user, clb=callback)
    await bot.answer_callback_query(callback.id)
    await UserFSM.home.set()


async def last_tickets_clb(callback: CallbackQuery):
    last_tickets = users_db.get_list_object(user_id=callback.from_user.id, list_object="last_ticket")
    saved_tickets = users_db.get_saved_tickets(user_id=callback.from_user.id)
    lt_text = ["Последний запрос:"]
    st_text = ["\nСохранённый запрос:"]
    if len(last_tickets) > 0:
        for ticket in last_tickets:
            result = converter(coin=ticket["coin"], target=ticket["target"], value=ticket["value"])
            text = f"{result['value']} {result['coin'].upper()} = {result['total']} {result['target'].upper()}"
            lt_text.append(text)
    else:
        lt_text.append("---")
    if len(saved_tickets) > 0:
        for target in saved_tickets[0]["targets"]:
            result = converter(coin=saved_tickets[0]["coin"], target=target, value=saved_tickets[0]["value"])
            text = f"{result['value']} {result['coin'].upper()} = {result['total']} {result['target'].upper()}"
            st_text.append(text)
    else:
        st_text.append("---")
    lt_text.extend(st_text)
    kb = inline.last_tickets_kb()
    await callback.message.edit_text("\n".join(lt_text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def set_primary_coin_clb(callback: CallbackQuery):
    text = "Выберите валюту для которой будем рассчитывать курсы конвертации"
    currencies = users_db.get_list_object(user_id=callback.from_user.id, list_object="currencies")
    custom_currencies = users_db.get_list_object(user_id=callback.from_user.id, list_object="custom_currencies")
    currencies.extend(custom_currencies)
    kb = inline.rates_list_kb(rates=currencies, step="primary")
    await callback.message.edit_text(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def manual_clb(callback: CallbackQuery):
    step = callback.data.split(":")[1]
    text = "Введите тикер валюты"
    kb = inline.manual_kb()
    if step == "primary":
        await UserFSM.primary_manual.set()
    else:  # secondary
        await UserFSM.secondary_manual.set()
    await callback.message.edit_text(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def value_render(user: User,
                       rate: str,
                       value: float | int,
                       targets: list,
                       button_list: list,
                       step: Literal["primary", "secondary"],
                       state: FSMContext,
                       ticket_timestamp: Optional[float] = None,
                       clb: CallbackQuery = None):
    text = ["Курс конвертации:"]
    last_ticket = []
    for target in targets:
        result = converter(coin=rate, target=target, value=value)
        row = f"{result['value']} {result['coin'].upper()} = {result['total']} {result['target'].upper()}"
        text.append(row)
        last_ticket.append(dict(coin=rate, target=target, value=value))
    async with state.proxy() as data:
        data["rate"] = rate
        data["value"] = value
        data["targets"] = targets
    users_db.update_user(user_id=user.id, update_object=dict(last_ticket=last_ticket))
    kb = inline.value_render_kb(button_list=button_list, step=step, ticket_timestamp=ticket_timestamp)
    if clb:
        await clb.message.edit_text(text="\n".join(text), reply_markup=kb)
    else:
        await bot.send_message(chat_id=user.id, text="\n".join(text), reply_markup=kb)


async def value_clb(callback: CallbackQuery, state: FSMContext):
    rate = callback.data.split(":")[1]
    step = callback.data.split(":")[2]
    button_list = ["save_ticket", "home"]
    if step == "primary":
        currencies = users_db.get_list_object(user_id=callback.from_user.id, list_object="currencies")
        await value_render(user=callback.from_user,
                           rate=rate,
                           value=1,
                           targets=currencies,
                           button_list=button_list,
                           step="primary",
                           state=state,
                           clb=callback)
    else:  # secondary
        async with state.proxy() as data:
            primary_rate = data.as_dict()["rate"]
            value = data.as_dict()["value"]
            targets: list = data.as_dict()["targets"]
        targets.append(rate)
        await value_render(user=callback.from_user,
                           rate=primary_rate,
                           value=value,
                           targets=targets,
                           button_list=button_list,
                           step="secondary",
                           state=state,
                           clb=callback)
    await bot.answer_callback_query(callback.id)


async def value_primary_coin_msg(message: Message, state: FSMContext):
    rate_manual = message.text.lower().strip()
    rate_db = rates_db.get_rates()["usd"]
    if rate_db.keys().__contains__(rate_manual):
        button_list = ["save_ticket", "home"]
        currencies = users_db.get_list_object(user_id=message.from_user.id, list_object="currencies")
        await value_render(user=message.from_user,
                           rate=rate_manual,
                           value=1,
                           targets=currencies,
                           button_list=button_list,
                           step="primary",
                           state=state)
        await UserFSM.home.set()
    else:
        await message.answer("Валюта не найдена. Попробуйте снова")


async def change_value_clb(callback: CallbackQuery, state: FSMContext = None):
    step = callback.data.split(":")[1]
    if step == "primary":
        text = "Введите количество"
        kb = inline.to_converter_kb()
    else:  # "secondary"
        async with state.proxy() as data:
            value = data.as_dict()["value"]
            rate = data.as_dict()["rate"]
        text = f"Измените количество:\n{value} {rate.upper()}"
        kb = inline.back_to_render_kb(rate=rate)
    await UserFSM.value.set()
    await callback.message.edit_text(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def value_secondary_value_msg(message: Message, state: FSMContext):
    value = message.text.strip().replace(",", ".")
    try:
        value = float(value)
        async with state.proxy() as data:
            rate = data.as_dict()["rate"]
            targets: list = data.as_dict()["targets"]
        button_list = ["save_ticket", "home"]
        await value_render(user=message.from_user,
                           rate=rate,
                           value=value,
                           targets=targets,
                           button_list=button_list,
                           step="secondary",
                           state=state)
    except ValueError:
        await message.answer("Вы ввели не число")


async def set_secondary_coin_clb(callback: CallbackQuery, state: FSMContext):
    custom_currencies = users_db.get_list_object(user_id=callback.from_user.id, list_object="custom_currencies")
    rates_kb_list = []
    async with state.proxy() as data:
        default_rate = data.as_dict()["rate"]
    for rate in custom_currencies:
        if rate != default_rate:
            rates_kb_list.append(rate)
    text = "Выберите валюту, в которую будем рассчитывать курсы конвертации"
    kb = inline.rates_list_kb(rates=rates_kb_list, step="secondary")
    await callback.message.edit_text(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def value_secondary_coin_msg(message: Message, state: FSMContext):
    rate_manual = message.text.lower().strip()
    rate_db = rates_db.get_rates()["usd"]
    if rate_db.keys().__contains__(rate_manual):
        button_list = ["save_ticket", "home"]
        async with state.proxy() as data:
            primary_rate = data.as_dict()["rate"]
            value = data.as_dict()["value"]
            targets: list = data.as_dict()["targets"]
        targets.append(rate_manual)
        await value_render(user=message.from_user,
                           rate=primary_rate,
                           value=value,
                           targets=targets,
                           button_list=button_list,
                           step="secondary",
                           state=state)
        await UserFSM.home.set()
    else:
        await message.answer("Валюта не найдена. Попробуйте снова")


async def saved_tickets_render(user_id: int | str, clb: CallbackQuery):
    saved_tickets = users_db.get_saved_tickets(user_id=user_id)
    text = "Ваши сохранённые запросы"
    kb = inline.saved_tickets_kb(tickets=saved_tickets)
    if clb:
        await clb.message.edit_text(text, reply_markup=kb)
    else:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)


async def saved_tickets_clb(callback: CallbackQuery):
    await saved_tickets_render(user_id=callback.from_user.id, clb=callback)
    await bot.answer_callback_query(callback.id)


async def save_ticket(callback: CallbackQuery, state: FSMContext):
    current_saved_tickets = users_db.get_saved_tickets(user_id=callback.from_user.id)
    if len(current_saved_tickets) == 10:
        text = "Не удалось сохранить запрос. Превышен лимит"
        kb = inline.to_converter_kb()
        await callback.message.edit_text(text, reply_markup=kb)
    else:
        async with state.proxy() as data:
            rate = data.as_dict()["rate"]
            value = data.as_dict()["value"]
            targets: list = data.as_dict()["targets"]
        new_ticket = dict(coin=rate, targets=targets, value=value, timestamp=datetime.utcnow().timestamp())
        current_saved_tickets.append(new_ticket)
        users_db.update_user(user_id=callback.from_user.id, update_object=dict(saved_tickets=current_saved_tickets))
        await saved_tickets_render(user_id=callback.from_user.id, clb=callback)
    await bot.answer_callback_query(callback.id)


async def saved_ticket_clb(callback: CallbackQuery, state: FSMContext):
    ticket_timestamp = float(callback.data.split(":")[1])
    ticket = users_db.get_saved_ticket_by_timestamp(user_id=callback.from_user.id, timestamp=ticket_timestamp)
    button_list = ["delete_ticket", "save_changes", "back_to_tickets"]
    await value_render(user=callback.from_user,
                       rate=ticket["coin"],
                       value=ticket["value"],
                       targets=ticket["targets"],
                       button_list=button_list,
                       step="secondary",
                       state=state,
                       ticket_timestamp=ticket_timestamp,
                       clb=callback)
    await bot.answer_callback_query(callback.id)


async def delete_ticket_clb(callback: CallbackQuery):
    ticket_timestamp = float(callback.data.split(":")[1])
    new_tickets = users_db.get_saved_tickets_after_delete(user_id=callback.from_user.id, timestamp=ticket_timestamp)
    users_db.update_user(user_id=callback.from_user.id, update_object=dict(saved_tickets=new_tickets))
    await saved_tickets_render(user_id=callback.from_user.id, clb=callback)
    await bot.answer_callback_query(callback.id)


async def change_saved_ticket_clb(callback: CallbackQuery, state: FSMContext):
    ticket_timestamp = float(callback.data.split(":")[1])
    new_tickets = users_db.get_saved_tickets_after_delete(user_id=callback.from_user.id, timestamp=ticket_timestamp)
    async with state.proxy() as data:
        rate = data.as_dict()["rate"]
        value = data.as_dict()["value"]
        targets: list = data.as_dict()["targets"]
    new_ticket = dict(coin=rate, targets=targets, value=value, timestamp=datetime.utcnow().timestamp())
    new_tickets.append(new_ticket)
    users_db.update_user(user_id=callback.from_user.id, update_object=dict(saved_tickets=new_tickets))
    await saved_tickets_render(user_id=callback.from_user.id, clb=callback)
    await bot.answer_callback_query(callback.id)


def register_user(dp: Dispatcher):
    """РЕГИСТРАТОР"""
    dp.register_message_handler(user_start_msg, commands=["start"], state="*")
    dp.register_message_handler(value_primary_coin_msg, state=UserFSM.primary_manual)
    dp.register_message_handler(value_secondary_coin_msg, state=UserFSM.secondary_manual)
    dp.register_message_handler(value_secondary_value_msg, state=UserFSM.value)

    dp.register_callback_query_handler(user_start_clb, lambda x: x.data == "main_menu", state="*")
    dp.register_callback_query_handler(last_tickets_clb, lambda x: x.data == "to_converter", state="*")
    dp.register_callback_query_handler(set_primary_coin_clb, lambda x: x.data == "set_coin", state="*")
    dp.register_callback_query_handler(manual_clb, lambda x: x.data.split(":")[0] == "manual", state="*")
    dp.register_callback_query_handler(value_clb, lambda x: x.data.split(":")[0] == "rate", state="*")
    dp.register_callback_query_handler(change_value_clb, lambda x: x.data.split(":")[0] == "change_value", state="*")
    dp.register_callback_query_handler(set_secondary_coin_clb, lambda x: x.data.split(":")[0] == "add_coin", state="*")
    dp.register_callback_query_handler(save_ticket, lambda x: x.data.split(":")[0] == "save_ticket", state="*")
    dp.register_callback_query_handler(saved_ticket_clb, lambda x: x.data.split(":")[0] == "saved_ticket", state="*")
    dp.register_callback_query_handler(saved_tickets_clb, lambda x: x.data == "saved_tickets", state="*")
    dp.register_callback_query_handler(delete_ticket_clb, lambda x: x.data.split(":")[0] == "delete_ticket", state="*")
    dp.register_callback_query_handler(change_saved_ticket_clb,
                                       lambda x: x.data.split(":")[0] == "save_changes",
                                       state="*")
