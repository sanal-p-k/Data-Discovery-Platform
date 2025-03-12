import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import plotly.express as px
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="LangChain SQL Chat App", page_icon="🦜", layout="wide")

# Home Page
def home_page():
    st.title("Welcome to LangChain SQL Chat App 🦜")
    st.markdown("""
        ### Features:
        - **Chat with SQL Database**: Interact with your SQL database using natural language.
        - **Visualize Query Results**: Automatically generate charts from query results.
        - **Support for SQLite and MySQL**: Connect to either a local SQLite database or a remote MySQL database.
    """)
    st.markdown("""
        ### How to Use:
        1. **Choose a Database**: Select either SQLite or MySQL from the sidebar.
        2. **Enter Connection Details**: Provide the necessary credentials for your database.
        3. **Start Chatting**: Ask questions in natural language and get answers from your database.
        4. **Visualize Data**: See automatic visualizations of your query results.
    """)
    st.markdown("""
        ### Get Started:
        Use the sidebar to navigate to the **SQL Chat** page and start interacting with your database.
    """)

# SQL Chat Page
def sql_chat_page():
    st.title("🦜 LangChain: Chat with SQL DB")

    LOCALDB = "USE_LOCALDB"
    MYSQL = "USE_MYSQL"

    radio_opt = ["Use SQLLite 3 Database- STUDENT.db", "Connect to your MySQL Database"]
    selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

    if radio_opt.index(selected_opt) == 1:
        db_uri = MYSQL
        mysql_host = st.sidebar.text_input("Provide MySQL Host")
        mysql_user = st.sidebar.text_input("MYSQL User")
        mysql_password = st.sidebar.text_input("MYSQL password", type="password")
        mysql_db = st.sidebar.text_input("MySQL database")
    else:
        db_uri = LOCALDB

    groq_api_key = os.getenv("GROQ_API_KEY")
    api_key = st.sidebar.text_input(label="GROQ API Key", type="password")

    if not db_uri:
        st.info("Please enter the database information and uri")

    if not api_key:
        st.info("Please add the GROQ API key")

    # LLM model
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

    @st.cache_resource(ttl="2h")
    def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
        if db_uri == LOCALDB:
            dbfilepath = (Path(__file__).parent / "STUDENT.db").absolute()
            print(dbfilepath)
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        elif db_uri == MYSQL:
            if not (mysql_host and mysql_user and mysql_password and mysql_db):
                st.error("Please provide all MySQL connection details.")
                st.stop()
            return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

    if db_uri == MYSQL:
        db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
    else:
        db = configure_db(db_uri)

    # Toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query = st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

            # Attempt to parse the response into a DataFrame for visualization
            try:
                # Assuming the response is a string representation of a table
                data = [line.split() for line in response.split('\n') if line.strip()]
                df = pd.DataFrame(data[1:], columns=data[0])

                # Generate a simple bar chart using Plotly
                if not df.empty:
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Query Results Visualization")
                    st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Could not generate chart: {e}")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "SQL Chat"])

if page == "Home":
    home_page()
elif page == "SQL Chat":
    sql_chat_page()