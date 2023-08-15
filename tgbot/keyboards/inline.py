from typing import List, Literal, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class UserInline:
    def __init__(self):
        self.__home_button = InlineKeyboardButton(text="В конвертер валют", callback_data="to_converter")

    @staticmethod
    def welcome_kb():
        home_button = InlineKeyboardButton(text="Калькулятор валют", callback_data="to_converter")
        return InlineKeyboardMarkup(row_width=1).add(home_button)

    @staticmethod
    def last_tickets_kb():
        set_coin_button = InlineKeyboardButton(text="Выбрать валюту", callback_data="set_coin")
        saved_tickets_button = InlineKeyboardButton(text="Сохранённые запросы", callback_data="saved_tickets")
        main_menu_button = InlineKeyboardButton(text="Назад в меню", callback_data="main_menu")
        return InlineKeyboardMarkup(row_width=1).add(set_coin_button, saved_tickets_button, main_menu_button)

    def rates_list_kb(self, rates: list, step: Literal["primary", "secondary"]):
        keyboard = InlineKeyboardMarkup(row_width=4)
        buttons = []
        for rate in rates:
            buttons.append(InlineKeyboardButton(text=rate.upper(), callback_data=f"rate:{rate.lower()}:{step}"))
        keyboard.add(*buttons)
        manual_button = InlineKeyboardButton(text="Ввод валюты вручную", callback_data=f"manual:{step}")
        keyboard.row(manual_button)
        keyboard.row(self.__home_button)
        return keyboard

    @staticmethod
    def manual_kb():
        back_button = InlineKeyboardButton(text="Калькулятор валют", callback_data="set_coin")
        return InlineKeyboardMarkup(row_width=1).add(back_button)

    def value_render_kb(self,
                        button_list:
                        List[str],
                        step: Literal["primary", "secondary"],
                        ticket_timestamp: Optional[float] = None):
        button_dict = dict(change_value=InlineKeyboardButton(text="Изменить количество",
                                                             callback_data=f"change_value:{step}"),
                           add_coin=InlineKeyboardButton(text="Добавить валюту", callback_data=f"add_coin:{step}"),
                           delete_ticket=InlineKeyboardButton(text="Удалить запрос",
                                                              callback_data=f"delete_ticket:{ticket_timestamp}"),
                           save_ticket=InlineKeyboardButton(text="Сохранить запрос", callback_data="save_ticket"),
                           save_changes=InlineKeyboardButton(text="Сохранить изменения",
                                                             callback_data=f"save_changes:{ticket_timestamp}"),
                           back_to_tickets=InlineKeyboardButton(text="Вернуться к запросам",
                                                                callback_data="saved_tickets"),
                           home=self.__home_button)
        default_button_list = ["change_value", "add_coin"]
        default_button_list.extend(button_list)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for button in default_button_list:
            keyboard.add(button_dict[button])
        return keyboard

    def to_converter_kb(self):
        return InlineKeyboardMarkup(row_width=1).add(self.__home_button)

    @staticmethod
    def back_to_render_kb(rate: str):
        button = InlineKeyboardButton(text="Назад", callback_data=f"rate:{rate.lower()}:secondary")
        return InlineKeyboardMarkup(row_width=1).add(button)

    def saved_tickets_kb(self, tickets: list):
        keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for ticket in tickets:
            buttons.append(InlineKeyboardButton(text=f"{ticket['value']} {ticket['coin'].upper()}",
                                                callback_data=f"saved_ticket:{ticket['timestamp']}"))
        keyboard.add(*buttons)
        keyboard.add(self.__home_button)
        return keyboard
