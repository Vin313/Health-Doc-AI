# HealthDoc AI: Conversational Healthcare Document Assistant

HealthDoc AI is a powerful, intuitive conversational AI application that allows users to chat with their healthcare documents. Built with Python, Streamlit, and LangChain, it provides a secure and private way to quickly find information within medical records like discharge summaries, lab reports, and prescriptions.

<img width="1920" height="960" alt="image" src="https://github.com/user-attachments/assets/7c595831-727b-47b2-8d8a-ae50e2014c18" />


## ✨ Core Features

* **Multi-Format Support:** Ingests and processes PDF, DOCX, and TXT documents.
* **Intuitive Chat Interface:** Ask questions in natural language and get immediate answers.
* **Context-Aware Conversations:** Remembers previous questions and answers for seamless follow-up queries.
* **Data Privacy First:** All processing happens in memory, and documents are never stored long-term. Your data remains private.
* **Advanced AI/ML:** Utilizes a powerful Retrieval Augmented Generation (RAG) pipeline with high-quality embeddings and state-of-the-art LLMs.
* **Built-in Medical Disclaimer:** Prominently displays a disclaimer to ensure responsible use.

---

## 🏗️ Technical Architecture

The application employs a RAG (Retrieval Augmented Generation) architecture orchestrated by the LangChain framework.

1.  **Document Ingestion & Chunking:** User-uploaded documents (PDF, DOCX, TXT) are read, and their text content is extracted. This text is then broken down into smaller, semantically meaningful chunks.
2.  **Embedding & Vectorization:** Each text chunk is converted into a numerical representation (embedding) using a Hugging Face sentence-transformer model. These embeddings capture the semantic meaning of the text.
3.  **Vector Storage:** The embeddings are stored in a FAISS in-memory vector store, which allows for incredibly fast similarity searches.
4.  **User Query:** The user asks a question through the Streamlit interface.
5.  **Retrieval:** The user's question is embedded, and the vector store is searched to find the most relevant text chunks from the original documents.
6.  **Generation:** The retrieved chunks, the user's question, and the chat history are passed to an OpenAI LLM (e.g., GPT-3.5-Turbo). The LLM synthesizes this information to generate a coherent, accurate answer.
7.  **Response:** The final answer is displayed to the user in the chat interface.

---

## 🛠️ Setup and Installation

Follow these steps to run the application locally.

### Prerequisites

* Python 3.9+
* An OpenAI API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Vin313/Health-Doc-AI
    cd HealthDoc-AI
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    * Create a file named `.env` in the root of the project.
    * Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY="YourSecretAPIKeyGoesHere"
        ```

### Running the Application

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
2.  Open your web browser and navigate to `http://localhost:8501`.

---

## 📖 Usage Guide

1.  **Upload Documents:** Use the sidebar to upload one or more healthcare documents. Supported formats are PDF, DOCX, and TXT.
2.  **Process Documents:** Click the "Process Documents" button. The app will extract text, create embeddings, and build the vector store. This might take a moment, especially the first time when the embedding model is downloaded.
3.  **Ask Questions:** Once processing is complete, use the chat input at the bottom of the screen to ask questions about your documents.

**Sample Questions:**
* _What medications were the patient prescribed?_
* _Summarize the key findings from the lab report._
* _What was the patient's glucose level?_
* _Are there any drug allergies mentioned?_
* _What follow-up care was recommended?_

---

## ⚖️ Data Privacy & Ethics

* **No Data Storage:** This application does not store your documents or conversations. All processing is done in-memory for the duration of your session.
* **Anonymized Data:** The provided sample documents are entirely fictional and contain no real patient data.

## ⚠️ Limitations

* **OCR Quality:** The accuracy for PDF documents depends heavily on the quality of the text layer. Scanned or image-based PDFs will not work well without an external OCR process.
* **Scope:** The AI's knowledge is strictly limited to the content of the uploaded documents.
