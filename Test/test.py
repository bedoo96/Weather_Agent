import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json

load_dotenv()

groq_api_key = os.getenv('groq_key')
class APITool:
    """General tool to fetch data from an API."""
    
    def __init__(self, name, url, method, params):
        self.name = name
        self.url = url
        self.method = method
        self.params = params
    
    def __call__(self, **kwargs):
        """Fetch data from the API."""
        try:
            for key, value in kwargs.items():
                if key in self.params:
                    self.params[key] = value
            if self.method.lower() == 'get':
                response = requests.get(self.url, params=self.params)
            else:
                response = requests.post(self.url, json=self.params)
            data = response.json()
            if response.status_code == 200:
                return {"data": data}
            else:
                return {"error": data.get("error", "Unknown error")}
        except Exception as e:
            return {"error": str(e)}

def generate_tools(api_info_list):
    tools = []
    for api_info in api_info_list:
        tool = Tool(
            name=api_info['name'],
            func=APITool(
                name=api_info['name'],
                url=api_info['url'],
                method=api_info['method'],
                params=api_info['params']
            ),
            description=f"Fetch data from {api_info['name']}"
        )
        tools.append(tool)
    return tools
