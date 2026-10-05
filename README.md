# 🔍 ClaimCheck AI

### OCR & LLM-Based Document Claim Verification System

ClaimCheck AI is an intelligent document verification system that uses **Optical Character Recognition (OCR)** and a **Large Language Model (LLM)** to analyze claims from documents and compare them with reference information.

The system extracts text from uploaded documents, identifies important claims, and verifies each claim against the provided reference document.

---

## 🚀 Project Overview

Documents can contain claims that are difficult to manually verify. ClaimCheck AI helps automate this process by combining OCR-based text extraction with AI-powered semantic comparison.

### How it works

```text
📄 Claim Document
        ↓
     🔍 OCR
        ↓
   Extracted Claims
        ↓
   🤖 LLM Analysis
        ↑
 Reference Document
        ↑
     🔍 OCR
        ↓
📊 Verification Report

---

## ✨ Key Features

- 📄 Upload claim documents
- 📚 Upload reference/evidence documents
- 🔍 Extract text using OCR
- 🤖 Analyze claims using an LLM
- ✅ Identify supported claims
- ❌ Identify contradicted claims
- ⚠️ Identify unverified claims
- 📊 Generate a structured verification report
- 📈 Display verification summary
- 🌐 Deployable as a Streamlit web application

---

## 🧠 Claim Verification

Each important claim is classified into one of three categories:

| Status | Meaning |
|---|---|
| ✅ **SUPPORTED** | The reference document provides evidence supporting the claim. |
| ❌ **CONTRADICTED** | The reference document contains information that conflicts with the claim. |
| ⚠️ **UNVERIFIED** | The reference document does not contain enough information to verify the claim. |

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Tesseract OCR**
- **Pytesseract**
- **Groq API**
- **OpenAI GPT-OSS 120B**
- **Pillow**
- **python-dotenv**

---

## 🏗️ System Architecture

```text
             USER
               │
               ▼
      ┌─────────────────┐
      │ Upload Documents│
      └────────┬────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
 Claim Document   Reference Document
        │             │
        ▼             ▼
      OCR             OCR
        │             │
        └──────┬──────┘
               ▼
       Extracted Text
               │
               ▼
       ┌───────────────┐
       │   LLM Model   │
       │ GPT-OSS 120B  │
       └───────┬───────┘
               │
               ▼
      Claim Verification
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   Supported  Contradicted  Unverified
       │       │        │
       └───────┼────────┘
               ▼
      📊 Verification Report

      ---

## 📂 Project Structure

```text
ClaimCheck-AI/
│
├── app.py
├── ocr.py
├── llm.py
├── requirements.txt
├── packages.txt
├── README.md
└── .gitignore
