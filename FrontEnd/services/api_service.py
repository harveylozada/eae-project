import os
import requests
import base64

BASE_URL = os.getenv("BASE_URL", "http://backend:8000/api")

# Crear la cabecera de autenticación manualmente
AUTH_HEADER = {
    "Authorization": "Basic " + base64.b64encode("admin:admin123".encode()).decode()
}

# Finalidad del archivo
# Realizar peticiones HTTP al backend para obtener información o enviar datos

def get_clients():
    response = requests.get(f"{BASE_URL}/clientes", headers=AUTH_HEADER)
    return response.json()

def create_client(client_data):    
    response = requests.post(f"{BASE_URL}/clientes", json=client_data, headers=AUTH_HEADER)    
    return response.json()

def update_client(client_id, client_data):
    response = requests.put(f"{BASE_URL}/clientes/{client_id}", json=client_data, headers=AUTH_HEADER)
    return response.json()

def delete_client(client_id):
    response = requests.delete(f"{BASE_URL}/clientes/{client_id}", headers=AUTH_HEADER)
    return response.json()

def get_analytics_summary():
    response = requests.get(f"{BASE_URL}/analytics/summary", headers=AUTH_HEADER)
    return response.json()
