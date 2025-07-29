from langchain.tools import BaseTool
from typing import Type
#from pydantic import BaseModel, Field
import pandas as pd
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
#from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

#class ExcelQueryInput(BaseModel):
#    query: str = Field(..., description="The question to ask about the Excel data.")

class ExcelQueryTool(BaseTool):
    name: str = "excel_query"
    description: str = "Use this tool to answer questions about an Excel file. This file DOES NOT DOWNLOAD the file from the web. Run the download_file_tool first"
    #args_schema: Type[BaseModel] = ExcelQueryInput

    #def __init__(self, filepath: str, llm=None):
    #    super().__init__()
    #    self.filepath = filepath
    #    self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    def _run(self, query: str, input_file_path: str) -> str:
        try:
            print("trying to process an excel file.")
            df = pd.read_excel(input_file_path)
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
            agent = create_pandas_dataframe_agent(llm, df, verbose=False)
            response = agent.run(query)
            return response
        except Exception as e:
            return f"Error processing Excel file: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")

