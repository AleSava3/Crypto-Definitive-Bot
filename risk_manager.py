def calculate_risk(entry, stop, capital, target_profit, max_leverage):
    move_percent = abs(entry - stop) / entry

    if move_percent == 0:
        return None

    position_size = target_profit / move_percent
    leverage = position_size / capital

    if leverage > max_leverage:
        leverage = max_leverage
        position_size = capital * leverage

    margin = position_size / leverage
    risk = position_size * move_percent
    rr = target_profit / risk if risk != 0 else 0

    return {
        "size": round(position_size,2),
        "leverage": round(leverage,2),
        "margin": round(margin,2),
        "risk": round(risk,2),
        "rr": round(rr,2)
    }
