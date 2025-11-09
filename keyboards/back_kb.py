from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_kb(lang):
    if lang == "uz":
        text = "⬅️ Ortga"
    else:
        text = "⬅️ Назад"

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text)]],  # <-- keyword argument ishlatildi
        resize_keyboard=True,
        one_time_keyboard=True
    )
