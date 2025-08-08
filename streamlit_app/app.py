import streamlit as st
import requests
from streamlit_extras.stylable_container import stylable_container  # Requires pip install streamlit-extras

API_BASE = "http://localhost:8000"  # Change if deployed elsewhere

# Configure page
st.set_page_config(
    page_title="LLM Query Retrieval",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .stTextArea textarea {
            min-height: 150px;
        }
        .file-uploader {
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .question-card {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .success-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #e6f7e6;
            margin-bottom: 15px;
        }
        .stButton>button {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Response creativity", 0.0, 1.0, 0.7, 0.1)
    max_length = st.slider("Max response length", 50, 500, 200, 50)
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("This tool extracts answers from your documents using AI.")
    st.markdown("[GitHub Repository](#)")  # Add your repo link

# Main content
st.title("🧠 Document Intelligence Assistant")
st.caption("Upload your documents and ask questions to extract precise answers")

# File upload section
with st.container(border=True):
    st.subheader("📂 Document Upload")
    uploaded_files = st.file_uploader(
        "Select files (PDF, DOCX, EML, MSG, TXT)",
        accept_multiple_files=True,
        type=["pdf", "docx", "eml", "msg", "txt"],
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        with st.expander("Uploaded Files", expanded=False):
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({round(file.size/1024)} KB)")

# Questions section
with st.container(border=True):
    st.subheader("❓ Your Questions")
    questions_text = st.text_area(
        "Enter questions (one per line):",
        placeholder="Type your questions here, one per line...\nExample:\nWhat are the key findings?\nWho is the main author?",
        label_visibility="collapsed"
    )

# Action button with improved feedback
col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Get Answers", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one document.", icon="⚠️")
            st.stop()
        if not questions_text.strip():
            st.warning("Please enter at least one question.", icon="⚠️")
            st.stop()

        with st.status("Processing your request...", expanded=True) as status:
            # Step 1: Upload and parse documents
            status.update(label="Uploading and parsing documents...", state="running")
            documents = []
            progress_bar = st.progress(0)
            
            for i, file in enumerate(uploaded_files):
                try:
                    files = {"file": (file.name, file.getvalue())}
                    resp = requests.post(f"{API_BASE}/parse/", files=files)
                    if resp.status_code == 200:
                        parsed_text = resp.json().get("text", "")
                        documents.append(parsed_text)
                    else:
                        st.error(f"Failed to parse {file.name}: {resp.text}")
                        st.stop()
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
                    st.stop()
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Step 2: Prepare questions
            questions = [q.strip() for q in questions_text.strip().split("\n") if q.strip()]
            payload = {
                "documents": documents,
                "questions": questions,
                "temperature": temperature,
                "max_length": max_length
            }
            
            # Step 3: Query LLM
            status.update(label="Generating answers...", state="running")
            try:
                response = requests.post(f"{API_BASE}/api/v1/hackrx/run", json=payload)
                
                if response.status_code == 200:
                    status.update(label="Processing complete!", state="complete")
                    st.session_state['answers'] = response.json().get("answers", [])
                    st.session_state['questions'] = questions
                else:
                    status.update(label="Error occurred", state="error")
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                status.update(label="Connection error", state="error")
                st.error(f"Failed to connect to API: {str(e)}")

# Display results if available
if 'answers' in st.session_state and 'questions' in st.session_state:
    st.divider()
    st.subheader("📝 Answers")
    
    for i, (question, answer) in enumerate(zip(st.session_state['questions'], st.session_state['answers'])):
        with stylable_container(
            key=f"answer_{i}",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                    margin-bottom: 1rem;
                }
            """,
        ):
            st.markdown(f"**Q{i+1}:** {question}")
            st.markdown(f"<div style='color: #2e9f60; font-weight: 500;'>{answer}</div>", unsafe_allow_html=True)
        
        # Add feedback buttons for each answer
        cols = st.columns(5)
        with cols[0]:
            st.button("👍", key=f"upvote_{i}")
        with cols[1]:
            st.button("👎", key=f"downvote_{i}")
        with cols[-1]:
            st.button("📋 Copy", key=f"copy_{i}")
        
        if i < len(st.session_state['answers']) - 1:
            st.divider()