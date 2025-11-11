"""..."""

import logging
import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from transformers import logging as transformers_logging
from transformers import pipeline

# 1. SETUP & CONFIGURATION
# -------------------------

log = logging.getLogger(__name__)
# Suppress the informational warnings from the transformers library
transformers_logging.set_verbosity_error()
# Load environment variables from .env file
load_dotenv()

# Initialize the FinBERT sentiment analysis pipeline.
# The model 'ProsusAI/finbert' is specifically trained on financial text.
log.info("Initialzing FinBERT sentiment pipeline...")
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
log.info("FinBERT pipeline initialized.")


# 2. DATA STRUCTURES (PYDANTIC MODELS)
# ----------------------------------
class AnalayzedArticle(BaseModel):
    """Holds the data for a single news article after sentiment analysis"""

    title: str
    sentiment_label: str
    sentiment_score: float


class NewsSentiment(BaseModel):
    """Represents the overall sentiment for a ticker, including analyzed articles."""

    ticker: str
    overall_sentiment: float
    articles: list[AnalayzedArticle] = []


# 3. CORE LOGIC
# ---------------


def get_news_with_sentiment(ticker: str) -> NewsSentiment | None:
    """
    Fetches news for a ticker, analyzes snetiment using FinBERT, and returns a summary.

    Args:
         ticker (str): The stock ticker symbol to analyze (e.g., "APPL").

    Returns:
         NewsSentiment | None: A dataclass containing the overall sentiment
         And a list of analyzed articles, or None if an error occurs.
    """

    # Set up logging and api_key
    log.info("Fetching and analyzing news for ticker: %s", ticker)
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        log.error("ALPHA_VANTAGE_API_KEY not found in environment variables.")
        return None

    try:
        # Step A: Fetch News from Alpha Vantage
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}"
        log.debug("Requesting news from URL: %s, url")

        # Set a timeout to prevent the request from hanging indefinitely
        # (connect_timeout, read_timeout) in seconds.
        response = requests.get(url, timeout=(3, 10))
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        data = response.json()
        # get everything from data["feed"] if it exists,
        # otherwise use an empty list.
        articles = data.get("feed", [])

        if not articles:
            log.warning("No news articles found for ticker: %s", ticker)
            return NewsSentiment(ticker=ticker, overall_sentiment=0.0)

        # Step B: Prepare titles for analysis
        titles = [article["title"] for article in articles]

        # Step C: Analyze Sentiment iwth FinBERT
        log.debug("Running %d titles through FinBERT pipeline...", len(titles))
        sentiment_results = sentiment_pipeline(titles)

        # Step D: Process and Combine results
        analyzed_articles = []
        total_score = 0
        for article, sentiment in zip(articles, sentiment_results, strict=True):
            finbert_score = sentiment[0]["score"]
            finbert_label = sentiment[0]["label"]

            # Negative scores --> negative numbers
            if finbert_label == "negative":
                finbert_score *= -1

            analyzed_articles.append(
                AnalayzedArticle(
                    title=article["title"],
                    sentiment_label=finbert_label,
                    sentiment_score=finbert_score,
                )
            )
            total_score += finbert_score

        # Step E: Calculate Overall Score and Return
        overall_score = total_score / len(articles) if articles else 0
        log.info(
            "Analysis complete for %s. Overall sentiment score: %.2f",
            ticker,
            overall_score,
        )

        return NewsSentiment(
            ticker=ticker, overall_sentiment=overall_score, articles=analyzed_articles
        )

    except requests.exceptions.RequestException as e:
        log.error("API request failed for ticker %s: %s", ticker, e, exc_info=True)
        return None
    except (ValidationError, KeyError) as e:
        log.error(
            "Failed to parse or validate API data for ticker %s: %s",
            ticker,
            e,
            exc_info=True,
        )
        return None
    except Exception as e:
        log.error(
            "An unexpected error occurred for ticker %s: %s", ticker, e, exc_info=True
        )
        return None
