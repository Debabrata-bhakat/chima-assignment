import streamlit as st
import time
import requests
from magic_script import return_summary

import os
from dotenv import load_dotenv

load_dotenv()

AUTH = st.secrets["SYNTHESIA_API"]
BEARER = st.secrets["BEARER"]
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



        # Dropdown for selecting the number of words in the ad script
        word_count = st.selectbox(
            "Approximately how many words in the ad script?",
            options=range(1, 51),  # Dropdown options from 1 to 50
            index=0  # Default selection is the first option
        )

        # Display the selected word count
        st.write(f"You selected {word_count} words for the ad script.")


        # scriptText = "  \n" +company + "  \n" + product + "  \n" + consumer
        scriptText = return_summary(company,product,consumer,BEARER,word_count)
        st.write(f"Title: *{title}*")
        st.write(f"Script: {scriptText}")
        submit_button = st.form_submit_button("Submit")


    if submit_button:
        payload["title"] = title
        payload["input"][0]['scriptText'] = scriptText
        print(scriptText)
        response = requests.post(url, json=payload, headers=headers).json()
        print(response)
        if response.get('status'):
            submit_button_clicked = True
            video_id = response.get('id')
        else:
            st.error("Some unknown error occured. Please try again after a few minutes")

    # If submit button is clicked, display form details and progress bar
    if submit_button_clicked:
        task_completed = False
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Title: **{title}")
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
                status_text.text(f"Progress: {current_progress}%")
            if task_completed:
                current_progress = 100
                progress_bar.progress(current_progress)
                status_text.text("Task completed! You can now download this video.")
            else:
                status_text.text("Our servers are going through a high load. Please ensure that your commercial contains at most 50 words!")


if __name__ == '__main__':
    main()