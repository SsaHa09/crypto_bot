from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from analysis import get_top_3_potential_coins

async def send_top_3_potential_coins(update=None, context=None):
    top_coins = get_top_3_potential_coins()
    keyboard = [[InlineKeyboardButton(coin, callback_data=coin)] for coin in top_coins]
    reply_markup = InlineKeyboardMarkup(keyboard)

    chat_id = update.effective_chat.id if update else context._chat_id
    await context.bot.send_message(chat_id=chat_id, text="⬆️ Топ-3 монети з потенціалом росту:", reply_markup=reply_markup)