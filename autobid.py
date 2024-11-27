import time
import requests

# Configuration
API_KEY = "your_vast_ai_api_key"  # Replace with your Vast.ai API key
INSTANCE_ID = input("Enter your Vast.ai instance ID: ").strip()
MAX_PRICE = float(input("Enter your maximum bid price (e.g., 0.05): "))
CHECK_INTERVAL = 60  # Time between checks (in seconds)

BASE_URL = "https://console.vast.ai/api/v0"

def get_instance_details(instance_id):
    """Fetch the details of the specified instance."""
    response = requests.get(
        f"{BASE_URL}/instances/{instance_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    response.raise_for_status()
    return response.json()["instances"][0]

def set_bid_price(instance_id, bid_price):
    """Set the bid price for the specified instance."""
    response = requests.put(
        f"{BASE_URL}/instances/{instance_id}/set_bid",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"bid_price": bid_price}
    )
    response.raise_for_status()
    return response.json()

def manage_bid(instance_id, max_price):
    """Automatically manage the bid price for an instance."""
    while True:
        try:
            # Get instance details
            instance = get_instance_details(instance_id)
            current_bid = float(instance["bid_price"])
            current_status = instance["actual_status"]
            min_bid = float(instance["min_bid_price"])
            current_market_price = float(instance["current_market_price"])

            print(f"Current Bid: {current_bid}, Market Price: {current_market_price}, Min Bid: {min_bid}")

            if current_status == "running":
                # If the instance is running, try to lower the bid
                if current_bid > min_bid:
                    new_bid = max(min_bid, current_market_price + 0.0001)
                    print(f"Lowering bid to {new_bid:.5f}")
                    set_bid_price(instance_id, new_bid)
            else:
                # If the instance is not running, increase the bid within max_price
                if current_market_price < max_price:
                    new_bid = min(max_price, current_market_price + 0.0001)
                    print(f"Increasing bid to {new_bid:.5f}")
                    set_bid_price(instance_id, new_bid)
                else:
                    print(f"Market price ({current_market_price}) exceeds max price. Waiting...")
            
            print("Waiting for the next check...\n")
            time.sleep(CHECK_INTERVAL)

        except requests.RequestException as e:
            print(f"Error: {e}. Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
        except KeyError as e:
            print(f"Unexpected response structure: {e}. Exiting...")
            break

if __name__ == "__main__":
    manage_bid(INSTANCE_ID, MAX_PRICE)
