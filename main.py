import streamlit as st
import time
import requests
from magic_script import return_summary
from streamlit_gsheets import GSheetsConnection

import pandas as pd
from save_vid_data import save_vid

import os
from dotenv import load_dotenv

load_dotenv()

# AUTH = st.secrets["SYNTHESIA_API"]
# BEARER = st.secrets["BEARER"]
AUTH = os.environ['SYNTHESIA_API']
BEARER = os.environ['BEARER']


url = "https://api.synthesia.io/v2/videos"

payload = {
    "test": "false",
    "visibility": "public",
    "input": [
        {
            "avatarSettings": {
                "horizontalAlign": "center",
                "scale": 1,
                "style": "rectangular",
                "seamless": False
            },
            "backgroundSettings": {"videoSettings": {
                "shortBackgroundContentMatchMode": "freeze",
                "longBackgroundContentMatchMode": "trim"
            }},
            "avatar": "anna_costume1_cameraA",
            "background": "\"off_white\""
        }
    ]
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": AUTH
}

def main():
    st.title("Generate commercials for your target consumers in a click! ⚡⚡⚡")
    st.subheader("Our models churn text to magic 🎩🪄")

    submit_button_clicked = False

    # Create a form to get user input
    with st.form("my_form"):
        company = st.text_input("Enter company Information")
        product = st.text_input("Enter product Information")
        consumer = st.text_input("Enter target Consumer Profile")
        title = st.text_input("Enter title for the commercial")



        # Dropdown for selecting the ad script length
        length_options = ["Short", "Medium", "Long"]
        selected_length = st.selectbox(
            "Advertisement length",
            options=length_options,
            index=0  # Default selection is the first option
        )

        # scriptText = "  \n" +company + "  \n" + product + "  \n" + consumer
        submit_button = st.form_submit_button("Submit")

    scriptText = ""
    if submit_button:
        word_count = 15
        if(selected_length == "Short"):
            word_count = 15
        elif(selected_length == "Medium"):
            word_count = 30
        else:
            word_count = 50
        scriptText = return_summary(company,product,consumer,BEARER,word_count)
        payload["title"] = title
        payload["input"][0]['scriptText'] = scriptText
        print(scriptText)
        response = requests.post(url, json=payload, headers=headers).json()
        print(response)

        # st.write(f"Title: *{title}*")
        # st.write(f"Script: {scriptText}")

        if response.get('status'):
            submit_button_clicked = True
            video_id = response.get('id')
            save_vid(video_id,title)
        else:
            st.error("Some unknown error occured. Please try again after a few minutes")
    
    

    # If submit button is clicked, display form details and progress bar
    if submit_button_clicked:
        task_completed = False
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Title: {title}")
            st.write(f"Script: {scriptText}")

        with col2:
            progress_bar = st.progress(0)
            status_text = st.empty()
            max_time = 400
            hook_url = url + "/" + video_id
            # hook_url = url  + "/" + '18d24a08-a741-496e-a374-ec848550648c'
            for i in range(max_time):
                response = requests.get(hook_url, headers=headers).json()
                print(i)
                if response.get('status') == "complete":
                    data = response['download']
                    st.video(data, format="video/mp4", start_time=0, subtitles=None, end_time=None, loop=False,
                             autoplay=False, muted=False)

                    task_completed = True
                    break
                time.sleep(3)  # Simulate some computation
                current_progress = 100*i//max_time
                progress_bar.progress(current_progress)
                status_text.text(f"Progress: {current_progress}%\n Your video id is : {video_id}\n Please take note of it. \nYou can leave this page now. \nYour video will be in downloads page.")
            if task_completed:
                current_progress = 100
                progress_bar.progress(current_progress)
                status_text.text("Task completed! You can now download this video.")
            else:
                status_text.text("Our servers are going through a high load. Please ensure that your commercial contains at most 50 words!")


if __name__ == '__main__':
    main()