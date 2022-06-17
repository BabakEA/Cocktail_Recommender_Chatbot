###https://dev.to/petr7555/rasa-slots-in-detail-3e85

port=$1

if [ "$port" ];
then
	echo "port *** $port *** is going to be stoped "
else
	echo "Please Enter the port number to be killed"
	read -r port
fi


echo "the follwoing process are going to be stoped"
lsof -i :$port

kill -9 $(lsof -t -i:$port)

lsof -i :$port


