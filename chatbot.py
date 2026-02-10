# import streamlit as st
# import ollama
# import os
# st.title("Demo ChatBot Solar & Sons")           # Title of Chat

# IS_CLOUD = os.environ.get(  "STREAMLIT_SHARING") is not True
# if "messages" not in st.session_state:          # Define the chat history in st.session_state
#     st.session_state.messages = []

# for message in st.session_state.messages:       # Print the chat history
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# prompt = st.chat_input("Type your message here...")  # User message

# if prompt:
#     # Add and display user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)
    
#     # Display assistant message
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
        
#         # Show Loading Spinner for better UX
#         with st.spinner("Thinking..."):
#             try:
#                 # Initialize the stream
#                 stream = ollama.chat(
#                     model="deepseek-r1:1.5b",
#                     messages=st.session_state.messages,
#                     stream=True
#                 )
                
#                 # Iterate over the stream (the spinner disappears when this loop starts printing)
#                 for chunk in stream:
#                     content = chunk['message']['content']
#                     full_response += content
#                     message_placeholder.write(full_response + "▌")
                
#                 # Final update to remove the cursor
#                 message_placeholder.write(full_response)
                
#                 # Save to history
#                 st.session_state.messages.append({"role": "assistant", "content": full_response})

#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Assistant", layout="centered")

st.title("🌞 Solar Assistant Chatbot")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your AI assistant. Ask me anything."
        }
    ]

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Type your question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
                    messages=st.session_state.messages,
                    stream=True
                )

                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    placeholder.write(full_response + "▌")

            except Exception as e:
                full_response = f"⚠️ Error: {e}"

        placeholder.write(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
