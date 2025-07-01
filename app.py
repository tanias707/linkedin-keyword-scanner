import streamlit as st
import fitz  # PyMuPDF
import re

def load_keywords(role):
    try:
        with open(f"keywords/{role}.txt", "r") as f:
            return [kw.strip().lower() for kw in f.readlines()]
    except FileNotFoundError:
        return []

def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text.lower()

def check_keywords(text, keywords):
    present = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', text)]
    missing = [kw for kw in keywords if kw not in present]
    return present, missing

st.title("🔍 LinkedIn Resume Keyword Scanner")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
role = st.selectbox("Select job role", ["data_scientist", "frontend_developer"])

if uploaded_file and role:
    with st.spinner("Analyzing resume..."):
        text = extract_text_from_pdf(uploaded_file)
        keywords = load_keywords(role)
        present, missing = check_keywords(text, keywords)

        st.success("✅ Scan Complete!")
        st.markdown(f"**Matched Keywords ({len(present)})**")
        st.write(present)

        st.markdown(f"**Missing Keywords ({len(missing)})**")
        st.write(missing)
