import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Directly configure Gemini API key
genai.configure(api_key="AIzaSyDsm8Rpp9nPzKhHAM9zvCKSRAEJR-c6ABc")  # <-- Replace with your API key

# Model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Title
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Basic AI Chatbot UI (With Bonus Features)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# BONUS FEATURE 1: Chatbot Personality Selector
personality = st.selectbox(
    "Choose Chatbot Personality:",
    ["Friendly 😊", "Professional 💼", "Funny 😂", "Short Answers ✨"]
)

# BONUS FEATURE 2: Clear Chat Button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.toast("Chat cleared!")

# User input
user_input = st.text_input("You:", placeholder="Type your message...")

# Send Button
if st.button("Send"):
    if user_input.strip() != "":
        # Add user message to history
        st.session_state.messages.append(
            {"role": "user", "text": user_input, "time": datetime.now().strftime("%H:%M")}
        )

        # Personality prompt logic
        persona_prompt = {
            "Friendly 😊": "Respond in a friendly and warm tone.",
            "Professional 💼": "Respond formally and professionally.",
            "Funny 😂": "Respond with humor and light jokes.",
            "Short Answers ✨": "Respond very briefly in 1-2 lines."
        }

        prompt = f"""
        You are an AI assistant. {persona_prompt[personality]}
        User message: {user_input}
        """

        # Call Gemini API
        response = model.generate_content(prompt).text

        # Add bot reply to history
        st.session_state.messages.append(
            {"role": "bot", "text": response, "time": datetime.now().strftime("%H:%M")}
        )

# BONUS FEATURE 3: Beautiful Chat Bubbles
st.markdown("### 💬 Chat History")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="background:#DCF8C6;padding:10px;border-radius:10px;margin-bottom:10px;text-align:right;color:black;">
                <b>You:</b> {msg['text']} <br><small>{msg['time']}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background:#E8E8E8;padding:10px;border-radius:10px;margin-bottom:10px;text-align:left;color:black;">
                <b>Bot:</b> {msg['text']} <br><small>{msg['time']}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
