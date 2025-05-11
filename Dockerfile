FROM jupyterhub/jupyterhub:5.3

RUN pip install \
    dockerspawner \
    jupyterhub-dummyauthenticator \
    jupyterhub-firstuseauthenticator \
    jupyterhub-nativeauthenticator \
    jupyterlab

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
