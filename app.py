import streamlit as st
import os
import pandas as pd
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    st.error("OPENAI_API_KEY is not set. Please check your .env file.")
else:
    openai.api_key = openai_api_key

def chat_with_csv(df, prompt):
    try:
        data = df.to_csv(index=False)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": f"Here is the data:\n{data}\n\n{prompt}"}
            ],
        )
        result = response['choices'][0]['message']['content'].strip()
        print(result)
        return result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.set_page_config(layout='wide')

st.title("ChatCSV powered by GPT-3.5-turbo")

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        input_text = st.text_area("Enter your query")

        if input_text is not None:
            if st.button("Chat with CSV"):
                st.info("Your Query: " + input_text)
                result = chat_with_csv(data, input_text)
                if result is not None:
                    st.success(result)
