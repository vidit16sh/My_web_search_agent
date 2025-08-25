# app.py
import asyncio
import streamlit as st
from core import handle_query  # your handler

st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🤖", layout="wide")

# -------------------------
# Custom CSS (blue glow UI)
# -------------------------
st.markdown("""
<style>
:root{
  --bg:#060608;
  --panel:#0b0f12;
  --text:#cbd6df;
  --muted:#8d98a3;
  --accent:#1e90ff;      /* main blue */
  --accent-light:#5ec8ff;/* lighter blue */
}

/* page */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}

/* center column spacing */
main .block-container {
    padding-top: 36px;
    padding-bottom: 90px;  /* leave room for input */
}

/* Title */
h1 {
    font-family: 'Bebas Neue', sans-serif;
    text-align: center;
    color: var(--text);
    letter-spacing: 8px;
    margin-bottom: 6px;
    text-shadow: 0 6px 18px rgba(30,144,255,0.10);
    font-size: 48px;
}
h1::after{
    content: "";
    display:block;
    margin: 12px auto 0;
    width: 110px;
    height: 6px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(94,200,255,0.12), rgba(30,144,255,0.22));
}

/* subtitle */
p {
    text-align: center;
    color: var(--muted);
    margin-top: 6px;
    margin-bottom: 26px;
}

/* chat message container adjustments */
[data-testid="stChatMessage"] {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin: 10px 0;
    padding-left: 22px; /* space for accent bar */
}

/* inner bubble (actual visible content) */
[data-testid="stChatMessage"] > div {
    position: relative;
    width: 100%;
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 16px 18px;
    color: var(--text);
    line-height: 1.6;
    box-shadow: 0 4px 22px rgba(0,0,0,0.6);
    overflow-wrap: anywhere;
}

/* assistant bubble subtle blue tint */
[data-testid="stChatMessage"][data-author="assistant"] > div {
    background: rgba(30,144,255,0.02);
}

/* user bubble subtle red tint (keeps user messages distinct) */
[data-testid="stChatMessage"][data-author="user"] > div {
    background: rgba(229,9,20,0.03);
}

/* replace heavy border-left with a slim accent bar using ::before
   This avoids the huge rounded-outline problem and creates a neat accent */
[data-testid="stChatMessage"][data-author="assistant"] > div::before {
    content: "";
    position: absolute;
    left: -14px;
    top: 12px;
    bottom: 12px;
    width: 8px;
    border-radius: 8px;
    background: linear-gradient(180deg, var(--accent-light), var(--accent));
    box-shadow: 0 0 22px rgba(30,144,255,0.20);
}

/* user accent bar on the right (small, distinct) */
[data-testid="stChatMessage"][data-author="user"] > div::after {
    content: "";
    position: absolute;
    right: -14px;
    top: 12px;
    bottom: 12px;
    width: 8px;
    border-radius: 8px;
    background: linear-gradient(180deg,#ff8a8a,#ff4f4f);
    box-shadow: 0 0 16px rgba(255,79,79,0.12);
}

/* subtle icon indicator (if streamlit places an icon block before message) */
[data-testid="stChatMessage"] > div > .stMarkdown, 
[data-testid="stChatMessage"] > div > .stText {
    color: var(--text);
}

/* fade-in animation for messages */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"] > div {
    animation: fadeIn 260ms ease-in-out;
}

/* Chat input (glass pill) */
[data-testid="stChatInput"] > div {
    position: fixed;               /* pinned to bottom */
    left: 50%;
    transform: translateX(-50%);
    bottom: 18px;                  /* spacing from bottom */
    width: calc(100% - 160px);     /* responsive width with side margins */
    max-width: 1100px;
    background: linear-gradient(180deg, rgba(255,255,255,0.018), rgba(255,255,255,0.01));
    border: 1px solid rgba(30,144,255,0.12);
    border-radius: 999px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 10px 40px rgba(8,18,36,0.7), 0 0 28px rgba(30,144,255,0.035) inset;
    z-index: 9999;
}

/* input field itself */
[data-testid="stChatInput"] input {
    background: transparent !important;
    border: none !important;
    outline: none !important;
    color: var(--text) !important;
    font-size: 16px;
    flex: 1;
    padding: 6px 8px;
}

/* placeholder color */
[data-testid="stChatInput"] input::placeholder {
    color: rgba(200,220,255,0.30) !important;
}

/* send button circle */
[data-testid="stChatInput"] button {
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 50%;
    background: transparent;
    border: 1px solid rgba(30,144,255,0.16);
    color: var(--accent);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 180ms ease;
    box-shadow: 0 6px 24px rgba(10,30,60,0.55);
}

/* hover / active for send button */
[data-testid="stChatInput"] button:hover {
    background: var(--accent);
    color: #00121a;
    transform: translateY(-2px);
    box-shadow: 0 10px 36px rgba(30,144,255,0.28), 0 0 32px rgba(30,144,255,0.18);
}

/* reduce Streamlit menu visual clutter */
header[role="banner"] { background: transparent !important; }

/* small screens: make input full width with side padding */
@media (max-width: 880px) {
  [data-testid="stChatInput"] > div {
    width: calc(100% - 32px);
    left: 16px;
    transform: none;
    border-radius: 16px;
    bottom: 12px;
  }
  h1 { font-size: 36px; letter-spacing: 6px; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Main UI (centered layout)
# -------------------------
# center content with columns so messages don't stretch too wide
left, center, right = st.columns([1, 6, 1])

with center:
    st.title("J.A.R.V.I.S.")
    st.markdown("<p>Your personal AI assistant.</p>", unsafe_allow_html=True)

    # chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # display messages
    for role, content in st.session_state.history:
        # 'role' should be "user" or "assistant"
        with st.chat_message(role):
            st.markdown(content)

# --- input handling (outside column so chat_input is rendered and our fixed input CSS picks it) ---
if prompt := st.chat_input("How may I assist you?"):
    # show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # add to history
    st.session_state.history.append(("user", prompt))

    # assistant - show spinner while processing
    with st.chat_message("assistant"):
        with st.spinner("J.A.R.V.I.S. is thinking..."):
            try:
                answer = asyncio.run(handle_query(prompt))
            except Exception as e:
                answer = f"⚠️ Error: {e}"

            st.markdown(answer)
            st.session_state.history.append(("assistant", answer))
