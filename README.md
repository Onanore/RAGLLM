# RAGLLM

Chat application with Ollama integration and ChromaDB vector store.

## Installation

1. Clone repository:
```bash
git clone https://github.com/Onanore/RAGLLM
cd RAGLLM
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install and start Ollama server locally:
```bash
curl https://ollama.ai/install.sh | sh
ollama serve
```

## Usage

1. Start application:
```bash
streamlit run app.py
```

2. Access application:
- Open browser
- Navigate to `http://localhost:8501`

## Features

- Real-time chat interface
- File attachment support
- Vector storage with ChromaDB
- Ollama LLM integration
- Chat history persistence

## Project Structure

```
streamlit-chat-app/
├── README.md
├── requirements.txt
├── License
└── src/
    └── app.py
```

## Examples

1. Basic chat:
```python
question = "What is machine learning?"
response = chat_app.get_response(question)
```

2. File upload:
```python
with open("document.txt", "rb") as file:
    response = chat_app.process_file(file)
```
