import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd



def save_vid(vid_id, vid_title):
    # Establishing a Google Sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing vendors data
    existing_data = conn.read(worksheet="vid", ttl=5)
    print(existing_data)
    existing_data = existing_data.dropna(how="all")
    vendor_data = pd.DataFrame(
                [
                    {
                        "video_id": vid_id,
                        "video_title": vid_title
                    }
                ]
            )
    updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
    # Update Google Sheets with the new vendor data
    conn.update(worksheet="vid", data=updated_df)

