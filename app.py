import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Deloitte Strategy Insight Tool", layout="wide")

# Centered logo, heading, input, and button using one central column
with st.container():
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .input-full {
            width: 100%;
            max-width: 700px;
            margin-top: 1rem;
        }
        .button-full {
            width: 100%;
            max-width: 700px;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.image("Deloitte.png", width=200)
    st.markdown("### Strategy Insight Tool")

    # Form with full-width input and button
    with st.form("query_form", clear_on_submit=False):
        st.markdown('<div class="input-full">', unsafe_allow_html=True)
        query = st.text_input(
            label="",
            placeholder="e.g. What are UBC’s top 3 priorities for 2025, and how can Deloitte support?",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="button-full">', unsafe_allow_html=True)
        search = st.form_submit_button("Discover")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close centered div

# Result section
if search and query:
    with st.spinner("Powered by Deloitte’s deep sector knowledge and data assets…"):
        try:
            response = requests.post("http://localhost:8000/query", json={"question": query})
            result = response.json()

            st.divider()
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader("Insight")
                st.markdown(
                    f"<div style='white-space: pre-wrap; line-height: 1.6;'>{result['answer']}</div>",
                    unsafe_allow_html=True
                )

            with col2:
                st.subheader("📚 Sources")
                for src in sorted(set(result["sources"])):
                    st.markdown(f"- {src}")

        except Exception as e:
            st.error("Failed to connect to backend. Make sure the FastAPI server is running.")
            st.exception(e)
