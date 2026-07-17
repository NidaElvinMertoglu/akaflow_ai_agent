import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from .prompts import CUSTOM_SQL_PREFIX

load_dotenv()

# Gemini bağlantısı
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

db = SQLDatabase.from_uri("sqlite:///data/student_data.db")


agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    verbose=True,
    agent_type="tool-calling", # openai-tools yerine standart tool-calling
    prefix=CUSTOM_SQL_PREFIX   # Özel talimatlarını buraya veriyoruz
)

def ask_agent(question: str) -> str:
    try:
        # invoke metodu ile soruyu iletiyoruz
        response = agent_executor.invoke({"input": question})
        return response["output"]
    except Exception as e:
        return f"Sorgu çalıştırılırken bir hata oluştu: {str(e)}"