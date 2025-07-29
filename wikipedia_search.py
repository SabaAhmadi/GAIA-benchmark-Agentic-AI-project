# from langchain.tools import BaseTool
# from typing import Type
# from langchain.tools.base import ToolException
# #from pydantic import BaseModel, Field
# import wikipedia

# #class WikipediaQueryInput(BaseModel):
# #    query: str = Field(..., description="The topic to search on Wikipedia")

# class WikipediaTool(BaseTool):
#     name: str = "wikipedia_query"
#     description: str = "Use this tool to search for summaries of topics on Wikipedia. The query should not contain any noise and ask for something specific."
#     #args_schema: Type[BaseModel] = WikipediaQueryInput

#     def _run(self, query: str) -> str:
#         try:
#             page = wikipedia.page(query, auto_suggest=True)
#             return page.content
#         except wikipedia.exceptions.DisambiguationError as e:
#             return f"Ambiguous topic. Options: {', '.join(e.options[:5])}"
#         except wikipedia.exceptions.PageError:
#             return "No page found for the given topic."
#         except Exception as e:
#             return f"Error: {e}"

#     def _arun(self, query: str):
#         raise NotImplementedError("Async not implemented.")
# Importing necessary libraries and modules
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
#from pydantic import PrivateAttr
from langchain_core.tools.base import BaseTool
#from langchain_community.document_loaders import WikipediaLoader
#import requests
from bs4 import BeautifulSoup
import wikipedia

# Defining the WikipediaTool class which extends BaseTool
class WikipediaTool(BaseTool):
    name: str = "wikipedia_tool"
    description: str = "Search Wikipedia for a given query, retrieving the corresponding page's HTML content. The query should not contain any noise and ask for something specific."

    def __init__(self):
        # Initializing the WikipediaTool
        super().__init__()

    def _run(self, query: str):
        # Method to run the Wikipedia tool with the given query
        print(f"wikipedia_search_html called with query='{query}'")  # Logging the query
        # Step 1: Get Wikipedia HTML
        page = wikipedia.page(query)  # Fetching the Wikipedia page for the query
        html = page.html()  # Extracting the HTML content of the page

        # Step 2: Parse HTML
        soup = BeautifulSoup(html, "html.parser")  # Parsing the HTML content
        content_div = soup.find("div", class_="mw-parser-output")  # Finding the content division
        # content_div = soup.find("table", class_="wikitable")
        if not content_div:
            return ""

        # Step 3: Find all tags to remove (style, script, sup, infobox, etc.)
        to_decompose = []  # Collecting tags to be removed
        for tag in content_div.find_all():  # Looping through all tags in the content division
            tag_classes = tag.get("class", [])
            if (
                tag.name in ["style", "script", "sup"]
                or any(cls in ["infobox", "navbox", "reference"] for cls in tag_classes)
            ):
                to_decompose.append(tag)

        # Remove them after collecting
        for tag in to_decompose:  # Decompose and remove the collected tags
            tag.decompose()
        
        return str(content_div)  # Returning the cleaned content division as string