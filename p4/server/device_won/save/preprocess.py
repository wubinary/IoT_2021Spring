import os
import csv
import pandas as pd
import math

wlan0_path = './wlan0'
wlan1_path = './wlan1'
wlan2_path = './wlan2'

wlan0 = os.listdir(wlan0_path)
wlan1 = os.listdir(wlan1_path)
wlan2 = os.listdir(wlan2_path)
'''
for i, j, k in zip(wlan0, wlan1, wlan2):   # 找wlan2缺少哪個檔案
    if i==j and i==k and j==k:
        print('OK')
    else:
        print(i)
        print(j)
        print(k)
        break
'''
for i in range(len(wlan0)):
    wlan0[i] = './wlan0/' + wlan0[i]  # 89*?*136
for i in range(len(wlan1)):
    wlan1[i] = './wlan1/' + wlan1[i]  # 89*?*136
for i in range(len(wlan2)):
    wlan2[i] = './wlan2/' + wlan2[i]  # 88*?*136

# 此檔案似乎有問題 先拿掉 (5.98, 2.13, 1.01)
print(wlan0.pop(60))
print(wlan1.pop(60))




wlan012 = []
for i in range(len(wlan0)):
    a = pd.read_csv(wlan0[i])
    b = pd.read_csv(wlan1[i])
    c = pd.read_csv(wlan2[i])
    if 'y_2.13' in wlan0[i]:   # y=2.13的檔案內部都誤植為2.74，將他改回來
        a.loc[:, 'y'] = 2.13
        b.loc[:, 'y'] = 2.13
        c.loc[:, 'y'] = 2.13
    t = pd.concat([a, b, c], keys=['wlan0', 'wlan1', 'wlan2'], names=['name', 'sample'])
    wlan012.append(t)
data = pd.concat(wlan012)
#data.to_csv('./wlan012/data.csv')
print(data)




nanumber = data.count(axis='rows')
n = []
for i in range(len(nanumber)):
    if nanumber[i] > len(data)*0.8:
        n.append(i)
data1 = data.iloc[:, n]
#data1.to_csv('./wlan012/data1.csv')
print(data1)




data2 = data1.fillna(0)
#data2.to_csv('./wlan012/data2.csv')
print(data2)

