import streamlit as st
import requests

# Define the API URL
API_URL = "http://127.0.0.1:5000/chat"

# Streamlit UI
st.set_page_config(page_title="Chat Assistant", layout="centered")
st.title("🗨️ AI Chat Assistant")
st.write("Ask me anything!")

# Input box
user_query = st.text_input("Enter your query:")

# Button to send request
if st.button("Ask"):
    if user_query.strip():
        try:
            # Send request to Flask API
            response = requests.post(API_URL, json={"query": user_query})
            
            # Debug: Show raw response (remove in production)
            st.write("Debug Response:", response.status_code, response.text)

            if response.status_code == 200:
                st.success(response.json().get("response", "No response received."))
            else:
                st.error("Error: API request failed.")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a valid query.")
