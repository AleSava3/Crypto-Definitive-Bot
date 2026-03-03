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

    # Se MultiIndex (può succedere), lo appiattiamo
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    # Forziamo tutto a float 1D
    close = pd.Series(df["Close"]).astype(float)
    high = pd.Series(df["High"]).astype(float)
    low = pd.Series(df["Low"]).astype(float)
    volume = pd.Series(df["Volume"]).astype(float)

    df["ema21"] = ta.trend.ema_indicator(close, 21)
    df["ema50"] = ta.trend.ema_indicator(close, 50)
    df["ema200"] = ta.trend.ema_indicator(close, 200)
    df["rsi"] = ta.momentum.rsi(close, 14)
    df["macd"] = ta.trend.macd_diff(close)
    df["atr"] = ta.volatility.average_true_range(high, low, close)

    # Prendiamo SOLO L’ULTIMO VALORE come float puro
    ema50 = float(df["ema50"].iloc[-1])
    ema200 = float(df["ema200"].iloc[-1])
    rsi = float(df["rsi"].iloc[-1])
    macd = float(df["macd"].iloc[-1])
    atr = float(df["atr"].iloc[-1])
    close_price = float(close.iloc[-1])
    volume_last = float(volume.iloc[-1])
    vol_mean = float(volume.rolling(20).mean().iloc[-1])
    atr_mean = float(df["atr"].rolling(20).mean().iloc[-1])
    ema21_last = float(df["ema21"].iloc[-1])

    score = 0

    # TREND
    if ema50 > ema200:
        direction = "LONG"
        score += 20
    else:
        direction = "SHORT"
        score += 20

    # RSI
    if 40 < rsi < 65:
        score += 15

    # MACD
    if (direction == "LONG" and macd > 0) or \
       (direction == "SHORT" and macd < 0):
        score += 15

    # Volume
    if volume_last > vol_mean * 0.8:
        score += 15

    # ATR
    if atr > atr_mean * 0.8:
        score += 15

    # Pullback EMA21
    if abs(close_price - ema21_last) / close_price < 0.003:
        score += 20

    entry = close_price
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
