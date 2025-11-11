"""
This test verifies our professional news analysis function.
It uses mocks to simuate the Alpha Vantage API call and
the FinBert transformer pipeline.
This ensures our internal logic (processing, scoring, averaging) works correctly.

** Alpha Vantage's News & Sentiments API offers real-time access to
financial news and sentiment analysis across a wide range of topics,
including economics, technology, real estate, and individual tickers.

Leveraging advanced AI, the API not only aggregates news but also
provides sentiment scores to help assess potential market impact.
"""

from unittest.mock import MagicMock

import pytest
import requests
from pydantic import ValidationError

from src.enrichment.news import (
    NewsSentiment,
    get_news_with_sentiment,
)


def test_get_news_with_sentiment_success(mocker):
    """
    Given a ticker,
    When the Alpha Vantage API returns valid news data,
    And the FinBERT pipeline returns predictable sentiment scores,
    Then the function should return a correctly structured and
    calculated NewsSentiment object.
    """
    # ARRANGE: Mock the 'requests.get' call
    # Create a mock response object that has a .json() method.
    mock_api_response = {
        "feed": [
            {
                "title": "ACME Corp Announces Record Profits",
                "summary": "Profits are up 50% year over year...",
                "source": "Business Wire",
            },
            {
                "title": "Regulatory headwinds hit ACME Corp stock",
                "summary": "New government regulations may impact future earnings.",
                "source": "Reuters",
            },
        ]
    }
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock()  # Mock this to do nothing
    mock_response.json = mocker.Mock(return_value=mock_api_response)
    mocker.patch("requests.get", return_value=mock_response)

    # ---- Mock FinBERT (transformers pipeline) ----
    # Define a simple function that returns different scores for our test headlines.
    # We want to control the exact output of the sentiment pipeline for our test.
    def mock_pipeline_logic(text_list):
        results = []
        for text in text_list:
            if "Profits" in text:
                # FinBERT returns a list of dictionaries
                results.append([{"label": "positive", "score": 0.98}])
            elif "headwinds" in text:
                results.append([{"label": "negative", "score": 0.95}])
        return results

    # Use a MagicMock to make the pipeline callable and assign the dynamic function
    mock_sentiment_pipeline = MagicMock(side_effect=mock_pipeline_logic)
    mocker.patch("src.enrichment.news.sentiment_pipeline", mock_sentiment_pipeline)

    # Act
    result = get_news_with_sentiment("ACME")

    # Assert
    assert isinstance(result, NewsSentiment)
    assert len(result.articles) == 2
    assert result.articles[0].title == "ACME Corp Announces Record Profits"
    assert result.articles[0].sentiment_label == "positive"
    assert result.articles[0].sentiment_score == pytest.approx(0.98)

    assert result.articles[1].title == "Regulatory headwinds hit ACME Corp stock"
    assert result.articles[1].sentiment_label == "negative"
    # NOTE: We'll convert negative labels to negative scores in our logic
    assert result.articles[1].sentiment_score == pytest.approx(-0.95)

    # The overall score should be the average of the individual scores (0.98 and -0.95)
    expected_overall_score = (0.98 - 0.95) / 2
    assert result.overall_sentiment == pytest.approx(expected_overall_score)


def test_returns_None_when_no_api_key_found(mocker):
    """
    When os.getenv returns nothing, or api_key not found,
    application logs.error(<error_msg>)
    exits runtime with a return of None
    """
    # Arrange
    err_msg = "ALPHA_VANTAGE_API_KEY not found in environment variables."
    mocker.patch("os.getenv", return_value=None)

    # Mock the logger to capture log calls
    mock_logger = mocker.patch("src.enrichment.news.log")

    # Act
    result = get_news_with_sentiment("ACME")

    # Assert
    assert result is None
    mock_logger.error.assert_called_once_with(err_msg)


def test_returns_NewsSentiment_obj_with_zero_sentiment_when_no_articles_found(mocker):
    """
    When the API returns no articles, the function should return
    a NewsSentiment object with an empty articles list and an overall
    sentiment score of 0.0.
    """
    # Mock API response with empty feed
    mock_response = mocker.Mock()
    mock_response.raise_for_status = mocker.Mock()
    mock_response.json = mocker.Mock(return_value={"feed": []})
    mocker.patch("requests.get", return_value=mock_response)

    # Ensure sentiment pipeline is present but not used (or returns empty)
    mock_sentiment_pipeline = MagicMock(return_value=[])
    mocker.patch("src.enrichment.news.sentiment_pipeline", mock_sentiment_pipeline)

    result = get_news_with_sentiment("ACME")

    assert isinstance(result, NewsSentiment)
    assert isinstance(result.articles, list)
    assert len(result.articles) == 0
    assert result.overall_sentiment == pytest.approx(0.0)


@pytest.mark.parametrize(
    "exception_to_raise, expected_log_message_part",
    [
        (
            requests.exceptions.RequestException("Simulated network failure"),
            "API request failed for ticker",
        ),
        (
            ValidationError.from_exception_data("Simulated validation mismatch", []),
            "Failed to parse or validate API data",
        ),
        # More realistic Pydantic error
        (
            KeyError("Simulated key 'feed' not found"),
            "Failed to parse or validate API data",
        ),
        (Exception("Simulated generic error"), "An unexpected error occurred"),
    ],
)
def test_get_news_with_sentiment_handles_exception(
    mocker, exception_to_raise, expected_log_message_part
):
    # Arrange: ensure an API key exists and
    # simulate the requests.get raising the provided exception
    mocker.patch("os.getenv", return_value="DUMMY_API_KEY")
    mocker.patch("requests.get", side_effect=exception_to_raise)
    # Mock the logger object within the news module
    mock_log_error = mocker.patch("src.enrichment.news.log.error")

    # Act
    result = get_news_with_sentiment("ACME")

    # Assert
    assert result is None
    mock_log_error.assert_called_once()

    # The first positional arg is the format string
    logged_message = mock_log_error.call_args[0][0]
    assert expected_log_message_part in logged_message
