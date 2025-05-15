import requests

def get_top_3_potential_coins():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    try:
        response = requests.get(url)
        data = response.json()
        coins = data["result"]["list"]

        usdt_pairs = [coin for coin in coins if "USDT" in coin["symbol"]]

        ranked = []
        for coin in usdt_pairs:
            try:
                symbol = coin["symbol"]
                change_24h = float(coin["price24hPcnt"])  # % зміна за 24 год
                volume = float(coin["turnover24h"])       # оборот у USDT
                last_price = float(coin["lastPrice"])

                # Можна вводити додаткові метрики — ось простий "рейтинг":
                if volume > 1_000_000 and last_price > 0.001:  # фільтр "сміттєвих" монет
                    score = (change_24h * 0.6) + ((volume / 1_000_000) * 0.4)
                    ranked.append((symbol, score))
            except:
                continue

        top3 = sorted(ranked, key=lambda x: x[1], reverse=True)[:3]
        return [item[0] for item in top3]

    except Exception as e:
        print(f"Error in market analysis: {e}")
        return ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
