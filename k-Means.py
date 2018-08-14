import numpy as np
import random as rn
import matplotlib.pyplot as plt    

fileTrain = np.genfromtxt('Trainset.txt')
fileTest = np.genfromtxt('Testset.txt')
k = int(input("input k: "))
cluster = []
train = []
test = []

#generate data train
for i in range(0,len(fileTrain)):
    train.append([fileTrain[i][0],fileTrain[i][1]])
    
#generate data test
for i in range(0,len(fileTest)):
    test.append([fileTest[i][0],fileTest[i][1]])

#function for generate centroid
def generateCentroid():
    indeks = rn.sample(range(0,len(train)),k)
    for i in range(0,k):
        cluster.append([train[indeks[i]][0],train[indeks[i]][1],i]) 

#function for count the euclidean distance
def euclide(a10, a11, a20, a21):
    return np.sqrt((a10-a20)**2 + (a11-a21)**2)

#function for clustering the data
def clustering(cluster, data):
    hasil = []
    similar = []
    for i in range(0,len(data)):
        for j in range(0,len(cluster)):
            jarak = euclide(cluster[j][0],cluster[j][1],data[i][0],data[i][1])
            similar.append([jarak,cluster[j][2]])
        similar.sort()
        hasil.append([data[i][0],data[i][1],similar[0][1]])
        similar.clear()
    return(hasil)

#function for check the different before and after clustering
def differentCek(data1,data2):
    cek = 0
    for i in range(0,len(data1)):
        if cek == 0:
            if data1[i][2] == data2[i][2]:
                cek = 0
            else:
                cek = 1
    return cek

#function for generate new centroid
def generateNewCentroid(data):
    newCentroid = []
    x = []
    y = []
    for i in range(0,len(cluster)):
        for j in range(0,len(data)):
            if data[j][2] == i:
                x.append(data[j][0])
                y.append(data[j][1])
        newCentroid.append([np.mean(x),np.mean(y),i])
        x.clear()
        y.clear()
    return newCentroid
    
#k-means process start from here, use 
generateCentroid()
cek = 0
centroid = cluster
dataTrain = train
resultCluster1 = []
resultCluster2 = []
while cek == 0:
    resultCluster1 = clustering(centroid,dataTrain)
    centroid = generateNewCentroid(resultCluster1)
    resultCluster2 = clustering(centroid,dataTrain)
    diffCek = differentCek(resultCluster1,resultCluster2)
    if diffCek == 0:
        sumSse = 0.0
        for i in range(0,len(centroid)):
            for j in range(0,len(resultCluster2)):
                if centroid[i][2] == resultCluster2[j][2]:#count the SSE
                    sumSse += euclide(centroid[i][0],centroid[i][1],resultCluster2[j][0],resultCluster2[j][1])
        print('K : ',k,' sse : ',sumSse)
        cek = 1
    else:
        cek = 0

x = []
y = []
z = []
xc = []
yc = []
zc = []
for i in range(0,len(train)):
    x.append(resultCluster2[i][0])
    y.append(resultCluster2[i][1])
    z.append(resultCluster2[i][2])
for i in range(0,len(centroid)):
    xc.append(centroid[i][0])
    yc.append(centroid[i][1])
    zc.append(centroid[i][2])

plt.plot(x, y, 'ro', color='powderblue')
plt.plot(xc, yc, 'bs', color='black')
plt.show()

#try it on test set
ClusterTest = clustering(cluster,test)
file = open('result.txt','w+')#generate the result file to txt (result.txt)
for item in ClusterTest:
    file.write('%s\n' % item)
file.close

