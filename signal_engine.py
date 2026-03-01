from strategy import analyze
from market_filter import btc_trend_ok
from risk_manager import calculate_risk
from config import *
from state_manager import state
from datetime import datetime
import pytz

def generate_signal(symbol):

    state.reset_if_new_day()

    if state.signals_today >= MAX_SIGNALS_PER_DAY:
        return None

    now = datetime.now(pytz.timezone(TIMEZONE))
    if not (START_HOUR <= now.hour <= END_HOUR):
        return None

    if not btc_trend_ok():
        return None

    signal = analyze(symbol)
    if not signal:
        return None

    if signal["level"] == "HIGH":
        if state.high_today >= MAX_HIGH_PER_DAY:
            return None

    risk_data = calculate_risk(
        signal["entry"],
        signal["stop"],
        CAPITAL,
        TARGET_HIGH_PROFIT if signal["level"]=="HIGH" else 10,
        MAX_LEVERAGE
    )

    state.signals_today += 1
    if signal["level"]=="HIGH":
        state.high_today += 1

    return signal, risk_data
