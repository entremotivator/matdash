# app.py
import streamlit as st
from vapi_python import Vapi

# --- Sidebar ---
st.sidebar.title("Vapi Voice Assistant")
api_key = st.sidebar.text_input("Vapi Public API Key", type="password")
assistant_id = st.sidebar.text_input("Assistant ID")

if 'vapi' not in st.session_state and api_key:
    st.session_state.vapi = Vapi(api_key=api_key)

if st.sidebar.button("Start Call", disabled=not (api_key and assistant_id)):
    st.session_state.vapi.start(assistant_id=assistant_id)
    st.sidebar.success("Call started!")

if st.sidebar.button("Stop Call", disabled='vapi' not in st.session_state):
    st.session_state.vapi.stop()
    st.sidebar.info("Call stopped.")

st.sidebar.markdown("---")
st.sidebar.write("Powered by [VapiAI/client-sdk-python]")

# --- Main Page ---
st.title("🗣️ Community Chatroom")
st.write("Welcome to the online community! Chat with others or use the sidebar to interact with the Vapi voice assistant.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

user_msg = st.text_input("Type your message:")

if st.button("Send", key="send_btn") and user_msg:
    st.session_state.messages.append(("You", user_msg))

# Display chat history
for sender, msg in st.session_state.messages:
    st.write(f"**{sender}:** {msg}")

