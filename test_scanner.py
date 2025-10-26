import pandas as pd
from scanner import find_premarket_movers

# This test checks if the 'find_premarket_movers' function behaves correctly. 
# It uses a "mock" to pretend to be the 'finvizfinance' library, isolating our test, making it fast and reliable- a UNIT test?

def test_find_movers_successfully(mocker):
    """
    Given that the finviz library returns a valid DataFrame of stocks,
    When we call find_premarket_movers,
    Then we should get a simple list of ticker symbols.
    """
    # Arrange: Setup our mock data
    mock_data = {
        "Ticker": ['AAPL', 'TSLA', 'NVDA'],
        "Company": ['Apple Inc.', 'Tesla, Inc.', 'NVIDIA Corporation'],
        'Price': [170.00, 250.00, 450.00]
    }
    mock_dataframe = pd.DataFrame(mock_data)

    # Arrange: Create the mock object with pytest's 'mocker' to find Screener class from the library + replace its 'get_as_dataframe' method wiht one that just returns our fake data.
    mock_screener_instance = mocker.patch(
        'finvizfinance.screener.overview.Overview.screener_view',
        return_value=mock_dataframe
    )

    # Act: Call the function we are testing
    tickers = find_premarket_movers()

    # Assert: Check if the result is what we expect
    assert tickers == ['AAPL', 'TSLA', 'NVDA']
    assert isinstance(tickers, list)

def test_find_movers_when_none_found(mocker):
    """Given that the finviz library returns an empty DataFrame,
    When we call find_premarket_movers,
    Then we should get an empty list back.
    This test handles "edge case" - when no tickers are returned.
    """
    # Arrange: Setup an empty DataFrame
    empty_dataframe = {'Ticker': []}
    mock_empty_dataframe = pd.DataFrame(empty_dataframe)
    mocker.patch(
        'finvizfinance.screener.overview.Overview.screener_view',
        return_value=mock_empty_dataframe
    )

    # Act
    tickers = find_premarket_movers()

    # Assert
    assert tickers == []
#    assert isinstance(tickers, list)
     