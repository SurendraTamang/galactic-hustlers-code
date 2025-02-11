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
