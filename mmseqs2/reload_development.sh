sudo docker stop mmseq_docker
sudo docker remove mmseq_docker
sudo docker build --no-cache -t mmseq_docker .
sudo docker run --name mmseq_docker --volume /mnt/databases:/app -p 8000:8000 mmseq_docker