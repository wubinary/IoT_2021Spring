import os, sys
import time
import pickle
import argparse
import pandas as pd 

from wifi import Cell, Scheme

# parser
parser = argparse.ArgumentParser()
parser.add_argument('--wlan', type=str, default='wlan0')
args = parser.parse_args()
print(args)

#########################################################
#################### search wifi ########################

ssids = set()
ssid_info = {}

start_time = time.time()
while True:
	os.system(f'sudo iwlist {args.wlan} scan')
	cell = Cell.all(f'{args.wlan}')
	for AP_SSID in cell:
		ssids.add(AP_SSID.ssid)
		ssid_info[AP_SSID.ssid] = {
				'address': AP_SSID.address,
				'frequency': AP_SSID.frequency,
				'channel': AP_SSID.channel
			}
	stop_time = time.time()
	if ( (stop_time - start_time) > 20):
		break

ssids = list(ssids)


#######################################################
#################### write back #######################

df = pd.DataFrame(data={
	'ssid': ssids,
	'address': [ssid_info[ssid]['address'] for ssid in ssids],
	'frequency': [ssid_info[ssid]['frequency'] for ssid in ssids],
	'channel': [ssid_info[ssid]['channel'] for ssid in ssids],
})

if not os.path.exists('./save/wifi_df.csv'):
	df.to_csv('./save/wifi_df.csv', index=False)
	df_big = df
else:
	df_old = pd.read_csv('./save/wifi_df.csv')
	df_big = pd.concat([df_old, df], axis=0, ignore_index=True)
	df_big.to_csv('./save/wifi_df.csv', index=False)

mac_list = sorted(list(set(df_big['address'].tolist())))
with open('./save/mac_list.pkl', 'wb') as fp:
	pickle.dump(mac_list, fp)
with open('./save/mac_list.txt', 'w') as fp:
	for mac in mac_list:
		fp.write(mac+'\n')

print(mac_list)


