#!/bin/bash
while [ true ]
do
	echo "Paused" > /tmp/picam-status
	sleep 30s
	echo "Running" > /tmp/picam-status
	python /tmp/2016PiVision/main.py > /tmp/picam-log
	c=`ps aux | grep python | grep main.py | wc -l`
	while [ c -geq 1 ]
	do
		sleep 1s
		c=`ps aux | grep python | grep main.py | wc -l`
	done
	
	echo "Ended$c" > /tmp/picam-status
done
