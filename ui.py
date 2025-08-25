import asyncio
import streamlit as st
from core import handle_query

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Poppins', sans-serif;
    background: #0e0e0e;
    color: #e0e0e0;
    min-height: 100vh;
}

/* Title */
h1 {
    font-family: 'Bebas Neue', sans-serif;
    text-align: center;
    color: #FFD700;
    text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    margin-bottom: 0.2em;
}
p {
    text-align: center;
    color: #888;
    margin-top: -0.3em;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    padding: 0.9em 1.1em;
    margin: 0.5em 0;
    border-radius: 14px;
    backdrop-filter: blur(12px);
    border-left: 3px solid;
    word-wrap: break-word;
    white-space: pre-wrap;
    animation: fadeIn 0.3s ease-in-out;
}

/* User bubble */
[data-testid="stChatMessage"][data-author="user"] {
    background: rgba(229, 9, 20, 0.12);
    border-color: #E50914;
    margin-left: auto;
    max-width: 60%;
}

/* Assistant bubble */
[data-testid="stChatMessage"][data-author="assistant"] {
    background: rgba(255, 215, 0, 0.12);
    border-color: #FFD700;
    margin-right: auto;
    max-width: 75%;
}

/* Smooth fade-in animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Chat Input Styling */
[data-testid="stChatInput"] > div {
    background: rgba(20, 20, 20, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 215, 0, 0.4);
    border-radius: 30px;
    padding: 0.6em 1em;
    color: #fff;
    transition: all 0.3s ease-in-out;
}

[data-testid="stChatInput"] > div:focus-within {
    border: 1px solid #FFD700;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
}

[data-testid="stChatInput"] input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

[data-testid="stChatInput"] input {
    color: #fff !important;
}

[data-testid="stChatInput"] button {
    background: rgba(255, 215, 0, 0.2);
    border: 1px solid rgba(255, 215, 0, 0.6);
    border-radius: 50%;
    color: #FFD700;
    transition: all 0.3s ease-in-out;
}

[data-testid="stChatInput"] button:hover {
    background: #FFD700;
    color: black;
    box-shadow: 0 0 10px #FFD700, 0 0 20px #FFD700;
}
</style>
""", unsafe_allow_html=True)

# --- Main UI ---
st.title("J.A.R.V.I.S.")
st.markdown("<p>Your personal AI assistant.</p>", unsafe_allow_html=True)

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Show messages
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

# Input + response
if query := st.chat_input("How may I assist you?"):
    with st.chat_message("user"):
        st.markdown(query)

    try:
        answer = asyncio.run(handle_query(query))
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.history.append(("user", query))
    st.session_state.history.append(("assistant", answer))
