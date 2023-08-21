from tgbot.models.mongo import RatesDB

rates_db = RatesDB()


def converter(coin: str, target: str, value: float) -> dict:
    rates = rates_db.get_rates()["usd"]
    coin = coin.lower()
    target = target.lower()
    if coin == target:
        return None
    if coin != "usd":
        course1 = float(rates[coin])
    else:
        course1 = 1
    if target != "usd":
        course2 = float(rates[target])
    else:
        course2 = 1
    total = value * (course2 / course1)
    if total >= 1:
        return dict(coin=coin, target=target, value=round(value, 2), total=round(total, 2))
    else:
        return dict(coin=coin, target=target, value=round(value, 2), total=round(total, 6))
