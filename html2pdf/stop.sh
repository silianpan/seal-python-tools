#!/bin/bash

pid=$(ps -ef | grep html2pdf | grep -v grep | awk '{print $2}');

echo "----- start -----"

for id in $pid
do

kill 9 $id
echo "kill pid $id"

done

echo "------ end ------"
