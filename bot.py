import random
import os

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv ("8476618316:AAGY-CNnsHxneE0SfuzLw21WphTmktiyJS0")

number_game = {}

quiz_questions = [
    ("Столиця Франції?", "париж"),
    ("2 + 2 = ?", "4"),
    ("Найбільший океан?", "тихий")
]

history_facts = [
    "📜 1991 — Україна здобула незалежність",
    "🚀 1969 — Людина висадилась на Місяць",
    "🏛 476 — Падіння Римської імперії"
]


# =========================
# КЛАВІАТУРА
# =========================
def main_menu():
    keyboard = [
        ["🎯 Вгадай число", "🧠 Вікторина"],
        ["✂️ Камінь Ножиці Папір"],
        ["💡 Цікавий факт", "📅 Мій розклад"],
        ["⚙️ Налаштування"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    await update.message.reply_text(
        f"👋 Привіт, {user}!\n"
        f"Я багатофункціональний бот 🤖",
        reply_markup=main_menu()
    )


# =========================
# HELP
# =========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Мої можливості:\n\n"
        "/start - запуск бота\n"
        "/help - допомога\n"
        "/about - інформація\n"
        "/menu - меню\n"
        "/quiz - вікторина\n"
        "/stats - статистика"
    )


# =========================
# ABOUT
# =========================
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👨‍💻 Розробник: YourName\n"
        "⚡ Версія: 1.0"
    )


# =========================
# MENU
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Головне меню:",
        reply_markup=main_menu()
    )


# =========================
# STATS
# =========================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    g = context.user_data.get("guess", 0)
    r = context.user_data.get("rps", 0)
    q = context.user_data.get("quiz", 0)

    await update.message.reply_text(
        f"🏆 Твоя статистика:\n"
        f"🎯 Вгадай число: {g}\n"
        f"✂️ Камінь Ножиці Папір: {r}\n"
        f"🧠 Вікторина: {q}"
    )


# =========================
# QUIZ INLINE
# =========================
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Париж", callback_data="wrong"),
            InlineKeyboardButton("Лондон", callback_data="wrong")
        ],
        [
            InlineKeyboardButton("Берлін", callback_data="wrong"),
            InlineKeyboardButton("Київ", callback_data="correct")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌍 Столиця України?",
        reply_markup=reply_markup
    )


async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "correct":
        await query.edit_message_text("Правильно! ✅")
    else:
        await query.edit_message_text("Спробуй ще раз! ❌")


# =========================
# ОБРОБКА ПОВІДОМЛЕНЬ
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name

    # Привіт
    if text == "привіт":
        await update.message.reply_text(
            f"👋 Привіт, {name}! Як справи?"
        )

    # Дякую
    elif text == "дякую":
        await update.message.reply_text(
            "😊 Завжди радий допомогти!"
        )

    # Історія
    elif text == "історія":
        await update.message.reply_text(
            random.choice(history_facts)
        )

    # Цікавий факт
    elif text == "💡 цікавий факт":
        facts = [
            "🐙 У восьминога 3 серця",
            "🍯 Мед не псується",
            "🦒 Жирафи сплять лише 30 хв на день"
        ]

        await update.message.reply_text(random.choice(facts))

    # Розклад
    elif text == "📅 мій розклад":
        await update.message.reply_text(
            "📚 Сьогодні:\n"
            "09:00 - Математика\n"
            "11:00 - Програмування\n"
            "14:00 - Англійська"
        )

    # Налаштування
    elif text == "⚙️ налаштування":
        await update.message.reply_text(
            "⚙️ Налаштування поки недоступні"
        )

    # 🎯 Вгадай число
    elif text == "🎯 вгадай число":
        number_game[user_id] = random.randint(1, 10)
        await update.message.reply_text(
            "🔢 Я загадав число від 1 до 10!"
        )

    elif text.isdigit() and user_id in number_game:
        if int(text) == number_game[user_id]:
            context.user_data["guess"] = context.user_data.get("guess", 0) + 1

            await update.message.reply_text(
                "🎉 Ти вгадав!"
            )

            del number_game[user_id]

        else:
            await update.message.reply_text(
                "❌ Ні, спробуй ще"
            )

    # ✂️ Камінь Ножиці Папір
    elif text == "✂️ камінь ножиці папір":
        keyboard = [["камінь", "ножиці", "папір"]]

        await update.message.reply_text(
            "Обери:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )

    elif text in ["камінь", "ножиці", "папір"]:
        bot = random.choice(["камінь", "ножиці", "папір"])

        if text == bot:
            result = "Нічия"

        elif (
            (text == "камінь" and bot == "ножиці") or
            (text == "ножиці" and bot == "папір") or
            (text == "папір" and bot == "камінь")
        ):
            result = "Ти виграв 🎉"

            context.user_data["rps"] = context.user_data.get("rps", 0) + 1

        else:
            result = "Бот виграв 🤖"

        await update.message.reply_text(
            f"Бот: {bot}\n{result}"
        )

    # 🧠 Вікторина
    elif text == "🧠 вікторина":
        question, answer = random.choice(quiz_questions)

        context.user_data["quiz_answer"] = answer

        await update.message.reply_text(question)

    elif "quiz_answer" in context.user_data:
        if text == context.user_data["quiz_answer"]:
            context.user_data["quiz"] = context.user_data.get("quiz", 0) + 1

            await update.message.reply_text(
                "✅ Правильно!"
            )

        else:
            await update.message.reply_text(
                "❌ Неправильно"
            )

        del context.user_data["quiz_answer"]

    else:
        await update.message.reply_text(
            "🤔 Я не зрозумів повідомлення"
        )


# =========================
# APP
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("version", about))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("quiz", quiz))

app.add_handler(CallbackQueryHandler(quiz_answer))

app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

print("Бот запущено 🚀")

app.run_polling()