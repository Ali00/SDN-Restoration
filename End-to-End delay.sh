#!/bin/bash
#This script is used to measure the delay of path setup
# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

tcpdump -r $1 | awk '{print $1}' > temp1
tcpdump -r $2 | awk '{print $1}' > temp2

declare -a Stime
index=0
#record 1: icmp request send time
#record 2: icmp response received time
#record 3: icmp request send time after link fails
#record 4: icmp response received time after link fails
while read -r line || [[ -n "$line" ]]; do
    #echo "Text read from file: $line"
    Stime[$index]="$line"
    index=`expr $index + 1`
done < temp1

declare -a Rtime
index=0
while read -r line || [[ -n "$line" ]]; do
    #echo "Text read from file: $line"
    Rtime[$index]="$line"
    index=`expr $index + 1`
done < temp2

for ((index=0; index<${#Stime[@]}; index++)); do
   echo "Stime[$index]: ${Stime[$index]}"
done

for ((index=0; index<${#Rtime[@]}; index++)); do
   echo "Rtime[$index]: ${Rtime[$index]}"
done
