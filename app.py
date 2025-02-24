import ssl
import certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

import math
from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

app = Flask(__name__)
app.secret_key = "supersecretkey"
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
INGESTED_CONTENT = ""

def scrape_url_text(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ")
        text = " ".join(text.split())
        print(f"Scraped text from {url} (first 200 chars): {text[:2000]}")
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def chunk_text(text, max_words=400, overlap=50):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_len = 0
    for sentence in sentences:
        words = sentence.split()
        if current_len + len(words) > max_words:
            chunks.append(" ".join(current_chunk))
            overlap_chunk = current_chunk[-overlap:] if overlap < len(current_chunk) else current_chunk
            current_chunk = overlap_chunk + [sentence]
            current_len = sum(len(s.split()) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_len += len(words)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls = request.form.get("urls")
        if urls:
            url_list = [url.strip() for url in urls.replace(",", "\n").split("\n") if url.strip()]
            all_text = ""
            for url in url_list:
                text = scrape_url_text(url)
                all_text += text + "\n\n"
            if all_text:
                global INGESTED_CONTENT
                INGESTED_CONTENT = all_text
                return redirect(url_for("qa"))
    return render_template_string("""
        <!doctype html>
        <html>
          <head>
            <title>Web Content Q&A Tool - Ingest URLs</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 2em; }
              textarea { width: 100%; height: 150px; }
              input[type="submit"] { padding: 0.5em 1em; }
            </style>
          </head>
          <body>
            <h1>Enter URLs to Ingest Content</h1>
            <form method="post">
              <label for="urls">Enter one or more URLs (separated by commas or newlines):</label><br>
              <textarea id="urls" name="urls" required></textarea><br><br>
              <input type="submit" value="Ingest Content">
            </form>
          </body>
        </html>
    """)

@app.route("/qa", methods=["GET", "POST"])
def qa():
    answer = None
    question = ""
    if request.method == "POST":
        question = request.form.get("question")
        if question and INGESTED_CONTENT:
            chunks = [chunk for chunk in chunk_text(INGESTED_CONTENT, max_words=400) if chunk.strip()]
            print(f"Total non-empty chunks: {len(chunks)}")
            best_answer = None
            best_score = -float("inf")
            for chunk in chunks:
                try:
                    result = qa_pipeline(question=question, context=chunk)
                    print(f"Result from chunk: {result}")
                    if result["score"] > best_score:
                        best_score = result["score"]
                        best_answer = result["answer"]
                except Exception as e:
                    print(f"QA error: {e}")
                    continue
            answer = best_answer if best_answer else "No answer found based on the ingested content."
    return render_template_string("""
        <!doctype html>
        <html>
          <head>
            <title>Web Content QA Tool - Ask a Question</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 2em; }
              input[type="text"] { width: 100%; padding: 0.5em; }
              input[type="submit"] { padding: 0.5em 1em; margin-top: 1em; }
              .answer { background-color: #f0f0f0; padding: 1em; margin-top: 1em; }
            </style>
          </head>
          <body>
            <h1>Ask a Question</h1>
            <form method="post">
              <label for="question">Enter your question (based solely on the ingested content):</label><br>
              <input type="text" id="question" name="question" value="{{ question }}" required><br><br>
              <input type="submit" value="Get Answer">
            </form>
            {% if answer %}
              <div class="answer">
                <h3>Answer:</h3>
                <p>{{ answer }}</p>
              </div>
            {% endif %}
          </body>
        </html>
    """, answer=answer, question=question)

if __name__ == "__main__":
    app.run(debug=True)
