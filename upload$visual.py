import csv
import urllib.request
import codecs
from pandas.core.frame import DataFrame
dic={}
topline=0 ###top 16 samples
toprow=0 ###top 10 species
url = "https://europepmc.org/articles/PMC6143520/bin/41598_2018_32219_MOESM2_ESM.csv"
ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
for i in csvfile:
    toprow += 1
    topline=len(i)
toprow -= 1
            
def select_mouse(count,url,dic):
    url = url
    ftpstream = urllib.request.urlopen(url)
    reader = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
    ls=[]
    
    for item in reader:
        k=item[count]
        ls += [k]
       
        
    if ls[0] in dic:
        dic[ls[0]] = dic[ls[0]] + ls[1:]
    else:
        dic[ls[0]]=ls[1:]


for count in range(1,topline):
    select_mouse(count,url,dic)

###find rowname
ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
rowna=[]
value=[]
for item in csvfile:
    rowna += [item[0]]
rowname = rowna[1:]


###find colname
ftpstream = urllib.request.urlopen(url)
csvfile = csv.reader(codecs.iterdecode(ftpstream, 'utf-8'))
colna=[]
for item in csvfile:
    colna += item
    break
colname = colna[1:]

#trans to float
dict={}
for i in colname:
    dict[i]=map(float, dic[i])
        
data=DataFrame(dict)


import seaborn as sns
sns.heatmap(data, yticklabels=rowname)
#sns.heatmap(data)
