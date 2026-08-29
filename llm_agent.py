import re
import pandas as pd
from openai import OpenAI
from sqlalchemy import create_engine, inspect, text

engine = create_engine("sqlite:///company.db")

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def get_schema():
  inspector = inspect(engine)
  schema_text = ""
  for table_name in inspector.get_table_names():
    schema_text += f"Table: {table_name}\nColumns:\n"
    for column in inspector.get_columns(table_name):
      schema_text += f"  - {column['name']} ({column['type']})\n"
    schema_text += "\n"
  return schema_text


def generate_sql(user_query):
  schema = get_schema()
  prompt = f"""You are an expert SQL assistant. Given the following SQLite database schema:

{schema}

Convert this natural language query into a valid SQLite SQL query:
"{user_query}"

CRITICAL RULES:
1. Return ONLY the raw executable SQL query.
2. Do not use Markdown block syntax (no ```sql or ```).
3. Do not provide explanations or commentary.
"""

  response = client.chat.completions.create(
      model="qwen2.5-coder-1.5b-instruct",
      messages=[{"role": "user", "content": prompt}],
      temperature=0,
  )

  raw_sql = response.choices[0].message.content.strip()
  clean_sql = re.sub(r"```(?:sql)?", "", raw_sql).strip()
  return clean_sql


FORBIDDEN_KEYWORDS = (
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "CREATE", "TRUNCATE", "REPLACE", "ATTACH", "PRAGMA",
)


def execute_query(sql_query):
  stripped = sql_query.strip().rstrip(";")

  if not stripped.upper().startswith("SELECT"):
    raise ValueError("Only SELECT queries are allowed.")

  if ";" in stripped:
    raise ValueError("Multiple statements are not allowed.")

  upper_sql = stripped.upper()
  for keyword in FORBIDDEN_KEYWORDS:
    if keyword in upper_sql:
      raise ValueError(f"Query contains a forbidden keyword: {keyword}")

  with engine.connect() as conn:
    df = pd.read_sql_query(text(stripped), conn)
  return df