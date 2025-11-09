# utils.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select
from db_async import AsyncSessionLocal
from models import User, Product, Transaction, Order

# -------------------- Keyboards --------------------
def main_keyboard(lang='uz'):
    buttons = [
        ['⭐ Rank sotib olish', '🌕 Coin sotib olish'],
        ['💰 Hisobim', "💸 Hisobni to'ldirish"],
        ['❓ Bot haqida', '📜 Tarix']
    ]
    keyboard = [[KeyboardButton(text=text) for text in row] for row in buttons]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

# -------------------- User management --------------------
async def ensure_user(chat_id, username=None, lang='uz'):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.chat_id==chat_id))
        user = res.scalars().first()
        if not user:
            user = User(chat_id=chat_id, username=username or '', lang=lang, balance=0)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

async def set_lang(chat_id, lang):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.chat_id==chat_id))
        user = res.scalars().first()
        if user:
            user.lang = lang
            await session.commit()

async def get_lang(chat_id):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.chat_id==chat_id))
        user = res.scalars().first()
        return user.lang if user else 'uz'

# -------------------- Transactions --------------------
async def add_transaction(chat_id, amount, status='pending'):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User).where(User.chat_id==chat_id))
        user = res.scalars().first()
        uid = user.id if user else None
        tr = Transaction(user_id=uid, amount=amount, status=status)
        session.add(tr)
        await session.commit()
        await session.refresh(tr)
        return tr

async def approve_transaction(tr_id):
    async with AsyncSessionLocal() as session:
        tr = await session.get(Transaction, tr_id)
        if not tr: return None
        tr.status = 'approved'
        user = await session.get(User, tr.user_id)
        if user:
            user.balance += tr.amount
        await session.commit()
        return tr, user

async def reject_transaction(tr_id):
    async with AsyncSessionLocal() as session:
        tr = await session.get(Transaction, tr_id)
        if not tr: return None
        tr.status = 'rejected'
        await session.commit()
        return tr

# -------------------- Products --------------------
async def create_product(kind, name, price, description=''):
    async with AsyncSessionLocal() as session:
        p = Product(kind=kind, name=name, price=price, description=description)
        session.add(p)
        await session.commit()
        await session.refresh(p)
        return p

async def list_products():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Product))
        return res.scalars().all()

async def get_product(pid):
    async with AsyncSessionLocal() as session:
        return await session.get(Product, pid)

async def update_product(pid, **fields):
    async with AsyncSessionLocal() as session:
        p = await session.get(Product, pid)
        if not p: return None
        for k,v in fields.items():
            setattr(p, k, v)
        await session.commit()
        await session.refresh(p)
        return p

async def delete_product(pid):
    async with AsyncSessionLocal() as session:
        p = await session.get(Product, pid)
        if not p: return False
        await session.delete(p)
        await session.commit()
        return True

# -------------------- Orders --------------------
async def create_order(chat_id, product_id, nickname):
    async with AsyncSessionLocal() as session:
        user = (await session.execute(select(User).where(User.chat_id==chat_id))).scalars().first()
        product = await session.get(Product, product_id)
        if not user: return None, 'user_not_found'
        if not product: return None, 'product_not_found'
        if user.balance < product.price: return None, 'insufficient_balance'
        order = Order(user_id=user.id, product_id=product.id, nickname=nickname, status='pending')
        user.balance -= product.price
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order, None

async def set_order_status(order_id, status):
    async with AsyncSessionLocal() as session:
        order = await session.get(Order, order_id)
        if not order: return None
        order.status = status
        await session.commit()
        return order

# -------------------- Broadcast --------------------
async def broadcast(bot, text):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User))
        users = res.scalars().all()
        count = 0
        for u in users:
            try:
                await bot.send_message(u.chat_id, text, parse_mode='HTML')
                count += 1
            except Exception:
                pass
        return count
