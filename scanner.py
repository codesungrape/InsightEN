"""..."""

from finvizfinance.screener.overview import Overview


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
    filters_dict = {
        "Price": "Over $5",
        "Relative Volume": "Over 2",
        "Volatility": "Week - Over 10%",
        # Optional: Add more specific filters here if you want
        # 'Sector': 'Technology',
    }

    try:
        # The Overview class handles screening for the 'overview' page on Finviz
        stock_screener = Overview()

        stock_screener.set_filter(filters_dict=filters_dict)

        # Make the call to finviz library to perform the scan
        # The 'order' parameter tells Finviz how to sort the results.
        # Prepending '-' makes it sort in descending order (highest first).
        results_df = stock_screener.screener_view(order="Change")

        # Handle edge case gracefully
        if results_df.empty:
            return []

        # Extract the 'Ticker' column and convert it to a simple Python list.
        tickers = results_df["Ticker"].tolist()

        # Reverse the list so highest gainers are first
        tickers.reverse()

        return tickers[:limit]

    except Exception as e:
        # A simple print for now, but in produc tion use a structured logger
        print(f"An error occured during scanning: {e}")
        return []


print(find_premarket_movers())
