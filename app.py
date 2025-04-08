import streamlit as st
from groq import Groq
from langchain_community.llms import Groq
from langchain.chains import LLMChain
st.set_page_config(
    page_title= "NL2SQL",
)

st.title("LLama NL2SQL")
import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key
def initialize_llm():
    if groq_api_key is None:
        return "No API KEY Found"
    else:
        llm = Groq(model="mixtral-8x7b-32768")

        return "LLM is Initialized Successfully"

def llm_query_generator(user_question):
    global llm
    schema = '''job_role VARCHAR,
        experience_level VARCHAR(50),         
        min_salary DECIMAL(10,2),            
        max_salary DECIMAL(10,2),
        location VARCHAR(100),
        department VARCHAR(100)'''
    model_name = "llama-3.1-8b-instant"
    prompt =  f"""
    Given the following database schema:
    
    {schema}
    
    Convert this natural language question into a SQL query:
    
    "{user_question}"
    
    Return ONLY the SQL query without any explanations. Make sure it's valid SQL that could be executed directly.
    """

    try:
        chain = LLMChain(llm=llm, prompt=prompt)

        
        sql_query = chain.run(prompt)
        print(sql_query)
        
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
            
        return sql_query
    
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")

user_question = st.chat_input("Ask You Queries ")

if user_question:
    llm_query = llm_query_generator(user_question)
    print(llm_query)

if __name__ =="__main__":
    initialize_llm()
    print("LLM in initialized succesfully")