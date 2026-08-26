import streamlit as st
from database import init_db
from llm_agent import execute_query, generate_sql

init_db()

st.set_page_config(page_title="Text-to-SQL Agent", layout="wide")
st.title("🤖 Text-to-SQL AI Agent")
st.write(
    "Ask questions in natural language to generate and execute SQL queries on"
    " the database."
)

sample_questions = [
    "Show total spending for each user along with their name",
    "Which products have the highest stock in inventory?",
    "List all users who are located in New York",
    "What is the average review rating for each product?",
]

selected_sample = st.selectbox(
    "Select a sample question (optional):", ["-- Select --"] + sample_questions
)

default_text = (
    selected_sample
    if selected_sample != "-- Select --"
    else "Show total spending for each user along with their name"
)

user_input = st.text_input("Your Question:", value=default_text)

if st.button("Run Query"):
  if user_input:
    with st.spinner("Generating SQL query..."):
      try:
        sql_query = generate_sql(user_input)
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")

        results = execute_query(sql_query)
        st.subheader("Execution Results:")
        st.dataframe(results, use_container_width=True)
      except Exception as e:
        st.error(f"Execution Error: {e}")