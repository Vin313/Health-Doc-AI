import streamlit as st
from dotenv import load_dotenv
from utils import get_document_text, get_text_chunks, get_vectorstore, get_conversation_chain
import os

def handle_user_input(user_question):
    """
    Processes user input, gets a response from the conversation chain, and updates chat history.
    """
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        # Display chat messages
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                with st.chat_message("user"):
                    st.markdown(message.content)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message.content)
    else:
        st.warning("Please upload and process documents before asking a question.")

def main():
    """
    Main function to run the Streamlit application.
    """
    # Load environment variables (like OPENAI_API_KEY)
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY not found. Please set it in your .env file.")
        st.stop()
        
    # --- Page Configuration ---
    st.set_page_config(page_title="HealthDoc AI", page_icon="🩺", layout="wide")

    # --- Session State Initialization ---
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # --- UI Rendering ---
    st.header("HealthDoc AI 🩺")

    # --- Medical Disclaimer ---
    st.warning(
        """
        **Hello!:** I'm your medical document assistant, How may I helpyou today!
        """
    )

    # --- Sidebar for Document Upload and Processing ---
    with st.sidebar:
        st.subheader("Your Documents")
        uploaded_files = st.file_uploader(
            "Upload your PDFs, DOCX, or TXT files here",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt']
        )
        if st.button("Process Documents"):
            if uploaded_files:
                with st.spinner("Processing documents... This may take a moment."):
                    # 1. Get text from all uploaded documents
                    raw_text = get_document_text(uploaded_files)
                    
                    if raw_text:
                        # 2. Get text chunks
                        text_chunks = get_text_chunks(raw_text)
                        
                        # 3. Create vector store with embeddings
                        vectorstore = get_vectorstore(text_chunks)
                        
                        # 4. Create conversation chain and store in session state
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        st.success("Documents processed successfully! You can now ask questions.")
                    else:
                        st.error("Could not extract text from the documents. Please check the files.")
            else:
                st.warning("Please upload at least one document.")

    # --- Main Chat Interface ---
    
    # Display initial message if no documents are processed
    if not st.session_state.conversation:
        st.info("Please upload and process your documents using the sidebar to start chatting.")
    
    # Display existing chat history
    if st.session_state.chat_history:
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                with st.chat_message("user"):
                    st.markdown(message.content)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message.content)
                    
    # Chat input for new questions
    user_question = st.chat_input("Ask a question about your documents...")
    if user_question:
        handle_user_input(user_question)

if __name__ == '__main__':
    main()