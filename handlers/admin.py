from aiogram import Router
from aiogram.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import config, texts
from utils import create_product, list_products, delete_product, update_product, broadcast

router = Router()
bot_data = {}  # Global dictionary for awaiting states

@router.message(Text("/admin"))
async def admin_menu(message: Message):
    if message.chat.id not in config.ADMIN_IDS:
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Mahsulotlar", callback_data="admin_products")],
            [InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="📩 Buyurtmalar", callback_data="admin_orders")],
        ]
    )
    await message.answer("Admin panel", reply_markup=kb)

@router.callback_query(Text("admin_products"))
async def products_cb(callback: CallbackQuery):
    prods = await list_products()
    text = "Mahsulotlar:\n"
    for p in prods:
        text += f"{p.id}: {p.kind} - {p.name} - {p.price} UZS\n"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Yangi mahsulot", callback_data="product_add")]
        ]
    )
    await callback.message.answer(text, reply_markup=kb)

@router.callback_query(Text("product_add"))
async def product_add_start(callback: CallbackQuery):
    await callback.message.answer(
        "Yangi mahsulot qo'shish. Format: kind|name|price|description\nMisol: rank|Gold|50000|Premium rank"
    )
    bot_data["awaiting_product_from"] = callback.from_user.id

@router.message()
async def product_add_receive(message: Message):
    if bot_data.get("awaiting_product_from") != message.chat.id:
        return
    parts = message.text.split("|")
    if len(parts) < 3:
        await message.answer("Noto'g'ri format")
        return
    kind, name, price = parts[0].strip(), parts[1].strip(), int(parts[2].strip())
    desc = parts[3].strip() if len(parts) > 3 else ""
    p = await create_product(kind, name, price, desc)
    await message.answer(f"Mahsulot qo'shildi: {p.id} - {p.name} - {p.price} UZS")
    bot_data.pop("awaiting_product_from", None)

@router.callback_query(Text("admin_broadcast"))
async def broadcast_start(callback: CallbackQuery):
    await callback.message.answer(texts.TEXTS["uz"]["admin_broadcast_prompt"])
    bot_data["awaiting_broadcast_from"] = callback.from_user.id

@router.message()
async def broadcast_receive(message: Message):
    if bot_data.get("awaiting_broadcast_from") != message.chat.id:
        return
    text = message.text
    cnt = await broadcast(message.bot, text)
    await message.answer(f"Xabar {cnt} foydalanuvchiga yuborildi")
    bot_data.pop("awaiting_broadcast_from", None)
