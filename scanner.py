"""..."""

from finvizfinance.screener.overview import Overview
from logger_config import log


def find_premarket_movers(limit: int = 40) -> list[str]:
    """
    Scans for stocks that are "in-play" based on price, volume, and volatility.

    Args:
        limit (int): The maximum number of tickers to return. Defaults to 40.

    Returns:
        list[str]: A sorted list of stock ticker symbols (highest movers first).
    """

    # Define filters to narrow down thousands of stocks to a manageable few.
    # Using high "Relative Volume" is a classic way to find stocks with unsual interest from traders
    log.info("Starting pre-market scan with a limit of %d tickers.", limit)
    filters_dict = {
        "Price": "Over $5",
        "Relative Volume": "Over 2",
        "Change": "Up",
        "Gap": "Up",
        "Current Volume": "Over 1M",
        # Optional: Add more specific filters here if you want
        # "Volatility": "Week - Over 10%", # "Show me stocks that are consistently wild and are also having a good day today."
        # 'Sector': 'Technology',
        # "Industry": "Any"
    }
    log.debug("Using filters: %s", filters_dict)

    try:
        # The Overview class handles screening for the 'overview' page on Finviz
        stock_screener = Overview()

        stock_screener.set_filter(filters_dict=filters_dict)

        # Make the call to finviz library to perform the scan
        # The 'order' parameter tells Finviz how to sort the results.
        # Prepending '-' makes it sort in descending order (highest first).
        log.info("Fetching data from Finviz...")
        results_df = stock_screener.screener_view(order="Change")

        # Handle edge case gracefully
        if results_df.empty:
            log.warning("No stocks matched the screening criteria.")
            return []

        # Extract the 'Ticker' column and convert it to a simple Python list.
        tickers = results_df["Ticker"].tolist()
        log.info("Found %d raw tickets from Finviz", len(tickers))

        # Reverse the list so highest gainers are first
        tickers.reverse()

        limited_tickers = tickers[:limit]
        log.info(
            "Returning top %d tickers out of %d.", len(limited_tickers), len(tickers)
        )
        return limited_tickers

    except Exception as e:
        log.error("An error occurred during scanning: %d", e, exc_info=True)
        return []


print(find_premarket_movers())
