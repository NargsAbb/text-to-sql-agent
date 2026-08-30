# Text-to-SQL AI Agent

A streamlined Natural Language to SQL generation interface built with Python, Streamlit, and SQLAlchemy. Powered by local Large Language Models via LM Studio for complete data privacy and zero API costs.

---

## Features

- **Natural Language Querying:** Convert plain English questions into executable SQLite queries.
- **Local LLM Integration:** Connects seamlessly to LM Studio using OpenAI's Python client.
- **Dynamic Schema Inspection:** Automatically extracts table structures and data types from SQLite databases.
- **Clean Execution Output:** Strips Markdown formatting and renders query results instantly in a Streamlit table.
- **Read-Only Query Guard:** Only `SELECT` statements are executed. Any generated query containing write/DDL keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, etc.) or multiple statements is rejected before it reaches the database.

---

## Architecture & Stack

- **Frontend:** Streamlit
- **ORM / Database:** SQLAlchemy & SQLite
- **Inference Engine:** LM Studio (Local OpenAI API emulation)
- **Base Model:** Qwen2.5-Coder-1.5B-Instruct

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- LM Studio installed and set up.

### 2. Setup LM Studio
1. Open LM Studio and search for `Qwen2.5-Coder-1.5B-Instruct`.
2. Download the model and navigate to the **Developer / Local Server** tab.
3. Select `Qwen2.5-Coder-1.5B-Instruct` from the top dropdown menu.
4. Click **Start Server** (runs by default on `http://localhost:1234`).

### 3. Installation
Clone the repository and install required packages:

`git clone https://github.com/NargsAbb/text-to-sql-agent.git`
`cd text-to-sql-agent`
`pip install streamlit pandas sqlalchemy openai`

---

## Usage

Run the Streamlit application:

`streamlit run app.py`

1. Enter your database query in plain English (or pick a sample question from the dropdown).
2. Click **Run Query**.
3. View the generated SQL query along with the execution results, and optionally download the results as CSV.
4. Previous questions are kept in the **Question History** section for quick reference.

> Note: the app only executes `SELECT` queries. If the model generates a write/DDL statement, it is blocked and an error is shown instead of being run against the database.