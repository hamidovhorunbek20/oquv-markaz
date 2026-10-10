"""
KRYSEC Academy bot (aiogram 3).
Mini App'dan kelgan arizani adminga (8539937553) yuboradi.

O'rnatish:   pip install aiogram
Ishga tushirish (Linux/Mac):
    export BOT_TOKEN="BotFather bergan YANGI token"
    export WEBAPP_URL="https://sizning-domen.uz/index.html"   # HTTPS majburiy
    python bot.py
"""
import asyncio, json, os, html

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (Message, ReplyKeyboardMarkup, KeyboardButton,
                           WebAppInfo, ReplyKeyboardRemove)

BOT_TOKEN  = os.environ["BOT_TOKEN"]          # tokenni kodga yozmang!
WEBAPP_URL = os.environ["WEBAPP_URL"]
ADMIN_ID   = 8539937553

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(m: Message):
    # tg.sendData faqat ReplyKeyboard (KeyboardButton) orqali ochilgan Mini App'da ishlaydi
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛡 KRYSEC Academy", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
    )
    await m.answer("KRYSEC Cybersecurity Academy ga xush kelibsiz!\nLEARN. PRACTICE. DEFEND.", reply_markup=kb)


@dp.message(F.web_app_data)
async def on_application(m: Message):
    try:
        d = json.loads(m.web_app_data.data)
    except json.JSONDecodeError:
        return await m.answer("Xatolik: ma'lumot noto'g'ri.")

    u = m.from_user
    text = (
        "🆕 <b>Yangi ariza — KRYSEC Academy</b>\n\n"
        f"👤 Ism: <b>{html.escape(str(d.get('name', '')))}</b>\n"
        f"📞 Telefon: <code>{html.escape(str(d.get('phone', '')))}</code>\n"
        f"📚 Kurs: <b>{html.escape(str(d.get('course', '')))}</b>\n\n"
        f"🔗 Telegram: {('@' + u.username) if u.username else 'username yo‘q'} (ID: <code>{u.id}</code>)\n"
        f"🕒 {html.escape(str(d.get('ts', '')))}"
    )
    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    await m.answer("✅ Arizangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.", reply_markup=ReplyKeyboardRemove())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
