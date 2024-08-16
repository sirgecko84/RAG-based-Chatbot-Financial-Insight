import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from query_data import query_rag



def main():
    st.title("RAG based Chatbot about Sun* Inc.'s Financial Insight")
    st.write("Enter your query and get a response based on the context in the database.")

    query_text = st.text_input("Enter your query:")

    if st.button("Get Response"):
        if query_text:
            response = query_rag(query_text)
            st.write(response)
        else:
            st.write("Please enter a query.")

if __name__ == "__main__":
    main()
