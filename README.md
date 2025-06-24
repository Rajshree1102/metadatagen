# 🤖 Intelligent Metadata Extractor

An interactive web app to extract intelligent, structured metadata from documents using **Groq’s LLaMA 3.1** and **spaCy NLP** — with built-in OCR and support for multiple file formats.

---

## ✨ What It Does

- 📄 **Text Extraction**: Reads content from PDF, DOCX, and TXT files, including scanned PDFs using OCR
- 🧠 **AI Summarization**: Uses LLaMA 3.1 (Groq) to generate short, meaningful summaries
- 🧵 **Entity Extraction**: Identifies names, organizations, and dates using NLP
- 🏷️ **Keyword Detection**: Extracts top keywords using lemmatization and frequency
- 📊 **Document Insights**: Shows file stats like word count, sentence count, and creation date
- 🧾 **Metadata Export**: Outputs everything in a clean, downloadable `.json` format

---

## 🚀 Try the App

- 🌐 **Live App**: [autometadatagen.streamlit.app](https://metadatagen-9ckvems8ztdnczmvjxkpgw.streamlit.app/)
- 📽️ **Demo Video**: [demo_video](https://drive.google.com/file/d/1mn6sRJ_mcgJbG1UJyNgoC885soNwqXjw/view?usp=sharing)

---

## 🛠️ How to Set It Up

### 📌 Requirements

#### Installation
```bash
git clone https://github.com/Rajshree1102/metadatagen.git
cd metadatagen
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
### Run locally
```bash
streamlit run app.py
```

### Groq API Key Setup
1. Visit console.groq.com and create a free account.

2. Generate your API key.

3. Paste the key into the sidebar of the app when prompted.


