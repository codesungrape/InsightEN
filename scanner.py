from finvizfinance.screener.overview import Overview
import pandas as pd


def find_premarket_movers():
    """
    Scans for stocks with high relative volume and volatility to identify potential day trading opportunities. 
    Returns:
        list[str]: A list of stock ticker symbols that match the criteria.
        Returns an empty list if none are found or an error occurs. 
    """
    # Define filters to narrow down thousands of stocks to a manageable few. 
    # Using high "Relative Volume" is a classic way to find stocks with unsual interest from traders
    filters = [
        'sh_price_o5', # Price over $5 
        'ta_relvol_o2', # Relative Volume over 4 (trading >2x normal)
        'ta_volatility_wo10' # Weekly volatility over 10% (find stocks that move)
    ]
    # UPDATE: I Want it to check for the highest movers and above 3$

    try:
        
        # The Overview class handles screening for the 'overview' page on Finviz
        stock_screener = Overview()
        # Make the call to finviz library to perform the scan
        results_df = stock_screener.screener_view(
            filters=filters,
            signal='Top Gainers'
            )
        
        # Handle edge case gracefully
        if results_df.empty:
            return []
        
        # Extract the 'Ticker' column and convert it to a simple Python list. 
        tickers = results_df['Ticker'].tolist()
        return tickers
    
    except Exception as e:
        # A simple print for now, but in produc tion use a structured logger
        print(f"An error occured duting scanning: {e}")
        return []
    


