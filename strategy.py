import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()

def analyze(symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe="15m", limit=200)
    df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])

    df["ema21"] = ta.trend.ema_indicator(df["c"], 21)
    df["ema50"] = ta.trend.ema_indicator(df["c"], 50)
    df["ema200"] = ta.trend.ema_indicator(df["c"], 200)
    df["rsi"] = ta.momentum.rsi(df["c"], 14)
    df["macd"] = ta.trend.macd_diff(df["c"])
    df["atr"] = ta.volatility.average_true_range(df["h"], df["l"], df["c"])

    last = df.iloc[-1]
    score = 0

    if last["ema50"] > last["ema200"]:
        direction = "LONG"
        score += 25
    else:
        direction = "SHORT"
        score += 25

    if 45 < last["rsi"] < 60:
        score += 15

    if last["macd"] > 0:
        score += 15

    if last["v"] > df["v"].rolling(20).mean().iloc[-1]:
        score += 15

    if last["atr"] > df["atr"].rolling(20).mean().iloc[-1]:
        score += 15

    entry = last["c"]
    stop = entry * 0.996 if direction == "LONG" else entry * 1.004
    tp = entry * 1.02 if direction == "LONG" else entry * 0.98

    if score >= 75:
        level = "HIGH"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "stop": stop,
        "tp": tp,
        "score": score,
        "level": level
    }
