# Air India Chatbot

A simple Streamlit-based chatbot for answering questions about Air India using PDF documents as the knowledge base. Powered by xAI's Grok-4 model via LangChain.

## Overview

This project creates an interactive Q&A interface where users can ask questions related to Air India. The chatbot loads content from PDF files stored in the `pdfs` folder and uses it as context to generate accurate, concise responses. It leverages LangChain for document loading and prompting, and xAI's Grok-4 for natural language processing.

Key features:
- Loads and processes multiple PDF files recursively from a directory.
- Concatenates PDF content to form a single context (note: for production, consider using a vector store for better scalability).
- Streams responses in real-time for a smooth user experience.
- Caches documents and the LLM instance to optimize performance.
- Restricts answers to information available in the provided PDFs; responds with "I don't have enough information" if the query can't be answered from the context.

## Features

- **PDF Document Loading**: Automatically loads all `.pdf` files from the `pdfs` folder using `DirectoryLoader` and `PyPDFLoader`.
- **Prompt Engineering**: Uses a custom prompt template to ensure responses are based solely on the provided context.
- **Streaming Responses**: Real-time response generation with a loading cursor for better UX.
- **Chat History**: Maintains conversation history in the session state.
- **Error Handling**: Graceful handling of missing APIs, empty PDF folders, or loading errors.
- **Clear Chat Option**: Sidebar button to reset the chat history.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/pik1989/Air-India-Chatbot.git
   cd Air-India-Chatbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes:
   ```
   streamlit
   langchain-xai
   langchain-community
   langchain-core
   ```

3. Set up your xAI API key:
   - Create a `.streamlit/secrets.toml` file in the project root with the following content:
     ```
     XAI_API_KEY = "your-xai-api-key-here"
     ```
   - Alternatively, set it as an environment variable:
     ```
     export XAI_API_KEY="your-xai-api-key-here"
     ```

4. Add PDF documents:
   - Place Air India-related PDF files (e.g., policies, FAQs, manuals) in the `pdfs` folder.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open the app in your browser (typically at `http://localhost:8501`).

3. Ask questions in the chat input, such as "What are Air India's baggage policies?" or "How do I book a flight?"

4. The chatbot will respond based on the PDF content. If the information isn't available, it will indicate so.

### Example

- User: "What is Air India's policy on refunds?"
- Bot: (Streams response based on PDF context)

To clear the chat history, use the "Clear Chat History" button in the sidebar.

## Configuration

- **PDF Folder**: Set in `PDF_FOLDER = "pdfs"`. Change this if your PDFs are in a different directory.
- **Glob Pattern**: `GLOB_PATTERN = "**/*.pdf"` for recursive loading.
- **LLM Settings**: Uses Grok-4 with `temperature=0.15` and `max_tokens=2048`. Adjust in `get_llm()` if needed.
- **Prompt Template**: Customizable in `prompt_template`. Ensures context-bound responses.

## Limitations

- **Context Size**: All PDF content is concatenated into a single string, which may exceed token limits for very large document sets. For production, integrate a text splitter and vector database (e.g., FAISS or Pinecone).
- **No External Knowledge**: Responses are strictly limited to PDF content—no web searches or general knowledge.
- **API Dependency**: Requires a valid xAI API key.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements, such as:
- Adding vector embeddings for better retrieval.
- Supporting more document formats.
- Enhancing error handling or UI.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/), [LangChain](https://langchain.com/), and [xAI's Grok](https://x.ai/).
- Inspired by simple PDF Q&A tutorials for educational purposes.
