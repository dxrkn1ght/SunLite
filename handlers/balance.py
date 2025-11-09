from aiogram import Router, F
from aiogram.filters import Text
from keyboards.back_kb import back_kb
import texts, config
from utils import add_transaction, get_lang
import re

router = Router()

# ✅ | o‘rniga F.text.in_([...]) ishlatyapmiz
@router.message(F.text.in_(['💸 Hisobni to\'ldirish', '💸 Hisобни to\'ldirish']))
async def topup_start(message):
    lang = await get_lang(message.chat.id)
    await message.answer(
        texts.TEXTS[lang]['enter_topup_amount'].format(
            min=config.MIN_TOPUP,
            max=config.MAX_TOPUP
        ),
        reply_markup=back_kb(lang)
    )


@router.message()
async def capture_amount(message):
    lang = await get_lang(message.chat.id)
    digits = re.sub(r'[^0-9]', '', message.text or '')
    if not digits:
        return

    amount = int(digits)
    if amount < config.MIN_TOPUP or amount > config.MAX_TOPUP:
        await message.answer(
            texts.TEXTS[lang]['invalid_amount'].format(
                min=config.MIN_TOPUP,
                max=config.MAX_TOPUP
            )
        )
        return

    tr = await add_transaction(message.chat.id, amount, status='pending')
    await message.answer(
        texts.TEXTS[lang]['send_screenshot'].format(amount=amount)
    )

    # 👑 Adminlarga xabar yuborish
    for aid in config.ADMIN_IDS:
        try:
            await message.bot.send_message(
                aid,
                f"💰 Yangi to‘lov keldi!\n📎 ID: {tr.id}\n👤 @{message.from_user.username or message.chat.id}\n💳 Summa: {amount} UZS"
            )
        except:
            pass
