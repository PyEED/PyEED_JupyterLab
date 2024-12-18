sudo docker stop foldseek
sudo docker remove foldseek
sudo docker build --no-cache -t foldseek_image .
sudo docker run -it --name foldseek -p 7001:7001 foldseek_image