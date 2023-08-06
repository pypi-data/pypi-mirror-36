# dst-server-deploy
A Python package for generating server files for use with [Don't Starve Together Docker Imags](https://github.com/fairplay-zone/docker-dontstarvetogether).

The image requires docker engine to be installed on the host system. This script requires pyYAML to be installed (to generate the docker-compose.yml file) and docker-compose (to run the docker-compose.yml file).

This script is indended to be run in the directory in which you want to store the server data to generate most generic servers. If you need to tune the server after generation, look at https://github.com/fairplay-zone/docker-dontstarvetogether/blob/develop/docs/configuration.md for reference.

# Installation
```console
pip install dst-server-deploy
```

# Running
```console
dst-server-deploy
```

# Known Issues / Notes
* BE AWARE: This will overwrite any docker-compose.yml file you have in a directory.
* This assumes assume you are only running one cluster on your machine. If you are running clusters, you will need to adjust the ports accordingly.
* This is just intended to help generate a moderate amount of server framework to aid users who are new to docker or this image. It is not meant to address all use cases.


