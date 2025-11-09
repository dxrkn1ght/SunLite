from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from keyboards.main_kb import main_keyboard
import texts
from utils import get_lang, list_products, create_order
import config

router = Router()
pending_buy = {}  # vaqtinchalik xotira

# 🔹 Mahsulotlar menyusi
@router.message(F.text.in_(["⭐ Rank sotib olish", "🌕 Coin sotib olish"]))
async def shop_menu(message: Message):
    lang = await get_lang(message.chat.id)
    prods = await list_products()
    kb_rows = []
    for p in prods:
        kb_rows.append([KeyboardButton(f"{p.id} - {p.name} - {p.price} UZS")])
    kb_rows.append([KeyboardButton('⬅️ Ortga')])
    kb = ReplyKeyboardMarkup(keyboard=kb_rows, resize_keyboard=True)
    await message.answer(texts.TEXTS[lang]["choose_product"], reply_markup=kb)


# 🔹 Mahsulot tanlash
@router.message(F.text.regexp(r"^\d+ - "))
async def buy_flow(message: Message):
    parts = message.text.split(" - ")
    pid = int(parts[0])
    pending_buy[message.chat.id] = pid

    lang = await get_lang(message.chat.id)
    await message.answer(texts.TEXTS[lang]["enter_nickname"])


# 🔹 Nickname kiritish
@router.message(F.text)
async def buy_nick(message: Message):
    if message.chat.id not in pending_buy:
        return

    pid = pending_buy.pop(message.chat.id)
    nick = message.text.strip()
    order, err = await create_order(message.chat.id, pid, nick)

    lang = await get_lang(message.chat.id)

    if err == 'insufficient_balance':
        await message.answer(
            texts.TEXTS[lang]['insufficient_balance'],
            reply_markup=main_keyboard(lang)
        )
        return

    # 👑 Adminlarga xabar
    for aid in config.ADMIN_IDS:
        try:
            await message.bot.send_message(
                aid,
                f"🛒 Yangi buyurtma!\n👤 @{message.from_user.username or message.chat.id}\n🆔 Order ID: {order.id}\n🎮 Nick: {nick}"
            )
        except:
            pass

    await message.answer(
        texts.TEXTS[lang]['order_sent_admin'],
        reply_markup=main_keyboard(lang)
    )
