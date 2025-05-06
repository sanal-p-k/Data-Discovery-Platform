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
st.set_page_config(page_title="Data Discovery Platform", page_icon="🦜📊", layout="wide")
# Add background image using CSS
def set_background_image(image_path):
    # Check if it's a URL or a local image file
    if image_path.startswith("https://img.freepik.com/free-vector/background-realistic-abstract-technology-particle_23-2148431735.jpg?ga=GA1.1.577877657.1743059272&semt=ais_hybrid") or image_path.startswith("https://img.freepik.com/free-vector/background-realistic-abstract-technology-particle_23-2148431735.jpg?ga=GA1.1.577877657.1743059272&semt=ais_hybrid"):
        image_url = image_path
    else:
        # If it's a local image, ensure it's in the correct directory
        image_url = f'file://{Path(image_path).absolute()}'
    
    # Inject custom CSS to apply the background
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """, 
        unsafe_allow_html=True
    )

# Set the background image (replace with the image path or URL)
background_image_path = "https://img.freepik.com/free-vector/background-realistic-abstract-technology-particle_23-2148431735.jpg?ga=GA1.1.577877657.1743059272&semt=ais_hybrid"  # Use a URL for external image
# OR if you are using a local file, use the relative path
# background_image_path = "./images/background-image.jpg"
set_background_image(background_image_path)
# Home Page
def home_page():
    st.title("Welcome to Data Discovery Platform 🦜📊")
    st.markdown("""
        ## Your All-in-One Data Interaction Hub
        
        Transform how you work with databases and analytics with our powerful integration platform.
        """)
    
    st.image("WTD.png")  # Add your banner image
    
    with st.expander("✨ Key Features", expanded=True):
        st.markdown("""
        ### **Database Interaction**
        - **Natural Language to SQL**: Chat with your database using plain English
        - **Multi-Database Support**: Works with SQLite, MySQL, PostgreSQL, and SQL Server
        - **Schema Exploration**: Auto-discover tables, relationships, and metadata
        - **Query Optimization**: Get AI-suggested query improvements
        
        ### **Power BI Integration**
        - **Direct Dataset Updates**: Push query results as new Power BI datasets
        - **Real-time Streaming**: Enable live dashboard updates
        - **Scheduled Refreshes**: Set up automatic data updates
        - **Visualization Suggestions**: Get recommended chart types for your data
        
        ### **Advanced Capabilities**
        - **Data Profiling**: Automatic analysis of data quality and distributions
        - **Export Options**: Download results as CSV, Excel, or JSON
        - **Collaboration Tools**: Share queries and results with team members
        - **History Tracking**: Maintain a log of all your queries and results
        """)
    
    with st.expander("📘 Step-by-Step Guide", expanded=False):
        st.markdown("""
        ### **Getting Started**
        1. **Connect to Your Database**
           - Navigate to the 'Connection Settings' page
           - Select your database type (SQLite, MySQL, etc.)
           - Enter your connection credentials
           - Test and save your connection
        
        2. **Query Your Data**
           - Go to the 'SQL Chat' interface
           - Type your question in natural language or SQL
           - Review the generated query before execution
           - View and analyze your results
        
        3. **Power BI Integration**
           - Authenticate with your Power BI account
           - Select a target workspace and dataset
           - Choose between one-time push or streaming mode
           - Configure refresh schedules if needed
        
        4. **Advanced Operations**
           - Use 'Save Query' to store frequently used queries
           - Set up alerts for data changes
           - Create automated reports
        """)
    
    with st.expander("🔧 System Requirements", expanded=False):
        st.markdown("""
        - **Supported Databases**: SQLite 3.0+, MySQL 5.7+, PostgreSQL 12+, SQL Server 2016+
        - **Power BI Requirements**: Power BI Pro or Premium license
        - **Browser Support**: Latest Chrome, Firefox, Edge, or Safari
        - **Network**: HTTPS connection required for Power BI integration
        """)
    
    st.markdown("""
    ### **Need Help?**
    - Check out our [documentation](https://docs.example.com)
    - Join our [community forum](https://community.example.com)
    - Contact support: support@example.com
    """)
    
    st.success("🚀 Ready to get started? Select a page from the sidebar to begin your data journey!")   

# SQL Chat Page with Power BI Integration
def sql_chat_page():
    st.title("🦜 Welcome to our Chatbot")

    # Database selection
    LOCALDB = "USE_LOCALDB"
    MYSQL = "USE_MYSQL"
    
    radio_opt = ["Use SQLLite 3 Database - STUDENT.db", "Connect to your MySQL Database"]
    selected_opt = st.sidebar.radio(label="Choose Database", options=radio_opt)

    if radio_opt.index(selected_opt) == 1:
        db_uri = MYSQL
        mysql_host = st.sidebar.text_input("MySQL Host")
        mysql_user = st.sidebar.text_input("MySQL User")
        mysql_password = st.sidebar.text_input("MySQL Password", type="password")
        mysql_db = st.sidebar.text_input("MySQL Database Name")
    else:
        db_uri = LOCALDB

    # API keys
    groq_api_key = os.getenv("GROQ_API_KEY")
    api_key = st.sidebar.text_input(label="GROQ API Key", type="password", value=groq_api_key or "")

    if not db_uri:
        st.info("Please enter database information")
    if not api_key:
        st.info("Please add your GROQ API key")

    # Database configuration
    @st.cache_resource(ttl="2h")
    def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
        if db_uri == LOCALDB:
            dbfilepath = (Path(__file__).parent / "STUDENT.db").absolute()
            creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
            return SQLDatabase(create_engine("sqlite:///", creator=creator))
        elif db_uri == MYSQL:
            if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
                st.error("Please provide all MySQL connection details")
                st.stop()
            return SQLDatabase(create_engine(
                f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            ))

    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db) if db_uri == MYSQL else configure_db(db_uri)

    # LLM and agent setup
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    # Chat interface
    if "messages" not in st.session_state or st.sidebar.button("Clear chat history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you query your database?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_query = st.chat_input(placeholder="Ask a question about your database")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)

            # Try to parse response into DataFrame
            try:
                data = [line.split("|") for line in response.split('\n') if "|" in line]
                if len(data) > 1:
                    df = pd.DataFrame(data[1:], columns=[col.strip() for col in data[0]])
                    
                    if not df.empty:
                        st.dataframe(df)
                        
                        # Power BI Integration Buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📊 Send to Power BI Dataset"):
                                try:
                                    push_to_powerbi_dataset(df)
                                    st.success("Data sent to Power BI dataset!")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        
                        with col2:
                            if st.button("⚡ Stream to Power BI (Real-Time)"):
                                try:
                                    push_to_powerbi_streaming(df)
                                    st.success("Data streaming to Power BI!")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        
                        # Visualization
                        st.subheader("Quick Visualizations")
                        chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Scatter"])
                        
                        if chart_type == "Bar":
                            fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                        elif chart_type == "Line":
                            fig = px.line(df, x=df.columns[0], y=df.columns[1])
                        else:
                            fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
                        
                        st.plotly_chart(fig)
            except Exception as e:
                st.warning(f"Could not parse results for visualization: {str(e)}")


# Power BI Dashboard Page
def powerbi_page():
    st.title("📊 Power BI Dashboard")
    
    # Get URL directly from .env
    embed_url = os.getenv("POWERBI_EMBED_URL")
    
    if embed_url:
        try:
            st.components.v1.iframe(
                embed_url,
                width=1000,
                height=600,
                scrolling=True
            )
        except Exception as e:
            st.error(f"Failed to load Power BI: {str(e)}")
            st.text(f"Debug - Embed URL: {embed_url}")
    else:
        st.warning("""
        Power BI URL not configured. Please:
        1. Add POWERBI_EMBED_URL to your .env file
        2. Ensure the URL is from 'Embed' in Power BI Service
        """)


# Update navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "SQL Chat", "Power BI Dashboard"])

    if page == "Home":
        home_page()
    elif page == "SQL Chat":
        sql_chat_page()
    elif page == "Power BI Dashboard":
        powerbi_page()

# Keep all other existing functions unchanged
# ... [Keep all other existing functions from previous code]

if __name__ == "__main__":
    main()