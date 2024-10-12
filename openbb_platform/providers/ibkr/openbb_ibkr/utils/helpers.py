"""IBKR Provider Helpers"""
# def fetch_in_batches(self, symbols, batch_size=100):
#     for i in range(0, len(symbols), batch_size):
#         batch = symbols[i:i + batch_size]
#         # Fetch data for each batch
#         data = self.connection.ib.reqMktData(batch, ...)

def fetch_and_cache(self, symbol):
    if symbol in self.cache:
        return self.cache[symbol]
    data = self.connection.ib.reqMktData(symbol)
    self.cache[symbol] = data
    return data

def is_live_account(account_mode: str) -> bool:
    """Check if the current account mode is live or paper."""
    return account_mode == "live"
