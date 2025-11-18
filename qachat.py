from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Set a dark theme for a look closer to the reference image
st.set_page_config(
    page_title="AI-Powered Financial Planner", 
    page_icon="💰", 
    layout="wide", # Use wide layout for more space
    initial_sidebar_state="expanded"
)

# Load API Key and configure the model
# NOTE: Replace 'os.getenv("GOOGLE_API_KEY")' with your actual key in a deployed environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-2.5-flash" # Use the corrected model name

# Function to reset history when preferences change
def reset_history():
    """Clears both the displayed chat history and the model's internal history."""
    st.session_state['chat_history'] = []
    st.session_state['model_history'] = []
    
# Store the chat object in session state so we can access its history later
if 'chat_session' not in st.session_state:
    st.session_state['chat_session'] = None

def get_gemini_response(system_prompt, question):
    """
    Function to load Gemini model, apply the system prompt, and get streaming response.
    Stores the chat object in session_state.
    """
    try:
        # Re-create the model and start a new chat with the system instruction
        model = genai.GenerativeModel(
            MODEL_NAME, 
            system_instruction=system_prompt
        )
        # We start a new chat, using the saved model history (if available).
        chat = model.start_chat(history=st.session_state.get('model_history', []))
        
        # Save the chat object to session state for accessing history later
        st.session_state['chat_session'] = chat 
        
        response = chat.send_message(question, stream=True)
        
        return response
    except Exception as e:
        st.error(f"An API error occurred: {e}")
        return None

# --- 2. SIDEBAR FINANCIAL PREFERENCES (Customized for Financial Planning) ---

with st.sidebar:
    st.title("🏦 Financial Profile")
    
    age_group = st.selectbox(
        "Age Group",
        ("18-25 (Young Professional)", "26-35 (Family Planning)", "36-50 (Mid-Career)", "51+ (Pre/Post Retirement)"),
        key='current_age',
        on_change=reset_history,
        help="Select your current life stage."
    )
    
    income = st.selectbox(
        "Monthly Income Range (Approx.)",
        ("Less than ₹20,000", "₹20,000 - ₹50,000", "₹50,000 - ₹1,00,000", "More than ₹1,00,000"),
        key='current_income',
        on_change=reset_history,
        help="Select your approximate monthly take-home income in Rupees."
    )
    
    interest_rate = st.selectbox(
        "Avg. Debt Interest Rate (Approx.)",
        ("None (No significant debt)", "Under 8% (e.g., Home/Auto Loan)", "8% - 15% (e.g., Personal Loan)", "Over 15% (e.g., Credit Card/High-Interest Debt)"),
        key='current_rate',
        on_change=reset_history,
        help="Estimate the average annual interest rate on your debts."
    )
    
    risk_tolerance = st.selectbox(
        "Risk Tolerance",
        ("Conservative (Safety first)", "Moderate (Balanced growth and safety)", "Aggressive (High growth, high risk)"),
        key='current_risk',
        on_change=reset_history,
        help="How much risk are you willing to take with investments?"
    )
    
    goal = st.selectbox(
        "Primary Financial Goal",
        ("Debt Reduction", "Retirement Planning", "Large Purchase (e.g., house/car)", "General Wealth Building"),
        key='current_goal',
        on_change=reset_history,
        help="What is the main financial objective you are working towards?"
    )
    
    time_horizon = st.selectbox(
        "Investment Time Horizon",
        ("Short-term (1-3 years)", "Medium-term (3-10 years)", "Long-term (10+ years)"),
        key='current_horizon',
        on_change=reset_history,
        help="How long until you need the money for your primary goal?"
    )
    
    knowledge = st.selectbox(
        "Financial Knowledge Level",
        ("Novice", "Familiar", "Experienced Investor", "Professional"),
        key='current_knowledge',
        on_change=reset_history,
        help="How comfortable are you with financial terms and planning concepts?"
    )

    st.markdown("---")
    st.title("⚙️ App Controls")
    
    if st.button("🧹 Clear Conversation History", help="This clears both the displayed history and the model's internal memory."):
        reset_history()
        
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("Your personal AI-Powered Financial Planner, customized via the profile settings above.")

# --- 3. MAIN APP LAYOUT AND SYSTEM PROMPT GENERATION ---

st.markdown("<h1 style='text-align: center;'>💰 AI-Powered Financial Planner Chatbot</h1>", unsafe_allow_html=True)
st.markdown("---")

# Generate the comprehensive System Instruction based on sidebar inputs
system_prompt = f"""
You are a highly qualified and ethical Financial Planner. Your specialization is creating customized financial plans.
Your goal is to provide safe, realistic, and personalized advice based on the user's financial profile:
- **Age Group:** {age_group}
- **Monthly Income:** {income} (Rupees)
- **Average Debt Interest Rate:** {interest_rate}
- **Risk Tolerance:** {risk_tolerance}
- **Primary Financial Goal:** {goal}
- **Investment Time Horizon:** {time_horizon}
- **Financial Knowledge Level:** {knowledge}

Always tailor your response to these settings. For example, if 'Average Debt Interest Rate' is 'Over 15%', prioritize debt payoff methods (like Avalanche or Snowball) over new investments. For a '18-25 (Young Professional)', suggest higher risk/equity exposure. For a '51+ (Pre/Post Retirement)', suggest conservative, income-generating instruments. Use a tone appropriate for a user with a {knowledge} level of knowledge. Provide clear steps and actionable recommendations focused on achieving the user's {goal} within a {risk_tolerance} risk framework. If the user asks for investment advice, prioritize safety and diversification. DO NOT provide specific buy/sell recommendations, only general asset allocation advice.

CRITICAL INSTRUCTION: When providing investment or financial product recommendations, **ALWAYS format them as a numbered or bulleted list** for the clearest possible output, explaining how each option aligns with the user's profile.
"""

# Initialize session states if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
if 'model_history' not in st.session_state:
    st.session_state['model_history'] = []


# ==============================
# ✅ Display All Previous History
# ==============================

st.subheader("Ask for Your Personalized Plan")
chat_container = st.container(height=400, border=True)

with chat_container:
    if not st.session_state['chat_history']:
        # Applied custom class for bright color to the greeting
        st.markdown(f"<p class='greeting-message'>**Hello! I am your AI Financial Planner. I'm ready to help you plan for your goal: {goal}**</p>", unsafe_allow_html=True)

    for role, text in st.session_state['chat_history']:
        # Use Streamlit's built-in chat elements
        with st.chat_message("user" if role == "You" else "assistant"):
            st.markdown(text)


# ==============================
# ✅ Handle New User Input (with Loading Indicator)
# ==============================
if prompt := st.chat_input("Ask for a budget, investment strategy, or debt plan..."):
    # 1. Display the user message immediately in the container
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # 2. Add user message to history
    st.session_state['chat_history'].append(("You", prompt))

    # 3. Get and display bot response with streaming and loading indicator
    with chat_container:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Call the function with the dynamically generated system prompt
            response_stream = get_gemini_response(system_prompt, prompt)
            
            if response_stream:
                for chunk in response_stream:
                    try:
                        if chunk.text: 
                            full_response += chunk.text
                            # Use st.markdown here for the streaming text
                            message_placeholder.markdown(full_response + "▌") 
                    except ValueError:
                        continue
                
                # Final update to remove the cursor
                message_placeholder.markdown(full_response)
                
                # 4. Add bot response to history for display persistence
                st.session_state['chat_history'].append(("Bot", full_response))

    # 5. Save the history only AFTER the streaming iteration is complete
    if st.session_state['chat_session']:
        try:
            st.session_state['model_history'] = st.session_state['chat_session'].history
        except Exception as e:
            st.error(f"Error saving model history: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #aaa;'>Powered by AI – Disclaimer: I am an AI, not a certified financial advisor. Always consult a professional before making major financial decisions.</p>", unsafe_allow_html=True)

# 🎨 Custom CSS for Improved Bot Response Visibility and Custom Look
st.markdown("""
<style>
/* 1. Ensure full screen dark background for consistency */
.stApp {
    background-color: #0d1117; /* Dark background (GitHub dark theme) */
    min-height: 100vh;
}

/* Fix for main content area to cover full width/height */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
}

/* Selector for sidebar background */
.st-emotion-cache-1c9v62e, .st-emotion-cache-16j9op3 { 
    background-color: #161b22 !important; /* Slightly lighter dark for sidebar */
}

/* 🌟 CHANGE 1: REMOVE BLACK BACKGROUND FROM CHAT INPUT */
/* Target the actual input field background/color */
[data-testid="stChatInput"] > div:first-child > textarea {
    background-color: #161b22 !important; /* Set to match sidebar/dark theme, removing black */
    color: #f0f6fc !important; /* Ensure input text is bright */
    border: 1px solid #30363d !important; 
}
/* Target the surrounding container for the chat input */
[data-testid="stChatInput"] {
    background-color: transparent !important; 
}


/* --- 🌟 SIDEBAR TITLE COLOR (override) --- */
/* Target the st.title elements (H1 and H2) inside the sidebar and force white for contrast */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #ffffff !important; /* Force white color for sidebar titles */
}


/* --- 🌟 CHANGE 3: FORCING BRIGHT WHITE BOT RESPONSE TEXT (IMPROVED) --- */

/* Target the core markdown container and its children aggressively */
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) div[data-testid="stMarkdownContainer"] *, 
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) div[data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important; /* Pure White for maximum contrast */
}

/* Explicitly target common text elements (p, li, span, code) inside the assistant's message */
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) p,
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) li,
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) span,
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) code,
[data-testid="stChatMessage"]:has(.st-emotion-cache-1c5c1g3) a {
    color: #FFFFFF !important; /* Force all text inside the bubble to white */
    text-shadow: 0 0 1px #FFFFFF; /* Optional: Adds a tiny bit of glow/boldness */
}


/* Ensure the assistant message bubble itself is dark for contrast */
.st-emotion-cache-1c5c1g3 { /* Class for the assistant bubble */
    background-color: #21262d !important; /* A nice dark shade for the bubble */
}


/* --- 🌟 CHANGE 2: BRIGHT COLOR FOR INITIAL GREETING --- */
.greeting-message {
    color: #4CAF50 !important; /* A bright green/teal color for emphasis */
    font-size: 1.1em;
    font-weight: bold;
}

/* --- GENERAL TEXT BRIGHTENING (Sidebar, Headings) --- */

h1, h2, h3, h4, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div[data-testid="stText"],
.st-emotion-cache-18ni7ap,
.st-emotion-cache-10a4v9k 
{ 
    color: #f0f6fc !important; /* Brighter text/headings */
}

/* Fix for the user's chat bubble text */
.st-chat-message-container [data-testid="chat-message-container"]:has(.st-emotion-cache-1c5c1g3) div[data-testid="stMarkdownContainer"] {
    color: #f0f6fc !important;
}

</style>
""", unsafe_allow_html=True)
