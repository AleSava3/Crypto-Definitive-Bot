import pandas as pd
import ta
import yfinance as yf


def analyze(symbol):
    try:
        df = yf.download(
            symbol,
            interval="15m",
            period="3d",
            progress=False,
            auto_adjust=False,
            threads=False
        )
    except Exception as e:
        print(f"Errore fetch {symbol}: {e}")
        return None

    if df.empty or len(df) < 50:
        return None

    df = df.reset_index()

    # 🔥 RENDIAMO LE COLONNE 1D SICURE
    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()

    score = 0

    df["ema21"] = ta.trend.ema_indicator(close, 21)
    df["ema50"] = ta.trend.ema_indicator(close, 50)
    df["ema200"] = ta.trend.ema_indicator(close, 200)
    df["rsi"] = ta.momentum.rsi(close, 14)
    df["macd"] = ta.trend.macd_diff(close)
    df["atr"] = ta.volatility.average_true_range(high, low, close)

    last = df.iloc[-1]

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
    vol_mean = volume.rolling(20).mean().iloc[-1]
    if last["Volume"] > vol_mean * 0.8:
        score += 15

    # ATR
    atr_mean = df["atr"].rolling(20).mean().iloc[-1]
    if last["atr"] > atr_mean * 0.8:
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
        "entry": float(entry),
        "stop": float(stop),
        "tp": float(tp),
        "score": score,
        "level": level
    }
