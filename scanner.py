from finvizfinance.screener.overview import Overview
import pandas as pd


def find_premarket_movers() -> list[str]:
    """
    Scans for stocks with high relative volume and volatility to identify potential day trading opportunities. 
    Returns:
        list[str]: A list of stock ticker symbols that match the criteria.
                    Returns an empty list if none are found or an error occurs. 
    """

    # UPDATE: I Want it to check for the highest movers and above 3$

    try:
        
        # The Overview class handles screening for the 'overview' page on Finviz
        stock_screener = Overview()

        # Define filters to narrow down thousands of stocks to a manageable few. 
        # Using high "Relative Volume" is a classic way to find stocks with unsual interest from traders
        filters_dict = {
            'Price': 'Over $5', 
            'Relative Volume': 'Over 2', 
            'Volatility': 'Week - Over 10%'
        }

        stock_screener.set_filter(filters_dict=filters_dict)

        # Make the call to finviz library to perform the scan
        results_df = stock_screener.screener_view()
        
        # Handle edge case gracefully
        if results_df.empty:

            return []
        
        # Extract the 'Ticker' column and convert it to a simple Python list. 
        tickers = results_df['Ticker'].tolist()
        print(f"Found {len(tickers)} potential movers: {tickers}")
        return tickers
    
    except Exception as e:
        # A simple print for now, but in produc tion use a structured logger
        print(f"An error occured during scanning: {e}")
        return []
    

print(find_premarket_movers())
