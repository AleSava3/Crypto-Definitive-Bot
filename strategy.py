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

    # TREND
    if last["ema50"] > last["ema200"]:
        direction = "LONG"
        score += 20
    else:
        direction = "SHORT"
        score += 20

    # RSI
    if 40 < last["rsi"] < 65:
        score += 15

    # MACD
    if (direction == "LONG" and last["macd"] > 0) or \
       (direction == "SHORT" and last["macd"] < 0):
        score += 15

    # Volume
    vol_mean = df["v"].rolling(20).mean().iloc[-1]
    if last["v"] > vol_mean * 0.8:
        score += 15

    # ATR
    if last["atr"] > df["atr"].rolling(20).mean().iloc[-1] * 0.8:
        score += 15

    # Pullback EMA21
    if abs(last["c"] - last["ema21"]) / last["c"] < 0.003:
        score += 20

    entry = last["c"]
    stop = entry * 0.997 if direction == "LONG" else entry * 1.003
    tp = entry * 1.015 if direction == "LONG" else entry * 0.985

    if score >= 70:
        level = "HIGH"
    elif score >= 45:
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
