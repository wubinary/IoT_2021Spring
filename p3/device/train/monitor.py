import os 
import glob
import pandas as pd 

wlans = glob.glob('./save/wlan*')

for wlan in wlans:
	os.system(f'ls {wlan} | wc -l')

