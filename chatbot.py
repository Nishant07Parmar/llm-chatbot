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
import requests
import os

st.title("Demo ChatBot Solar & Sons")

OLLAMA_URL = "http://localhost:11434/api/chat"

# ------------------------
# Function: check ollama
# ------------------------
def ollama_available():
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except:
        return False

USE_OLLAMA = ollama_available()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # ------------------------
        # LOCAL OLLAMA MODE
        # ------------------------
        if USE_OLLAMA:
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": "deepseek-r1:1.5b",
                        "messages": st.session_state.messages,
                        "stream": True
                    },
                    stream=True,
                    timeout=60
                )

                for line in response.iter_lines():
                    if line:
                        chunk = line.decode("utf-8")
                        if '"content":"' in chunk:
                            content = chunk.split('"content":"')[1].split('"')[0]
                            full_response += content
                            placeholder.write(full_response + "▌")

                placeholder.write(full_response)

            except Exception as e:
                st.error(f"Ollama error: {e}")

        # ------------------------
        # CLOUD FALLBACK MODE
        # ------------------------
        else:
            full_response = (
                "⚠ Local AI server not connected.\n\n"
                "This chatbot runs using **offline LLM (Ollama)**.\n"
                "For full demo, run locally on the developer machine."
            )
            placeholder.write(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )



