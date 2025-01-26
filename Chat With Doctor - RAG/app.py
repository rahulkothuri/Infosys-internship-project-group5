import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    """Extracts text from uploaded PDF documents."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Splits text into manageable chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Creates and saves a FAISS vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    """Builds the conversational chain using a refined prompt."""
    prompt_template = """
    You are an intelligent assistant designed to analyze and extract insights from medical case datasets containing:

    1. **Clinical Summaries**: Detailed descriptions of patient conditions, treatments, and outcomes.
    2. **Conversations**: Doctor-patient dialogues discussing the cases in detail.

    Your tasks:
    - Provide accurate, concise, and contextually relevant answers to user queries based on the data.
    - For factual queries, extract information from the context and you can add some content related to health and diseases.
    - For conversational queries, simulate natural responses based on doctor-patient dialogues.
    - If the information is unavailable, respond with "Answer is not available in the context provided."

    Context:
    {context}

    Question:
    {question}
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question, chat_history):
    """Handles user input and generates a response using the RAG pipeline."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    chat_history.append({"user": user_question, "bot": response["output_text"]})
    return chat_history

def display_chat(chat_history):
    """Displays the chat history in a UI-friendly format."""
    for chat in chat_history:
        st.markdown(
            f"""<div style='background-color:#232323;padding:10px;margin:10px 0;border-radius:5px;'>
            <b>You:</b> {chat['user']}</div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            f"""<div style='background-color:#232323;padding:10px;margin:10px 0;border-radius:5px;'>
            <b>Bot:</b> {chat['bot']}</div>""",
            unsafe_allow_html=True
        )

def main():
    st.set_page_config("Doctor Chat")
    st.header("Chat with Doctor \U0001F3E5")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_question = st.text_input("Ask a Question...")

    if user_question:
        with st.spinner("Generating response..."):
            st.session_state["chat_history"] = user_input(user_question, st.session_state["chat_history"])

    display_chat(st.session_state["chat_history"])

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your conversation files and click Submit & Process", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Processing complete! Data is ready for queries.")

if __name__ == "__main__":
    main()
