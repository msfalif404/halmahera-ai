import streamlit as st
import requests
import json
import uuid

# --- Config ---
API_URL = "http://localhost:8000"
st.set_page_config(page_title="Scholarship Agent", page_icon="🎓")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# --- Sidebar ---
with st.sidebar:
    st.title("🎓 Halmahera AI")
    st.markdown("Scholarship Assistant")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# --- Main Interface ---
st.title("Scholarship Assistant Agent")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("I want to find a scholarship..."):
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get AI Response (Streamed)
    with st.chat_message("assistant"):
        # We use a placeholder to stream content
        message_placeholder = st.empty()
        full_response = ""
        
        # Generator for streaming
        def stream_response():
            url = f"{API_URL}/stream"
            payload = {
                "message": prompt,
                "thread_id": st.session_state.thread_id
            }
            
            with requests.post(url, json=payload, stream=True) as response:
                if response.status_code != 200:
                    yield f"Error: {response.status_code} - {response.text}"
                    return

                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data_str = decoded_line[6:] # Strip "data: "
                            try:
                                data = json.loads(data_str)
                                if data["type"] == "token":
                                    yield data["content"]
                                elif data["type"] == "status":
                                    # Optional: Could show a status indicator
                                    pass 
                            except Exception as e:
                                print(f"Error parsing line: {e}")

        # Streamlit's write_stream automatically consumes the generator and updates UI
        full_response = st.write_stream(stream_response)
        
    # 3. Add Assistant Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})
