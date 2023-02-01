# FROM alpine:3.17.1
FROM ubuntu:22.04

ENV port=8000
ENV conda=/opt/conda/bin/conda

# Install conda and create environment
COPY conda_env.yml conda_env.yml
RUN apt update -y && apt upgrade -y
RUN apt-get install wget -y
RUN ["wget", "https://repo.anaconda.com/miniconda/Miniconda3-py39_22.11.1-1-Linux-x86_64.sh"]
RUN ["bash", "Miniconda3-py39_22.11.1-1-Linux-x86_64.sh", "-b", "-p", "/opt/conda"]
RUN $conda update -n base -c defaults conda -y
RUN $conda env create -f conda_env.yml
SHELL ["/opt/conda/bin/conda", "run", "--no-capture-output", "-n", "sample_inference_env", "/bin/bash", "-c"]
RUN python -m spacy download en_core_web_sm

COPY main.py main.py

ENTRYPOINT uvicorn --port $port --host 0.0.0.0 main:app
