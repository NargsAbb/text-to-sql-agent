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

if "question_text" not in st.session_state:
  st.session_state.question_text = sample_questions[0]
if "history" not in st.session_state:
  st.session_state.history = []


def _apply_sample():
  if st.session_state.sample_select != "-- Select --":
    st.session_state.question_text = st.session_state.sample_select


st.selectbox(
    "Select a sample question (optional):",
    ["-- Select --"] + sample_questions,
    key="sample_select",
    on_change=_apply_sample,
)

user_input = st.text_input("Your Question:", key="question_text")

if st.button("Run Query"):
  if user_input:
    try:
      with st.spinner("Generating SQL query..."):
        sql_query = generate_sql(user_input)
      st.subheader("Generated SQL Query:")
      st.code(sql_query, language="sql")

      with st.spinner("Running query against the database..."):
        results = execute_query(sql_query)
      st.subheader("Execution Results:")
      st.dataframe(results, use_container_width=True)
      st.download_button(
          "Download results as CSV",
          results.to_csv(index=False).encode("utf-8"),
          file_name="query_results.csv",
          mime="text/csv",
      )

      st.session_state.history.insert(
          0, {"question": user_input, "sql": sql_query}
      )
    except Exception as e:
      st.error(f"Execution Error: {e}")

if st.session_state.history:
  st.subheader("Question History")
  for item in st.session_state.history[:10]:
    with st.expander(item["question"]):
      st.code(item["sql"], language="sql")