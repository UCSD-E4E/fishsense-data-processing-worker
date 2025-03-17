# Fishsense Data Processing Worker
This software package shall recieve and execute requests/jobs for processing data

## Setup
1. Mount appropriate remote volumes:
```
docker volume create \
   --driver local \
   --opt type=cifs \
   --opt device=//storage.lan/media-movies \
   --opt o=addr=storage.lan,vers=3.0,username=foo,password=bar,uid=1000,gid=1000 \
   media-movies
```