from typing import List, Literal, Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.texts.user import get_text_kb


class UserInline:
    def __init__(self):
        pass

    @staticmethod
    def __home_button(lang: Literal["ru", "en"]):
        return InlineKeyboardButton(text=get_text_kb(param="home_button", lang=lang), callback_data="to_converter")

    @staticmethod
    def welcome_kb(lang: Literal["ru", "en"] = "ru"):
        home_button = InlineKeyboardButton(text=get_text_kb(param="welcome_kb", lang=lang),
                                           callback_data="to_converter")
        return InlineKeyboardMarkup(row_width=1).add(home_button)

    @staticmethod
    def last_tickets_kb(lang: Literal["ru", "en"] = "ru"):
        set_coin_button = InlineKeyboardButton(text=get_text_kb(param="set_coin", lang=lang),
                                               callback_data="set_coin")
        saved_tickets_button = InlineKeyboardButton(text=get_text_kb(param="saved_tickets", lang=lang),
                                                    callback_data="saved_tickets")
        main_menu_button = InlineKeyboardButton(text=get_text_kb(param="main_menu", lang=lang),
                                                callback_data="main_menu")
        return InlineKeyboardMarkup(row_width=1).add(set_coin_button, saved_tickets_button, main_menu_button)

    def rates_list_kb(self, rates: list, step: Literal["primary", "secondary"], lang: Literal["ru", "en"] = "ru"):
        keyboard = InlineKeyboardMarkup(row_width=4)
        buttons = []
        for rate in rates:
            buttons.append(InlineKeyboardButton(text=rate.upper(), callback_data=f"rate:{rate.lower()}:{step}"))
        keyboard.add(*buttons)
        manual_button = InlineKeyboardButton(text=get_text_kb(param="manual_button", lang=lang),
                                             callback_data=f"manual:{step}")
        keyboard.row(manual_button)
        keyboard.row(self.__home_button(lang=lang))
        return keyboard

    @staticmethod
    def manual_kb(lang: Literal["ru", "en"] = "ru"):
        back_button = InlineKeyboardButton(text=get_text_kb(param="manual_kb", lang=lang), callback_data="set_coin")
        return InlineKeyboardMarkup(row_width=1).add(back_button)

    def value_render_kb(self,
                        button_list:
                        List[str],
                        step: Literal["primary", "secondary"],
                        lang: Literal["ru", "en"] = "ru",
                        ticket_timestamp: Optional[float] = None):
        button_dict = dict(change_value=InlineKeyboardButton(text=get_text_kb(param="change_value", lang=lang),
                                                             callback_data=f"change_value:{step}"),
                           add_coin=InlineKeyboardButton(text=get_text_kb(param="add_coin", lang=lang),
                                                         callback_data=f"add_coin:{step}"),
                           delete_ticket=InlineKeyboardButton(text=get_text_kb(param="delete_ticket", lang=lang),
                                                              callback_data=f"delete_ticket:{ticket_timestamp}"),
                           save_ticket=InlineKeyboardButton(text=get_text_kb(param="save_ticket", lang=lang),
                                                            callback_data="save_ticket"),
                           save_changes=InlineKeyboardButton(text=get_text_kb(param="save_changes", lang=lang),
                                                             callback_data=f"save_changes:{ticket_timestamp}"),
                           back_to_tickets=InlineKeyboardButton(text=get_text_kb(param="back_to_tickets", lang=lang),
                                                                callback_data="saved_tickets"),
                           home=self.__home_button(lang=lang))
        default_button_list = ["change_value", "add_coin"]
        default_button_list.extend(button_list)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for button in default_button_list:
            keyboard.add(button_dict[button])
        return keyboard

    def to_converter_kb(self, lang: Literal["ru", "en"] = "ru"):
        return InlineKeyboardMarkup(row_width=1).add(self.__home_button(lang=lang))

    @staticmethod
    def back_to_render_kb(rate: str, lang: Literal["ru", "en"] = "ru"):
        button = InlineKeyboardButton(text=get_text_kb(param="back", lang=lang),
                                      callback_data=f"rate:{rate.lower()}:secondary")
        return InlineKeyboardMarkup(row_width=1).add(button)

    def saved_tickets_kb(self, tickets: list, lang: Literal["ru", "en"] = "ru"):
        keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = []
        for ticket in tickets:
            buttons.append(InlineKeyboardButton(text=f"{ticket['value']} {ticket['coin'].upper()}",
                                                callback_data=f"saved_ticket:{ticket['timestamp']}"))
        keyboard.add(*buttons)
        keyboard.add(self.__home_button(lang=lang))
        return keyboard
