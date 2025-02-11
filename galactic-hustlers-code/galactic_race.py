import random
import time
from geopy.distance import geodesic
from geopy import Point
import networkx as nx
import requests
import json

# Constants
GAME_RADIUS_MILES = 50
CIRCLE_RADIUS_MILES = 2
HOME_RADIUS_MILES = 0.5
MIN_GALACTIC_WORMS = 5
MIN_GALACTIC_HUSTLERS = 5
GAME_TIME_INTERVAL = 20 * 60
INITIAL_BONUS_USD = 25
BONUS_MULTIPLIER_NFT = 1.03
FOUNDER_FEE_PERCENTAGE = 0.15

# Global variables
active_wallets = set()
registered_locations = []
founder_wallet = "11111111111111111111111111111111"  # Replace with actual founder wallet
founder_earnings = 0

# Communication Graph to Detect Collusion
communication_graph = nx.Graph()

class SimpleWallet:
    def __init__(self, public_key: str):
        self.public_key = public_key
        self.rpc_url = "https://api.mainnet-beta.solana.com"

    def check_balance(self):
        """Fetch wallet balance"""
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [self.public_key]
            }
            response = requests.post(self.rpc_url, headers=headers, json=payload)
            result = response.json()
            if 'result' in result:
                return result['result']['value']
            return 0
        except Exception as e:
            print(f"Error checking balance: {e}")
            return 0

    def transfer(self, to_wallet: str, amount: int):
        """Transfer tokens to another wallet"""
        try:
            print(f"Transferring {amount} tokens to {to_wallet}")
            return True
        except Exception as e:
            print(f"Error transferring tokens: {e}")
            return False

    def check_token_balance(self):
        """Fetch token balance"""
        return 0

class GalacticWorm:
    def __init__(self, name, location, home_location, avatar_color, nft=None):
        self.name = name
        self.location = location
        self.home_location = home_location
        self.position = None
        self.avatar_color = avatar_color
        self.nft = nft

    def is_near_home(self):
        current_location = Point(self.location[0], self.location[1])
        home_location = Point(self.home_location[0], self.home_location[1])
        distance = geodesic(current_location, home_location).miles
        return distance <= HOME_RADIUS_MILES

    def race(self):
        if self.is_near_home():
            print(f"{self.name} has disappeared, as they are too close to their origin!")
            self.position = None
            return

        race_result = random.uniform(0, 1)
        if race_result < 0.5:
            self.position = 1
        else:
            self.position = random.randint(2, 5)

    def apply_nft_bonus(self, bet_amount):
        if self.nft:
            bonus = (BONUS_MULTIPLIER_NFT - 1) * bet_amount
            return bet_amount + bonus
        return bet_amount

class GalacticHustler:
    def __init__(self, name, bet_amount, bet_on_worm: GalacticWorm, bet_token="SOL"):
        self.name = name
        self.bet_amount = bet_amount
        self.bet_on_worm = bet_on_worm
        self.bet_token = bet_token
        self.payout = 0

    def place_bet(self, wallet: SimpleWallet):
        if wallet.check_balance() >= self.bet_amount:
            return wallet.transfer(self.bet_on_worm.name, self.bet_amount)
        else:
            print("Not enough balance to place bet")
            return False

    def calculate_payout(self):
        global founder_earnings

        founder_fee = self.bet_amount * FOUNDER_FEE_PERCENTAGE
        founder_earnings += founder_fee
        net_bet_amount = self.bet_amount - founder_fee

        if self.bet_on_worm.position == 1:
            self.payout = net_bet_amount * 2
        elif self.bet_on_worm.position == 2:
            self.payout = net_bet_amount * 1.5
        elif self.bet_on_worm.position == 3:
            self.payout = net_bet_amount * 1.2

        self.payout = self.bet_on_worm.apply_nft_bonus(self.payout)
        return self.payout

class GalacticRace:
    def __init__(self, game_id, city_coordinates, galactic_worms, galactic_hustlers):
        self.game_id = game_id
        self.city_coordinates = city_coordinates
        self.galactic_worms = galactic_worms
        self.galactic_hustlers = galactic_hustlers
        self.start_time = None
        self.circle_locked = False
        self.winning_hustlers = []
        self.circle_center = None
        self.circle_active = False

    def create_dynamic_circle(self):
        while True:
            random_lat = self.city_coordinates[0] + random.uniform(-0.5, 0.5)
            random_lon = self.city_coordinates[1] + random.uniform(-0.5, 0.5)
            self.circle_center = (random_lat, random_lon)
            print(f"Circle moving to: {self.circle_center}")

            time.sleep(random.uniform(1, 3))
            if random.random() < 0.3:
                print(f"Circle stopped at: {self.circle_center}")
                self.circle_active = True
                break

    def is_location_within_circle(self, lat, lon):
        if not self.circle_center:
            return False
        circle_point = Point(self.circle_center[0], self.circle_center[1])
        point = Point(lat, lon)
        return geodesic(circle_point, point).miles <= CIRCLE_RADIUS_MILES

    def validate_worm_entry(self, worm: GalacticWorm):
        if self.circle_active and self.is_location_within_circle(*worm.location):
            print(f"{worm.name} entered the circle and is eligible!")
            return True
        else:
            print(f"{worm.name} is disqualified due to early entry or wrong location.")
            return False

    def start_game(self):
        if len(self.galactic_worms) >= MIN_GALACTIC_WORMS and len(self.galactic_hustlers) >= MIN_GALACTIC_HUSTLERS:
            self.start_time = time.time() + random.randint(1, 3) * GAME_TIME_INTERVAL
            print("Game has started!")
            self.create_dynamic_circle()
            for worm in self.galactic_worms:
                if self.validate_worm_entry(worm):
                    worm.race()

    def settle_bets(self):
        for hustler in self.galactic_hustlers:
            payout = hustler.calculate_payout()
            print(f"{hustler.name} received payout: {payout}")

def register_location(new_user_location):
    for location in registered_locations:
        existing_location = Point(location[0], location[1])
        new_location = Point(new_user_location[0], new_user_location[1])
        if geodesic(existing_location, new_location).miles <= GAME_RADIUS_MILES:
            print("Location already registered within the 50-mile radius.")
            return False

    registered_locations.append(new_user_location)
    print(f"New game location registered: {new_user_location}")
    return True

def get_token_price():
    """Mock function to get token price"""
    return 0.5

def award_initial_bonus(wallet: SimpleWallet):
    token_price = get_token_price()
    bonus_tokens = INITIAL_BONUS_USD / token_price
    wallet.transfer(wallet.public_key, int(bonus_tokens))
    print(f"Awarded {bonus_tokens} tokens as initial bonus.")

def process_hourly_payouts(wallet: SimpleWallet):
    global founder_earnings
    if founder_earnings > 0:
        wallet.transfer(founder_wallet, int(founder_earnings))
        print(f"Transferred {founder_earnings} tokens to the founder's wallet.")
        founder_earnings = 0

if __name__ == "__main__":
    # Example usage
    user_location = (random.uniform(-90, 90), random.uniform(-180, 180))
    
    if register_location(user_location):
        # Create Galactic Worms
        galactic_worms = [
            GalacticWorm(
                f"Worm-{i}", 
                (random.uniform(-90, 90), random.uniform(-180, 180)),
                (random.uniform(-90, 90), random.uniform(-180, 180)),
                random.choice(["Red", "Blue", "Green", "Purple", "Yellow", "Orange", "Pink", "Cyan", "White", "Black"]),
                nft=random.choice([True, False])
            ) for i in range(5)
        ]

        # Create Galactic Hustlers
        galactic_hustlers = [
            GalacticHustler(
                f"Hustler-{i}",
                random.randint(1, 10),
                galactic_worms[random.randint(0, 4)],
                bet_token=random.choice(["SOL", "$GWORM"])
            ) for i in range(5)
        ]

        # Initialize sample wallet and award bonus
        sample_wallet = SimpleWallet("sample_public_key")
        award_initial_bonus(sample_wallet)

        # Start and run game
        galactic_race = GalacticRace("Game-1", user_location, galactic_worms, galactic_hustlers)
        galactic_race.start_game()
        galactic_race.settle_bets()

        # Process founder payouts
        founder_wallet_instance = SimpleWallet(founder_wallet)
        process_hourly_payouts(founder_wallet_instance)