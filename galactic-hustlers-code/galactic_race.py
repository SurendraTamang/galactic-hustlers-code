import random
import time
from geopy.distance import geodesic
from geopy import Point
import networkx as nx
from solana.publickey import PublicKey
from solana.account import Account
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

# Constants
GAME_RADIUS_MILES = 50  # 250-mile radius for the game location
CIRCLE_RADIUS_MILES = 2  # 2 miles for the actual game circle during testing
HOME_RADIUS_MILES = 0.5  # Galactic Worm disappears within 0.5 miles of origin
MIN_GALACTIC_WORMS = 5
MIN_GALACTIC_HUSTLERS = 5
GAME_TIME_INTERVAL = 20 * 60  # Every 20 minutes
INITIAL_BONUS_USD = 25  # Initial registration bonus in USD
BONUS_MULTIPLIER_NFT = 1.03  # 3% bonus for Galactic Worm NFT owners
FOUNDER_FEE_PERCENTAGE = 0.15  # 15% founder fee

# Global variables
active_wallets = set()  # Active wallets currently in use
registered_locations = []  # List of registered locations (Lat, Lon, user)
founder_wallet = PublicKey("FounderWalletPublicKey")  # Replace with actual founder wallet public key
founder_earnings = 0  # Track total earnings for the founder

# Communication Graph to Detect Collusion
communication_graph = nx.Graph()

# WalletConnect integration for Solana
class SolanaWalletConnect:
    def __init__(self, public_key: PublicKey, private_key: bytes):
        self.public_key = public_key
        self.private_key = private_key
        self.client = Client("https://api.mainnet-beta.solana.com")

    def check_balance(self):
        """Fetch wallet balance in SOL"""
        balance = self.client.get_balance(self.public_key)
        return balance['result']['value']  # Balance in lamports (1 SOL = 1,000,000,000 lamports)

    def transfer_sol(self, to_wallet: PublicKey, amount: int):
        """Transfer SOL to another wallet"""
        transaction = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=self.public_key,
                    to_pubkey=to_wallet,
                    lamports=amount,
                )
            )
        )
        # Sign and send the transaction
        response = self.client.send_transaction(transaction, self.private_key)
        return response['result']

    def check_gworm_balance(self, gworm_wallet: PublicKey):
        """Fetch $GWORM token balance from user's wallet (if integrated with smart contract)"""
        # Placeholder for token balance check
        return 0

    def transfer_gworm(self, to_wallet: PublicKey, amount: int):
        """Transfer $GWORM tokens to another wallet"""
        # Placeholder for token transfer
        pass

# Function to fetch real-time token price (mocked for now)
def get_gworm_token_price():
    """Fetch the real-time $GWORM token price in USD (mocked as 0.5 USD/token)"""
    return 0.5  # Replace with live API call in production

# Galactic Worms & Galactic Hustlers Classes
class GalacticWorm:
    def __init__(self, name, location, home_location, avatar_color, nft=None):
        self.name = name
        self.location = location  # Current GPS coordinates (Lat, Lon)
        self.home_location = home_location  # Origin GPS coordinates (Lat, Lon)
        self.position = None  # Position after race
        self.avatar_color = avatar_color  # Avatar color chosen by the user
        self.nft = nft  # Optional: NFT for the Galactic Worm, could provide bonuses

    def is_near_home(self):
        """Check if the Galactic Worm is within 0.5 miles of their home location"""
        current_location = Point(self.location[0], self.location[1])
        home_location = Point(self.home_location[0], self.home_location[1])
        distance = geodesic(current_location, home_location).miles
        return distance <= HOME_RADIUS_MILES

    def race(self):
        """Simulate race outcome for a Galactic Worm"""
        if self.is_near_home():
            print(f"{self.name} has disappeared, as they are too close to their origin!")
            self.position = None  # The worm is disqualified
            return

        race_result = random.uniform(0, 1)  # Random race outcome
        if race_result < 0.5:
            self.position = 1
        else:
            self.position = random.randint(2, 5)  # Random finishing position

    def apply_nft_bonus(self, bet_amount):
        """If a user has an NFT, apply a bonus to the winnings"""
        if self.nft:
            bonus = (BONUS_MULTIPLIER_NFT - 1) * bet_amount  # 3% bonus
            return bet_amount + bonus
        return bet_amount


class GalacticHustler:
    def __init__(self, name, bet_amount, bet_on_worm: GalacticWorm, bet_token="SOL"):
        self.name = name
        self.bet_amount = bet_amount
        self.bet_on_worm = bet_on_worm
        self.bet_token = bet_token  # Can be SOL or $GWORM
        self.payout = 0

    def place_bet(self, sol_wallet: SolanaWalletConnect, gworm_wallet: SolanaWalletConnect):
        """Place a SOL or $GWORM token bet"""
        if self.bet_token == "SOL":
            if sol_wallet.check_balance() >= self.bet_amount:
                sol_wallet.transfer_sol(self.bet_on_worm, self.bet_amount)
            else:
                print("Not enough balance to place bet in SOL")
        elif self.bet_token == "$GWORM":
            if gworm_wallet.check_gworm_balance() >= self.bet_amount:
                gworm_wallet.transfer_gworm(self.bet_on_worm, self.bet_amount)
            else:
                print("Not enough balance to place bet in $GWORM")

    def calculate_payout(self, gworm_wallet: SolanaWalletConnect):
        """Calculate payout based on the race result"""
        global founder_earnings

        # Deduct founder fee from the bet amount
        founder_fee = self.bet_amount * FOUNDER_FEE_PERCENTAGE
        founder_earnings += founder_fee
        net_bet_amount = self.bet_amount - founder_fee

        # Calculate payout based on race position
        if self.bet_on_worm.position == 1:
            self.payout = net_bet_amount * 2  # 2x payout for Win
        elif self.bet_on_worm.position == 2:
            self.payout = net_bet_amount * 1.5  # 1.5x payout for Place
        elif self.bet_on_worm.position == 3:
            self.payout = net_bet_amount * 1.2  # 1.2x payout for Show

        # Apply NFT bonus if applicable
        self.payout = self.bet_on_worm.apply_nft_bonus(self.payout)

        # Transfer winnings back to hustler's wallet
        gworm_wallet.transfer_gworm(self.name, self.payout)
        return self.payout

# Circle and Game Area Management
class GalacticRace:
    def __init__(self, game_id, city_coordinates, galactic_worms, galactic_hustlers):
        self.game_id = game_id
        self.city_coordinates = city_coordinates  # Lat, Lon for the city
        self.galactic_worms = galactic_worms
        self.galactic_hustlers = galactic_hustlers
        self.start_time = None
        self.circle_locked = False
        self.winning_hustlers = []
        self.circle_center = None
        self.circle_active = False

    def create_dynamic_circle(self):
        """Move a circle dynamically within a 50-mile radius and stop randomly"""
        while True:
            random_lat = self.city_coordinates[0] + random.uniform(-0.5, 0.5)
            random_lon = self.city_coordinates[1] + random.uniform(-0.5, 0.5)
            self.circle_center = (random_lat, random_lon)
            print(f"Circle moving to: {self.circle_center}")

            # Simulate slowing down and randomly stopping
            time.sleep(random.uniform(1, 3))
            if random.random() < 0.3:  # 30% chance to stop
                print(f"Circle stopped at: {self.circle_center}")
                self.circle_active = True
                break

    def is_location_within_circle(self, lat, lon):
        """Check if a given lat, lon is within the 2-mile circle"""
        if not self.circle_center:
            return False
        circle_point = Point(self.circle_center[0], self.circle_center[1])
        point = Point(lat, lon)
        return geodesic(circle_point, point).miles <= CIRCLE_RADIUS_MILES

    def validate_worm_entry(self, worm: GalacticWorm):
        """Ensure worms entering the circle after stopping are eligible"""
        if self.circle_active and self.is_location_within_circle(*worm.location):
            print(f"{worm.name} entered the circle and is eligible!")
        else:
            print(f"{worm.name} is disqualified due to early entry or wrong location.")

    def start_game(self):
        """Start the race, ensuring conditions are met"""
        if len(self.galactic_worms) >= MIN_GALACTIC_WORMS and len(self.galactic_hustlers) >= MIN_GALACTIC_HUSTLERS:
            self.start_time = time.time() + random.randint(1, 3) * GAME_TIME_INTERVAL
            print("Game has started!")
            self.create_dynamic_circle()
            for worm in self.galactic_worms:
                self.validate_worm_entry(worm)
                worm.race()

    def settle_bets(self):
        """After race, settle bets and calculate winnings"""
        for hustler in self.galactic_hustlers:
            hustler.calculate_payout()

# Function to register a new game location
def register_location(new_user_location):
    """Register a new game location if no existing game is within 50 miles"""
    for location in registered_locations:
        # Calculate distance between new location and existing ones
        existing_location = Point(location[0], location[1])
        new_location = Point(new_user_location[0], new_user_location[1])
        if geodesic(existing_location, new_location).miles <= GAME_RADIUS_MILES:
            print("Location already registered within the 50-mile radius.")
            return False

    registered_locations.append(new_user_location)
    print(f"New game location registered: {new_user_location}")
    return True

# Function to award initial registration bonus
def award_initial_bonus(wallet: SolanaWalletConnect):
    """Award initial $GWORM token bonus to new users"""
    token_price = get_gworm_token_price()
    bonus_tokens = INITIAL_BONUS_USD / token_price
    wallet.transfer_gworm(wallet.public_key, bonus_tokens)
    print(f"Awarded {bonus_tokens} $GWORM tokens as initial bonus.")

# Function to process founder's hourly payouts
def process_hourly_payouts(wallet: SolanaWalletConnect):
    """Process hourly payouts to the founder's wallet"""
    global founder_earnings
    if founder_earnings > 0:
        wallet.transfer_gworm(founder_wallet, founder_earnings)
        print(f"Transferred {founder_earnings} $GWORM tokens to the founder's wallet.")
        founder_earnings = 0  # Reset earnings

# Function to monitor communication between players
def monitor_communication(player1, player2):
    """Monitor and log communication or collusion attempts between players"""
    communication_graph.add_edge(player1, player2)
    if nx.shortest_path_length(communication_graph, source=player1, target=player2) < 3:
        print(f"Potential collusion detected between {player1} and {player2}")

# Example usage
user_location = (random.uniform(-90, 90), random.uniform(-180, 180))  # Random location
if register_location(user_location):
    # Registering new Galactic Worms
    galactic_worms = [GalacticWorm(f"Worm-{i}", (random.uniform(-90, 90), random.uniform(-180, 180)),
                      (random.uniform(-90, 90), random.uniform(-180, 180)), 
                      random.choice(["Red", "Blue", "Green", "Purple", "Yellow", "Orange", "Pink", "Cyan", "White", "Black"]),
                      nft=random.choice([True, False]))
                      for i in range(5)]

    # Registering Galactic Hustlers
    galactic_hustlers = [GalacticHustler(f"Hustler-{i}", random.randint(1, 10), galactic_worms[random.randint(0, 4)], bet_token=random.choice(["SOL", "$GWORM"]))
                         for i in range(5)]

    # Award initial bonus to each hustler
    for hustler in galactic_hustlers:
        hustler_wallet = SolanaWalletConnect(Account().public_key(), Account().secret_key())
        award_initial_bonus(hustler_wallet)

    # Starting a game
    galactic_race = GalacticRace("Game-1", user_location, galactic_worms, galactic_hustlers)
    galactic_race.start_game()
    galactic_race.settle_bets()

    # Process hourly payouts to founder
    founder_wallet_instance = SolanaWalletConnect(founder_wallet, b"founder_private_key")
    process_hourly_payouts(founder_wallet_instance)
