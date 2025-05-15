import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from analysis import get_top_3_potential_coins
from tracking import start_tracking
from bot_functions import send_top_3_potential_coins
import os

# 🔐 Твій Telegram-токен
TOKEN = '7932744530:AAEXr5U2CYDGw-7Xk_Td-qGsnrR5n987Sog'

# 🔧 Налаштування логування
logging.basicConfig(level=logging.INFO)

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я трейдинг-бот 💹\nНадішли /top, щоб отримати топ-3 монети.")

# 📊 Команда /top (аналіз монет)
async def send_top_3(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None):
    top_coins = get_top_3_potential_coins()
    keyboard = [[InlineKeyboardButton(coin, callback_data=coin)] for coin in top_coins]
    reply_markup = InlineKeyboardMarkup(keyboard)

    chat_id = update.effective_chat.id if update else context._chat_id
    await context.bot.send_message(chat_id=chat_id, text="⬆️ Топ-3 монети з потенціалом росту:", reply_markup=reply_markup)

# 👆 Обробка вибору монети
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_coin = query.data

    # 💾 Зберігаємо вибір
    with open("state.json", "w") as f:
        json.dump({"coin": selected_coin}, f)

    await query.edit_message_text(f"✅ Ви обрали: {selected_coin}\nЯ починаю стежити за цією монетою 📈")
    await start_tracking(context, selected_coin)

# ▶️ Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", send_top_3))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()