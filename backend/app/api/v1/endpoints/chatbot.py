from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from pydantic import BaseModel
import openai
import os
import tempfile
from langchain_community.document_loaders import Docx2txtLoader
from fastapi.responses import JSONResponse
from ....db.session import OPENAI_API_KEY
import docx2txt

# Load environment variables
openai.api_key = OPENAI_API_KEY

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    file: UploadFile = None

class QueryResponse(BaseModel):
    response: str

@router.post("/chat", response_model=QueryResponse)
async def chat_with_zasti_ai(query: str = Form(...), file: UploadFile = File(None)):
    document_text = ""

    # If a file is uploaded, process it
    if file and file.filename.endswith(".docx"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(file.file.read())
            tmp_file_path = tmp_file.name

        try:
            # Load the DOCX file
            loader = Docx2txtLoader(tmp_file_path)
            documents = loader.load()

            # Combine the text from all pages
            document_text = " ".join([doc.page_content for doc in documents])

        finally:
            # Delete the temporary file
            os.remove(tmp_file_path)
    elif file and not file.filename.endswith(".docx"):
        return JSONResponse({"error": "Please upload a .docx file for document-based queries or ask me anything related to LCA and carbon footprints."}, status_code=400)

    # Prepare the optimized prompt
    prompt_template = f"""
    You are Zasti AI, a friendly and knowledgeable assistant specializing in Life Cycle Assessment (LCA) and carbon footprints. 
    {query}
    {document_text}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Zasti AI, a friendly and knowledgeable assistant specializing in Life Cycle Assessment (LCA) and carbon footprints."},
            {"role": "user", "content": prompt_template}
        ]
    )
    
    return QueryResponse(response=response['choices'][0]['message']['content'].strip())
