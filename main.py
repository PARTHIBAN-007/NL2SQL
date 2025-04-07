import streamlit as st
import time
import os
from groq import Groq

# Set page configuration
st.set_page_config(
    page_title="NLQ2SQL Converter",
    page_icon="🔍",
    layout="wide"
)

# App title and description
st.title("🔍 Natural Language to SQL Converter")
st.markdown("""
Convert your natural language questions into SQL queries using Llama model via Groq.
""")

# Define styling
st.markdown("""
<style>
    .sql-output {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for API key input and settings
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Groq API Key", type="password")
    
    # Model selection
    model_options = ["llama3-8b-8192", "llama3-70b-8192", "llama2-70b-4096"]
    selected_model = st.selectbox("Select Llama Model", model_options)
    
    # Example schema display
    st.subheader("Example Database Schema")
    st.code("""
    -- Users Table
    CREATE TABLE users (
        user_id INT PRIMARY KEY,
        username VARCHAR(50),
        email VARCHAR(100),
        signup_date DATE
    );
    
    -- Products Table
    CREATE TABLE products (
        product_id INT PRIMARY KEY,
        name VARCHAR(100),
        category VARCHAR(50),
        price DECIMAL(10,2)
    );
    
    -- Orders Table
    CREATE TABLE orders (
        order_id INT PRIMARY KEY,
        user_id INT,
        order_date DATE,
        total_amount DECIMAL(10,2),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    
    -- OrderItems Table
    CREATE TABLE order_items (
        item_id INT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

# Function to call the Groq API
def query_llama_model(question, schema, model_name):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
        return None
    
    client = Groq(api_key=api_key)
    
    # Construct the prompt
    prompt = f"""
    Given the following database schema:
    
    {schema}
    
    Convert this natural language question into a SQL query:
    
    "{question}"
    
    Return ONLY the SQL query without any explanations. Make sure it's valid SQL that could be executed directly.
    """
    
    try:
        # Call the Groq API with the selected model
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a SQL expert that converts natural language questions to SQL queries. Provide only the SQL query without explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        # Extract and clean up the response
        sql_query = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
            
        return sql_query
    
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")
        return None

# Main app area
col1, col2 = st.columns([3, 2])

with col1:
    # Schema input area
    st.subheader("Database Schema")
    schema = st.text_area(
        "Enter your database schema (CREATE TABLE statements)",
        height=200,
        value="""
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
        """
    )
    
    # User question input
    st.subheader("Your Question")
    question = st.text_area("Enter your question in natural language", placeholder="Example: Show me the top 5 customers who spent the most in the last month")
    
    # Process query button
    if st.button("Convert to SQL"):
        if not question:
            st.warning("Please enter a question.")
        elif not schema:
            st.warning("Please enter your database schema.")
        elif not api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        else:
            with st.spinner("Converting to SQL..."):
                # Show processing animation
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Call the API
                sql_result = query_llama_model(question, schema, selected_model)
                
                if sql_result:
                    # Add to history
                    st.session_state.history.append({
                        "question": question,
                        "sql": sql_result,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Display result
                    st.subheader("Generated SQL Query")
                    st.markdown(f'<div class="sql-output">{sql_result}</div>', unsafe_allow_html=True)
                    
                    # Copy button
                    st.code(sql_result, language="sql")
                    st.button("Copy to Clipboard", key="copy_button")

with col2:
    # History section
    st.subheader("Query History")
    
    if not st.session_state.history:
        st.info("No queries yet. Start by asking a question!")
    else:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Query {len(st.session_state.history) - i}: {item['question'][:50]}..."):
                st.caption(f"Time: {item['timestamp']}")
                st.markdown("**Question:**")
                st.write(item['question'])
                st.markdown("**SQL:**")
                st.code(item['sql'], language="sql")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and Groq's Llama models")