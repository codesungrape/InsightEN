"""..."""

import pytest
import pandas as pd
from scanner import find_premarket_movers

# This test checks if the 'find_premarket_movers' function behaves correctly.
# It uses a "mock" to pretend to be the 'finvizfinance' library,
# isolating our test, making it fast and reliable- a UNIT test?


def test_find_movers_successfully(mocker):
    """
    Given that the finviz library returns a valid DataFrame of stocks,
    When we call find_premarket_movers,
    Then we should get a simple list of ticker symbols.
    """
    # Arrange: Setup our mock data
    mock_data = {
        "Ticker": ["AAPL", "TSLA", "NVDA"],
        "Company": ["Apple Inc.", "Tesla, Inc.", "NVIDIA Corporation"],
        "Price": [170.00, 250.00, 450.00],
    }
    mock_dataframe = pd.DataFrame(mock_data)

    # Arrange:
    # Create the mock object with pytest's 'mocker' to find Screener class from the library
    # replace it's 'get_as_dataframe' method with one that just returns our fake data.
    _mock_screener_instance = mocker.patch(
        "finvizfinance.screener.overview.Overview.screener_view",
        return_value=mock_dataframe,
    )

    # Act: Call the function we are testing
    tickers = find_premarket_movers()

    # Assert: Check if the result is what we expect
    assert tickers == ["NVDA", "TSLA", "AAPL"]
    assert isinstance(tickers, list)


def test_find_movers_when_none_found(mocker):
    """Given that the finviz library returns an empty DataFrame,
    When we call find_premarket_movers,
    Then we should get an empty list back.
    This test handles "edge case" - when no tickers are returned.
    """
    # Arrange: Setup an empty DataFrame
    empty_dataframe = {"Ticker": []}
    mock_empty_dataframe = pd.DataFrame(empty_dataframe)
    mocker.patch(
        "finvizfinance.screener.overview.Overview.screener_view",
        return_value=mock_empty_dataframe,
    )

    # Act
    tickers = find_premarket_movers()

    # Assert
    assert tickers == []


#    assert isinstance(tickers, list)


@pytest.mark.parametrize(
    "exception_to_raise, expected_log_message_part",
    [
        # Provide tuples of values for each test run
        (ValueError("Simulated invalid filter"), "Simulated invalid filter"),
        (TypeError("Simulated type mismatch"), "Simulated type mismatch"),
        (AttributeError("Simulated attribute error"), "Simulated attribute error"),
    ],
)
def test_find_movers_handles_exception(
    exception_to_raise, expected_log_message_part, mocker
):
    """
    Given that the finviz library raises a specific, handled exception,
    When we call find_premarket_movers,
    Then the function should log the error and return an empty list gracefully.
    """
    # Arrange with 'side-effect'
    _mock_screener_instance = mocker.patch(
        "finvizfinance.screener.overview.Overview.screener_view",
        side_effect=exception_to_raise,
    )
    # Mock the logger and get a reference to our "spy button"
    mock_log_error = mocker.patch("scanner.log.error")

    # Act
    result = find_premarket_movers()

    assert result == []
    mock_log_error.assert_called_once()

    # Get the arguments that our "spy button" was called with.
    # call_args is a tuple of the positional arguments. The second one is the exception object 'e'.
    call_args, _call_kwargs = mock_log_error.call_args
    logged_exception_object = call_args[1]

    # Assert that the string representation of the logged exception contains our expected text.
    assert expected_log_message_part in str(logged_exception_object)
