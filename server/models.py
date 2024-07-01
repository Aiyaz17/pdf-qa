from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Assuming Base is defined in database.py

class PdfDocument(Base):
    __tablename__ = 'pdf_document'
   
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    extracted_texts = relationship("ExtractedText", back_populates="pdf_document")

class ExtractedText(Base):
    __tablename__ = 'extracted_text'
  
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    pdf_document_id = Column(Integer, ForeignKey('pdf_document.id'))  # Corrected foreign key name
    pdf_document = relationship("PdfDocument", back_populates="extracted_texts")

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    history = Column(String)
    pdf_document_id = Column(Integer, ForeignKey('pdf_document.id'))
    