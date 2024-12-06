sudo docker stop blast
sudo docker remove blast
sudo docker build --no-cache -t blast_image .
sudo docker run --name blast --volume /mnt/databases:/blast/blastdb -p 6001:6001 blast_image