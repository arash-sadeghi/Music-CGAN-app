## TODO:
- play with buffer size
- code quits after a time window ends. you need to recall again and make windows overlap. each added note should carry previous notes with itself (to a certain time)
- drummer will always generate drum for previous track. How to make a catch up dynamic.
 

## How to run locally
- these instructions are for Macos operating system.
- first go ahead and istall docker from this website: https://docs.docker.com/desktop/install/mac-install/
- once docker is installed, open a terminal and copy and paste these commands:
```
docker pull arashsadeghi/drummer-companion:1.0.0
docker run -p 3000:3000 -d arashsadeghi/drummer-companion:1.0.0
```
- now go ahead to your browser and go to this address
```
http://127.0.0.1:3000
```
you should be able to see the app running.
- whenver you want the app to stop running, go to the same terminal that you started the app and pres ```Command + C```. This will stop the app from running

## info
- tempos will change to 100 even if it was different at beggining. but it can be changed by changing tempo variable in constants. 
- generated drum track for the same bass track is very similar. this could be sign of overfitting. but its different than original drum track
- docker build -t flask-app .
- docker run -p 3000:3000 flask-app 
- heroku container:push web --app drummer-companion
- docker inspect --format='{{.Size}}' flask-app-no-torch
- Azure website: drummer-companion-wa.azurewebsites.net

### Docker hub commands:
-  docker build -t drummercompanion .  
-  docker tag drummercompanion arashsadeghi/drummer-companion:latest
- docker login   
- docker push arashsadeghi/drummer-companion:latest   

### Azure commands:
-  docker build -t drummercompanion.azurecr.io/drummercompanion  .
-  docker push drummercompanion.azurecr.io/drummercompanion
- update docker image on azure: [link](https://stackoverflow.com/questions/57241655/switch-docker-image-in-azure-appservice)
### progress
- 'Transformer assigns velocity successfully. Now integration part should be done. models weights too big for adding to git'
- modifying CGAN to only output drum midi. The whole app will work as such. no more returning bass
- CGAN might be clipping the end of songs. must be checked
- __pycahce__ was geeting copied to docker. that was consuming space and throwing low disk space warning
    - /usr/local/lib/python3.11/site-packages/huggingface_hub/file_download.py:1006: UserWarning: Not enough free disk space to download the file. The expected file size is: 0.00 MB. The target location /root/.cache/huggingface/hub only has 0.00 MB free disk space.

