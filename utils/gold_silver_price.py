import requests

def get_gold_silver_price_per_gram():

    url = "https://api.gold-api.com/price/XAU"

    try:
        response = requests.get(url)
        data_gold = response.json()

        gold_price_per_ounce = data_gold["price"] 

        # silver endpoint
        silver_url = "https://api.gold-api.com/price/XAG"
        
        data_silver = requests.get(silver_url).json()
        silver_price_per_ounce = data_silver["price"]
        
        grams_per_ounce = 31.1035

        gold_price_per_gram = gold_price_per_ounce / grams_per_ounce
        silver_price_per_gram = silver_price_per_ounce / grams_per_ounce

        return gold_price_per_gram, silver_price_per_gram
    except:
        print("Exception")
        return 75, 0.9 # fallback price
