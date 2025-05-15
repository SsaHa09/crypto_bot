import requests
import asyncio
import os
import json
from bot_functions import send_top_3_potential_coins

async def start_tracking(context, symbol):
    print(f"Стежимо за: {symbol}")
    initial_price = await get_price(symbol)
    if initial_price is None:
        return

    has_grown = False
    peak_price = initial_price

    while True:
        await asyncio.sleep(60)
        current_price = await get_price(symbol)
        if current_price is None:
            continue

        if not has_grown and current_price >= initial_price * 1.05:
            has_grown = True
            peak_price = current_price
            print(f"{symbol} зросла на 5%! Стежимо за падінням.")

        if has_grown and current_price > peak_price:
            peak_price = current_price

        if has_grown and current_price <= peak_price * 0.97:
            message = f"⚠️ ПРОДАЖ: {symbol}\nПадіння на 3% після зростання!"
            await context.bot.send_message(chat_id=context._chat_id, text=message)

            if os.path.exists("state.json"):
                os.remove("state.json")

            await context.bot.send_message(chat_id=context._chat_id, text="🔁 Запускаю новий аналіз...")
            await send_top_3(None, context)
            break

async def get_price(symbol):
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    try:
        response = requests.get(url)
        data = response.json()["result"]["list"]
        for coin in data:
            if coin["symbol"] == symbol:
                return float(coin["lastPrice"])
    except Exception as e:
        print(f"Помилка: {e}")
    return None