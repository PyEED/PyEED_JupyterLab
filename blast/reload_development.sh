sudo docker stop blast_docker
sudo docker remove blast_docker
sudo docker build --no-cache -t blast_docker .
sudo docker run --name blast_docker --volume /mnt/databases:/blast/blastdb -p 6001:6001 blast_docker