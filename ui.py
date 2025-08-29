import streamlit as st
import time
from datetime import datetime

# --- 1. Page Configuration & Styling ---
st.set_page_config(
    page_title="J.A.R.V.I.S. Multi-Agent Console",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for the J.A.R.V.I.S. theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@400;500&display=swap');

    /* --- Global Styles --- */
    .stApp {
        background: linear-gradient(135deg, #0a0f1c 0%, #1a1f2e 100%);
        color: #00d4ff;
    }
    .stApp > header {
        background-color: transparent;
    }
    .main .block-container {
        padding-top: 2rem;
    }

    /* --- Animation --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }

    /* --- Landing Page Title --- */
    .landing-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #0099cc, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        margin-bottom: 0.5rem;
    }
    .landing-subtitle {
        font-family: 'Roboto Mono', monospace;
        text-align: center;
        font-size: 1.2rem;
        color: rgba(0, 212, 255, 0.8);
        margin-bottom: 4rem;
    }

    /* --- Agent Card Styling --- */
    .agent-card {
        background: rgba(10, 25, 50, 0.7);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .agent-card:hover {
        border-color: rgba(0, 255, 255, 0.8);
        box-shadow: 0 0 40px rgba(0, 255, 255, 0.3);
        transform: translateY(-10px);
    }
    .agent-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .agent-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d4ff;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    .agent-description {
        font-family: 'Roboto Mono', monospace;
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.5;
        margin: 1rem 0;
        flex-grow: 1;
    }

    /* --- Agent Panel Styling --- */
    .agent-panel {
        background: rgba(10, 25, 50, 0.9);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        max-width: 800px;
        margin: 1rem auto;
    }
    .agent-panel-header {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .status-badge {
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
        padding: 8px 16px;
        border-radius: 20px;
        text-transform: uppercase;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    .status-active {
        background: rgba(0, 255, 100, 0.2);
        color: #00ff64;
        border: 1px solid #00ff64;
    }
    .console-area {
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1.5rem 0;
        height: 300px;
        overflow-y: auto;
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
    }
    .log-entry {
        margin-bottom: 0.5rem;
    }
    .log-timestamp {
        color: rgba(0, 255, 255, 0.7);
    }

    /* --- Button & Input Styling --- */
    .stButton button, .stTextInput input {
        border-radius: 25px !important;
        border: 2px solid rgba(0, 212, 255, 0.5) !important;
        background: rgba(0, 20, 40, 0.8) !important;
        color: #00d4ff !important;
        font-family: 'Roboto Mono', monospace !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        border-color: #00ffff !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. Agent Definitions ---
AGENTS = {
    "web_search": {"name": "Web Search Agent", "desc": "Advanced web crawling and real-time data retrieval from global networks.", "icon": "🌐"},
    "rag": {"name": "RAG Agent", "desc": "Knowledge synthesis using retrieval-augmented generation from vector databases.", "icon": "🧠"},
    "analytics": {"name": "Analytics Agent", "desc": "Data analysis and statistical processing with advanced ML algorithms.", "icon": "📊"},
    "vision": {"name": "Vision Agent", "desc": "Computer vision and image analysis with neural network pattern recognition.", "icon": "👁️"}
}

# --- 3. Session State Initialization ---
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None
if "logs" not in st.session_state:
    st.session_state.logs = {}
if "final_answer" not in st.session_state:
    st.session_state.final_answer = ""

# --- 4. Helper Functions ---
def add_log(agent_id, message):
    """Adds a timestamped log message for a specific agent."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    if agent_id not in st.session_state.logs:
        st.session_state.logs[agent_id] = []
    st.session_state.logs[agent_id].append(f"<span class='log-timestamp'>[{timestamp}]</span> > {message}")

def simulate_processing(agent_id, query):
    """Simulates agent activity with live log updates."""
    st.session_state.final_answer = ""
    st.session_state.logs[agent_id] = [] # Clear previous logs
    log_area = st.empty()

    steps = [
        f"Initializing protocols for query: '{query}'...",
        "Connecting to data streams...",
        "Analyzing query parameters...",
        "Executing core logic module...",
        "Cross-referencing data points...",
        "Synthesizing results...",
        "Finalizing response package...",
        "Processing complete."
    ]

    for step in steps:
        add_log(agent_id, step)
        log_html = "<div class='console-area'>" + "<br>".join(st.session_state.logs[agent_id]) + "</div>"
        log_area.markdown(log_html, unsafe_allow_html=True)
        time.sleep(0.4)

    st.session_state.final_answer = f"**Analysis for '{query}':** Based on multi-modal processing, the optimal course of action has been determined. All relevant data points indicate a 97.5% probability of success for the proposed solution."

# --- 5. UI Rendering Functions ---

def render_landing_page():
    """Displays the main dashboard with agent selection cards."""
    st.markdown("<div class='landing-title'>J.A.R.V.I.S. CONSOLE</div>", unsafe_allow_html=True)
    st.markdown("<p class='landing-subtitle'>Just A Rather Very Intelligent System // Multi-Agent Dashboard</p>", unsafe_allow_html=True)

    cols = st.columns(len(AGENTS))

    for i, (agent_id, agent_info) in enumerate(AGENTS.items()):
        with cols[i]:
            # Use st.markdown to create the styled container
            st.markdown(
                f"""
                <div class="agent-card fade-in">
                    <div>
                        <div class="agent-icon">{agent_info['icon']}</div>
                        <div class="agent-name">{agent_info['name']}</div>
                        <p class="agent-description">{agent_info['desc']}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Place the button below the markdown card
            if st.button("Activate Module", key=f"activate_{agent_id}", use_container_width=True):
                st.session_state.active_agent = agent_id
                st.rerun()

def render_agent_panel():
    """Displays the interactive panel for the currently active agent."""
    agent_id = st.session_state.active_agent
    agent_info = AGENTS[agent_id]

    st.markdown(f"""
        <div class='agent-panel fade-in'>
            <div class='agent-panel-header'>
                <span>{agent_info['icon']} {agent_info['name']}</span>
                <span class='status-badge status-active'>Active</span>
            </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Return to Dashboard"):
        st.session_state.active_agent = None
        st.session_state.final_answer = ""
        if agent_id in st.session_state.logs:
             st.session_state.logs[agent_id] = [] # Clear logs on exit
        st.rerun()

    st.write("---")
    query = st.text_input("Enter your query or command:", key=f"query_{agent_id}", placeholder="e.g., Analyze market trends...")

    if st.button("Execute Task", key=f"run_{agent_id}", use_container_width=True):
        if query:
            simulate_processing(agent_id, query)
        else:
            st.warning("Please enter a query before executing.", icon="⚠️")

    # Display Logs and Final Answer
    if agent_id in st.session_state.logs and st.session_state.logs[agent_id]:
        log_html = "<div class='console-area'>" + "<br>".join(st.session_state.logs[agent_id]) + "</div>"
        st.markdown(log_html, unsafe_allow_html=True)

    if st.session_state.final_answer:
        st.success("✅ **Final Report:**")
        st.markdown(st.session_state.final_answer)

    st.markdown("</div>", unsafe_allow_html=True) # Close agent-panel div


# --- 6. Main App Router ---
if st.session_state.active_agent is None:
    render_landing_page()
else:
    render_agent_panel()