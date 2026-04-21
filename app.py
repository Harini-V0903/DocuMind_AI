import os
import streamlit as st
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client (SAFE)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="StudyMate AI", layout="centered")
st.title("📘 StudyMate AI (RAG Assistant)")


# ---------------- PDF LOADER ----------------
def load_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# ---------------- CHUNKER ----------------
def chunk_text(text, size=800):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i:i + size]))

    return chunks


# ---------------- SIMPLE RETRIEVAL ----------------
def retrieve(query, chunks):
    query_words = set(query.lower().split())

    scored = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words.intersection(chunk_words))
        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    top_chunks = [c for s, c in scored[:3] if s > 0]

    if not top_chunks:
        top_chunks = chunks[:2]

    return "\n".join(top_chunks)


# ---------------- UI ----------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:

    text = load_pdf(uploaded_file)

    if not text.strip():
        st.error("Could not extract text. Try a different PDF.")
        st.stop()

    chunks = chunk_text(text)

    st.success("PDF processed successfully!")

    question = st.text_input("Ask your question:")

    if question:

        context = retrieve(question, chunks)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a study assistant. Answer only from the given context. If not found, say 'Not found in notes'."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
        )

        st.subheader("Answer:")
        st.write(response.choices[0].message.content)