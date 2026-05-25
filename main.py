import asyncio
import os
from aiogram.filters import Command

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile
)
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BUG_CHANNEL_ID = os.getenv("BUG_CHANNEL_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")

if not BUG_CHANNEL_ID:
    raise ValueError("BUG_CHANNEL_ID is missing")

BUG_CHANNEL_ID = int(BUG_CHANNEL_ID)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📥 Скачать плагин")],
            [KeyboardButton(text="🐞 Сообщить о баге")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Добро пожаловать",
        reply_markup=keyboard
    )

@dp.message(Command("instruction"))
async def instruction(message: Message):

    instruction_text = (
        "🌿 Рекомендации по отображению деревьев и растений\n\n"
        "Для корректного и красивого отображения Billboard-объектов рекомендуется:\n\n"
        "• выделить все растения/деревья и установить прозрачность 1% — "
        "это помогает устранить артефакты, возникающие из-за ограничений Revit;\n\n"
        "• в параметрах визуального стиля → "
        "«Параметры отображения графики» отключить опцию "
        "«Показать ребра».\n\n"
        "Это позволит отображать Billboard-растения и деревья "
        "без лишней графики и визуальных артефактов."
    )

    await message.answer(instruction_text)


@dp.message(lambda message: message.text == "📥 Скачать плагин")
async def send_plugin(message: Message):

    await message.answer(
        "📥 Скачать Billboard Plugin:\n\n"
        "https://github.com/ArtiomLavreca/MOOD-Billboard-Plugin/releases/download/v0.28_Base/Billboard_Plugin_0.28_Base.exe"
    )

    warning_text = (
        "⚠️ Тестовая версия плагина Billboard\n\n"
        "Данная версия плагина создана для выявления возможных ошибок, "
        "недочетов и проблем в работе.\n\n"
        "Плагин был протестирован на версии Revit 2025.\n\n"
        "Если вы столкнулись с ошибками, некорректной работой или другими "
        "проблемами, пожалуйста, напишите в бот с:\n"
        "• описанием проблемы;\n"
        "• приложенным скриншотом ошибки или ситуации.\n\n"
        "Спасибо за помощь в тестировании и понимание!\n"
        "Желаем вам успешной работы 🚀"
    )

    await message.answer(warning_text)


@dp.message(lambda message: message.text == "🐞 Сообщить о баге")
async def bug_info(message: Message):
    await message.answer(
        "Отправьте описание бага.\n"
        "Можно приложить фото."
    )


@dp.message(lambda message: message.photo)
async def handle_bug_photo(message: Message):
    username = message.from_user.username or "без username"
    user_id = message.from_user.id
    caption = message.caption or "Без описания"

    text = (
        "🐞 Новый баг-репорт\n\n"
        f"👤 User: @{username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"📝 Описание:\n{caption}"
    )

    photo = message.photo[-1].file_id

    await bot.send_photo(
        chat_id=BUG_CHANNEL_ID,
        photo=photo,
        caption=text
    )

    await message.answer("Баг с фото отправлен разработчику.")


@dp.message(lambda message: message.text)
async def handle_bug_text(message: Message):
    username = message.from_user.username or "без username"
    user_id = message.from_user.id

    text = (
        "🐞 Новый баг-репорт\n\n"
        f"👤 User: @{username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"📝 Описание:\n{message.text}"
    )

    await bot.send_message(
        chat_id=BUG_CHANNEL_ID,
        text=text
    )

    await message.answer("Баг отправлен разработчику.")





async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())