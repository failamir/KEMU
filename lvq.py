# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 22:05:22 2018

@author: USER
"""
import numpy as np
import csv
import time

#dataClass = [[[1.0,1.0,0.0,0.0],0],[[0.0,0.0,0.0,1.0],1]]
#dataTraining = [[[0.0,0.0,1.0,1.0],1],[[1.0,0.0,0.0,0.0],0],[[0.0,1.0,1.0,0.0],1]]

alpha = 0.1
start_time = time.time()

def read_csv(file_name):
    array_2D = []
    with open(file_name, 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=';')
        for row in read:
            array_2D.append(row)
    return array_2D

def featureSelection(listFeatures):
    res = np.transpose(listFeatures)
    result = []    
    #eliminated = [4,5,14,15,24,25,26,34,35] # Relief 
    #eliminated = [1,2,9,10,11,12,19,20,21,22,29,30,31,32,39,40,41,42,44,45,46,48,49] # Korelasi
    #eliminated = [1,2,3,5,6,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,43,46,47,48,49,50,51,52] # CFS
    eliminated = [] # Tanpa Seleksi
    for i in range(len(res)):
        if ((i+1) not in eliminated):
            resJ = []
            for j in range(len(res[i])):
                resJ.append(res[i][j])
            result.append(resJ)
    return np.transpose(result).tolist()

def getPCAFeatures(listFeatures):    
    res = listFeatures
    result = []    
    for i in range(len(res)):
        fiturPCA = []
        fiturPCA.append((0.209*res[i][13])+(0.209*res[i][12])+(0.208*res[i][32])+(0.208*res[i][33])+(0.208*res[i][17]))
        fiturPCA.append((-0.293*res[i][11])-(0.293*res[i][10])-(0.293*res[i][30])-(0.293*res[i][31])-(0.292*res[i][21]))
        fiturPCA.append((-0.301*res[i][5])-(0.301*res[i][4])-(0.299*res[i][25])-(0.299*res[i][24])-(0.297*res[i][34]))
        fiturPCA.append((-0.386*res[i][47])-(0.385*res[i][45])-(0.352*res[i][49])-(0.352*res[i][43])-(0.345*res[i][51]))
        fiturPCA.append((0.348*res[i][18])+(0.345*res[i][28])+(0.344*res[i][8])+(0.341*res[i][38])-(0.264*res[i][40]))
        fiturPCA.append((0.391*res[i][39])+(0.37*res[i][19])+(0.369*res[i][9])+(0.366*res[i][29])-(0.283*res[i][8]))
        fiturPCA.append((-0.41*res[i][41])-(0.393*res[i][46])+(0.373*res[i][51])-(0.349*res[i][43])-(0.34*res[i][40]))
        fiturPCA.append((0.607*res[i][40])-(0.53*res[i][42])+(0.22*res[i][45])+(0.212*res[i][47])-(0.208*res[i][43]))
        result.append(fiturPCA)
    return result

data1 = read_csv('data/pengujian134/dataTrain134.csv') # Data Training
data2 = read_csv('data/pengujian134/dataClass134.csv') # Data Class (Vector Reference)
data3 = read_csv('data/pengujian134/dataTest134.csv') # Data Testing
'''
data1 = read_csv('data/dataTrainAll50.csv') # Data Training
data2 = read_csv('data/dataClassAllTL.csv') # Data Class (Vector Reference)
data3 = read_csv('data/dataTestAll50.csv') # Data Testing

data1 = read_csv('datatraining.csv') # Data Training
data2 = read_csv('refvector.csv') # Data Class (Vector Reference)
data3 = read_csv('datatesting.csv') # Data Testing
'''
dataTrain = ((np.array(data1[:]))[:,1:-1]).astype(np.float64).tolist()

dataC = ((np.array(data2[:]))[:,1:-1]).astype(np.float64).tolist()
dataT = ((np.array(data3[:]))[:,1:-1]).astype(np.float64).tolist()
classDataTrain = ((np.array(data1[:]))[:,-1:]).astype(int).tolist()
classDataClass = ((np.array(data2[:]))[:,-1:]).astype(int).tolist()
classDataTest = ((np.array(data3[:]))[:,-1:]).astype(int).tolist()
dataTraining = []
dataClass = []

dataC = getPCAFeatures(dataC)
dataTrain = getPCAFeatures(dataTrain)
dataT = getPCAFeatures(dataT)

'''
dataC = featureSelection(dataC)
dataTrain = featureSelection(dataTrain)
dataT = featureSelection(dataT)
'''

dataTesting = []
ignoredClass = [] # eliminated Class
#ignoredClass = [8,22,23,25,27,29]

for i in range(len(dataTrain)):
    if (classDataTrain[i][0] not in ignoredClass):
        dataArray = []
        dataArray.append(dataTrain[i])
        dataArray.append(classDataTrain[i][0])
        dataTraining.append(dataArray)

for i in range(len(dataC)):
    if (classDataClass[i][0] not in ignoredClass):
        dataArray2 = []
        dataArray2.append(dataC[i])
        dataArray2.append(classDataClass[i][0])
        dataClass.append(dataArray2)
        #dataTesting.append(dataT[i])
for i in range(len(dataT)):
    dataTesting.append(dataT[i])
    


# Initialize Weight Matrix
weightMatrix = np.zeros((len(dataClass),len(dataTraining[0][0])),dtype=np.float64)
#weightMatrix = np.zeros((len(dataClass),len(dataTraining[0][0])),dtype=np.float64)
for i in range(len(weightMatrix)):
    #print(len(weightMatrix))
    for j in range(len(dataTraining[i][0])):
        weightMatrix[i][j] = dataClass[i][0][j]

jmlUpdate = 0
# ITERATION LVQ
iterasi = 1
for x in range(iterasi):
    
    # Find Euclidean Distance
    jarak = np.zeros(len(dataClass),dtype=np.float64)
    for i in range(len(dataTraining)):
        #print(weightMatrix)
        for j in range(len(dataClass)):
            jarak[j] = 0
            for k in range(len(dataTraining[i][0])):
                jarak[j] += np.power(dataTraining[i][0][k] - weightMatrix[j][k],2)
            jarak[j] = np.sqrt(jarak[j])
        
        #print(jarak)
    
               
        winnerClass = -1
        minValue = 999999
        for k in range(len(jarak)):
            if(jarak[k] < minValue):
                minValue = jarak[k]
                winnerClass = k 
                
        
        #print(minValue)
        #print(winnerClass)
    
        for j in range(len(weightMatrix)):
            #print(winnerClass)
            for k in range(len(weightMatrix[j])):
                #print(j,winnerClass)
                if (j == winnerClass):
                    jmlUpdate+=1
                    #print(j,dataTraining[i][1])
                    if(j == dataTraining[i][1]):
                        
                        #print(weightMatrix[j][k],"Masuk")
                        #weightMatrix[j][k] = (1-alpha)*weightMatrix[j][k] + alpha*dataTraining[i][0][k]
                        weightMatrix[j][k] = weightMatrix[j][k] + alpha*(weightMatrix[j][k] - dataTraining[i][0][k])
                    else:                        
                        #weightMatrix[j][k] = (1+alpha)*weightMatrix[j][k] - alpha*dataTraining[i][0][k]
                        weightMatrix[j][k] = weightMatrix[j][k] - alpha*(weightMatrix[j][k] - dataTraining[i][0][k])
    alpha = 0.1*alpha
   
# Testing
#dataTest = [0.0,0.0,1.0,1.0]
wrongClass = 0
with open('data/hasil134/testingResultPCALVQ1.csv', 'a') as myfile:
    wr = csv.writer(myfile, delimiter=',')
    for z in range(len(dataTesting)):
        testing = classDataTest[z][0]-1
        dataTest = dataTesting[testing]
        
        classResult = -1
        minValue = 999999999    
        for i in range(len(weightMatrix)):
            sumValue = 0
            for j in range(len(weightMatrix[i])):
                sumValue += np.power(dataTesting[z][j] - weightMatrix[i][j],2)
            if (sumValue < minValue):
                minValue = sumValue
                classResult = i
        result = [testing,classResult]
        wr.writerow(result)
        if (testing != classResult):
            print('Real Class   = '+str(testing)+' -> Class Result = '+str(classResult)+' -> Min Value = '+str(minValue))
            wrongClass+=1
print('Akurasi   = '+str(np.divide(float(len(dataTesting) - wrongClass),float(len(dataTesting)))))


print(jmlUpdate)
print(time.time()-start_time)