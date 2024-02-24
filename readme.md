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