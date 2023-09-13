

from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import uvicorn

app = FastAPI()

# Create blob client
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_client = blob_service_client.get_container_client(
    os.getenv("AZURE_STORAGE_CONTAINER")
)


@app.get("/")
def read_root():
    return {"message": "Connected to Azure Blob Storage!"}

def print_hello():
    print("Hello, world!")

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b!=0:
        return a / b
    else:
        return "division by zero is not allowed"

@app.get("/read_blob/{blob_name}")
async def read_blob(blob_name: str):
    blob_client = container_client.get_blob_client(blob_name)

    if not blob_client.exists():
        return {"error": "Blob not found"}

    data = blob_client.download_blob().readall()

    return {"blob_name": blob_name, "data": data}


def calculate_area_of_rectangle(a, b):
    return a * b

def calculate_area_of_circle(radius):
    from math import pi
    return pi * radius ** 2

def greet_person(name):
    return f"Hello, {name}!"


@app.post("/upload_blob")
async def upload_blob(file):
    blob_client = container_client.get_blob_client(file.filename)

    try:
        data = await file.read()
        blob_client.upload_blob(data)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

