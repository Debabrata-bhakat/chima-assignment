import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
import os

# AUTH = st.secrets["SYNTHESIA_API"]
# BEARER = st.secrets["BEARER"]
AUTH = os.environ['SYNTHESIA_API']
BEARER = os.environ['BEARER']

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": AUTH
}

conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="vid", ttl=5)
existing_data = existing_data.dropna(how="all")
existing_data = existing_data[['video_id','video_title']]

url = "https://api.synthesia.io/v2/videos"


# reverse traversing the dataframe so as to get the latest videos on top
for index in range(len(existing_data) - 1, -1, -1):
    row = existing_data.iloc[index]
    hook_url = url + "/" + row['video_id']
    response = requests.get(hook_url, headers=headers).json()
    # if video generation is complete
    if response.get('status') == "complete":
        data = response['download']
        st.subheader(f"Video with id {row['video_id']} and title {row['video_title']} is available for download below.")
        st.video(data, format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False,
                    autoplay=False, muted=False)
    # if not complete show corresponding message
    else:
        st.subheader(f"Video with id {row['video_id']} and title {row['video_title']} is still generating.")




