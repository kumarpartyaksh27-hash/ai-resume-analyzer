import streamlit as st
from google import genai
import pypdf

# Page Setup
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & ATS Matcher")
st.write("Apna Resume upload/paste karo aur Target Job Description daalo. AI batayega Resume kitna match karta hai!")

# Sidebar for API key
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
st.sidebar.markdown("[Get Free Gemini API Key](https://aistudio.google.com/app/apikey)")

# Inputs
job_desc = st.text_area("🎯 Paste Job Description / Role Details:", height=120)
uploaded_file = st.file_uploader("📤 Upload Resume (PDF format)", type=["pdf"])
resume_text_input = st.text_area("✍️ Or Paste Resume Text directly:", height=150)

resume_content = ""
if uploaded_file is not None:
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_content += page.extract_text() or ""
        st.success("PDF Resume successfully read!")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
elif resume_text_input:
    resume_content = resume_text_input

if st.button("📊 Analyze Resume", use_container_width=True):
    if not api_key:
        st.warning("⚠️ Kripya sidebar me Gemini API Key dalein!")
    elif not resume_content:
        st.warning("⚠️ Kripya Resume upload karein ya text paste karein!")
    elif not job_desc:
        st.warning("⚠️ Kripya Job Description dalein!")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Resume analyze ho raha hai..."):
                prompt = f"""
                You are an expert HR and ATS reviewer. Analyze this resume against the job description.
                
                JOB DESCRIPTION:
                {job_desc}
                
                RESUME CONTENT:
                {resume_content}
                
                Provide a detailed feedback report in Markdown with:
                1. **Match Score**: Percentage score out of 100%.
                2. **Strengths**: Matching skills and strong areas.
                3. **Missing Skills**: Key missing skills/keywords required for this role.
                4. **Actionable Suggestions**: 3-4 bullet points to improve the resume for this job.
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                st.subheader("📋 Analysis Result")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")