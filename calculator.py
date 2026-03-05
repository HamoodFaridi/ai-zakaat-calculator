ZAKAAT_RATE = 0.025

def calculate_zakaat(data, nisab_threshold):
    total_assets = (
        data["cash"] +
        data["investments"] +
        data["gold"] +
        data["silver"] +
        data["business"] +
        data["rental"] +
        data["loans"] -
        data["debts"]
    )

    if total_assets >= nisab_threshold:
        zakaat_due = total_assets * ZAKAAT_RATE
    else:
        zakaat_due = 0
    
    return total_assets, zakaat_due