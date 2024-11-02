import asyncio
import json
import logging
import os
import threading

import websockets
from dotenv import load_dotenv
from ib_async.ib import IB

# Configure logging for the WebSocket
logger = logging.getLogger("Websocket")
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create a lock for thread-safe file writing
file_lock = threading.Lock()

# Load environment variables from the .env file
load_dotenv()
IBKR_ACCOUNT_MODE = os.getenv("IBKR_ACCOUNT_MODE", "paper")
IBKR_PORT = 7497 if IBKR_ACCOUNT_MODE == "paper" else 7496

class IBKRConnectionSingleton:
    """Singleton class to manage IBKR connection."""

    _instance = None  # Holds the singleton instance

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the class."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the IBKR connection."""
        logging.info("Initializing IBKR connection singleton")
        self.ib = IB()
        self._is_connected = False
        logging.info("Initialization complete: _is_connected set to False")

    async def connect_ibkr(self):
        """Connect to IBKR synchronously with retry mechanism."""
        max_retries = 3
        retry_delay = 2  # Seconds between retries

        for attempt in range(max_retries):
            try:
                logger.info(f"Connecting to IBKR {IBKR_ACCOUNT_MODE} account on port {IBKR_PORT} (Attempt {attempt + 1})")
                self.ib.connect("127.0.0.1", IBKR_PORT, clientId=1)  # Removed await
                self.is_connected = True
                logger.info("Connected successfully.")
                return  # Exit after successful connection
            except Exception as e:
                self.is_connected = False
                logger.error(f"Failed to connect to IBKR on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)  # Wait before retrying
                else:
                    raise e  # Raise error after max retries

    def disconnect(self):
        """Gracefully disconnect IBKR connection."""
        if self.is_connected:
            self.ib.disconnect()
            logging.info("Disconnected from IBKR.")
            self.is_connected = False

    @property
    def is_connected(self) -> bool:
        """Check if IBKR connection is active."""
        return self._is_connected

    @is_connected.setter
    def is_connected(self, value: bool):
        """Setter for the is_connected property."""
        self._is_connected = value

class IBKRWebSocketService:
    """IBKR WebSocket service for managing connections, subscriptions, and streaming data."""

    def __init__(self):
        self.ib = IB()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.server = None
        self.thread = None

    async def handler(self, websocket, path):
        """Handle incoming WebSocket connections and messages."""
        while True:
            try:
                message = await websocket.recv()
                logger.info(f"Received message: {message}")
                data = json.loads(message)
                await self.process_message(data)  # Use your generic message processor
            except websockets.ConnectionClosed:
                logger.info("WebSocket connection closed")
                break

    async def subscribe(self, websocket, subscription_type: str, data: dict):
        """Send a subscription request for a generic data stream."""
        subscribe_event = {
            "event": "subscribe",
            "data": {
                "type": subscription_type,
                "params": data,  # Additional params for the subscription (generic)
            },
        }
        try:
            await websocket.send(json.dumps(subscribe_event))
            response = await websocket.recv()
            logger.info(f"Subscription response: {response}")
        except Exception as e:
            logger.error(f"Error during subscription: {e}")

    async def process_message(self, data):
        """Process incoming WebSocket messages. Generic handler for any stream type."""
        if "event" in data and data["event"] != "heartbeat":
            logger.info(f"Data received: {json.dumps(data)}")
            # Process specific data type here
        else:
            logger.info(f"Heartbeat or other event: {data}")

    async def _run_server(self):
        """Start the WebSocket server for handling requests."""
        self.server = await websockets.serve(self.handler, "localhost", 8765)
        logger.info("WebSocket server started")
        await self.server.wait_closed()

    def start(self):
        """Start the WebSocket service."""
        asyncio.run(self._run_server())

    def stop(self):
        """Stop the WebSocket service."""
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.server:
            self.server.close()
        if self.thread:
            self.thread.join()
        logger.info("WebSocket server stopped")

    def connect_ibkr(self):
        """Connect to the IBKR Trader Workstation."""
        try:
            logger.info(f"Connecting to IBKR {IBKR_ACCOUNT_MODE} account...")
            self.ib.connect("127.0.0.1", IBKR_PORT, clientId=1)
            logger.info("Connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to IBKR: {e}")
            raise

    def disconnect_ibkr(self):
        """Disconnect from the IBKR Trader Workstation."""
        self.ib.disconnect()
        logger.info("Disconnected from IBKR.")

    def subscribe_to_data(self, subscription_type, params):
        """Subscribe to a specific data stream."""
        try:
            self.loop.run_until_complete(self._subscribe(subscription_type, params))
        except Exception as e:
            logger.error(f"Failed to subscribe to data: {e}")

    async def _subscribe(self, subscription_type, params):
        """Internal method for handling subscriptions asynchronously."""
        async with websockets.connect("ws://localhost:8765") as websocket:
            await self.subscribe(websocket, subscription_type, params)
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                await self.process_message(data)

if __name__ == "__main__":
    service = IBKRWebSocketService()
    service.connect_ibkr()
    service.start()
    # To stop the service, call service.stop()
