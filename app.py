import os
import streamlit as st
from langchain_xai import ChatXAI
#from langchain_ollama import ChatOllama
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.prompts import PromptTemplate

# ─── Page Config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PDF Q&A with Grok",
    page_icon="📄",
    layout="wide"
)
XAI_API_KEY = "YOUR-KEY"
os.environ["XAI_API_KEY"] = XAI_API_KEY

# ─── Configuration ─────────────────────────────────────────────────────────
# Best practice: use st.secrets or environment variable
XAI_API_KEY = os.getenv("XAI_API_KEY") or st.secrets.get("XAI_API_KEY", "")

if not XAI_API_KEY:
    st.error("XAI_API_KEY not found. Please set it in environment variables or .streamlit/secrets.toml")
    st.stop()

PDF_FOLDER = "pdfs"           # ← change this to your actual folder
GLOB_PATTERN = "**/*.pdf"     # recursive search

# ─── Prompt (modern style - no PipelinePromptTemplate) ─────────────────────
prompt_template = """You are a helpful assistant answering questions based **only** on the provided context.
If the information is not in the context, say "I don't have enough information in the documents".

Context:
{context}

Question: {question}

Answer concisely, clearly and naturally:"""

PROMPT = PromptTemplate.from_template(prompt_template)

# ─── Cache documents (load only once) ──────────────────────────────────────
@st.cache_resource(show_spinner="Loading and processing PDFs...")
def load_documents():
    try:
        loader = DirectoryLoader(
            path=PDF_FOLDER,
            glob=GLOB_PATTERN,
            loader_cls=PyPDFLoader,
            show_progress=True,
            silent_errors=False
        )
        docs = loader.load()
        
        if not docs:
            st.warning(f"No PDF files were found in folder: '{PDF_FOLDER}'")
            return []
            
        total_pages = len(docs)
        st.success(f"Loaded **{total_pages}** pages from PDFs")
        return docs
        
    except Exception as e:
        st.error(f"Error loading documents:\n{str(e)}")
        return []

# ─── Cache LLM instance ────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatXAI(
        model="grok-4",
        api_key=XAI_API_KEY,
        temperature=0.15,
        max_tokens=2048,
        streaming=True
    )

# ─── Main Application ──────────────────────────────────────────────────────
def main():
    st.title("📄 AirIndia Chatbot")
    st.caption("Ask questions about Air India")

    # Load documents (cached)
    documents = load_documents()

    if not documents:
        st.stop()

    # Very simple context concatenation
    # (for production → use text splitter + vectorstore!)
    context_text = "\n\n".join(doc.page_content for doc in documents)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if question := st.chat_input("Ask a question about the documents..."):
        # Add user message to history & UI
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Format prompt
        formatted_prompt = PROMPT.format(
            context=context_text,
            question=question
        )

        # Generate response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                llm = get_llm()

                for chunk in llm.stream(formatted_prompt):
                    if hasattr(chunk, "content"):
                        delta = chunk.content
                    else:
                        delta = str(chunk)
                        
                    full_response += delta
                    message_placeholder.markdown(full_response + "▌")

                # Final clean message
                message_placeholder.markdown(full_response)

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

            except Exception as e:
                st.error(f"Error during generation:\n{str(e)}")

    # Optional: clear chat button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()