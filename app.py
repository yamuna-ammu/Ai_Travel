import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime

# Load API Key from Streamlit Secrets
GOOGLE_API_KEY = st.secrets.get("hugging_face_api")

# Function to Generate Travel Recommendations
def fetch_travel_suggestions(source, destination, travel_date):
    prompt_system = SystemMessage(
        content=(
            "You are an AI travel assistant. Provide travel options including cab, train, bus, and flight, "
            "with estimated costs, durations, and relevant travel tips. Consider date-specific availability "
            "and price fluctuations. Additionally, recommend top tourist spots with travel tips."
        )
    )
    prompt_user = HumanMessage(
        content=f"Plan a trip from {source} to {destination} on {travel_date}. Suggest travel modes with cost and duration."
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
    try:
        response = llm.invoke([prompt_system, prompt_user])
        return response.content if response else "⚠️ No response received from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# Streamlit UI Configuration
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# Header Section
st.markdown("""
    <div style='text-align: center;'>
        <h1>🌍 Smart Travel Planner</h1>
        <p style='font-size: 16px;'>Get AI-powered travel recommendations effortlessly.</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# Input Section
st.subheader(" Plan Your Journey")
source = st.text_input(" Source Location", placeholder="Enter your location")
destination = st.text_input(" Destination", placeholder="Enter your destination")
travel_date = st.date_input("📅 Travel Date", min_value=datetime.today())

if st.button("🔍 Get Travel Options"):
    if source.strip() and destination.strip():
        with st.spinner("🔄 Fetching travel recommendations..."):
            travel_details = fetch_travel_suggestions(source, destination, travel_date)
            st.success("✅ Here are your travel recommendations:")
            st.markdown(travel_details)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")

# Footer Section
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <p>✨ Powered by Streamlit & Google Gemini AI ✨</p>
    </div>
""", unsafe_allow_html=True)
