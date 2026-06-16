import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.title("AI Test Case Generator")

story = st.text_area(
    "Enter User Story",
    height=200
)

if st.button("Generate Test Cases"):

    prompt = f"""
    You are a Senior QA Architect.

    Generate:

    1. Functional Test Cases
    2. Negative Test Cases
    3. Boundary Test Cases
    4. API Test Cases

    For this requirement:

    {story}

    Output in table format:
    Test ID
    Scenario
    Steps
    Expected Result
    Priority
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    st.sidebar.title("AI QA Assistant")
    st.markdown(response.choices[0].message.content)