import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import os
from dotenv import load_dotenv  # Make sure you have installed `python-dotenv`
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Load environment variables from a .env file
load_dotenv()

# Set environment variables
os.environ["USER_AGENT"] = "MyColdEmailApp/1.0"


# Fetch GROQ API key
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("Missing GROQ_API_KEY in environment or .env file.")
os.environ["groq_api_key1"] = groq_key


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    st.title("Cold Mail Generator")

    url_input = st.text_input("Enter a job post URL:", value="https://jobs.nike.com/job/R-45600?from=job%20search%20funnel")

    if url_input and not url_input.startswith("http"):
        st.warning("Please enter a valid URL starting with 'http' or 'https'.")

    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner('Processing...'):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
