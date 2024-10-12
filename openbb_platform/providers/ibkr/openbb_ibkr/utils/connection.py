import asyncio
import logging
import os

import websockets
from dotenv import load_dotenv
from ib_async.ib import IB

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()
IBKR_ACCOUNT_MODE = os.getenv("IBKR_ACCOUNT_MODE", "paper")
IBKR_PORT = 7497 if IBKR_ACCOUNT_MODE == "paper" else 7496

class IBKRWebSocketService:
    def __init__(self):
        self.ib = IB()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.server = None
        self.thread = None

    async def handler(self, websocket, path):
        while True:
            try:
                message = await websocket.recv()
                logger.info(f"Received message: {message}")
                # Process the message and communicate with IBKR
            except websockets.ConnectionClosed:
                logger.info("Connection closed")
                break

    def start(self):
        asyncio.run(self._run_server())

    async def _run_server(self):
        self.server = await websockets.serve(self.handler, "localhost", 8765)
        logger.info("WebSocket server started")
        await self.server.wait_closed()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.server:
            self.server.close()
        if self.thread:
            self.thread.join()
        logger.info("WebSocket server stopped")

    def connect_ibkr(self):
        try:
            logger.info(f"Connecting to IBKR {IBKR_ACCOUNT_MODE} account...")
            self.ib.connect("127.0.0.1", IBKR_PORT, clientId=1)
            logger.info("Connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to IBKR: {e}")
            raise

    def disconnect_ibkr(self):
        self.ib.disconnect()
        logger.info("Disconnected from IBKR.")

if __name__ == "__main__":
    service = IBKRWebSocketService()
    service.connect_ibkr()
    service.start()
    # Service will keep running, and you can send messages via WebSocket
    # To stop the service, call service.stop()
