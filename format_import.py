import csv
dic={}
topline=17 ###top 16 samples
toprow=10 ###top 10 species
def select_mouse(count,csv_name,dic):
    csvFile = open(csv_name, "r")
    reader = csv.reader(csvFile)
    ls=[]
    
    for item in reader:
        k=item[count]
        ls += [k]
       
        
    if ls[0] in dic:
        dic[ls[0]] = dic[ls[0]] + ls[1:]
    else:
        dic[ls[0]]=ls[1:]


for count in range(1,topline):
    select_mouse(count,'phylum.csv',dic)
    
    
###find rowname
csvFile = open('phylum.csv', "r")
reader = csv.reader(csvFile)
rowna=[]
value=[]
for item in reader:
    rowna += [item[0]]
rowname = rowna[1:]


###find colname
csvFile = open('phylum.csv', "r")
reader = csv.reader(csvFile)
colna=[]
for item in reader:
    colna += item
    break
colname = colna[1:]


###find value
for i in colname:
    for j in dic[i]:
        value.append(float(j))
        
        
        
        
my_mouse=[]
for i in range(1,topline):
    my_mouse.append([i]*toprow)
    
### find mid
mouse=[]
for i in my_mouse:
    for j in i:
        mouse.append(j)

        
### find top tid
ti=[]
for i in range(1,toprow+2):
    ti.append(i)
    
tid=ti*len(dic)



import pandas as pd
df=pd.DataFrame({'mid':mouse,'tid':tid, 'value':value})
df.to_csv("abundance.csv",index=False,sep=',')



import pandas as pd
df2=pd.DataFrame({'tid':ti,'name':rowname})
df2.to_csv("taxonomic.csv",index=False,sep=',')
