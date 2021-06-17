
PASSWD=raspberry
CH=0
ESSID=assistant_5

enable_monitor_mode:
	echo ${PASSWD} | sudo -S airmon-ng check
	echo ${PASSWD} | sudo -S airmon-ng start wlan1

listen:
	echo ${PASSWD} | sudo -S airodump-ng wlan1mon

listen_ch:
	echo ${PASSWD} | sudo -S airodump-ng -c ${CH} wlan1mon

fake_pkg:
	echo ${PASSWD} | sudo -S aireplay-ng -9 -e ${ESSID} wlan1mon
	

