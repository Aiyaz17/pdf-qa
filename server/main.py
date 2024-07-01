from fastapi import FastAPI,HTTPException,Depends,UploadFile,File
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal,engine
import models
from fastapi.middleware.cors import CORSMiddleware
from util import extractTextFromPDF,chunkAndEmbed,preprocess_text,loadEmbeddings
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub,Cohere
from langchain.chains import RetrievalQA
import uuid

load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# Create a middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Create a class to represent the data model for new conversation
class NewConversationModel(BaseModel):
    query: str
    pdf_document_id: int

# Create a class to represent the data model for follow-up questions
class FollowUpConversationModel(BaseModel):
    session_id: str
    query: str



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

# Create a route to create a new PDF document
@app.post('/pdf-upload/')
def upload_pdf(db: db_dependency,pdf_document: UploadFile = File(...)):
    file_location = f'./pdfs/{pdf_document.filename}'
    
    # Save the PDF file to the server / Local
    with open(file_location, 'wb+') as file_object:
        file_object.write(pdf_document.file.read())
    
    # Save the PDF document entry to the database
    db_pdf_document = models.PdfDocument(filename=pdf_document.filename)
    db.add(db_pdf_document)
    db.commit()
    db.refresh(db_pdf_document)

    # Extract text from the PDF document
    text = extractTextFromPDF(file_location)
    preprocessed_paragraphs = preprocess_text(text)

    # Save the preprocessed extracted text to the database
    db_extracted_text = models.ExtractedText(text="\n\n".join(preprocessed_paragraphs), pdf_document_id=db_pdf_document.id)
    db.add(db_extracted_text)
    db.commit()
    db.refresh(db_extracted_text)

    # index = create_index(text,db_pdf_document.id)
    chunkAndEmbed(preprocessed_paragraphs,db_pdf_document.id)

    print("PDF Document ID: ", db_pdf_document.id)

    return db_pdf_document


@app.post('/start_conversation/')
def start_conversation(new_conversation: NewConversationModel, db: db_dependency):
    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    # Extract the text and create embeddings
    vectorstore = loadEmbeddings(new_conversation.pdf_document_id)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    cohere_llm = Cohere()
    qa = RetrievalQA.from_chain_type(llm=cohere_llm, chain_type="stuff", retriever=retriever)
    res = qa({"query": new_conversation.query})

    # Store the conversation history in the database
    conversation = models.Conversation(session_id=session_id, history=new_conversation.query + " " + res["result"], pdf_document_id=new_conversation.pdf_document_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {"session_id": session_id, "response": res["result"]}

# Create a route to handle follow-up questions
@app.post('/follow_up/')
def follow_up(follow_up: FollowUpConversationModel, db: db_dependency):
    # Retrieve the conversation history
    conversation = db.query(models.Conversation).filter(models.Conversation.session_id == follow_up.session_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Append the new query to the history
    history = conversation.history + " " + follow_up.query

    # Retrieve the text and create embeddings
    pdf_document_id = conversation.pdf_document_id # Retrieve based on your logic
    vectorstore = loadEmbeddings(pdf_document_id)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    cohere_llm = Cohere()
    qa = RetrievalQA.from_chain_type(llm=cohere_llm, chain_type="stuff", retriever=retriever)
    res = qa({"query": history})

    # Update the conversation history in the database
    conversation.history = history + " " + res["result"]
    db.commit()

    return {"response": res["result"]}

# # Create a route to get all conversations
# @app.get('/conversations/')
# def read_conversations( db: db_dependency):
#     conversations = db.query(models.Conversation).all()
#     return conversations