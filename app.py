import streamlit as st
import time
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re

# Set up API Key (Ensure to store it securely, not hardcoded)
api_key = "AIzaSyCW7TyrAH-tKnoeZJR6xCnhYGXf6EOFthY"
if not api_key: 
    st.error("API key not found! Set GOOGLE_API_KEY in your environment variables.")
    st.stop()   
genai.configure(api_key=api_key)

# Screener.in credentials (Use environment variables for security)
SCREENER_USERNAME = "tempradhi@gmail.com"
SCREENER_PASSWORD = "Radhi@123"

# Function to upload PDFs to Gemini
def upload_to_gemini(file_obj, mime_type="application/pdf"):
    file = genai.upload_file(file_obj, mime_type=mime_type)
    return file

# Function to wait for file processing
def wait_for_files_active(files):
    for file in files:
        while True:
            file_status = genai.get_file(file.name)
            if file_status.state.name == "ACTIVE":
                break
            elif file_status.state.name == "FAILED":
                st.error(f"File {file.name} failed to process")
                return False
            time.sleep(5)
    return True

# Function to extract financial data using Gemini API
def extract_financial_data(file, user_prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message([file, user_prompt])
    return response.text

# Function to fetch financial data from Screener.in with authentication
def fetch_screener_data(company_symbol):
    login_url = 'https://www.screener.in/login/'
    data_url = f'https://www.screener.in/company/{company_symbol}/consolidated/#quarters'
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    # Get CSRF token
    session = requests.Session()
    login_page = session.get(login_url, headers=headers)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Login
    payload = {
        'username': 'tempradhi@gmail.com',
        'password': 'Radhi@123',
        'csrfmiddlewaretoken': csrf_token
    }
    session.post(login_url, data=payload, headers=headers)
    
    # Fetch data
    response = session.get(data_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all('table', {'class': 'data-table'})
    financials = {}
    
    if tables:
        rows = tables[0].find_all('tr')  # Process only the first table (Latest Quarter Data)
        for row in rows[1:]:  # Skip header
            columns = row.find_all('td')
            if len(columns) > 1:
                key = columns[0].text.strip()
                value = columns[-1].text.strip()
                financials[key] = value
    
    return financials if financials else {"error": "No financial data found"}

# Streamlit UI
st.title("📊 Financial Data Extractor and Screener Fetcher")

option = st.radio("Select Data Source:", ("Upload PDF", "Fetch from Screener.in"))

if option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload Financial PDF", type=["pdf"])
    prompt = st.text_area("Enter Prompt", "Extract Revenue, Net Profit, EPS, Operating Margin, and FCF for the latest quarter.")

    if st.button("Process"):
        if uploaded_file:
            file = upload_to_gemini(uploaded_file, mime_type="application/pdf")
            if wait_for_files_active([file]):
                st.success("File uploaded and processed successfully.")
                extracted_data = extract_financial_data(file, prompt)
                st.subheader("Extracted Data:")
                st.text(extracted_data)
        else:
            st.warning("Please upload a PDF file.")

elif option == "Fetch from Screener.in":
    company_name = st.text_input("Enter Company Symbol (e.g., TCS, INFY, RELIANCE)")
    
    if st.button("Fetch Data"):
        if company_name:
            screener_data = fetch_screener_data(company_name.upper())
            st.subheader("Screener.in Data:")
            st.json(screener_data)
        else:
            st.warning("Please enter a company symbol.")
