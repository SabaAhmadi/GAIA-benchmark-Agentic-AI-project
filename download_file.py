from langchain_core.tools.base import BaseTool
import requests
#import base64
#import pandas as pd
import os
#import tempfile
#import whisper

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"
class DownloadFile(BaseTool):
    name : str = "download_file_tool"
    # description: str = """
    #     This tool downloads a file (image, pdf, python code, excel, etc.) given the file url. 
        
    #     Output:
    #     IF the file is a document, image or audio:
    #     A string with the path to the file.
        
    #     IF the file is a piece of code:
    #         A dict made of:
    #             The text of the image

    #     IF the file is an excel:
    #         A dict made of:
    #         A pandas dataframe
    #     """
    description: str = """
        This tool downloads a file (image, pdf, python code, excel, etc.) given the path of the file. 
        You may have to download a file in 2 different scenarios:
        - A file given already as part of the task. In this case the format of the url must be: https://agents-course-unit4-scoring.hf.space/files/{input_file_path}
        - A url retrieved from the internet in the format https://some_url. In that case, you simply need to provide the url of the file that needs to be retrieved.

        Args: 
            file_url: the url of the file to be retrieved https://agents-course-unit4-scoring.hf.space/files/{input_file_path} or https://some_url
            
        Output:
        IF the file is a document, image or audio:
        A string with the path to the file.
        
        IF the file is a piece of code:
            A dict made of:
                The text of the image

        IF the file is an excel:
            A dict made of:
            A pandas dataframe
         """

    #def _run(self, file_url: str, file_extension: str) -> dict:
    #def _run(self, input_file_path: str) -> dict:
    def _run(self, file_url: str) -> dict:
        #file_name = file_url.split("/")[-1].split(".")[0]
        #file_extension = file_url.split(".")[1]
        file_name = file_url.rsplit("/",maxsplit=1)[1].split(".")[0]
        file_extension = file_url.rsplit(".",maxsplit=1)[1]
        file_url_without_extension = file_url.rsplit(".",maxsplit=1)[0]
        print("debug in download_file tool: file_url, file_name, file_extension, file_url_without_extension", file_url, file_name, file_extension, file_url_without_extension)
        #response = requests.get(file_url)
        #if file_extension in ["png", "jpg", "pdf", "mp3", "wav", "py", "xlsx"]:
        if file_url.startswith("https://agents-course-unit4-scoring.hf.space"):
            response = requests.get(file_url_without_extension) #no extensions included in the url
        else:
            response = requests.get(file_url)
        print("response status code is:", response.status_code)
        #print("response status code is:", response.status_code)
        
        if response.status_code == 200:
            msg = "File downloaded successfully!!"
            print(msg)
            if file_extension in ["png", "jpg", "pdf"]:
                file = response.content
                
                #with open("downloaded_files/image.png", "wb") as f:
                with open("/tmp/image.png", "wb") as f:
                    f.write(file)

                return "/tmp/image.png"
            elif file_extension in ["mp3", "wav"]:
                res = response.content
                with open("/tmp/audio.mp3", mode="wb") as f:
                    f.write(res)

                return f"/tmp/audio.{file_extension}"

            elif file_extension == "py":
                return {"text": response.text}
            elif file_extension == "xlsx":
                #file_name = file_url.split("/")[-1]
                print("debug, downloading an excel file.")
                with open(f"/tmp/{file_name}.xlsx", "wb") as f:
                    f.write(response.content)

                return f"/tmp/{file_name}.xlsx"
            else:
                return "The file extension is not valid."
        else:
            msg = "There was an error downloading the file."
            print("msg, file_url_without_extension, response.status_code", msg, file_url_without_extension, response.status_code)

            return msg
# from langchain.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field
# import requests
# import os

#class DownloadFileInput(BaseModel):
#    url: str = Field(..., description="The URL of the file to download.")

# class DownloadFile(BaseTool):
#     name: str = "download_file"
#     description: str = "Downloads a file from a URL and saves it locally."
#     #args_schema: Type[BaseModel] = DownloadFileInput

#     # def __init__(self, download_dir: str = "/tmp/downloads"):
#     #     super().__init__()
#     #     self.download_dir = download_dir
#     #     os.makedirs(download_dir, exist_ok=True)

#     def _run(self, url: str) -> str:
#         try:
#             self.download_dir = "/tmp/downloads"
#             response = requests.get(url, timeout=10)
#             response.raise_for_status()

#             filename = os.path.basename(url.split("?")[0]) or "downloaded_file"
#             file_path = os.path.join(self.download_dir, filename)

#             with open(file_path, "wb") as f:
#                 f.write(response.content)

#             return f"File downloaded to: {file_path}"
#         except Exception as e:
#             return f"Error: {e}"

#     def _arun(self, url: str):
#         raise NotImplementedError("Async not supported.")
