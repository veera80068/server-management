import streamlit as st
import docker
from docker.errors import APIError, NotFound

def get_docker_client(ip, port):
    """ Connect to Docker client with given IP and port """
    try:
        client = docker.DockerClient(base_url=f'tcp://{ip}:{port}')
        client.ping()  # Test connection
        return client
    except APIError as e:
        st.error(f"Unable to connect to Docker: {e}")
        return None

def list_containers(client):
    """ List all containers """
    try:
        containers = client.containers.list()
        if containers:
            st.write("Running Containers:")
            for container in containers:
                st.write(f"Container Name: {container.name}, Status: {container.status}")
        else:
            st.write("No containers are running.")
    except APIError as e:
        st.error(f"Error listing containers: {e}")

def show_container_logs(client, container_id):
    """ Fetch and display container logs """
    try:
        container = client.containers.get(container_id)
        logs = container.logs()
        st.text_area(f"Logs for Container {container_id}:", logs.decode('utf-8'), height=300)
    except NotFound:
        st.error(f"Container {container_id} not found")
    except APIError as e:
        st.error(f"Error fetching logs: {e}")

def restart_container(client, container_id):
    """ Restart a container """
    try:
        container = client.containers.get(container_id)
        container.restart()
        st.success(f"Container {container_id} restarted successfully")
    except NotFound:
        st.error(f"Container {container_id} not found")
    except APIError as e:
        st.error(f"Error restarting container: {e}")

# Streamlit app layout
st.title('Docker Management Dashboard')

# Input fields
ip = st.text_input('Enter the EC2 IP address:')
port = st.number_input('Enter the Docker port (e.g., 2375):', min_value=1, max_value=65535)
container_id = st.text_input('Enter the Container ID (for logs or restart):')

if ip and port:
    st.write(f"Connecting to Docker at IP: {ip} and Port: {port}")
    
    # Get Docker client
    client = get_docker_client(ip, port)
    
    # List containers if client is available
    if client:
        st.header("Container List")
        list_containers(client)
        
        st.header("Container Actions")
        action = st.selectbox("Choose an action:", ["View Logs", "Restart Container"])

        if action == "View Logs" and container_id:
            show_container_logs(client, container_id)
        
        if action == "Restart Container" and container_id:
            restart_container(client, container_id)
