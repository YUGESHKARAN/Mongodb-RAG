# Mongodb-RAG

[![Deploy on Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/)

## Overview

**Mongodb-RAG** is a Python project that implements a Retrieval Augmented Generation (RAG) system using MongoDB for storage and the powerful `llama-3.1-8b-instant` LLM for generation. This project demonstrates scalable, context-aware response generation by combining efficient document retrieval from MongoDB with state-of-the-art language modeling.

## Features

- **Retrieval Augmented Generation (RAG):** Combines MongoDB-based retrieval with LLM-powered answer generation.
- **MongoDB Integration:** Efficient storage and retrieval of documents and context.
- **Latest LLM:** Utilizes `llama-3.1-8b-instant` for high-quality, instant responses.
- **Web Deployment Ready:** Easily deployable to Render.
- **Clean Python Codebase:** Modular Python scripts for easy understanding and customization.

## Folder Structure

![image1](image1)

```
.
├── __pycache__/
├── .gitignore
├── app.py
├── index.py
├── mongodb_database.py
├── query_generator.py
├── requirements.txt
└── vercel.json
```

- **app.py**: Main application logic (entry point for web deployment).
- **index.py**: Likely includes web server/router code.
- **mongodb_database.py**: MongoDB connection and data handling logic.
- **query_generator.py**: Core RAG logic for generating and retrieving responses.
- **requirements.txt**: Python package dependencies.
- **vercel.json**: Vercel deployment configuration (may be adapted for Render).

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB instance (local or Atlas)
- (Optionally) Node.js & Render CLI for deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YUGESHKARAN/Mongodb-RAG.git
   cd Mongodb-RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Set up your MongoDB URI and any required environment variables.

4. **Run the application**
   ```bash
   python app.py
   ```

### Deployment

To deploy on Render:
- Create a new Web Service on [Render](https://render.com/).
- Connect your GitHub repository.
- Set your build and start commands (typically, `pip install -r requirements.txt` and `python app.py`).
- Add your environment variables (e.g.,MODEL_API_KEY, MongoDB URI) in the Render dashboard.
- Deploy!

## Usage

- Access the service via the URL provided by Render after deployment.
- The system retrieves relevant documents from MongoDB and generates responses using the `llama-3.1-8b-instant` LLM.

## Contributing

Contributions, suggestions, and improvements are welcome! Please open an issue or pull request.

## Acknowledgements

- [MongoDB](https://www.mongodb.com/)
- [Meta Llama-3](https://ai.meta.com/llama/)
- [Render](https://render.com/)

---

_Maintained by [YUGESHKARAN](https://github.com/YUGESHKARAN)._
