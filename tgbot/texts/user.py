from typing import Literal

LEXICON_TEXT_RU = dict(start_render="Welcome",
                       last_tickets_clb_lt_text="Последний запрос:",
                       last_tickets_clb_st_text="\nСохранённый запрос:",
                       set_primary_coin_clb="Выберите валюту для которой будем рассчитывать курсы конвертации",
                       manual_clb="Введите тикер валюты",
                       value_render="Курс конвертации:",
                       value_primary_coin_msg="Валюта не найдена. Попробуйте снова",
                       change_value_clb_primary="Введите количество",
                       change_value_clb_secondary="Измените количество:",
                       value_secondary_value_msg="Вы ввели не число",
                       set_secondary_coin_clb="Выберите валюту, в которую будем рассчитывать курсы конвертации",
                       value_secondary_coin_msg="Валюта не найдена. Попробуйте снова",
                       saved_tickets_render="Ваши сохранённые запросы",
                       save_ticket="Не удалось сохранить запрос. Превышен лимит")


LEXICON_KB_RU = dict(home_button="В конвертер валют",
                     welcome_kb="Калькулятор валют",
                     set_coin="Выбрать валюту",
                     saved_tickets="Сохранённые запросы",
                     main_menu="Назад в меню",
                     manual_button="Ввод валюты вручную",
                     manual_kb="Калькулятор валют",
                     change_value="Изменить количество",
                     add_coin="Добавить валюту",
                     delete_ticket="Удалить запрос",
                     save_ticket="Сохранить запрос",
                     save_changes="Сохранить изменения",
                     back_to_tickets="Вернуться к запросам",
                     back="Назад")


def get_text(param: str, lang: Literal["ru", "en"] = "ru") -> str:
    langs = dict(ru=LEXICON_TEXT_RU)
    return langs[lang][param]


def get_text_kb(param: str, lang: Literal["ru", "en"] = "ru") -> str:
    langs = dict(ru=LEXICON_KB_RU)
    return langs[lang][param]


print(get_text_kb(param="save_changes", lang="ru"))
