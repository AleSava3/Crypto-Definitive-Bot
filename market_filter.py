import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()

def btc_trend_ok():
    ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=200)
    df = pd.DataFrame(ohlcv, columns=["t","o","h","l","c","v"])
    df["ema50"] = ta.trend.ema_indicator(df["c"], 50)
    df["ema200"] = ta.trend.ema_indicator(df["c"], 200)

    last = df.iloc[-1]
    return abs(last["ema50"] - last["ema200"]) / last["c"] > 0.002
