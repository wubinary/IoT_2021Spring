import os
from multiprocessing import Process

def job(wlan):
	os.system(f'python3 signals.py --wlan {wlan}')
	
if __name__ == '__main__':
	os.system('rm -rf ./save/wlan*')

	processes = []
	for wlan in ['wlan0', 'wlan1', 'wlan2']:
		p = Process(target=job, args=(wlan,))
		p.start()
		processes.append(p)

	for p in processes:
		p.join()

	#os.system('scp -P 87 -r save/wlan* aa@lab.wubinray.com:~/Desktop/hw/iot/p4/data_inference')

