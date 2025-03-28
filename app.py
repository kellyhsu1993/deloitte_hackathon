import streamlit as st
import requests

st.set_page_config(page_title="Deloitte Strategy Insight Tool", layout="wide")

# Centered logo 
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])  # Responsive spacing
    with col2:
        st.image("Deloitte.png", width=120)

with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("query_form", clear_on_submit=False):
            query = st.text_input("", placeholder="e.g. What are UBC’s top 3 priorities for 2025, and how can Deloitte support?”")
            search = st.form_submit_button("Get Insight", use_container_width=True)

if search and query:
    with st.spinner("Powered by Deloitte’s deep sector knowledge and data assets…"):
        try:
            response = requests.post("http://localhost:8000/query", json={"question": query})
            result = response.json()

            st.divider()

            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("Insight")
                st.markdown(f"<div style='white-space: pre-wrap;'>{result['answer']}</div>", unsafe_allow_html=True)

            with col2:
                st.subheader("Sources")
                for src in sorted(set(result["sources"])):
                    st.markdown(f"- {src}")

        except Exception as e:
            st.error("Failed to connect to backend. Make sure the FastAPI server is running.")
            st.exception(e)