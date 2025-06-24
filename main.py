# libraries
import os
import json
import time
import fitz
import pytesseract
import spacy
import requests
import streamlit as st
from PIL import Image
from collections import Counter
from pdf2image import convert_from_path
from docx import Document


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# --------------------------
# Helper Functions
# --------------------------
def extract_text(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        doc = fitz.open(file_path)
        text = ''.join([page.get_text() for page in doc])
        if not text.strip():
            images = convert_from_path(file_path)
            text = "\n".join([pytesseract.image_to_string(img) for img in images])
        return text
    elif ext == 'docx':
        return "\n".join([p.text for p in Document(file_path).paragraphs])
    elif ext == 'txt':
        return open(file_path, 'r', encoding='utf-8').read()
    else:
        return ""

def extract_spacy_metadata(text):
    doc = nlp(text)
    words = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
    keywords = [word for word, _ in Counter(words).most_common(7)]
    people = list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"]))
    orgs = list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
    dates = list(set([ent.text for ent in doc.ents if ent.label_ == "DATE"]))
    return {
        "keywords": keywords,
        "people": people,
        "organizations": orgs,
        "dates": dates
    }

def generate_summary_with_groq(text, api_key):
    prompt = f"""
You are a summarization assistant.
From the document below, extract only the summary.
The summary should be concise and no longer than 4 lines.

Document:
{text[:3000]}
"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 256
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return "Summary generation failed."

# --------------------------
# Streamlit Interface
# --------------------------
st.set_page_config(page_title="Metadata Extractor", layout="wide")
st.title("📄 Automated Metadata Extraction")

st.sidebar.header("🔐 API Configuration")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file and groq_api_key:
    with st.spinner("Processing document..."):
        # Save uploaded file
        temp_path = f"./temp_uploaded_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text & metadata
        text = extract_text(temp_path)
        # Limit text to 50,000 characters
        MAX_CHARS = 50000
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS]

        summary = generate_summary_with_groq(text, groq_api_key)
        spacy_data = extract_spacy_metadata(text)
        file_info = {
            "file_name": uploaded_file.name,
            "creation_date": time.ctime(os.path.getctime(temp_path))
        }

        metadata = {
            **file_info,
            "summary": summary,
            **spacy_data
        }

        # Save to JSON
        output_file = uploaded_file.name.rsplit(".", 1)[0] + "_metadata.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Display
        st.success("✅ Metadata extracted successfully!")
        st.subheader("📋 Summary")
        st.write(summary)

        st.subheader("📊 Named Entities")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("👤 People")
            st.write(spacy_data["people"])
        with col2:
            st.write("🏢 Organizations")
            st.write(spacy_data["organizations"])
        with col3:
            st.write("📅 Dates")
            st.write(spacy_data["dates"])

        st.subheader("🏷️ Keywords")
        st.write(spacy_data["keywords"])

        st.download_button("📥 Download Metadata JSON", data=json.dumps(metadata, indent=2), file_name=output_file, mime="application/json")
else:
    st.info("Please upload a file and enter your API key.")

