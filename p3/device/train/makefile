X=-1.0
Y=-1.0
Z=-1.0
WLAN=wlan0

#####################################################
####################  Scripts  ######################

main:

search_ssids:
	#python3 search_ssids.py --wlan wlan0
	#python3 search_ssids.py --wlan wlan1
	#python3 search_ssids.py --wlan wlan2 

get_signals:
	python3 signals.py --x ${X} --y ${Y} --z ${Z} --wlan wlan0
	python3 signals.py --x ${X} --y ${Y} --z ${Z} --wlan wlan1
	python3 signals.py --x ${X} --y ${Y} --z ${Z} --wlan wlan2
	#python3 signals.py --x ${X} --y ${Y} --z ${Z} --wlan ${WLAN}

monitor:
	watch -n 0.5 python3 monitor.py

