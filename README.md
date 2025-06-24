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

- 🌐 **Live App**: [autometadatagen.streamlit.app](https://autometadatagen.streamlit.app)
- 📽️ **Demo Video**: Coming soon

---

## 🛠️ How to Set It Up

### 📌 Requirements

#### Ubuntu / Debian
```bash
sudo apt-get install tesseract-ocr poppler-utils
