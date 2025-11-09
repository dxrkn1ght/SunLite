from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard(lang='uz'):
    buttons = [
        ['⭐ Rank sotib olish', '🌕 Coin sotib olish'],
        ['💰 Hisobim', "💸 Hisobni to'ldirish"],
        ['❓ Bot haqida', '📜 Tarix']
    ]
    # ReplyKeyboardMarkup uchun har bir element KeyboardButton bo'lishi kerak
    keyboard = [[KeyboardButton(text=text) for text in row] for row in buttons]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
