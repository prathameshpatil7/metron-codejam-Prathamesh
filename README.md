# File Monitor Application

This is a Python application that monitors a local directory for file changes and pushes information about new files to Elasticsearch. The application runs inside a Docker container and can be configured to monitor specific file types in a user-specified folder (default: `Downloads`).

## Features

- Monitors a specified folder (default: `Downloads`) for new files.
- Supports multiple file extensions (e.g., `.pdf`, `.jpg`, `.txt`).
- Pushes file information (name, path, timestamp) to Elasticsearch upon detecting new files.
- Configurable via environment variables for flexibility.

## Prerequisites

To run this application, you need:

- **Docker**: Ensure Docker and Docker Compose are installed on your machine. You can install Docker from [here](https://docs.docker.com/get-docker/).
- **Elasticsearch**: You need access to an Elasticsearch instance. You can use a hosted Elasticsearch service or run it locally. 

## Setup

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/file-monitor.git
cd file-monitor
```

### 2. Install Dependencies

Ensure Docker and Docker Compose are installed on your system. If not, follow the instructions for installation on the Docker website.

### 3. Configuration

#### Elasticsearch Configuration

In the `docker-compose.yml` file, set the following environment variables with your Elasticsearch details:

- **ELASTICSEARCH_HOST**: The URL of your Elasticsearch server (e.g., `https://your-elasticsearch-host`).
- **ELASTICSEARCH_API_KEY**: Your Elasticsearch API key for authentication.
- **ELASTICSEARCH_INDEX**: The Elasticsearch index where the data will be pushed.

You can also use a `.env` file to set these variables.

```bash
ELASTICSEARCH_HOST=https://your-elasticsearch-host
ELASTICSEARCH_API_KEY=your-api-key
ELASTICSEARCH_INDEX=your-index-name
```

#### Monitoring Folder Configuration

The application monitors a folder for new files. By default, this is set to `~/Downloads`. You can change this by setting the `DOWNLOADS_FOLDER` environment variable.

For example, you can set it via the `.env` file or directly in the `docker-compose.yml`.

##### Example `.env` file:

```
DOWNLOADS_FOLDER=/home/user/Downloads
MONITORED_EXTENSIONS=.pdf,.jpg,.jpeg,.png,.txt
```

The `MONITORED_EXTENSIONS` environment variable allows you to specify which file types to monitor (comma-separated).

#### Docker Compose Configuration

Ensure that the `docker-compose.yml` file is configured to mount your local `Downloads` folder into the container.

```yaml
version: '3.8'

services:
  file-monitor:
    build: .
    container_name: file-monitor
    environment:
      - ELASTICSEARCH_HOST=${ELASTICSEARCH_HOST}
      - ELASTICSEARCH_API_KEY=${ELASTICSEARCH_API_KEY}
      - ELASTICSEARCH_INDEX=${ELASTICSEARCH_INDEX}
      - DOWNLOADS_FOLDER=${DOWNLOADS_FOLDER}  # Path inside the container
      - MONITORED_EXTENSIONS=${MONITORED_EXTENSIONS}  # Add your desired extensions here
    volumes:
      - ${DOWNLOADS_FOLDER}:${DOWNLOADS_FOLDER}  # Mount local Downloads folder to container's /downloads
    restart: always
```

### 4. Running the Application

#### Using `.env` File

You can define all the environment variables in a `.env` file in the same directory as your `docker-compose.yml`. This will automatically load them when you run Docker Compose.

```bash
# Example of .env file
DOWNLOADS_FOLDER=/home/prathamesh/Downloads
MONITORED_EXTENSIONS=.pdf,.jpg,.jpeg,.png,.txt
```

#### Running the Docker Container

After configuring the environment variables, you can start the container by running:

```bash
docker-compose up
```

This will build the Docker image and start the application. The container will begin monitoring the `Downloads` folder for any new files with the extensions specified in `MONITORED_EXTENSIONS`.

#### Running with Custom Environment Variables

Alternatively, you can pass the environment variables directly when running the container:

```bash
DOWNLOADS_FOLDER=/home/prathamesh/Downloads MONITORED_EXTENSIONS=.pdf,.jpg,.jpeg,.png,.txt docker-compose up
```

### 5. Verifying the Application

Once the application is running, you can check the logs for output:

```bash
docker-compose logs -f
```

If the application is monitoring the correct folder, you should see logs about new files being detected and pushed to Elasticsearch.

#### Verifying Volume Mapping

To ensure the volume is properly mounted and accessible inside the container, you can execute the following command:

```bash
docker exec -it file-monitor /bin/bash
ls /downloads
```

This will list the contents of the `Downloads` folder inside the container. It should show the same files as your local `Downloads` folder.

### 6. Stopping the Application

To stop the application, simply use:

```bash
docker-compose down
```

This will stop the container and remove it from the Docker network.

## Troubleshooting

- **Permissions Issues**: Ensure that the Docker container has access to the local `Downloads` folder. Check that the user running Docker has the necessary read permissions.
- **File Not Being Detected**: Verify that the folder path (`DOWNLOADS_FOLDER`) and file extensions (`MONITORED_EXTENSIONS`) are correctly set.
- **Elasticsearch Connectivity**: Ensure that the Elasticsearch instance is running and accessible from the container. Check the `ELASTICSEARCH_HOST` and `ELASTICSEARCH_API_KEY`.
