import streamlit as st
import requests

# NewsAPI.org API Key (You can replace this with user input)
API_KEY = "YOUR_NEWSAPI_KEY"

# Base URL for NewsAPI.org
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Function to get news articles based on a search query
def get_news_articles(query, api_key):
    params = {
        'q': query,
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        articles = response.json().get('articles')
        return articles
    else:
        st.error("Error fetching news articles.")
        return None

# Function to get trending stocks related to economic events
def get_trending_stocks():
    # Add your logic to fetch trending stocks based on economic events
    # You can use financial APIs or news sentiment analysis for this

    # Placeholder data for demonstration purposes
    trending_stocks = ["Stock1", "Stock2", "Stock3"]
    return trending_stocks

# Streamlit App
def main():
    st.title("Economic Indicator News and Trending Stocks")

    # User input for API key
    user_api_key = st.text_input("Enter your NewsAPI.org API key:", API_KEY)

    # Search query input
    search_query = st.text_input("Enter a search query for economic indicator news:")

    # Get news articles
    if st.button("Search News"):
        if user_api_key:
            news_articles = get_news_articles(search_query, user_api_key)

            if news_articles:
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
        trending_stocks = get_trending_stocks()

        if trending_stocks:
            st.header("Trending Stocks Related to Economic Events:")
            for stock in trending_stocks:
                st.write(f"- {stock}")
        else:
            st.warning("No trending stocks found.")

if __name__ == "__main__":
    main()