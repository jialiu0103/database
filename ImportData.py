import csv
#csvFile = open("species.csv", "r")
#reader = csv.reader(csvFile)
dic={}
k=17

def select_mouse(count,csv_name,dic):
    csvFile = open(csv_name, "r")
    reader = csv.reader(csvFile)
    ls=[]
    for item in reader:
        k=item[count]
        ls += [k]
        #print(ls)
    if ls[0] in dic:
        dic[ls[0]] = dic[ls[0]] + ls[1:]
    else:
        dic[ls[0]]=ls[1:]
        
for count in range(1,k):
    select_mouse(count,'phylum.csv',dic)
#species_len=len(dic['LZX10C'])
#print(species_len)

for count in range(1,k):
    select_mouse(count,'class.csv',dic)
#genus_len=len(dic['LZX10C'])-species_len
#print(genus_len)

for count in range(1,k):
    select_mouse(count,'order.csv',dic)
#family_len=len(dic['LZX10C'])-genus_len-species_len
#print(family_len)

for count in range(1,k):
    select_mouse(count,'family.csv',dic)
#order_len=len(dic['LZX10C'])-family_len-genus_len-species_len
#print(order_len)

for count in range(1,k):
    select_mouse(count,'genus.csv',dic)
#class_len=len(dic['LZX10C'])-order_len-family_len-genus_len-species_len
#print(class_len)

for count in range(1,k):
    select_mouse(count,'species.csv',dic)
#phylum_len=len(dic['LZX10C'])-class_len-order_len-family_len-genus_len-species_len
#print(phylum_len)

print(len(dic['LZX10C']))
print(dic.keys())
#print(dic['LZX10C'])




import pandas as pd
import numpy as np
data=np.random.randn(86*16,3)




value=[]
ordermouse=['LZX1C', 'LZX2C', 'LZX3C', 'LZX4C', 'LZX5C', 'LZX6C', 'LZX7C', 'LZX8C','LZX9C','LZX10C', 'LZX11C', 'LZX12C','LZX13C', 'LZX14C', 'LZX15C', 'LZX16C']
for i in ordermouse:
    for j in dic[i]:
        value.append(float(j))
print(len(value))




my_mouse=[]
for i in range(1,17):
    my_mouse.append([i]*len(dic['LZX10C']))
mouse=[]
for i in my_mouse:
    for j in i:
        mouse.append(j)
        
        
        
ti=[]
for i in range(1,len(dic['LZX10C'])+1):
    ti.append(i)
    
tid=ti*len(dic)





import pandas as pd
df=pd.DataFrame({'mid':mouse,'tid':tid, 'value':value})
df.to_csv("abundance.csv",index=False,sep=',')
