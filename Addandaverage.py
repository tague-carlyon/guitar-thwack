import sys
import numpy
import matplotlib.pyplot as plt

ReadFile = input("Enter file Name: ")
print(type(ReadFile))
print(ReadFile)

DataArr = numpy.loadtxt(f"C:\\Reserch Test\{ReadFile}")
print(DataArr[:,1])
print(DataArr)
DataTot = 0.0
time = 0.0

j = len(DataArr)

DataArr = numpy.empty(shape=(j,2))

for i in range(j):
    time = DataArr[i,0]
    print(time)
    DataTemp = DataArr[i,1]
    print(DataTemp)
    DataTot = DataTemp + DataTot

print(DataArr)

DataAdjust = DataTot / j

for k in range(j):
    DataArr[k,1] = DataArr[k,1] - DataAdjust

print(DataArr)

plt.plot(DataArr[:,0],DataArr[:,1])
plt.show()