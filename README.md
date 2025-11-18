# AI-Powered Financial Planner (Streamlit + Gemini 2.5)

A smart, interactive financial planning assistant built with Streamlit and Google Gemini 2.5, designed to generate personalized financial plans based on age, income, debt, risk tolerance, and long-term goals.

# 🚀 Features
🔹 Personalized Financial Planning

Real-time recommendations based on:

Age group

Monthly income

Debt & interest rate

Risk tolerance

Financial goals

Time horizon

Investment knowledge level

🔹 Built-in Sidebar Controls

The user can update preferences anytime, and the model automatically resets its internal memory.

🔹 Real-Time Streaming Chat

Gemini 2.5 responses stream smoothly using Streamlit’s chat interface.

🔹 Clean Dark UI

Custom CSS added for:

Chat bubble redesign

Clean input box

High-contrast dark theme

Better readability

# 🛠️ Tech Stack

Python

Streamlit

Google Gemini 2.5 Flash

dotenv

Custom CSS


# 🔑 Environment Setup

Create a .env file:

GOOGLE_API_KEY=your_api_key_here


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

# ⭐ How It Works

User selects their financial profile

System generates a custom system prompt

Gemini 2.5 processes it

Chatbot streams personalized financial plans

Chat history is maintained across interactions
