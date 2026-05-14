from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

# Токен вашого бота
TOKEN = "8476618316:AAGY-CNnsHxneE0SfuzLw21WphTmktiyJS0"

# Ініціалізація бота і диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обробник команди /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привіт! Я простий Telegram бот. 😊 Напиши /help, щоб дізнатися, що я вмію!")

# Обробник команди /help
@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "📚 Доступні команди:\n"
        "/start - Привітатися з ботом\n"
        "/help - Показати цю довідку\n\n"
        "Я поки що простий бот, але можу стати кориснішим у майбутньому! 🚀"
    )
    await message.answer(help_text)

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
