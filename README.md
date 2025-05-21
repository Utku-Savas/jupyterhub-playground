# JupyterHub Workspace Environment with GPU Support and Monitoring

This project sets up a **multi-user JupyterHub environment** using Docker, with GPU support for user containers, personal workspaces for each user, and integrated monitoring via **Prometheus**, **Grafana**, and **cAdvisor**.


## Getting Started

### Prerequisites

- Docker + NVIDIA Container Toolkit (for GPU support)
- Docker Compose
- An external Docker network named `jupyterhub_net` (create with `docker network create jupyterhub_net`)

### Build and Start the Environment

```bash
# 1. Ensure Docker network exists
docker network create jupyterhub_net

# 2. Build and start the containers
docker-compose up --build
```

## User Authentication

- Uses [NativeAuthenticator](https://github.com/jupyterhub/nativeauthenticator)
- **Only approved users** can log in (see `jupyterhub_config.py`)
- Admin users (e.g., `admin`) **cannot spawn notebooks**

### Default Users

```text
Approved Users: admin, test
Admin Users: admin
```

You can edit these in jupyterhub_config.py under:

```python
approved_users = {"admin", "test"}
c.Authenticator.allowed_users = approved_users
c.Authenticator.admin_users = {"admin"}
```