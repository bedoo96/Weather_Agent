# config.py

# API information list
API_INFO_LIST = [
    {
        'name': 'weatherapi',
        'url': 'http://127.0.0.1:5000/api/weather',
        'method': 'get',
        'params': {
            'appid': '',
            'q': 'San Francisco',
            'units': 'metric'
        }
    },
    {
        'name': 'riskapi',
        'url': 'http://127.0.0.1:5000/api/risk',
        'method': 'get',
        'params': {
            'apiKey': ' ',
            'country': 'us'
        }
    }
]

# OpenAI API key
# OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
