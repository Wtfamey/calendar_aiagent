# app.py
from agents import main_agent
import streamlit as st
import prompts

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat title
st.title("Create A Google Calendar AI Agent!")

# Display existing messages
if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Enter your prompt here!")
if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from agent
    with st.chat_message("assistant"):
        try:
            # Try to use the agent directly
            if hasattr(main_agent, 'run'):
                response = main_agent.run(prompt)
            elif hasattr(main_agent, 'chat'):
                response = main_agent.chat(prompt)
            else:
                # Fallback: create a simple response
                response = f"I received your message: {prompt}. This is a placeholder response since the agent API is not fully configured."
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.markdown(response)
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)