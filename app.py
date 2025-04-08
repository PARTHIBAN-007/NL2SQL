import os
from dotenv import load_dotenv
load_dotenv()
import sqlite3
gemini_api_key = os.getenv("GEMINI_API_KEY")
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
st.set_page_config(
    page_title= "NL2SQL",
)

st.title("Gemini NL2SQL")


def llm_query_generator(user_question):
    llm = GoogleGenerativeAI(model = "gemini-1.5-flash",temperature=0.7)
    schema = '''job_role VARCHAR,
        experience_level VARCHAR(50),         
        min_salary DECIMAL(10,2),            
        max_salary DECIMAL(10,2),
        location VARCHAR(100),
        department VARCHAR(100)'''
    prompt =  f"""
    Given the following database schema:
    Table Name : jobs
    Columns : {schema}
    
    
    Convert this natural language question into a SQL query:
    
    "{user_question}"
    
    Return ONLY the SQL query without any explanations. Make sure it's valid SQL that could be executed directly.
    """

    try:
        
        print(prompt)
        sql_query = llm.invoke(prompt)
        print(sql_query)
        
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
            
        return sql_query
    
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")

def llm_response(user_query,sql_query,data):
    prompt = f"you are an AI Assistant designed to explain the response from from the database about the user question. user Question :{user_query} Query for SQl : {sql_query} Data in the database : {data}.Explain only the response with respect to user query not about sql_query"
    llm = GoogleGenerativeAI(model = "gemini-1.5-flash",temperature=0.7)
    response = llm.invoke(prompt)
    return response

user_question = st.chat_input("Ask You Queries ")

if user_question:
    llm_query = llm_query_generator(user_question)
    print(llm_query)
    st.write(llm_query)

    conn = sqlite3.connect("job.db")
    cursor = conn.cursor()
    cursor.execute(f'''{llm_query}''')
    data_response = cursor.fetchall()
    response = llm_response(user_question,llm_query,data_response)
    st.write(response)



