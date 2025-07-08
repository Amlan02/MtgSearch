import requests

def search_cards(card_query):
    search_url = f"https://api.scryfall.com/cards/search?q={card_query.replace(' ', '%20')}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        cards = data.get("data", [])
        if not cards:
            print("No cards found.")
            return []
        for idx, card in enumerate(cards):
            print(f"{idx+1}: {card.get('name')} ({card.get('set_name')})")
        return cards
    except requests.exceptions.RequestException as e:
        print(f"Failed to search cards: {e}")
        return []

def get_card_price_from_card(card):
    prices = card.get("prices", {})
    print("Price info:")
    print(f"  USD: {prices.get('usd')}")
    print(f"  USD Foil: {prices.get('usd_foil')}")
    print(f"  EUR (Cardmarket): {prices.get('eur')}")
    print(f"  EUR Foil (Cardmarket): {prices.get('eur_foil')}")
    print(f"  MTGO Tix: {prices.get('tix')}")
    # Optionally, return the prices dict if you want to use it elsewhere
    return prices

if __name__ == "__main__":
    card_query = input("Enter card search: ")
    cards = search_cards(card_query)
    if cards:
        try:
            choice = int(input("Enter the number of the card you want: ")) - 1
            if 0 <= choice < len(cards):
                card = cards[choice]
                print(f"Selected: {card.get('name')} ({card.get('set_name')})")
                price = get_card_price_from_card(card)
                if price:
                    print(f"USD price: {price}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")