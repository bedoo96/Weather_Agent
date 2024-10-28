from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
from Configuration.config import groq_api_key
from langchain import HuggingFaceHub

load_dotenv()
#groq_api_key = os.getenv('groq_key')

class Model:
           
        def llama3(self):
                llm = Ollama(base_url=" ",model="llama3.1")
                return llm
        
        def Groq_llama(self):
             model = ChatGroq(
                  api_key=groq_api_key, model_name="llama3-groq-70b-8192-tool-use-preview"
             )
             return model

        def TAIDE(self):
            llm = Ollama(base_url="",model="TAIDE-LX-7B-Chat")
            return llm
             

        def Mistral(self):
            llm_mistral = Ollama(base_url="http://localhost:11434",
                                 model="mistral",
                                #  temperature=1.0,
                                #  verbose=True
                                 )
            return llm_mistral
             

        def Gemma(self):
            llm = Ollama(base_url="",model="gemma2")
            return llm
