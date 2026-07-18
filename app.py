import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="My Custom AI Chatbot", page_icon="🤖")

st.title("🤖 My Custom AI Chatbot")
st.write("You can chat as much as you want. This page will never slow down!")

# Configure Gemini API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chats
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_question := st.chat_input("Ask me anything... (English ya Hindi me puchein)"):
    # Display user question
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Save to history
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    try:
        # Generate full context for Gemini
        full_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history])
        
        # Get AI Response
        response = model.generate_content(full_context)
        ai_response = response.text
        
        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
            
        # Save AI Response to history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
