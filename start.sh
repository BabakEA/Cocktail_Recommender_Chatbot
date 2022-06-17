bash kill_port.sh 5005
bash kill_port.sh 5021
bash kill_port.sh 9009
bash kill_port.sh 5055
bash kill_port.sh 9990

echo "ports have cleared"
echo "starting the process...."

clear


$nohup bash Widget.sh &
