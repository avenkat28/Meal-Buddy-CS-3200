import requests
import streamlit as st
import logging

logger = logging.getLogger(__name__)

API_BASE_URL = "http://api:4000/api"


class APIClient:

    @staticmethod
    def get(endpoint, params=None):
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {e}")
            return None

    @staticmethod
    def post(endpoint, data):
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {e}")
            return None

    @staticmethod
    def put(endpoint, data):
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT request failed: {e}")
            return None

    @staticmethod
    def delete(endpoint):
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.delete(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request failed: {e}")
            return None


def show_db_change(operation, table, details=""):
    st.info(f"Database {operation}: {table} table updated. {details}")


api = APIClient()