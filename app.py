import streamlit as st
import requests
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

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

# Function to extract entities from news articles using spaCy
def get_entities_from_articles(articles):
    entities = set()

    for article in articles:
        doc = nlp(article['title'])
        for ent in doc.ents:
            entities.add(ent.text)

    return list(entities)

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

    # Get entities from news articles
    if st.button("Get Entities from Articles"):
        if 'news_articles' in st.session_state:
            entities = get_entities_from_articles(st.session_state.news_articles)

            if entities:
                st.header("Entities Extracted from Articles:")
                for entity in entities:
                    st.write(f"- {entity}")
            else:
                st.warning("No entities found in the articles.")
        else:
            st.warning("Please search for news articles first.")

if __name__ == "__main__":
    main()
