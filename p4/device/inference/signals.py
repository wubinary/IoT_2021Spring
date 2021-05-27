import os, sys, time
import argparse
import pickle
import pandas as pd

from wifi import Cell, Scheme

# parser x,y,z,wlan
parser = argparse.ArgumentParser()
parser.add_argument('--x', type=float, default=-1.0)
parser.add_argument('--y', type=float, default=-1.0)
parser.add_argument('--z', type=float, default=-1.0)
parser.add_argument('--wlan', type=str, default='wlan0')
parser.add_argument('--stime', type=float, default=20.0)

args = parser.parse_args()
args.mac_list_path = f'./save/mac_list.pkl'
args.save_path = f'./save/{args.wlan.strip()}/'
args.log_path = f'./save/{args.wlan.strip()}/x_{args.x}_y_{args.y}_z_{args.z}_log.csv'

print(args)


####################################################
#################### mac_list ######################

with open(args.mac_list_path, 'rb') as fp:
	mac_list = pickle.load(fp)

#print(mac_list)
#input()

####################################################
############# init log.csv if not exit #############

os.system(f'mkdir -p {args.save_path}')

def create_clean_log_file():
	if os.path.exists(args.log_path):
		return 
	data = {'x':[], 'y':[], 'z':[], 'timestamp':[]}
	data.update({mac:[] for mac in mac_list})	
	
	df = pd.DataFrame(data=data)
	df.to_csv(args.log_path, index=False)

create_clean_log_file()


####################################################
################# collect signals ##################

logs = [] 

start_time = time.time()
while True:
	os.system(f'sudo iwlist {args.wlan} scan')
	cell = Cell.all(f'{args.wlan}')
	
	row = {'x':args.x, 'y':args.y, 'z':args.z, 'timestamp':time.time()}
	
	for AP_SSID in cell:
		address = AP_SSID.address
		signal = AP_SSID.signal
		
		if address in mac_list:
			row[address] = signal
		
	logs.append(row)

	stop_time = time.time()
	if ( (stop_time-start_time) > args.stime ):
		break


###################################################
################## write back #####################

df = pd.read_csv(args.log_path)
for row in logs:
	df = df.append(row, ignore_index=True)
df.to_csv(args.log_path, index=False)

print(f'\t[Info] x:{args.x} y:{args.y} z:{args.z}, sample {len(logs)} fingerprints ')

