

<img width="1440" alt="Screenshot 2025-02-24 at 5 19 20 PM" src="https://github.com/user-attachments/assets/a654be24-7d11-49fb-b2f1-26e2c484c509" />
<img width="1440" alt="Screenshot 2025-02-24 at 5 18 53 PM" src="https://github.com/user-attachments/assets/ad8550aa-1c33-4ce0-ac72-0a66ddb4a10b" />
<img width="1440" alt="Screenshot 2025-02-24 at 5 19 09 PM" src="https://github.com/user-attachments/assets/f88442ee-16c2-4ea2-bf95-930ec20b361a" />
<img width="1208" alt="Screenshot 2025-02-24 at 5 19 58 PM" src="https://github.com/user-attachments/assets/5435ff1c-1328-42a7-8909-7a5098e57f63" />
<img width="5" alt="Screenshot 2025-02-24 at 5 18 32 PM" src="https://github.com/user-attachments/assets/e00aef82-9cf8-48e6-adef-1f57e66f7c73" />


# Web Content Q&A Tool

Overview

Web Content Q&A Tool is a Flask-based web application that allows users to ask questions based on content scraped from provided URLs. The tool fetches, processes, and extracts text from web pages, then answers user queries using a transformer-based question-answering model (DistilBERT fine-tuned on SQuAD).

🔹 Frontend: A static user interface is hosted on Netlify.

🔹 Backend: Flask-based server that handles web scraping and model inference.

🔹 Machine Learning Model: Uses DistilBERT for question answering.

🚀 Live Demo

A static version of the UI is hosted here:
https://majestic-chaja-cd765a.netlify.app

⚠️ Note: This hosted version includes only the UI. To test full functionality (content ingestion & Q&A processing), follow the instructions below to run it locally.

🛠️ Running the Application Locally

✅ Prerequisites
Before you begin, ensure you have the following installed:

Python 3.12 (or higher)
Git
Internet Connection (for dependencies & NLTK data download)

📌 Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/chanchalalam/Assignment3.git
cd Ai-Scraper

2️⃣ Create & Activate a Virtual Environment

python3 -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  

3️⃣ Install Dependencies

pip install -r requirements.txt 

4️⃣ Run the Application

python app.py  

5️⃣ Test the Q&A Functionality

Open your browser and go to: http://127.0.0.1:5000
Enter one or more URLs (comma-separated or newline-separated) to ingest content.
After ingestion, you’ll be redirected to the Q&A page.
Enter a question based on the scraped content and click "Get Answer".
The model will process the text and return the most relevant answer.


📁 Project Structure

Ai-Scraper/

├── app.py               # Flask application (handles web scraping & Q&A)  
├── index.html           # Static UI (hosted on Netlify)  
├── requirements.txt     # Python dependencies  
└── README.md            # This README file 


🔍 How It Works

1️⃣ Content Ingestion
User Input: The user enters one or more URLs.
Web Scraping: The app uses requests & BeautifulSoup to fetch and clean text.
Storage: The extracted content is stored in a global variable.

2️⃣ Text Processing & Question Answering
Chunking: Text is split into 400-word chunks using NLTK's sentence tokenizer (with overlap for context retention).
Q&A Model: Each chunk is processed using DistilBERT (fine-tuned on SQuAD).
Answer Selection: The highest-confidence answer is returned to the user.


🤖 Technology Stack

Backend: Flask, BeautifulSoup, Requests
Frontend: HTML, CSS (Hosted on Netlify)
Machine Learning: Hugging Face transformers (DistilBERT on SQuAD)
Other Tools: NLTK, Python virtual environment

