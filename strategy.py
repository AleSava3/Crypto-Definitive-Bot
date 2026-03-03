import pandas as pd
import ta
import yfinance as yf

def analyze(symbol):
    try:
        df = yf.download(
            symbol,
            interval="15m",
            period="3d",
            progress=False
        )
    except Exception as e:
        print(f"Errore fetch {symbol}: {e}")
        return None

    if df.empty or len(df) < 50:
        return None

    df = df.reset_index()

    df["ema21"] = ta.trend.ema_indicator(df["Close"], 21)
    df["ema50"] = ta.trend.ema_indicator(df["Close"], 50)
    df["ema200"] = ta.trend.ema_indicator(df["Close"], 200)
    df["rsi"] = ta.momentum.rsi(df["Close"], 14)
    df["macd"] = ta.trend.macd_diff(df["Close"])
    df["atr"] = ta.volatility.average_true_range(
        df["High"], df["Low"], df["Close"]
    )

    last = df.iloc[-1]
    score = 0

    # Trend
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
    vol_mean = df["Volume"].rolling(20).mean().iloc[-1]
    if last["Volume"] > vol_mean * 0.8:
        score += 15

    # ATR
    if last["atr"] > df["atr"].rolling(20).mean().iloc[-1] * 0.8:
        score += 15

    # Pullback EMA21
    if abs(last["Close"] - last["ema21"]) / last["Close"] < 0.003:
        score += 20

    entry = last["Close"]
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
