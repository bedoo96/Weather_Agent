from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.tools import Tool
from langchain_groq import ChatGroq
from API.api_conf import API_INFO_LIST
from Test.tools.tool import generate_tools
from Preprocessing.preprocess_input import ContextRefiner
import os
from dotenv import load_dotenv
import json

load_dotenv()

def build_langchain_agent():
    # Initialize the LLM (Groq's GPT model)
    llm = ChatGroq(api_key="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", model_name="llama3-groq-70b-8192-tool-use-preview")
    
    # Generate tools from the API_INFO_LIST
    tools = generate_tools(API_INFO_LIST)

    # Define the main conversation prompt
    main_prompt_template = PromptTemplate(
        template="""
            You are an AI assistant with access to various tools.
            Based on the user's question, analyze which tool(s) to use.
            Generate the final response for the user based on the tools' outputs.
User: {user_prompt}
Assistant:""",
        input_variables=["user_prompt"]
    )
    
    # Define the tool selection prompt
    tool_choice_prompt_template = PromptTemplate(
        template="""
            You are a tool-using assistant with access to the following tools: {tool_names}.
            Based on the user's prompt, decide which tool to use, and output only the tool name.
User: {user_prompt}
Assistant:""",
        input_variables=["user_prompt", "tool_names"]
    )
    
    # Define conversation and tool choice chains
    conversation_chain = LLMChain(llm=llm, prompt=main_prompt_template)
    tool_choice_chain = LLMChain(llm=llm, prompt=tool_choice_prompt_template)
    
    return conversation_chain, tool_choice_chain, tools

def run_conversation(user_prompt):
    conversation_chain, tool_choice_chain, tools = build_langchain_agent()
    
    # Step 1: Choose the tool based on the user's prompt
    tool_names = ', '.join([tool.name for tool in tools])
    tool_choice_response = tool_choice_chain.run({"user_prompt": user_prompt, "tool_names": tool_names})
    chosen_tool_name = tool_choice_response.strip().lower()

    # Debugging step: Print chosen tool name to verify
    # print(f"Chosen tool: {chosen_tool_name}")
    
    # Step 2: Find the chosen tool in the tools list
    chosen_tool = next((tool for tool in tools if tool.name.lower() == chosen_tool_name), None)
    
    if not chosen_tool:
        return "Outil invalide"  # Return if no tool matches

    # Step 3: Extract required parameters based on the tool's expected input
    tool_params = {}
    for param in chosen_tool.func.params.keys():
        # Simple parsing logic to retrieve param values from the prompt
        if param in user_prompt:
            tool_params[param] = user_prompt.split(param)[-1].split()[0]
    
    # Debugging: Print extracted parameters
    # print(f"Extracted Parameters: {tool_params}")
    
    # Step 4: Execute the chosen tool with the extracted parameters
    try:
        result = chosen_tool.func(**tool_params)
        # print(f"Tool Result: {result}")
    except Exception as e:
        return f"Erreur lors de l'appel de l'outil : {e}"

    # Step 5: Prepare the LLM response based on tool result
    result_data = json.dumps(result)  # Convert tool result to JSON
    prompt_for_llm = f"Here are the results from the selected tool: {result_data}. Generate a readable response for the user."
    
    # Debugging: Print prompt for LLM response generation
    # print(f"Prompt for LLM: {prompt_for_llm}")

    # Step 6: Generate the final response with the conversation chain
    final_response = conversation_chain.run({"user_prompt": prompt_for_llm})
    
    return final_response

# Example usage with a complex user prompt
refiner = ContextRefiner()
user_prompt_complex = "comment est la temperature a San Francisco for the last month"
refined_prompt = refiner.refine_context(user_prompt_complex)
print("Complex Operation Response:", run_conversation(refined_prompt))
