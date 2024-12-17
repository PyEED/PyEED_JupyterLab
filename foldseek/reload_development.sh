sudo docker stop foldseek_docker
sudo docker remove foldseek_docker
sudo docker build --no-cache -t foldseek_docker .
sudo docker run -it --name foldseek_docker -p 7001:7001 foldseek_docker