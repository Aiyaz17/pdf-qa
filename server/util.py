import pymupdf
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import pickle
from langchain_community.embeddings import HuggingFaceEmbeddings


def extractTextFromPDF(pdf_path):
    """
    Extract text content from a PDF file.

    Args:
    - pdf_path (str): Path to the PDF file.

    Returns:
    - str: Extracted text content.
    """
    openned_pdf = pymupdf.open(pdf_path)
    number_of_pages = len(openned_pdf)
    text=""
    for page_number in range(number_of_pages):
        page = openned_pdf[page_number]
        text += page.get_text()
    openned_pdf.close()
    return text


def preprocess_text(text):
    """
    Preprocesses text by lowercasing, removing unnecessary whitespace and newlines,
    normalizing whitespace, and splitting into paragraphs.

    Args:
    - text (str): Input text to preprocess.

    Returns:
    - list of str: List of preprocessed paragraphs.
    """
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
    """
    Chunk input paragraphs, embed them using HuggingFaceEmbeddings, and store the embeddings.

    Args:
    - paragraphs (list of str): List of text paragraphs to process.
    - store_name (str): Name for storing the embeddings.

    Returns:
    - FAISS: VectorStore object containing embeddings.
    """
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
    chunks = text_splitter.split_text(text=" ".join(paragraphs))

    # path to the pre-trained model
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {'device':'cpu'}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {'normalize_embeddings': False}

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,    
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs 
    )

    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    with open(f"./embeddings/{store_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)

    return VectorStore


def loadEmbeddings(store_name):
    """
    Load embeddings from a stored file.

    Args:
    - store_name (str): Name of the stored embeddings file.

    Returns:
    - FAISS: VectorStore object containing embeddings.
    """
    
    with open(f"./embeddings/{store_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
    return VectorStore