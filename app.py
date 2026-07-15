import streamlit as st
from agent import agent_executor
 
# Page configuration
st.set_page_config(page_title="Loan Eligibility Assistant", page_icon="🏦", layout="wide")
 
# Sidebar for management
with st.sidebar:
    st.title("🏦 Agent Settings")
    if st.button("Clear Conversation History"):
        st.session_state.messages = []
        # Optional: Reset memory if using ConversationBufferMemory
        st.rerun()
    st.markdown("---")
    st.info("This assistant uses local Llama 3.1 for secure, private loan policy analysis.")
 
st.title("💰 Loan Eligibility Assistant")
 
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# Chat input
if prompt := st.chat_input("Ask about loan policies or check your eligibility..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Agent processing with spinner
    with st.chat_message("assistant"):
        with st.spinner("Assistant is thinking..."):
            try:
                # Invoke the agent
                response = agent_executor.invoke({"input": prompt})
                result = response["output"]
                st.markdown(result)
                # Save assistant response
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                st.error(f"An error occurred: {e}")