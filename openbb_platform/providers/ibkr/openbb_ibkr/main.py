import logging

from openbb_ibkr.utils.connection import IBKRConnection

logger = logging.getLogger(__name__)

class IBKRServiceManager:
    def __init__(self):
        self.connection = IBKRConnection()

    def start_service(self):
        logger.info("Starting IBKR service...")
        try:
            self.connection.connect()
            self.connection.keep_alive()
        except Exception as e:
            logger.error(f"Service encountered an error: {e}")
            self.stop_service()

    def stop_service(self):
        logger.info("Stopping IBKR service...")
        self.connection.disconnect()

if __name__ == "__main__":
    service_manager = IBKRServiceManager()
    try:
        service_manager.start_service()
    except KeyboardInterrupt:
        logger.info("Service interrupted by user.")
        service_manager.stop_service()
