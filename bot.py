import logging
import random
import json
from collections import defaultdict
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler, CallbackQueryHandler
)

TOKEN = '8420385107:AAH3bbwZchgSZSaMeoCOjciAbVfCpH4o0uk'

QUOTES = {
    "Motivatsiya": [
        {"text": "Harakat – muvaffaqiyatning kaliti.", "author": "Anonim"},
        {"text": "Kuchli bo‘lish – bu tanlov.", "author": "Anonim"},
    ],
    "Tarix": [
        {"text": "Tarix – bu o‘tmishdagi hayot maktabi.", "author": "Ciceron"},
        {"text": "O‘tmishni bilmagan kelajakni qurmaydi.", "author": "Abu Rayhon Beruniy"},
    ],
    "Hayot": [
        {"text": "Hayot – bu imkoniyat, undan foydalan.", "author": "Mother Teresa"},
        {"text": "Hayot go‘zal, uni qadrlang.", "author": "Anonim"},
    ]
}

CATEGORIES = list(QUOTES.keys())
STATS_FILE = 'category_stats.json'
USERS_FILE = 'users.json'
ADMIN_ID = 123456789  # Replace with your Telegram user ID

def load_json(filename, default):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception:
        return default()

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

stats = load_json(STATS_FILE, lambda: defaultdict(int))
users = load_json(USERS_FILE, dict)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def log_interaction(user_id, username, action):
    logging.info(f"User {user_id} ({username}): {action}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if str(user.id) not in users:
        users[str(user.id)] = {"name": user.first_name, "stats": defaultdict(int)}
        save_json(USERS_FILE, users)
        await update.message.reply_text(f"Salom, {user.first_name}! Ro‘yxatdan o‘tdingiz.")
    else:
        await update.message.reply_text(f"Yana xush kelibsiz, {user.first_name}!")
    kb = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in CATEGORIES]
    kb.append([InlineKeyboardButton("Statistika", callback_data="stat")])
    await update.message.reply_text(
        "Qaysi turdagi sitatani xohlaysiz?",
        reply_markup=InlineKeyboardMarkup(kb)
    )
    log_interaction(user.id, user.username, "start")

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data
    if data.startswith("cat_"):
        cat = data[4:]
        quote = random.choice(QUOTES[cat])
        stats[cat] = stats.get(cat, 0) + 1
        users[str(user.id)]["stats"][cat] = users[str(user.id)]["stats"].get(cat, 0) + 1
        save_json(STATS_FILE, stats)
        save_json(USERS_FILE, users)
        kb = [
            [InlineKeyboardButton("Yana shu kategoriyadan", callback_data=f"cat_{cat}")],
            [InlineKeyboardButton("Boshqa kategoriya", callback_data="menu")]
        ]
        await query.edit_message_text(
            f"📝 {quote['text']}\n\n— {quote['author']}",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        log_interaction(user.id, user.username, f"quote_{cat}")
    elif data == "stat":
        stat_text = "\n".join([f"{k}: {stats.get(k,0)} ta tanlangan" for k in CATEGORIES])
        await query.edit_message_text(f"Eng ko‘p tanlangan kategoriyalar:\n{stat_text}")
        log_interaction(user.id, user.username, "stat")
    elif data == "menu":
        kb = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in CATEGORIES]
        kb.append([InlineKeyboardButton("Statistika", callback_data="stat")])
        await query.edit_message_text(
            "Qaysi turdagi sitatani xohlaysiz?",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        log_interaction(user.id, user.username, "menu")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Botni boshlash\n"
        "/help - Yordam\n"
        "/my - Mening statistikam\n"
        "/reset - Statistika (faqat admin)\n"
        "Kategoriyani tanlang yoki oddiy savollar uchun yozing."
    )

async def my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats = users.get(str(user.id), {}).get("stats", {})
    if not user_stats:
        await update.message.reply_text("Siz hali hech qanday kategoriya tanlamagansiz.")
        return
    stat_text = "\n".join([f"{k}: {user_stats.get(k,0)} ta" for k in CATEGORIES])
    await update.message.reply_text(f"Sizning statistikangiz:\n{stat_text}")

async def reset_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_ID:
        await update.message.reply_text("Faqat admin uchun.")
        return
    global stats, users
    stats = defaultdict(int)
    users = {}
    save_json(STATS_FILE, stats)
    save_json(USERS_FILE, users)
    await update.message.reply_text("Statistika tozalandi.")
    log_interaction(user.id, user.username, "reset_stats")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user
    if "salom" in text:
        await update.message.reply_text(f"Salom, {user.first_name}! Sizga qanday yordam bera olaman?")
    elif "rahmat" in text:
        await update.message.reply_text("Doimo xursandman!")
    else:
        await update.message.reply_text("Sizga sitata kerakmi? Kategoriyani tanlang yoki savol bering.")
    log_interaction(user.id, user.username, f"chat: {text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("my", my_stats))
    app.add_handler(CommandHandler("reset", reset_stats))
    app.add_handler(CallbackQueryHandler(handle_category))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == '__main__':
    main()