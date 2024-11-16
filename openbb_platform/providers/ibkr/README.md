# OpenBB Interactive Brokers Data Provider

This directory contains the **IBKR** (Interactive Brokers) data provider extension for OpenBB. The extension integrates Interactive Brokers (IB) data and functionality into the OpenBB platform, allowing users to leverage IB's comprehensive trading tools and data.

## Overview

The IBKR provider for OpenBB enables users to:
- Fetch real-time and historical market data from Interactive Brokers.
- Access IB's order management system and trading functionalities.
- Seamlessly integrate Trader Workstation (TWS) or IB Gateway with OpenBB.

This project was developed with extensibility and reliability in mind, aligning with industry standards for data input and output, while ensuring ease of use.

## Installation

1. Ensure you have installed IB Gateway or TWS and have a valid Interactive Brokers account.
2. Follow the OpenBB [installation guide](https://docs.openbb.co/platform/installation#source) to set up the platform.
3. Configure TWS Settings:
   1. Enable ActiveX and Socket Clients
   2. Enable Download Open Orders on Connection
   3. Disable Read-Only API
   4. Ensure that the API port is enabled and correctly configured. The default port is usually 7496 (live) or 7497 (paper), but you can adjust this if needed.
   5. Go to Configure > Settings > Memory Allocation and set the minimum memory allocation to 4096 MB. This avoids crashes during large data loads.
   6. In Configuration > Lock and Exit, it is recommended to choose “Never lock Trader Workstation” and “Auto restart”.
4. Use Poetry to install the necessary dependencies for the IBKR provider:
   ```bash
   poetry install

## Usage

- Enivronment variables are stored in the .env file at the root of the OpenBB directory. These include:
  - IBKR_ACCOUNT_MODE = Use either the "live" or "paper" account modes.
  - IBKR_SNAPSHOT: Determines the market data request type.
    - Set to "1" for a snapshot request (one-time data fetch).
    - Set to "0" for streaming real-time market data (requires a subscription).
  - IBKR_MARKET_DATA_TYPE: Sets the type of market data to request.
    - 1 - Real-time data (requires a subscription).
    - 2 - Frozen real-time data.
    - 3 - Delayed data.
    - 4 - Delayed frozen data.
### Example .env configuration
```plaintext
# Options: "live" or "paper" to specify the IB account mode
IBKR_ACCOUNT_MODE="paper"

# Use "1" for a snapshot request; "0" for streaming market data
IBKR_SNAPSHOT="1"

# Set the market data type (1 for real-time, 2 for frozen, 3 for delayed, 4 for delayed frozen)
IBKR_MARKET_DATA_TYPE="3"
```

## Credits
This integration is built upon the solid foundation provided by the ib_async project, a continuation of ib_insync. Special thanks to Matt Stancliff, the primary maintainer of ib_async, for ensuring the continuation of the asynchronous client for Interactive Brokers. We also thank the other contributors who have helped make ib_async a reliable tool for interacting with the IB API.

We also want to express our deep appreciation for Erwin de Wit (@erdewit), the original author of ib_insync, whose dedication to open source development shaped the way the Interactive Brokers API is accessed today. His passing in 2024 marked the loss of a pioneer, but his legacy continues to live on through the work of the IB community.

This project stands on the shoulders of giants like Erwin, and it is with immense respect that we continue to build on his contributions. His work ethic and relentless pursuit of excellence have left an indelible mark on the world of open-source trading tools.
