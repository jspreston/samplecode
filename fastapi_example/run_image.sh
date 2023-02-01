#!/bin/sh
# Useful commands for debugging / running the container

# Command for starting a container from an image:
# docker run --name spacy -d -i -t jopresto/spacy:0.0.1 /bin/sh
# Command for creating an interactive shell in the running container:
# docker exec -it spacy bash
# Command to remove a running container:
# docker rm -f spacy
# Get logs from running (or failed) container:
# docker logs spacy

# Command to actually start the full container.  This gives the service a name
# ('spacy'), and binds the service (running on port 8000 of the container) to port 8080
# of the loopback adapter for the host.
docker run --name spacy -d -p 127.0.0.1:8080:8000 jopresto/spacy:0.0.1
