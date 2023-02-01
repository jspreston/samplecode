# FastAPI / Docker Example
A simple example of a FastAPI service, and a docker container to run it.

# To run the service locally:

- Build the conda environment
    ```
    conda env create -f conda_env.yml
    ```
- Start the service
    ```
    uvicorn --port 8000 main:app
    ```
- View the service documentation, visit with a browser:
    ```
    http://localhost:8000/docs
    ```

# To run the docker container

- Build the container
    ```
    ./build_docker.sh
    ```

- Run the container
    ```
    ./run_image.sh
    ```
    (note that this script also contains other useful commands for debugging (commented
    out))

- View the service documentation, visit with a browser:
    ```
    http://localhost:8080/docs
    ```
