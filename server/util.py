import pymupdf
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
import pickle
from langchain_community.embeddings import HuggingFaceEmbeddings


def extractTextFromPDF(pdf_path):
    openned_pdf = pymupdf.open(pdf_path)
    number_of_pages = len(openned_pdf)
    text=""
    for page_number in range(number_of_pages):
        page = openned_pdf[page_number]
        text += page.get_text()
    openned_pdf.close()
    return text


def preprocess_text(text):
    # Lower case the text
    text=text.lower()
    
    # Remove unnecessary whitespace and newlines
    text = re.sub(r'\s+', ' ', text)

    # Normalize whitespace
    text = ' '.join(text.split())

    # Example: Split text into paragraphs or sections (customize as needed)
    paragraphs = text.split('. ')

    # Remove empty paragraphs and strip extra whitespace
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs


def chunkAndEmbed(paragraphs,store_name):

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
    chunks = text_splitter.split_text(text=" ".join(paragraphs))

    # Define the path to the pre-trained model you want to use
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device':'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,     # Provide the pre-trained model's path
        model_kwargs=model_kwargs, # Pass the model configuration options
        encode_kwargs=encode_kwargs # Pass the encoding options
    )

    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    with open(f"./embeddings/{store_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)


    return VectorStore


def loadEmbeddings(store_name):
    with open(f"./embeddings/{store_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
    return VectorStore