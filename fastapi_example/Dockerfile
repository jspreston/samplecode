# FROM alpine:3.17.1
FROM ubuntu:22.04

# env name defined in rwep_aml_conda_env.yml
ENV env_name=rwep_aml_env
ENV env_bin=/opt/miniconda/envs/${env_name}/bin
ENV env_pip=${env_bin}/pip
ENV env_pip_install="$env_pip install --no-cache-dir"
ENV env_python=${env_bin}/python

# Install conda and create environment
COPY conda_env.yml conda_env.yml
RUN apt update -y && apt upgrade -y
RUN apt-get install wget -y
RUN ["wget", "https://repo.anaconda.com/miniconda/Miniconda3-py39_22.11.1-1-Linux-x86_64.sh"]
RUN ["bash", "Miniconda3-py39_22.11.1-1-Linux-x86_64.sh", "-b", "-p", "/opt/conda"]
ENV conda=/opt/conda/bin/conda
RUN $conda update -n base -c defaults conda -y
# RUN ["bash", "-c", "$conda env create -f conda_env.yml && source activate sample_inference_env"]
# RUN python -m spacy download en_core_web_sm

# COPY main.py main.py

# ENTRYPOINT uvicorn --port $port main:app
