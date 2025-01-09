import streamlit as st
import ollama
from chromadb import Client
import chromadb
import json
from datetime import datetime
import os

class ChatApp:
    def __init__(self):
        self.chroma_client = Client()
        self.collection = self.chroma_client.create_collection(
            name="chat_history",
            metadata={"hnsw:space": "cosine"}
        )
        
    def store_interaction(self, query, response):
        timestamp = datetime.now().isoformat()
        self.collection.add(
            documents=[f"Q: {query}\nA: {response}"],
            metadatas=[{"timestamp": timestamp}],
            ids=[timestamp]
        )

    def process_file(self, file):
        if file is not None:
            file_contents = file.read()
            if file.type == "text/plain":
                return file_contents.decode()
            return str(file_contents)
        return ""

def main():
    st.set_page_config(page_title="Chat Application", layout="wide")
    st.title("Chat Application")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_app" not in st.session_state:
        st.session_state.chat_app = ChatApp()

    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "doc"])
    file_content = ""
    if uploaded_file:
        file_content = st.session_state.chat_app.process_file(uploaded_file)
        st.write("File uploaded successfully!")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        context = f"\nFile content: {file_content}" if file_content else ""
        full_prompt = f"{prompt}{context}"
        
        try:
            response = ollama.chat(model='llama3.2:3b', messages=[
                {'role': 'user', 'content': full_prompt}
            ])
            
            assistant_response = response['message']['content']
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            
            # Store in session state
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Store in ChromaDB
            st.session_state.chat_app.store_interaction(prompt, assistant_response)
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()