from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Text
from utils import ensure_user, set_lang, get_lang, main_keyboard
import texts

router = Router()


# --- Til tanlash klaviaturasi ---
def choose_language_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbеkcha"), KeyboardButton(text="🇷🇺 Русский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# --- Oferta klaviaturasi ---
def offer_kb(lang="uz"):
    if lang == "uz":
        buttons = ["Tasdiqlayman ✅", "⬅️ Ortga"]
    else:
        buttons = ["Подтверждаю ✅", "⬅️ Назад"]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=b)] for b in buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# --- /start komandasi ---
@router.message(CommandStart())
async def start_handler(message: Message):
    # Foydalanuvchini bazaga yozamiz (agar yo‘q bo‘lsa)
    await ensure_user(message.chat.id, message.from_user.username)
    await message.answer(
        "Tilni tanlang / Выберите язык:",
        reply_markup=choose_language_kb()
    )


# --- O'zbek tili tanlanganda ---
@router.message(Text("🇺🇿 O'zbеkcha"))
async def choose_uz(message: Message):
    await set_lang(message.chat.id, "uz")
    await message.answer(
        texts.TEXTS["uz"]["offer"],
        reply_markup=offer_kb("uz")
    )


# --- Rus tili tanlanganda ---
@router.message(Text("🇷🇺 Русский"))
async def choose_ru(message: Message):
    await set_lang(message.chat.id, "ru")
    await message.answer(
        texts.TEXTS["ru"]["offer"],
        reply_markup=offer_kb("ru")
    )


# --- Oferta tasdiqlanganda ---
@router.message(Text(["Tasdiqlayman ✅", "Подтверждаю ✅"]))
async def offer_confirm(message: Message):
    lang = await get_lang(message.chat.id)
    await message.answer(
        texts.TEXTS[lang]["offer_confirmed"],
        reply_markup=main_keyboard(lang)
    )


# --- Asosiy menyu tugmalari uchun handler ---
@router.message(F.text.in_([
    "⭐ Rank sotib olish",
    "🌕 Coin sotib olish",
    "💰 Hisobim",
    "💸 Hisobni to'ldirish",
    "❓ Bot haqida",
    "📜 Tarix"
]))
async def handle_main_menu(message: Message):
    lang = await get_lang(message.chat.id)
    await message.answer(
        f"Siz '{message.text}' bo‘limini tanladingiz!",
        reply_markup=main_keyboard(lang)
    )
