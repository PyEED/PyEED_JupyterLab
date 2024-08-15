# Base image for mmseqs2
FROM soedinglab/mmseqs2:latest

# Install FastAPI and uvicorn
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install fastapi uvicorn

# Copy the FastAPI app to the container
COPY fastapi_server.py /app/fastapi_server.py

# Expose the port on which FastAPI will run
EXPOSE 8000

# Start the FastAPI server when the container starts
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
