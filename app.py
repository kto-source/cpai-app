import streamlit as st
from datetime import datetime, timedelta
import random
import time

# --- CONFIGURATION & PAGE SETUP ---
st.set_page_config(page_title="CPAI - College Pass AI", page_icon="🎓", layout="wide")

# Custom CSS for a "Vivid and Entertaining" look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FF5722;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# --- MOCK AI BRAIN (The Backend Logic) ---

def mock_ai_response(prompt, type="general"):
    """Simulates AI thinking and returns a response."""
    time.sleep(1) # Simulate processing time
    
    responses = {
        "explain": f"Okay, let's break this down Barney-style! 🧠\n\n**Concept:** {prompt}\n\nImagine this concept is like a pizza...",
        "quiz": f"Pop Quiz Time! 📝\n\nQ: What is the core idea of '{prompt}'?\nA) Something cool\nB) Something boring\nC) Both",
        "essay": f"Here is a draft essay on '{prompt}':\n\n**Title: The Hidden Depths**\n\nIntroduction: The topic of {prompt} has long fascinated scholars...",
        "paraphrase": f"Here is a smoother version:\n\n'{prompt}' essentially means rewriting the core idea in your own unique words.",
        "humanize": f"I've added a human touch to this:\n\nHonestly, the concept of {prompt} is pretty interesting when you look at it from a real-world perspective. It's not just theory; it's about how things actually work."
    }
    return responses.get(type, "I'm thinking... 🤔")

def generate_schedule(subjects, hours_per_day):
    schedule = []
    today = datetime.now()
    for i, subject in enumerate(subjects):
        day = today + timedelta(days=i)
        schedule.append({
            "Day": day.strftime("%A (%b %d)"),
            "Subject": subject.strip(),
            "Focus": f"Review Chapter {i+1} & Practice Problems",
            "Duration": f"{hours_per_day} Hours"
        })
    return schedule

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("# 🎓 CPAI Menu")
st.sidebar.info("Your vivid AI study buddy!")

mode = st.sidebar.radio(
    "Choose Your Mode:",
    ["🏠 Home", "📚 Study Buddy", "✍️ Writing Assistant", "📅 Study Scheduler"],
    index=0
)

# --- MAIN APP LOGIC ---

# 1. HOME SCREEN
if mode == "🏠 Home":
    st.markdown('<p class="main-header">Welcome to CPAI! 🎓</p>', unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🧠 **Study Buddy**\nRevise chapters and learn complex topics simply.")
    
    with col2:
        st.warning("✍️ **Writing Assistant**\nEssays, paraphrasing, and humanizing text.")
        
    with col3:
        st.error("📅 **Scheduler**\nPlan your study week efficiently.")
    
    st.write("\n")
    user_input = st.text_input("Ask me anything to get started:", placeholder="e.g., 'Help me understand Quantum Physics'")
    if st.button("Ask CPAI"):
        if user_input:
            with st.spinner("Thinking..."):
                response = mock_ai_response(user_input, "explain")
                st.success(response)
        else:
            st.error("Please type something first!")

# 2. STUDY BUDDY MODE
elif mode == "📚 Study Buddy":
    st.markdown('<p class="sub-header">📚 Study Buddy Mode</p>', unsafe_allow_html=True)
    st.write("Paste your notes or a chapter topic below. I'll help you understand it or quiz you!")
    
    study_input = st.text_area("Paste Chapter Text or Topic Here:", height=200)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Explain Like I'm 5 🧸"):
            if study_input:
                with st.spinner("Processing..."):
                    result = mock_ai_response(study_input, "explain")
                    st.write(result)
            else:
                st.warning("Please input some text first!")
                
    with col2:
        if st.button("Quiz Me! 📝"):
            if study_input:
                with st.spinner("Creating quiz..."):
                    result = mock_ai_response(study_input, "quiz")
                    st.write(result)
            else:
                st.warning("Please input some text first!")

# 3. WRITING ASSISTANT MODE
elif mode == "✍️ Writing Assistant":
    st.markdown('<p class="sub-header">✍️ Writing Assistant</p>', unsafe_allow_html=True)
    st.write("Need help with that paper? I've got your back.")
    
    writing_task = st.selectbox("What do you need help with?", 
                                ["Write an Essay Draft", "Paraphrase Text", "Humanize Text (Make it sound natural)"])
    
    user_text = st.text_area("Enter your topic or text to modify:", height=150)
    
    if st.button("Generate ✨"):
        if user_text:
            with st.spinner("Writing..."):
                if "Essay" in writing_task:
                    result = mock_ai_response(user_text, "essay")
                elif "Paraphrase" in writing_task:
                    result = mock_ai_response(user_text, "paraphrase")
                else:
                    result = mock_ai_response(user_text, "humanize")
                
                st.subheader("Result:")
                st.write(result)
                st.info("Tip: Always review and edit AI-generated content to ensure it matches your voice!")
        else:
            st.error("Input cannot be empty.")

# 4. STUDY SCHEDULER
elif mode == "📅 Study Scheduler":
    st.markdown('<p class="sub-header">📅 Smart Study Scheduler</p>', unsafe_allow_html=True)
    st.write("Let's organize your semester! Enter your subjects below.")
    
    subjects = st.text_input("Enter subjects (separated by commas)", "Math, History, Biology, Coding")
    hours = st.slider("Hours per subject per day", 1, 6, 2)
    
    if st.button("Create My Schedule"):
        subject_list = subjects.split(',')
        schedule = generate_schedule(subject_list, hours)
        
        st.subheader("📋 Your Custom Schedule")
        
        # Display as a nice table
        for item in schedule:
            with st.expander(f"{item['Day']} - {item['Subject']}"):
                st.write(f"**Duration:** {item['Duration']}")
                st.write(f"**Focus:** {item['Focus']}")
                st.button(f"Start {item['Subject']} Session", key=f"btn_{item['Day']}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("CPAI v1.0 | Made with ❤️ for Students")
