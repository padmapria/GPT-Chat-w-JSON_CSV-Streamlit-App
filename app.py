import streamlit as st
import os
import pandas as pd
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if the OPENAI_API_KEY is set, otherwise show an error in the app
if openai_api_key is None:
    st.error("OPENAI_API_KEY is not set. Please check your .env file.")
else:
    openai.api_key = openai_api_key

def chat_with_csv(df, prompt):
    try:
        # Convert the dataframe to CSV format without the index
        data = df.to_csv(index=False)
        # Call the OpenAI ChatCompletion API with the data and user's prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data analyst."},
                {"role": "user", "content": f"Here is the data:\n{data}\n\n{prompt}"}
            ],
        )
        # Extract the result from the API response
        result = response['choices'][0]['message']['content'].strip()
        print(result)
        return result
    except Exception as e:
        # Show any errors that occur during the API call
        st.error(f"Error: {e}")
        return None

# Set the page configuration to use a wide layout
st.set_page_config(layout='wide')

# Set the title of the page
st.title("ChatCSV powered by GPT-3.5-turbo")

# File uploader widget to accept CSV files
input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        # Read the uploaded CSV file into a DataFrame
        data = pd.read_csv(input_csv)
        # Display the DataFrame in a container
        st.dataframe(data, use_container_width=True)

    with col2:
        st.info("Chat Below")
        # Text area for the user to enter their query
        input_text = st.text_area("Enter your query")

        if input_text:
            # Button to initiate the chat
            if st.button("Chat with CSV"):
                st.info("Your Query: " + input_text)
                # Call the function to chat with the CSV data
                result = chat_with_csv(data, input_text)
                if result is not None:
                    # Display the chat result
                    st.success(result)
