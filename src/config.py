import os 
from dotenv import load_dotenv 

load_dotenv()
def get_api_key():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")
    return api_key

def get_max_concurrent_requests():
    max_concurrent_requests = os.environ.get("MAX_CONCURRENT_REQUESTS")
    if not max_concurrent_requests:
        raise ValueError("MAX_CONCURRENT_REQUESTS environment variable not set")
    return int(max_concurrent_requests)