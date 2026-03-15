ZAKAAT_RATE = 0.025
NISAB_GRAMS_GOLD = 87.48
NISAB_GRAMS_SILVER = 612.36

def calculate_zakat(data, gold_price_per_gram, silver_price_per_gram, nisab_method):
    
    if nisab_method == "Gold (87.48g)":
        nisab_threshold = gold_price_per_gram * NISAB_GRAMS_GOLD
    else:
        nisab_threshold = silver_price_per_gram * NISAB_GRAMS_SILVER

    total_assets = (
        data["cash"] +
        data["gold"] +
        data["silver"] +
        data["investments"] +
        data["business"] +
        data["rental"] +
        data["loans"] -
        data["debts"]
    )

    if total_assets >= nisab_threshold:
        zakat_due = total_assets * ZAKAAT_RATE
    else:
        zakat_due = 0
    
    return total_assets, nisab_threshold, zakat_due