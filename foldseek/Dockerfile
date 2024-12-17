FROM jinlongru/foldseek

# Install Python and Flask
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install fastapi uvicorn

#add the python script to the container
COPY app.py  /usr/local/bin/app.py

#set working directory 
WORKDIR /usr/local/bin

EXPOSE 7001

CMD ["python", "app.py"]