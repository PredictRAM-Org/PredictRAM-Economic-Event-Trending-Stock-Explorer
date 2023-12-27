import streamlit as st
import requests
import pandas as pd

# Function to get news articles based on a search query
def get_news_articles(query, api_key):
    params = {
        'q': query,
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
    }

    response = requests.get("https://newsapi.org/v2/everything", params=params)

    if response.status_code == 200:
        articles = response.json().get('articles')
        return articles
    else:
        st.error("Error fetching news articles.")
        return None

# Function to get trending stocks related to economic events
def get_trending_stocks(articles):
    # Extract economic event from the search query
    economic_event = st.session_state.search_query.lower()

    # Map economic events to relevant stocks
    economic_event_stocks = {
        "india inflation": ["HDFCBANK", "RELIANCE", "INFY", "TCS", "ITC"],
        "interest rate": ["ICICIBANK", "HDFCBANK", "AXISBANK", "SBIN"],
        "gdp india": ["HDFC", "RELIANCE", "TCS", "ICICIBANK", "LTI"],
        "infrastructure india": ["LT", "L&T", "BAJAJ-AUTO", "HAVELLS", "ABB"],
        "industrial production": ["BAJAJ-AUTO", "HAVELLS", "ABB", "LT", "TATASTEEL"],
        "manufacturing india": ["BAJAJ-AUTO", "HAVELLS", "ABB", "LT", "TATASTEEL"]
    }

    # Get relevant stocks based on the economic event
    known_stock_symbols = economic_event_stocks.get(economic_event, [])

    # Debugging statements
    st.write(f"Search Query: {st.session_state.search_query}")
    st.write(f"Selected Economic Event: {economic_event}")
    st.write(f"Known Stock Symbols: {known_stock_symbols}")

    # Extract stock symbols from news articles
    trending_stocks = set()

    for article in articles:
        for symbol in known_stock_symbols:
            # Check if the stock symbol is present in the article title
            if symbol.lower() in article['title'].lower():
                trending_stocks.add(symbol)

    return list(trending_stocks)

# Streamlit App
def main():
    st.title("Economic Indicator News and Trending Stocks")

    # User input for API key
    api_key = st.text_input("Enter your NewsAPI.org API key:")

    # Search query input
    search_query = st.text_input("Enter a search query for economic indicator news:")

    # Store the search query in session state
    st.session_state.search_query = search_query.lower()

    # Get news articles
    if st.button("Search News"):
        if api_key:
            news_articles = get_news_articles(search_query, api_key)

            if news_articles is not None:
                st.session_state.news_articles = news_articles  # Store in session state
                st.header("Latest News Articles:")
                for article in news_articles:
                    st.write(f"**{article['title']}**")
                    st.write(article['description'])
                    st.write(f"Source: {article['source']['name']}")
                    st.write("---")
            else:
                st.warning("No news articles found.")
        else:
            st.warning("Please enter your NewsAPI.org API key.")

    # Get trending stocks
    if st.button("Get Trending Stocks"):
        if 'news_articles' in st.session_state:
            trending_stocks = get_trending_stocks(st.session_state.news_articles)

            if trending_stocks:
                st.header("Trending Stocks Related to Economic Events:")
                for stock in trending_stocks:
                    st.write(f"- {stock}")
            else:
                st.warning("No trending stocks found.")
        else:
            st.warning("Please search for news articles first.")

if __name__ == "__main__":
    main()
