X=-1.0
Y=-1.0
Z=-1.0
WLAN=wlan0
POS=0

#####################################################
####################  Scripts  ######################

get_parallel_signals:
	python3 parallel_signals.py 
	scp -P 87 -r save/wlan* aa@lab.wubinray.com:~/Desktop/hw/iot/p4/data_inference
	
	#wait
	#cp -r save/ pos${POS} 
	#wait
	#scp -P 87 -r pos${POS}/wlan* aa@lab.wubinray.com:~/Desktop/hw/iot/p4/data_inference

scp:
	scp -P 87 -r pos${POS}/wlan* aa@lab.wubinray.com:~/Desktop/hw/iot/p4/data_inference


