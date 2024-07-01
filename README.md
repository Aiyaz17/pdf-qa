---

# PDF Document QA Application

## Overview

This application allows users to upload PDF documents, extract text, and interact with a question-answering (QA) system based on the content of the PDF. The backend is built with FastAPI, SQLAlchemy for database management, and integrates with a React frontend for a user-friendly interface.

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [API Documentation](#api-documentation)
3. [Application Architecture](#application-architecture)

## Setup Instructions

### Backend (FastAPI)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aiyaz17/pdf-qa.git
   cd pdf-qa
   ```

2. **Setup Python environment:**

   ```bash
   # Create and activate a virtual environment (optional but recommended)
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --reload
   ```

   The server should start at `http://localhost:8000`.

### Frontend (React)

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install  # or yarn install
   ```

3. **Set backend URL:**

   - Modify the `axios.defaults.baseURL` in `src/App.js` to match your FastAPI server URL or Add a env variable for the same and set key as REACT_APP_BACKEND_URL .

4. **Start the frontend development server:**

   ```bash
   npm start  # or yarn start
   ```

   The frontend should now be accessible at `http://localhost:3000`.

## API Documentation

### PDF Upload

- **Endpoint:** `/pdf-upload/`
- **Method:** `POST`
- **Description:** Uploads a PDF file to the server, extracts text, preprocesses it, and stores it in the database.
- **Request Body:**
  ```json
  {
    "pdf_document": "File"  // Upload PDF file
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "filename": "example.pdf",
    "upload_date": "2024-07-01T12:00:00"
  }
  ```

### Start Conversation

- **Endpoint:** `/start_conversation/`
- **Method:** `POST`
- **Description:** Initiates a new conversation session based on a query related to a specific PDF document.
- **Request Body:**
  ```json
  {
    "query": "Question text",
    "pdf_document_id": 1
  }
  ```
- **Response:**
  ```json
  {
    "session_id": "uuid-string",
    "response": "Answer to the question"
  }
  ```

### Follow-up Conversation

- **Endpoint:** `/follow_up/`
- **Method:** `POST`
- **Description:** Adds a follow-up question to an existing conversation session.
- **Request Body:**
  ```json
  {
    "session_id": "uuid-string session id",
    "query": "Follow-up question text"
  }
  ```
- **Response:**
  ```json
  {
    "response": "Answer to the follow-up question"
  }
  ```

## Application Architecture

The application follows a client-server architecture:

- **Backend (FastAPI):**
  - **Framework:** FastAPI for building robust APIs with Python.
  - **Database:** SQLAlchemy with SQLite (can be modified for other databases like PostgreSQL).
  - **Middleware:** CORS middleware for handling cross-origin resource sharing.
  - **Modules:** Utilizes PDF extraction, text preprocessing, embedding generation, and question-answering capabilities using LangChain and Hugging Face models.
  - **LLM:** Utilizing Cohere llm to generate structed answer from the feeded vectorstore.

- **Frontend (React):**
  - **UI Library:** React.js for building interactive user interfaces.
  - **State Management:** Uses `useState` hooks for managing local component state.
  - **Components:** Navbar for navigation and PDF upload, Chat component for displaying conversation history and sending queries.
  - **Styling:** Tailwind CSS for responsive and utility-first styling.

---
