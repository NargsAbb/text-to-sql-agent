import re
import ollama
import pandas as pd
from sqlalchemy import create_engine, inspect, text

engine = create_engine("sqlite:///company.db")

def get_schema():
    inspector = inspect(engine)
    schema_text = ""
    for table_name in inspector.get_table_names():
        schema_text += f"Table: {table_name}\nColumns:\n"
        for column in inspector.get_columns(table_name):
            schema_text += f"  - {column['name']} ({column['type']})\n"
        schema_text += "\n"
    return schema_text

def generate_sql(user_query, model_name="gemma3:4b"):
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
  response = ollama.generate(
      model=model_name,
      prompt=prompt,
      options={
          "num_ctx": 1024,
          "num_thread": 2,  # کاهش تعداد نخ‌های CPU برای جلوگیری از جهش رم
      },
  )
  raw_sql = response["response"].strip()

  clean_sql = re.sub(r"```(?:sql)?", "", raw_sql).strip()
  return clean_sql