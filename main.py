import streamlit as st
import docker
from docker.errors import APIError

def get_docker_client(ip, port):
    try:
        client = docker.DockerClient(base_url=f'tcp://{ip}:{port}')
        client.ping()
        return client
    except APIError as e:
        st.error(f"Unable to connect to Docker: {e}")
        return None

def list_containers(client):
    try:
        containers = client.containers.list()
        if containers:
            for container in containers:
                st.write(f"Container Name: {container.name}, Status: {container.status}")
        else:
            st.write("No containers are running.")
    except APIError as e:
        st.error(f"Error listing containers: {e}")

# Streamlit app layout
st.title('Docker Container Viewer')

# Input fields
client_id = st.selectbox('Select Client:', ['client1', 'client2'])  # Add more options as needed

# Define IP addresses and ports for each client
client_details = {
    'client1': {'ip': '44.203.138.165', 'port': '2376'},
    'client2': {'ip': '3.88.234.141', 'port': '2375'},
    # Add more clients as needed
}

if client_id:
    ip = client_details[client_id]['ip']
    port = client_details[client_id]['port']
    st.write(f"Connecting to Docker at IP: {ip} and Port: {port}")
    
    # Get Docker client
    client = get_docker_client(ip, port)
    
    # List containers if client is available
    if client:
        list_containers(client)
