import os
import logging
from dockerspawner import DockerSpawner
from nativeauthenticator import NativeAuthenticator

c = get_config()


logger = logging.getLogger("jupyterhub")

class LoggingNativeAuthenticator(NativeAuthenticator):
    async def authenticate(self, handler, data):
        username = data["username"]
        ip = handler.request.remote_ip
        logger.info(f"User login attempt: {username} from IP {ip}")
        return await super().authenticate(handler, data)

c.JupyterHub.authenticator_class = LoggingNativeAuthenticator

# NativeAuthenticator setup
# c.JupyterHub.authenticator_class = NativeAuthenticator

# Block open signup
c.NativeAuthenticator.open_signup = False  # disables free-for-all signup
c.NativeAuthenticator.auto_approve = True  # auto-approve from the allowed list

# Approved users only
approved_users = {"admin", "test"}
c.Authenticator.allowed_users = approved_users
c.Authenticator.admin_users = {"admin"}

# Spawner setup
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = os.environ.get('DOCKER_JUPYTER_IMAGE', 'jupyter-user-image')
c.DockerSpawner.network_name = "jupyterhub_net"
c.DockerSpawner.extra_host_config = {"runtime": "nvidia"}
c.DockerSpawner.remove = True

c.JupyterHub.authenticate_prometheus = False
c.JupyterHub.metrics_active = True
c.JupyterHub.metrics_url = "/hub/metrics"

# Pre-spawn hook for user workspace setup
def pre_spawn_hook(spawner):
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    username = spawner.user.name.lower()


    if username in spawner.authenticator.admin_users:
        raise Exception("Admins are not allowed to start notebook servers.")

    host_workspace = f"{dir_path}/workspaces/{username.capitalize()}"
    dataset_path = f"{dir_path}/train"

    os.makedirs(host_workspace, exist_ok=True)
    os.chown(host_workspace, 1000, 100)

    spawner.volumes = {
        host_workspace: "/home/jovyan/work",
        dataset_path: {
            "bind": "/home/jovyan/dataset",
            "mode": "ro"
        }
    }

c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.pre_spawn_hook = pre_spawn_hook
c.DockerSpawner.debug = True
c.DockerSpawner.notebook_dir = "/home/jovyan/work"

# Internal networking
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080
