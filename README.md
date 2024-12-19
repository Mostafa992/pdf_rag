# RAG App (PDF)

This is a **Retrieval-Augmented Generation (RAG)** application built using **FastAPI**, **Langchain**, and **Chroma** for querying content from PDFs. The app allows users to upload PDFs, split them into manageable chunks, and use those chunks for querying using a conversational model (powered by OpenAI's GPT).

## Features
- Upload a PDF file and extract its content.
- Split the PDF into smaller chunks for efficient retrieval.
- Use a conversational retrieval chain to query the contents of the uploaded PDF.
- Serve the app via a web interface (HTML) for easy interaction.

## Components
- **utils.py**: Utility functions to load and process PDFs, split documents, and initialize the Chroma vector store.
- **app.py**: FastAPI application that handles the frontend (HTML) and backend for uploading files and querying data.
- **Dockerfile**: Defines the environment for deploying the app in a containerized manner.

## Installation

### Prerequisites
- Python 3.9 or above.
- Docker (optional, for containerization).

### Steps to run the app locally

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-repo/rag-app.git
    cd rag-app
    ```

2. **Set up a virtual environment (optional but recommended)**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the application**:

    ```bash
    python app.py
    ```

    By default, the app will run on `http://localhost:8080`.

### Using Docker

1. **Build the Docker image**:

    ```bash
    docker build -t rag-app .
    ```

2. **Run the Docker container**:

    ```bash
    docker run -p 80:80 rag-app
    ```

    The app will be available at `http://localhost:80`.

## How to Use

1. **Upload a PDF**:
   - Open the app in a browser.
   - Upload a PDF file using the file input field and click "Upload".
   - The PDF will be processed, split into chunks, and indexed for querying.

2. **Query the PDF**:
   - Once the PDF is uploaded and indexed, enter your query in the input field under "Query the PDF".
   - The app will process your query and return relevant information from the PDF.

## Directory Structure

