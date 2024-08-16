import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initial CSS setup for light mode
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e8e0cd; /* Beige background */
        color: #352e25; /* Default brown text color */
    }
    .title, .subtitle {
        color: #352e25; /* Brown color for titles */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<h1 class="title">Billboard Chart Song Fetcher</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Options")
dark_mode = st.sidebar.checkbox('Enable Dark Mode')

# Dark Mode
if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #2E2E2E;
        color: #FFFFFF;
    }
    .title, .subtitle {
        color: #FFFFFF; /* White color for titles in dark mode */
    }
    </style>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<h2 class="subtitle">Find out what\'s hot or what was 🔥.</h2>', unsafe_allow_html=True)

# Chart selection dropdown
chart_choice = st.selectbox(
    "Select a chart",
    ("Billboard Hot 100", "TikTok Billboard Top 50")
)

# Date input (calendar widget)
selected_date = st.date_input("Select a date", value=datetime.now(), min_value=datetime(1958, 8, 4), max_value=datetime.now())
week_date = selected_date.strftime("%Y-%m-%d")

# Function to fetch data
@st.cache_data
def fetch_billboard_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to generate YouTube search URL
def generate_youtube_link(song, artist):
    search_query = f"{song} {artist} official music video"
    return f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"

# Chart URL and logic based on selection
if week_date:
    if chart_choice == "Billboard Hot 100":
        url = f"https://www.billboard.com/charts/hot-100/{week_date}"
        st.write(f"Fetching data from: {url}")
    else:
        url = f"https://www.billboard.com/charts/tiktok-billboard-top-50/{week_date}"
        st.write(f"Fetching data from: {url}")
    
    with st.spinner('Fetching data...'):
        web_page = fetch_billboard_data(url)

    if web_page:
        soup = BeautifulSoup(web_page, "html.parser")
        
        songs = []
        artists = []
        youtube_links = []

        if chart_choice == "Billboard Hot 100":
            tag = soup.find_all(name="li", class_="lrv-u-width-100p")
        else:
            tag = soup.find_all(name="li", class_="o-chart-results-list__item")

        for i in tag:
            song_tag = i.find(name="h3", class_="c-title")
            artist_tag = i.find(name="span", class_="c-label")
            if song_tag and artist_tag:
                song = song_tag.get_text(strip=True)
                artist = artist_tag.get_text(strip=True)
                youtube_link = generate_youtube_link(song, artist)
                
                songs.append(song)
                artists.append(artist)
                youtube_links.append(youtube_link)

        if songs and artists:
            st.markdown('<h2 class="subtitle">Top Songs on the Selected Billboard Chart:</h2>', unsafe_allow_html=True)
            for song, artist, link in zip(songs, artists, youtube_links):
                st.markdown(f"- {song} by {artist} [Watch on YouTube]({link})")

            # Display a bar chart of the top 10 songs
            fig, ax = plt.subplots()
            ax.barh([f"{i+1}. {song}" for i, song in enumerate(songs[:10])], range(10, 0, -1))
            st.pyplot(fig)

            # Provide an option to download the data as a CSV
            df = pd.DataFrame({'Song': songs, 'Artist': artists, 'YouTube Link': youtube_links})
            st.download_button('Download as CSV', df.to_csv(index=False).encode('utf-8'), 'billboard_chart.csv', 'text/csv')

        else:
            st.write("Nothing this week, try a week before 🙏.")
    else:
        st.write("Error fetching the Billboard chart data. Please check the date and try again.")
