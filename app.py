import os
import time
import json
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Elasticsearch configuration from environment variables
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'https://default_host.com')  # Default if not provided
ELASTICSEARCH_API_KEY = os.getenv('ELASTICSEARCH_API_KEY', '')  # Replace with your API key if needed
ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'metron-codejam-2025')

# Folder to monitor from environment variable or default to Downloads
DOWNLOADS_FOLDER = os.getenv('DOWNLOADS_FOLDER', '/downloads')  # Default folder

# List of file extensions to monitor
MONITORED_EXTENSIONS = os.getenv('MONITORED_EXTENSIONS', '.pdf,.jpg,.jpeg,.png,.txt').split(',')

# Function to push alert to Elasticsearch using POST request
def push_to_elasticsearch(file_path):
    url = f"{ELASTICSEARCH_HOST}/{ELASTICSEARCH_INDEX}/_doc/"
    headers = {
        "Authorization": f"ApiKey {ELASTICSEARCH_API_KEY}",
        "Content-Type": "application/json"
    }

    document = {
        "file_name": f"Prathamesh_Patil_{os.path.basename(file_path)}",
        "file_path": f"Prathamesh_Patil_{file_path}",
        # "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    
    try:
        response = requests.post(url, headers=headers, json=document)
        if response.status_code == 201:
            print(f"Document indexed successfully: {response.json()}")
        else:
            print(f"Error indexing document: {response.text}")
    except Exception as e:
        print(f"Error making request: {e}")

# Custom event handler for file system changes
class DownloadEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_extension = os.path.splitext(event.src_path)[1]
            if file_extension in MONITORED_EXTENSIONS:
                print(f"File detected: {event.src_path}")
                push_to_elasticsearch(event.src_path)

# Function to start monitoring the Downloads folder
def start_monitoring():
    print(f"Monitoring folder: {DOWNLOADS_FOLDER}")
    print(f"Monitored extensions: {', '.join(MONITORED_EXTENSIONS)}")

    event_handler = DownloadEventHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    start_monitoring()
