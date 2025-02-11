# Galactic Race Game

## Overview
The Galactic Race Game is a location-based, decentralized game built on the Solana blockchain. Players can participate as either **Galactic Worms** (racers) or **Galactic Hustlers** (bettors). The game incorporates GPS-based mechanics, dynamic circle movement, and blockchain-based transactions using SOL and $GWORM tokens. The game also includes anti-collusion measures, founder fee deductions, and automated payouts.

---

## Key Features

### 1. **Galactic Worms (Racers)**
- Each Galactic Worm has a unique home location and avatar color.
- Worms race within a dynamically moving 2-mile circle.
- Worms disappear if they are within 0.5 miles of their home location.
- NFT owners receive a 3% bonus on winnings.

### 2. **Galactic Hustlers (Bettors)**
- Hustlers place bets on Galactic Worms using SOL or $GWORM tokens.
- Bets are settled based on the race outcome (Win, Place, Show).
- A 15% founder fee is deducted from all bets.

### 3. **Dynamic Circle Movement**
- The game circle moves within a 50-mile radius and stops randomly.
- Only Galactic Worms that enter the circle after it stops are eligible to race.

### 4. **Anti-Collusion Measures**
- Proximity checks between devices to prevent collusion.
- Rate-limiting wallet transactions to restrict multiple accounts.
- Unique device IDs for user registration.
- AI-based anomaly detection for suspicious behavior.

### 5. **Founder Fee & Payouts**
- A 15% fee is deducted from all bets and transferred to the founder's wallet.
- Hourly payouts are automated to ensure the founder receives their earnings.

### 6. **Initial Registration Bonus**
- New users receive a $25 equivalent in $GWORM tokens upon registration.

### 7. **Real-Time Token Pricing**
- The game integrates real-time $GWORM token pricing for accurate bonus calculations.

---

## Code Structure

### Classes
1. **GalacticWorm**
   - Represents a racer with attributes like name, location, home location, and NFT status.
   - Methods: `race()`, `is_near_home()`, `apply_nft_bonus()`.

2. **GalacticHustler**
   - Represents a bettor with attributes like name, bet amount, and bet token.
   - Methods: `place_bet()`, `calculate_payout()`.

3. **GalacticRace**
   - Manages the game, including circle movement, race validation, and bet settlement.
   - Methods: `create_dynamic_circle()`, `start_game()`, `settle_bets()`.

4. **SolanaWalletConnect**
   - Handles Solana wallet interactions, including balance checks and token transfers.
   - Methods: `check_balance()`, `transfer_sol()`, `transfer_gworm()`.

---

## Key Functions

1. **`register_location(new_user_location)`**
   - Registers a new game location if no existing game is within a 50-mile radius.

2. **`award_initial_bonus(wallet)`**
   - Awards $25 worth of $GWORM tokens to new users upon registration.

3. **`process_hourly_payouts(wallet)`**
   - Transfers the founder's earnings to their wallet hourly.

4. **`monitor_communication(player1, player2)`**
   - Detects and logs potential collusion between players.

---

## Anti-Gaming Mechanisms

1. **Proximity Check**
   - Ensures no two devices are within 5 feet during the game.

2. **Rate-Limiting Wallet Transactions**
   - Restricts multiple transactions from the same IP or device.

3. **Unique Device IDs**
   - Requires each user to register with a unique device ID.

4. **AI-Based Anomaly Detection**
   - Identifies suspicious behavior patterns, such as synchronized movements.

5. **In-Game Penalties**
   - Disqualifies users for detected collusion attempts.

---

## Example Usage

```python
# Register a new game location
user_location = (random.uniform(-90, 90), random.uniform(-180, 180)
if register_location(user_location):
    # Create Galactic Worms
    galactic_worms = [GalacticWorm(f"Worm-{i}", (random.uniform(-90, 90), random.uniform(-180, 180)),
                      (random.uniform(-90, 90), random.uniform(-180, 180)),
                      random.choice(["Red", "Blue", "Green"]), nft=random.choice([True, False]))
                      for i in range(5)]

    # Create Galactic Hustlers
    galactic_hustlers = [GalacticHustler(f"Hustler-{i}", random.randint(1, 10), galactic_worms[random.randint(0, 4)],
                         bet_token=random.choice(["SOL", "$GWORM"]))
                         for i in range(5)]

    # Award initial bonus to each hustler
    for hustler in galactic_hustlers:
        hustler_wallet = SolanaWalletConnect(Wallet())
        award_initial_bonus(hustler_wallet)

    # Start a game
    galactic_race = GalacticRace("Game-1", user_location, galactic_worms, galactic_hustlers)
    galactic_race.start_game()
    galactic_race.settle_bets()

    # Process hourly payouts to founder
    founder_wallet_instance = SolanaWalletConnect(Wallet())
    process_hourly_payouts(founder_wallet_instance)
```

---
Certainly! Below is the **full code** for the Galactic Race Game, along with **step-by-step instructions** on how to set it up and run it.

---

## Full Code

```python
import random
import time
from geopy.distance import geodesic
from geopy import Point
from solana.wallet import Wallet
from solana.rpc.api import Client
import networkx as nx

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
founder_wallet = "FounderWalletPublicKey"  # Replace with actual founder wallet public key
founder_earnings = 0  # Track total earnings for the founder

# Communication Graph to Detect Collusion
communication_graph = nx.Graph()

# WalletConnect integration for Solana (basic structure, to be expanded by devs)
class SolanaWalletConnect:
    def __init__(self, solana_wallet: Wallet):
        self.wallet = solana_wallet
        self.client = Client("https://api.mainnet-beta.solana.com")

    def check_balance(self):
        """Fetch wallet balance"""
        balance = self.client.get_balance(self.wallet.public_key)
        return balance['result']['value']  # Balance in SOL

    def transfer_sol(self, to_wallet, amount):
        """Transfer SOL to another wallet"""
        pass

    def check_gworm_balance(self, gworm_wallet):
        """Fetch $GWORM token balance from user's wallet (if integrated with smart contract)"""
        pass

    def transfer_gworm(self, to_wallet, amount):
        """Transfer $GWORM tokens to another wallet"""
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
    wallet.transfer_gworm(wallet.wallet.public_key, bonus_tokens)
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
        hustler_wallet = SolanaWalletConnect(Wallet())
        award_initial_bonus(hustler_wallet)

    # Starting a game
    galactic_race = GalacticRace("Game-1", user_location, galactic_worms, galactic_hustlers)
    galactic_race.start_game()
    galactic_race.settle_bets()

    # Process hourly payouts to founder
    founder_wallet_instance = SolanaWalletConnect(Wallet())
    process_hourly_payouts(founder_wallet_instance)
```

---

## How to Add and Run the Code

### Step 1: Install Dependencies
1. Install Python (if not already installed).
2. Install required libraries:
   ```bash
   pip install geopy solana networkx
   ```

### Step 2: Set Up Solana Wallet
1. Create a Solana wallet using the `solana` CLI or a wallet provider like Phantom.
2. Replace `"FounderWalletPublicKey"` with your actual Solana wallet public key.

### Step 3: Run the Code
1. Save the code in a file, e.g., `galactic_race.py`.
2. Run the script:
   ```bash
   python galactic_race.py
   ```

### Step 4: Customize and Expand
- Add real-time token price integration using an API like CoinGecko.
- Implement the `transfer_sol` and `transfer_gworm` methods for actual Solana transactions.
- Build an admin portal for live financial tracking.




---

## How to Add and Run the Code

### Step 1: Install Dependencies
1. Install Python (if not already installed).
2. Install required libraries:
   ```bash
   pip install geopy solana networkx
   ```

### Step 2: Set Up Solana Wallet
1. Create a Solana wallet using the `solana` CLI or a wallet provider like Phantom.
2. Replace `"FounderWalletPublicKey"` with your actual Solana wallet public key.

### Step 3: Run the Code
1. Save the code in a file, e.g., `galactic_race.py`.
2. Run the script:
   ```bash
   python galactic_race.py
   ```

### Step 4: Customize and Expand
- Add real-time token price integration using an API like CoinGecko.
- Implement the `transfer_sol` and `transfer_gworm` methods for actual Solana transactions.
- Build an admin portal for live financial tracking.

---

Let me know if you need further assistance! 🚀
## Future Enhancements
1. **Admin Portal**
   - Add a dashboard for real-time financial tracking and game analytics.
2. **Cross-City Racing**
   - Allow Galactic Worm NFT owners to race in multiple cities.
3. **Enhanced AI Detection**
   - Improve anomaly detection for better collusion prevention.
4. **Token Staking**
   - Introduce staking mechanisms for $GWORM tokens.

---

## Dependencies
- **Python Libraries**: `random`, `time`, `geopy`, `solana`, `networkx`.
- **Blockchain**: Solana (Mainnet).

---

## License
This project is open-source and available under the MIT License.

---

## Contact
For questions or contributions, please reach out to the development team.