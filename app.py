import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
import time

# --- API Configuration ---
API_KEY = "AIzaSyADWhQdW-LgwsZADPpUtGXOKUu9-jClXVw"
SEARCH_ENGINE_ID = "96fda36fb2fe342a8"

# --- Styling ---
st.set_page_config(page_title="Company Domain Finder", page_icon="🌐", layout="centered")
st.markdown(
    """
    <style>
        .main { background-color: #f8f9fa; }
        .stButton button { background-color: #4CAF50; color: white; font-size: 16px; border-radius: 8px; }
        .stFileUploader { border: 2px dashed #4CAF50; padding: 10px; border-radius: 8px; }
        .stDownloadButton button { background-color: #007bff; color: white; font-size: 16px; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Function to Extract Domain ---
def clean_domain(url):
    """Extracts the domain from a URL, removing http/https, www, and trailing slashes."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain[4:] if domain.startswith("www.") else domain

def find_domain(company_name):
    """Fetches the official website domain using Google's Custom Search API."""
    query = f"{company_name} official website"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": API_KEY, "cx": SEARCH_ENGINE_ID, "q": query}

    try:
        response = requests.get(url, params=params)
        data = response.json()
    except Exception as e:
        return None

    if "items" in data:
        for item in data["items"]:
            link = item.get("link", "")
            if company_name.lower() in link.lower():
                return clean_domain(link)
        return clean_domain(data["items"][0]["link"])

    return None

def process_uploaded_file(uploaded_file):
    """Processes the CSV file and fetches domains for each company."""
    df = pd.read_csv(uploaded_file)
    df['domain'] = None

    progress_bar = st.progress(0)
    total_rows = len(df)

    for index, row in df.iterrows():
        df.at[index, 'domain'] = find_domain(row['company_name'])
        progress_bar.progress((index + 1) / total_rows)

    return df

# --- UI Layout ---
st.title("🌐 Company Domain Finder")
st.write("Upload a CSV file with a **company_name** column, and get a processed file with website domains.")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload CSV file", type="csv")

if uploaded_file:
    st.write("🔄 **Processing file... Please wait.**")
    time.sleep(1)  # Small delay for a better UI experience
    
    processed_df = process_uploaded_file(uploaded_file)
    
    st.success("✅ Processing Complete!")
    st.write("### 📊 Processed File Preview")
    st.dataframe(processed_df)

    # --- Download Button ---
    st.download_button(
        label="📥 Download Processed CSV",
        data=processed_df.to_csv(index=False).encode("utf-8"),
        file_name="output_with_domains.csv",
        mime="text/csv"
    )
