import requests
from langchain_core.tools import Tool

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
            # Update parameters with additional kwargs
            for key, value in kwargs.items():
                if key in self.params:
                    self.params[key] = value
            
            # Perform the API request
            if self.method.lower() == 'get':
                response = requests.get(self.url, params=self.params)
            else:
                response = requests.post(self.url, json=self.params)
            
            # Check if the request was successful
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx and 5xx)
            
            # Attempt to parse JSON
            data = response.json()
            return {"data": data}
        
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.RequestException as err:
            return {"error": f"Error occurred: {err}"}
        except ValueError as json_err:
            return {"error": f"JSON decode error: {json_err}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}


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
