import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Base URL for API
API_BASE_URL = "http://api:4000/api"

class APIClient:
    """Helper class for making API calls"""
    
    @staticmethod
    def get(endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make GET request to API"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {e}")
            return None
    
    @staticmethod
    def post(endpoint: str, data: Dict) -> Any:
        """Make POST request to API"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {e}")
            return None
    
    @staticmethod
    def put(endpoint: str, data: Dict) -> Any:
        """Make PUT request to API"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT request failed: {e}")
            return None
    
    @staticmethod
    def delete(endpoint: str) -> Any:
        """Make DELETE request to API"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.delete(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request failed: {e}")
            return None

# Convenience instance
api = APIClient()