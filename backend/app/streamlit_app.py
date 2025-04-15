import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://backend:8000")

st.set_page_config(page_title="Local AI Chatbot", page_icon="🤖")

st.title("🤖 Local AI Chatbot")

# Initialize session state for chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Try to fetch history from backend
    try:
        response = requests.get(f"{API_URL}/history")
        if response.status_code == 200:
            history = response.json()
            # Convert backend history format to streamlit format
            for msg in history:
                st.session_state.messages.append({"role": msg["role"], "content": msg["content"]})
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is up?"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send to backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Thinking..."):
                response = requests.post(f"{API_URL}/chat", json={"message": prompt})
                
                if response.status_code == 200:
                    data = response.json()
                    full_response = data["content"]
                    message_placeholder.markdown(full_response)
                    # Add assistant response to state
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    message_placeholder.error(f"Error: {response.text}")
        except Exception as e:
            message_placeholder.error(f"Connection error: {e}")
