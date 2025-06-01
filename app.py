# app.py
import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from deployment_agent import deploy_code

# Load environment variables from .env
load_dotenv()
from agents.requirements_agent import analyze_requirements
from agents.design_agent import create_design
from agents.coder_agent import generate_code
from deployment_agent import deploy_code

# Streamlit UI
st.set_page_config(page_title="Multi-Agent Code Generator")
st.title("Multi-Agent Code Generation and Deployment System")
st.write(
    "Enter a high-level prompt (e.g. *'Build me a website'* or *'Build me a snake game'*). "
    "Select models for each agent and click **Generate** to run the pipeline."
)

# Input prompt
prompt = st.text_input("Enter your prompt:")

# Model selection options
model_options = [
    "llama3-8b-8192",
    "Groq/Llama-3-Groq-8B-Tool-Use",
    "Groq/Llama-3-Groq-70B-Tool-Use",
    "gpt-3.5-turbo"  # Example OpenAI-compatible model via Groq
]

col1, col2, col3 = st.columns(3)
with col1:
    req_model = st.selectbox("Requirements Agent Model:", model_options, index=0)
with col2:
    design_model = st.selectbox("Design Agent Model:", model_options, index=0)
with col3:
    coder_model = st.selectbox("Coder Agent Model:", model_options, index=0)

# Button to trigger the pipeline
if st.button("Generate"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        # 1. Requirements Analysis
        st.subheader("1. Requirements Analysis")
        try:
            requirements = analyze_requirements(prompt, req_model)
            st.text(requirements)
        except Exception as e:
            st.error(f"Error in Requirements Agent: {e}")
            requirements = ""

        # 2. Design Specification
        if requirements:
            st.subheader("2. Design Specification")
            try:
                design = create_design(requirements, design_model)
                st.text(design)
            except Exception as e:
                st.error(f"Error in Design Agent: {e}")
                design = ""
        else:
            design = ""

        # 3. Code Generation
        if design:
            st.subheader("3. Code Generation")
            try:
                code_output = generate_code(design, coder_model)
                # Display the raw code output (Markdown formatted)
                st.markdown("```" + code_output + "```")
            except Exception as e:
                st.error(f"Error in Coder Agent: {e}")
                code_output = ""
        else:
            code_output = ""

        # 4. Deployment
        if code_output:
            st.subheader("4. Deployment")
            try:
                url, logs = deploy_code(code_output)
                st.success(f"App deployed at: {url}")
                st.text_area("Logs:", logs, height=200)
            except Exception as e:
                st.error(f"Error in Deployment Agent: {e}")
