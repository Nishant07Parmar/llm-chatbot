import streamlit as st
import ollama
import os
st.title("Demo ChatBot Solar & Sons")           # Title of Chat

IS_CLOUD = os.environ.get(  "STREAMLIT_SHARING") is not True
if "messages" not in st.session_state:          # Define the chat history in st.session_state
    st.session_state.messages = []

for message in st.session_state.messages:       # Print the chat history
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Type your message here...")  # User message

if prompt:
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Show Loading Spinner for better UX
        with st.spinner("Thinking..."):
            try:
                # Initialize the stream
                stream = ollama.chat(
                    model="deepseek-r1:1.5b",
                    messages=st.session_state.messages,
                    stream=True
                )
                
                # Iterate over the stream (the spinner disappears when this loop starts printing)
                for chunk in stream:
                    content = chunk['message']['content']
                    full_response += content
                    message_placeholder.write(full_response + "▌")
                
                # Final update to remove the cursor
                message_placeholder.write(full_response)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"An error occurred: {e}")





