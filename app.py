from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse
import os
from utils import read_pdf, split_documents, initialize_chroma_db
from typing import List
from fastapi.responses import JSONResponse
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI

app = FastAPI()

# Dummy vectorstore (global placeholder)
vectorstore = None

@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PDF Q&A</title>
        <script>
            async function uploadPDF(event) {
                event.preventDefault();
                const fileInput = document.getElementById("pdfFile");
                const formData = new FormData();
                formData.append("file", fileInput.files[0]);

                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();
                document.getElementById("response").innerText = result.message;
            }

            async function sendQuery(event) {
                event.preventDefault();
                const queryInput = document.getElementById("queryInput").value;

                const response = await fetch("/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: `query=${encodeURIComponent(queryInput)}`,
                });

                const result = await response.json();
                document.getElementById("queryResponse").innerText = JSON.stringify(result, null, 2);
            }
        </script>
    </head>
    <body>
        <h1>Upload PDF and Query</h1>
        <form onsubmit="uploadPDF(event)">
            <label for="pdfFile">Select PDF:</label>
            <input type="file" id="pdfFile" name="pdfFile" accept="application/pdf" required>
            <button type="submit">Upload</button>
        </form>
        <div id="response"></div>

        <h2>Query the PDF</h2>
        <form onsubmit="sendQuery(event)">
            <label for="queryInput">Enter your query:</label>
            <input type="text" id="queryInput" name="query" required>
            <button type="submit">Ask</button>
        </form>
        <pre id="queryResponse"></pre>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore

    # Check if the file is a PDF
    if file.filename.split(".")[-1].lower() != "pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # Save the uploaded file temporarily
    temp_file_path = f"./temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    try:
        # Read and split the PDF into chunks
        documents = read_pdf(pdf_path=temp_file_path)
        chunks = split_documents(documents=documents)

        # Initialize Chroma vector store
        vectorstore = initialize_chroma_db()

        # Index the chunks into Chroma
        vectorstore.add_documents(documents=chunks)

        # Clean up temporary file
        os.remove(temp_file_path)

        return {"message": "PDF uploaded and indexed successfully!"}

    except Exception as e:
        os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
@app.post("/query")
async def query_vectorstore(query: str = Form(...)):
    global vectorstore

    # Check if the vector store is initialized
    if vectorstore is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded. Please upload a PDF first.")

    # Initialize conversational retrieval chain
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
        memory=memory,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True,
        verbose=True
    )

    # Query the chain
    response = chain.invoke({"question": query})

    # Extract and format the response
    answer = response.get("answer")
    source_documents = response.get("source_documents")
    source_metadata = [doc.metadata for doc in source_documents]

    return JSONResponse(content={
        "answer": answer,
        "source_documents": source_metadata,
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)