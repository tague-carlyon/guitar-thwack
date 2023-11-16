import sys
import numpy
import matplotlib.pyplot as plt

ReadFile = input("Enter file Name: ")
print(type(ReadFile))
print(ReadFile)

DataArr = numpy.loadtxt(ReadFile)
#print(DataArr[:,1])
#print(DataArr)
DataTot = 0.0
time = 0.0

j = len(DataArr)

#DataArr = numpy.empty(shape=(j,2))

for i in range(j):
    time = DataArr[i,0]
#    print(time)
    DataTemp = DataArr[i,1]
#    print(DataTemp)
    DataTot = DataTemp + DataTot

#print(DataArr)

DataAdjust = DataTot / j

for k in range(j):
    DataArr[k,1] = DataArr[k,1] - DataAdjust

#print(DataArr)

SaveFile = input('Enter save file name: ')
SFile = open(SaveFile, 'w')

for l in range(j):
    SFile.write(str(DataArr[l,0])+' '+str(DataArr[l,1]))

Farr =numpy.fft.fft(DataArr[:,1])
plt.plot(DataArr[:,0],numpy.abs(Farr))
plt.show()
