from langchain.prompts import PromptTemplate

class PromptUpgrade:
        def __init__(self) -> None:
                
            self.prompt_template = """
                You are an agent with access to a toolbox containing
                various tools. Given a user query, analyze it to determine 
                the most appropriate tool(s) to use. If a single tool is insufficient,
                select additional tools to provide a comprehensive answer.
                Generate and deliver the final response based on your analysis.
                # user query: {query}
                # Agent:
                """
            prompt = PromptTemplate(
                input_variables=["query","chat_history"],
                template=self.prompt_template
            )

            #    # prompt template for choosing tools
            self.tool_choice_prompt_template = PromptTemplate(
                template="""You are an assistant with access to the following tools: {tool_names}. 
                            Based on the user prompt, determine which tool(s) to use. If multiple tools are needed, choose all that apply.
                            User: {user_prompt}
                            Previous conversation:
                            
                            Assistant: """,
                input_variables=["user_prompt", "tool_names","chat_history"]
            )

            self.extract_params_prompt_template = PromptTemplate(
            template="""Based on the user prompt and the chosen tool, extract the necessary parameters to call the API.
                        Tool: {tool_name}
                        User: {user_prompt}
                        Provide the parameters in JSON format.
                        Parameters: """,
            input_variables=["user_prompt", "tool_name","chat_history"]
        )
            
            # prompt template for generating the final response
            self.final_response_prompt_template = PromptTemplate(
            template="""The following tools were used to gather information: {tool_names}. 
                        Here are the results: {results}. 
                        Generate a human-readable response based on the results.
                        Previous conversation:
                        {chat_history}
                        User: {user_prompt}
                        Assistant: """,
            input_variables=["context"]  # Now expecting a single input key 'context',
        # input_variables=["tool_names", "results", "user_prompt"]
    )
        







    # You are an assistant that can fetch data from various APIs.
    # Use the appropriate tool to perform the requested operations and provide the results.
    # if __name__ == "__main__":
    #     # Create an instance of PromptUpgrade
    #     prompt_upgrade = PromptUpgrade()
    #     # Get the prompt template from the instance
    #     prompt = prompt_upgrade.prompt
    #     # Print an example prompt formatted with a query
    #     query='Are there flying cars?'
    #     llm_agent = 'llama3-8b-8192' #'llama3-70b-8192'

    #     def groq_agent():
    #         groq_chat = ChatGroq(
    #             groq_api_key = groq_api_key,
    #             model_name = llm_agent,
                
    #         )
    #         return groq_chat
    # query_chain = LLMChain(prompt=prompt, llm = groq_agent())
    # print(query_chain(query))