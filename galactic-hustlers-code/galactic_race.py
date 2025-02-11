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
founder_wallet = PublicKey(
    "FounderWalletPublicKey"
)  # Replace with actual founder wallet public key
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
        return balance["result"]["value"]  # Balance in lamports (1 SOL =
