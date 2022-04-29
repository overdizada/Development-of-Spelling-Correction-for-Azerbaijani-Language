from norvig import *
import os
arr=[]
files=os.listdir('../kitablar')
for t in files:
    arr.append('../kitablar/'+t)
print(arr)

train(arr)
