# Tree Clustering Project

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/groundcover/tech_interview)

This project clusters URLs based on their patterns.

## Docker Instructions

### Build the Docker Image

To build the Docker image, run the following command in the project directory:

```sh
docker build -t url-cluster-app .       
```

### Run the Docker Container

To run the Docker container, use the following command:

```sh
docker run --rm -v $(pwd)/sample_urls.txt:/app/sample_urls.txt url-cluster-app sample_urls.txt
```

This will start the container and run the application.