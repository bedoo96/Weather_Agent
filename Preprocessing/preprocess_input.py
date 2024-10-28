from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()  # Call load_dotenv to load the environment variables

groq_api_key = os.getenv("grop_key")

class ContextRefiner:
    def __init__(self) -> None:
        self.template = """
        Given the user's input: "{user_input}", perform the following tasks:
        1. Identify the key actions and intentions of the user.
        2. Rephrase the input to create a clearer and more understandable prompt for retrieval purposes but dispay only Rephrased Prompt.

        Example:
        Input: "Ce matin je dois aller au marché, mais je ne sais pas encore quoi acheter pour cuisiner ce matin."
        Output: "This morning, I need to go to the market, but I don't know what to buy for cooking today. Can you suggest some items or recipes for breakfast?"

        User Input: "{user_input}"
        Rephrased Prompt: """
    
        # self.llm_agent = 'llama3-8b-8192'  # 'llama3-70b-8192'
        self.prompt = PromptTemplate(template=self.template, input_variables=["user_input"])
        # self.groq_chat = ChatGroq(
        #     groq_api_key=groq_api_key,
        #     model_name=self.llm_agent,
        #     # verbose=False,
            
        #     # #self.llm_agent,
        #     # temperature=0
        # )
        self.llm = Ollama(base_url="http://localhost:11434", model="llama3", verbose=False, temperature=0)
        # self.groq_chat = self.llm
        self.query_chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def refine_context(self, user_input: str) -> str:
        output = self.query_chain.run(user_input=user_input)
        
    
        rephrased_prompt = ""
        if "Rephrased Prompt:" in output:
            # Split the output at "Rephrased Prompt:" and take the part after it
            parts = output.split("Rephrased Prompt:")
            if len(parts) > 1:
                rephrased_prompt = parts[1].strip()
        else:
            rephrased_prompt = output.strip()

        if rephrased_prompt.endswith("This rephrased prompt is clearer and more understandable, and it provides a specific context for retrieval purposes."):
            rephrased_prompt = rephrased_prompt.rsplit("This rephrased prompt is clearer and more understandable, and it provides a specific context for retrieval purposes.", 1)[0].strip()
        
        return rephrased_prompt

if __name__ == "__main__":
    user_input = "Give me an analysis information for 18 july 2024 about weather in Saint Francisco "
    #Example 1"propose a new approach from all you knows about Ai agent using RAG, langchain for this system"
    refiner = ContextRefiner()
    refined_prompt1 = refiner.refine_context(user_input)
    print(refined_prompt1)
