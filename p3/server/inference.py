import numpy as np
import pandas as pd
import pickle
import copy


#################################################
##################  mac list  ###################

with open('./ckpt/dataset.pkl', 'rb') as fp:
    dic = pickle.load(fp)
    mac_list = dic['mac_list']
print('len mac_list:', len(mac_list))


#################################################
##############  read training data  #############

data_srcs = ['./data_inference/']

# read training data
wlan_dfs_test = []
for wlan in ['wlan0', 'wlan1', 'wlan2']:
    df_cat = None
    for data_src in data_srcs:
        df = pd.read_csv(f'{data_src}/{wlan.strip()}/x_-1.0_y_-1.0_z_-1.0_log.csv')
        df_cat = df if df is None else pd.concat([df_cat, df])
    wlan_dfs_test.append(df_cat)

#################################################
##############  data preprocessing  #############

# 取 exp : y = e^(-x/80)
normalized_wlan_dfs_test = []
for wlan_df in wlan_dfs_test:
    sel_indexs = list(wlan_df.columns)[4:]
    wlan_df = wlan_df.copy()
    wlan_df[sel_indexs] = (-wlan_df[sel_indexs]/80)#.apply(np.exp)
    normalized_wlan_dfs_test.append(wlan_df)

# # find clean mac list
    
# make clean mac df
normalized_cleaned_wlan_dfs_test = []
for i in range(3):
    wlan_df = normalized_wlan_dfs_test[i]    
    selec_col = ['x','y','z','timestamp'] + mac_list
    df = pd.DataFrame(data={col:wlan_df[col] if col in wlan_df.columns else [np.nan] * len(wlan_df) for col in selec_col})
    normalized_cleaned_wlan_dfs_test.append(df)

# fill nan to 0
for i in range(3):
    normalized_cleaned_wlan_dfs_test[i] = normalized_cleaned_wlan_dfs_test[i].fillna(0)
    
[len(normalized_cleaned_wlan_dfs_test[i].columns) for i in range(3)]



###################################################################
########################   Wlan0,1,2並起來   #######################

X_test, Y_test = [], []

# 5*5*5
for idx1, row1 in normalized_cleaned_wlan_dfs_test[0].iterrows():
    x1 = row1.values[0]
    y1 = row1.values[1]
    signals1 = row1.values[4:]
    for idx2, row2 in normalized_cleaned_wlan_dfs_test[1].iterrows():
        x2 = row2.values[0]
        y2 = row2.values[1]
        signals2 = row2.values[4:]
        if x2!=x1 or y2!=y1:
            continue
        else:
            for idx3, row3 in normalized_cleaned_wlan_dfs_test[2].iterrows():
                x3 = row3.values[0]
                y3 = row3.values[1]
                signals3 = row3.values[4:]
                if x3!=x2 or y3!=y2:
                    continue
                else:
                    X_test.append(np.concatenate([signals1,signals2,signals3]))
                    Y_test.append([x1,y1])

#                     normalized_cleaned_wlan_dfs_test[2].drop(idx3, inplace=True)
#                     break
#             normalized_cleaned_wlan_dfs_test[1].drop(idx2, inplace=True)
#             break

X_test, Y_test = np.stack(X_test), np.stack(Y_test)

print('Shape: ', X_test.shape, Y_test.shape)



###################################################################
############################   Model   ############################

import torch 
import torch.nn as nn

class Model(nn.Module):
    def __init__(self, in_dim, hid_dim=64, out_dim=2):
        super().__init__()
        self.mlp = nn.Sequential(
            #nn.Dropout(0.5),
            nn.Linear(in_dim, hid_dim, bias=True),
            nn.Tanh(),
            nn.BatchNorm1d(hid_dim),
            
#             nn.Dropout(0.5),
            nn.Linear(hid_dim, hid_dim, bias=True),
            nn.Tanh(),
            nn.BatchNorm1d(hid_dim),
            
            nn.Dropout(0.5),
            nn.Linear(hid_dim, hid_dim, bias=True),
            nn.Tanh(),
            nn.BatchNorm1d(hid_dim),
                        
            nn.Dropout(0.5),
            nn.Linear(hid_dim, out_dim, bias=True)
        )
        
    def forward(self, x):
        x = self.mlp(x)
        return x
    
    
from torch.utils.data import TensorDataset, DataLoader

model = Model(in_dim=X_test.shape[1])
model.load_state_dict(torch.load('./ckpt/best.pt', map_location='cpu')['model'])
model.cuda()
model.eval()


test_dataset = TensorDataset(torch.tensor(X_test), torch.tensor(Y_test))

test_loader = DataLoader(test_dataset,
                          batch_size=256)

mse, n = 0, 0
pred, answ = [], []
for x, y_ in test_loader:
    y = model(x.cuda().float())
    
    pred.append(y.cpu().detach())
    answ.append(y_.cpu().detach())

pred = torch.cat(pred)
answ = torch.cat(answ)
    
pred_aug = []
answ_aug = []
x,y = 0,0
tmp = []
for i in range(len(answ)):
    x_, y_ = answ[i]
    if x==x_ and y==y_:
        tmp.append(pred[i])
    else:
        if len(tmp)!=0:
            pred_aug.append(torch.stack(tmp).mean(axis=0))
            answ_aug.append(ans)
        tmp = [pred[i]]
        ans = answ[i]
        x, y = x_, y_
pred_aug.append(torch.stack(tmp).mean(axis=0))
answ_aug.append(ans)
        
pred_aug = torch.stack(pred_aug)
answ_aug = torch.stack(answ_aug)

print('len pred_aug:',len(pred_aug), 'pred:', len(pred))

for i in range(len(answ_aug)):
    print(pred_aug[i].numpy(), answ_aug[i].numpy())
