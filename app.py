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
ip = st.text_input('Enter the EC2 IP address:')
port = st.text_input('Enter the Docker port (e.g., 2375):')

if ip and port:
    st.write(f"Connecting to Docker at IP: {ip} and Port: {port}")
    
    # Get Docker client
    client = get_docker_client(ip, port)
    
    # List containers if client is available
    if client:
        list_containers(client)
