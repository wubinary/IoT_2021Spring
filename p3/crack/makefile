mac=F0:2F:74:E3:D0:18
crack:
	aircrack-ng -a2 -b $(mac) -w $(dic) $(file)
base:
	hashcat -m 2500 -o base_result.txt $(file) $(dic)
base-show:
	hashcat -m 2500 --show $(file) $(dic)
convert:
	./hashcat-utils/src/cap2hccapx.bin $(file).cap $(file).hccapx	
pmk-convert:
	hcxpcapngtool -o $(file).22000 $(file).cap
pmk-hash:
	hashcat -m 22000 -o pmk_result.txt $(file) $(dic)
pmk-show:
	hashcat -m 22000 --show $(file) $(dic)
pmk:
	hcxpcapngtool -o $(file).22000 $(file).pcapng
	hashcat -m 22000 -o pmk-result.txt $(file).22000 $(dic)
show:
	cat ~/.hashcat/hashcat.potfile
