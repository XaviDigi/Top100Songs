Billboard Chart Song Fetcher
This project is a Streamlit web application that allows users to explore historical and current Billboard charts, including the Billboard Hot 100 and the TikTok Billboard Top 50. You can select a date and view the top songs for that week, with YouTube links for easy access. Additionally, a CSV download option is available for the chart data.

Features
Light and Dark Mode: Toggle between light and dark modes for a comfortable viewing experience.
Chart Selection: Choose between two popular Billboard charts: Billboard Hot 100 and TikTok Billboard Top 50.
Date Picker: Select any date from August 4, 1958, to the current day to view chart data from that week.
YouTube Integration: Automatically generate YouTube search links for the official music videos.
Top 10 Visualization: View a bar chart visualizing the top 10 songs of the selected week.
CSV Export: Download the song data (title, artist, YouTube link) as a CSV file.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/billboard-chart-fetcher.git
cd billboard-chart-fetcher
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
streamlit run app.py
How It Works
Select the Billboard Hot 100 or TikTok Billboard Top 50 chart from the dropdown menu.
Pick a date to view the chart for that week.
The app fetches the song titles, artists, and provides YouTube links to the official music videos.
Download the chart data as a CSV file or visualize the top 10 songs in a bar chart.
Example

Technologies Used
Streamlit: For building the interactive user interface.
BeautifulSoup: For scraping the Billboard website.
Matplotlib: For visualizing the top 10 songs.
Pandas: For handling and exporting the data.
Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to submit a pull request.
