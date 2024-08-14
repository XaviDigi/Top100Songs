import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Billboard Hot 100 Song Fetcher")

week_date = st.text_input("Enter the date you want to travel to (YYYY-MM-DD):", "")

if week_date:
    url = f"https://www.billboard.com/charts/hot-100/{week_date}"
    st.write(f"Fetching data from: {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        web_page = response.text
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
            st.write("### Top Songs on the Billboard Hot 100:")
            for song in song_artist:
                st.write(f"- {song}")
        else:
            st.write("No songs found for this date.")
    else:
        st.write("Error fetching the Billboard Hot 100 data. Please check the date and try again.")
