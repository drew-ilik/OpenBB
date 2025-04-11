import logging
import threading

from openbb_ibkr.utils.connection import IBKRWebSocketService

logger = logging.getLogger(__name__)

class IBKRServiceManager:
    """Manages the IBKR WebSocket Service, handling start, stop, and threading."""

    def __init__(self):
        self.connection = IBKRWebSocketService()
        self.service_thread = None
        self.is_running = False

    def start_service(self):
        """Start the IBKR WebSocket service and connect to IBKR."""
        if not self.is_running:
            logger.info("Starting IBKR service...")
            try:
                self.connection.connect_ibkr()
                # Start the WebSocket service in a separate thread
                self.service_thread = threading.Thread(target=self.connection.start)
                self.service_thread.start()
                self.is_running = True
                logger.info("IBKR WebSocket Service started.")
            except Exception as e:
                logger.error(f"Service encountered an error: {e}")
                self.stop_service()
        else:
            logger.warning("Service is already running.")

    def stop_service(self):
        """Stop the IBKR WebSocket service and disconnect from IBKR."""
        if self.is_running:
            logger.info("Stopping IBKR service...")
            self.connection.stop()
            if self.service_thread:
                self.service_thread.join()  # Wait for the thread to finish
            self.connection.disconnect_ibkr()
            self.is_running = False
            logger.info("IBKR WebSocket Service stopped.")
        else:
            logger.warning("Service is not currently running.")

if __name__ == "__main__":
    service_manager = IBKRServiceManager()
    try:
        service_manager.start_service()

    except KeyboardInterrupt:
        logger.info("Service interrupted by user.")
    finally:
        service_manager.stop_service()
