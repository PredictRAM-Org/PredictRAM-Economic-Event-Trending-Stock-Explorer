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
    # List of known stock symbols
    known_stock_symbols = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB", "V", "PYPL", "NFLX", "BA"]

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
