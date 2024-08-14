import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

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
st.markdown('<h1 class="title">Billboard Hot 100 Song Fetcher</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Options")
week_date = st.sidebar.text_input('Enter the date you want to travel to (YYYY-MM-DD):')
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

# Fetch Billboard data
@st.cache_data
def fetch_billboard_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

if week_date:
    url = f"https://www.billboard.com/charts/hot-100/{week_date}"
    st.write(f"Fetching data from: {url}")
    
    with st.spinner('Fetching data...'):
        web_page = fetch_billboard_data(url)

    if web_page:
        soup = BeautifulSoup(web_page, "html.parser")
        
        songs = []
        artists = []
        tag = soup.find_all(name="li", class_="lrv-u-width-100p")
        for i in tag:
            t = i.find_all(name="ul")
            for j in t:
                t1 = j.find_all(name="li")
                for k in t1:
                    t2 = k.find_all(name="h3")
                    for l in t2:
                        t3 = l.get_text()
                        songs.append(str(t3).strip("\n\t"))
                    t4 = k.find_all(name="span")
                    for m in list(t4):
                        t5 = m.get_text()
                        artists.append(str(t5).strip("\n\t"))
        
        artists = artists[::16]
        song_artist = [f"{songs[i]} by {artists[i]}" for i in range(len(songs))]
        
        if song_artist:
            st.markdown('<h2 class="subtitle">Top Songs on the Billboard Hot 100:</h2>', unsafe_allow_html=True)
            for song in song_artist:
                st.write(f"- {song}")

            # Display a bar chart of the top 10 songs
            fig, ax = plt.subplots()
            ax.barh([f"{i+1}. {song}" for i, song in enumerate(songs[:10])], range(10, 0, -1))
            st.pyplot(fig)

            # Provide an option to download the data as a CSV
            df = pd.DataFrame({'Song': songs, 'Artist': artists})
            st.download_button('Download as CSV', df.to_csv(index=False).encode('utf-8'), 'billboard.csv', 'text/csv')

        else:
            st.write("No songs found for this date.")
    else:
        st.write("Error fetching the Billboard Hot 100 data. Please check the date and try again.")
