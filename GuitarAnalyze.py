import numpy as np
import matplotlib.pyplot as plt

def import_and_convert(file_name):
    # Importing the text file
    data = np.loadtxt(file_name, dtype=str)
    
    # Assuming the text file has two columns, we split the data into two numpy arrays
    column1 = data[:, 0].astype(float)  # Convert first column to float numpy array
    column2 = data[:, 1].astype(float)  # Convert second column to float numpy array

    return column1, column2

 #To use this script, un-comment the following lines and run it in a Python environment
NumData = int(input("How many data files will you enter? "))
file_name = input("Enter the name of the first text file: ")
column1, column2 = import_and_convert(file_name)
N=len(column1)
fmax=N*(1.0/column1[N-1]) #Max frequency = number of samples times inverse of the time window
Array=np.zeros((N,2*NumData))
Array[:,0]=column1
Array[:,1]=column2-(np.sum(column2)/N) #This line removes the DC average 
plt.plot(Array[:,0],Array[:,1])
for k in range(1,NumData):
    file_name = input("Enter the name of the next text file: ")
    column1, column2 = import_and_convert(file_name)
    Array[:,2*k]=column1
    Array[:,2*k+1]=column2-(np.sum(column2)/N)
    plt.plot(Array[:,2*k],Array[:,2*k+1])

plt.xlabel('Time (s)')
plt.ylabel('Microphone signal')
plt.show()
freq=np.linspace(0,fmax,N) #This line creates the frequency axis
fftArray=np.zeros((N,NumData))
for m in range (NumData):
    f1=np.fft.fft(Array[:,2*m+1])
    fftArray[:,m]=np.abs(f1)
    plt.plot(freq[0:int(N/2)],np.log(fftArray[0:int(N/2),m]))

plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()
    
