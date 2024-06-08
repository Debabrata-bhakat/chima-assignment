import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Feeback form")
st.markdown("Please give us feedback where we can improve.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Sheet1", usecols=list(range(2)), ttl=5)
print(existing_data)
existing_data = existing_data.dropna(how="all")
# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    company_name = st.text_input(label="Your feedback*")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit form")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not company_name:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "CompanyName": company_name
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
            # Update Google Sheets with the new vendor data
            conn.update(worksheet="Sheet1", data=updated_df)

            st.success("Feedback successfully submitted!")
