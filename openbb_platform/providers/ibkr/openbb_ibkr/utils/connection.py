import logging
import os

from dotenv import load_dotenv
from ib_async.ib import IB

logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

# Fetch account mode from environment variables
IBKR_ACCOUNT_MODE = os.getenv("IBKR_ACCOUNT_MODE", "paper")  # default to 'paper'

# Use default ports for TWS or IB Gateway
IBKR_PORT = 7497 if IBKR_ACCOUNT_MODE == "paper" else 7496

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class IBKRConnection:
    def __init__(self):
        self.ib = IB()

    def connect(self):
        try:
            logger.info(f"Connecting to IBKR {IBKR_ACCOUNT_MODE} account...")
            self.ib.connect("127.0.0.1", IBKR_PORT, clientId=1)
            logger.info("Connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to IBKR: {e}")
            raise

    def disconnect(self):
        self.ib.disconnect()
        logger.info("Disconnected from IBKR.")


# Example usage:
if __name__ == "__main__":
    connection = IBKRConnection()
    connection.connect()
    # Do something with the connection (e.g., fetch data)
    connection.disconnect()
