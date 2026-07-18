import streamlit as st
import requests

# App Title & Personalization
st.set_page_config(page_title="My Personal AI", page_icon="✨")
st.title("✨ My Personal AI Chatbot")
st.write("Welcome to your custom AI space! Ekdum free aur fast.")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chats
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_question := st.chat_input("Apne dost se kuch bhi puchein..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    try:
        # Using a reliable free inference model (No personal key needed)
        API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        
        # System instructions to make it personalized
        system_instruction = "Tum user ke ek personal aur bohot pakke dost ho. Humesha friendly rehna aur Hinglish me baat karna."
        
        payload = {
            "inputs": f"<|system|>\n{system_instruction}</s>\n<|user|>\n{user_question}</s>\n<|assistant|>\n",
            "parameters": {"max_new_tokens": 400, "temperature": 0.7}
        }
        
        # Getting response from server
        response = requests.post(API_URL, json=payload).json()
        generated_text = response[0]['generated_text']
        ai_response = generated_text.split("<|assistant|>\n")[-1].strip()
        
        # Display AI Response
        with st.chat_message("assistant"):
            st.markdown(ai_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        st.error("Dost abhi thoda busy hai, ek baar phir se message type kijiye!")
        
