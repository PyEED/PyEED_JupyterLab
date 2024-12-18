FROM jinlongru/foldseek

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install FastAPI and Uvicorn
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install fastapi uvicorn

# Copy the Python application
COPY app.py /usr/local/bin/app.py

# Set the working directory
WORKDIR /usr/local/bin

# Ensure the virtual environment is activated in the CMD
ENV PATH="/opt/venv/bin:$PATH"

#Expose the port the server will run on
EXPOSE 7001

#Run the python server script
CMD ["python3", "app.py"]