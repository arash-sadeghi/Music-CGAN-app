## info
- tempos will change to 100 even if it was different at beggining. but it can be changed by changing tempo variable in constants. 
- generated drum track for the same bass track is very similar. this could be sign of overfitting. but its different than original drum track
- docker build -t flask-app .
- docker run -p 3000:3000 flask-app 
- heroku container:push web --app drummer-companion
- docker inspect --format='{{.Size}}' flask-app-no-torch