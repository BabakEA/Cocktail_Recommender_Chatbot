 
#rasa shell &
rasa run actions &
#rasa run actions -p 9990 -vv >> ./actionServer.log 2>&1 &
rasa run -m models --enable-api --cors "*" -p 9009 &
#rasa run -m models --enable-api --cors "*" &

#python -m http.server 9008&





