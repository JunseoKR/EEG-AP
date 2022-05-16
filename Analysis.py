# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
from scipy import signal
import csv
import pandas as pd



# ---------------------------------------------------------------------
# EEG Set
Wave = {
    'Delta' : {
        'Range' : {
            'Initial': 0,
            'End' : 4
        }
    },
    'Theta' : {
        'Range' : {
            'Initial': 4,
            'End' : 8
        }
    },
    'Alpha' : {
        'Range' : {
            'Initial': 8,
            'End' : 12
        }
    },
    'Beta' : {
        'Range' : {
            'Initial': 20,
            'End' : 30
        }
        # SMR : 12Hz ~ 15Hz
        # Mid-Beta : 15Hz ~ 20Hz
        # High-Beta : 20Hz ~ 30Hz
    },
    'Gamma' : {
        'Range' : {
            'Initial': 38,
            'End' : 45
        }
    }
}



# ---------------------------------------------------------------------
# Data Input

WavFile = input("Wav File (With Filename Extension) : ")
print("\n[ Wave Range ]\n\n[ Delta ]\n0 Hz ~ 4 Hz ( 1.3 Hz )\n\n[ Theta ]\n4 Hz ~ 8 Hz ( 6.3 Hz )\n\n[ Alpha ]\n8 Hz ~ 12 Hz ( 10.3 Hz )\n\n[ Beta ]\nSMR : 12 Hz ~ 15 Hz\nMid-Beta : 15 Hz ~ 18 Hz \nHigh-Beta : 20 Hz ~ 30 Hz\n\n[ Gamma ]\n38 Hz ~ 45 Hz ( 40 Hz )\n")
Initial = int(input("Initial Range : "))
End = int(input("End Range : "))

if Initial in range(0, 5):
    WaveRange = "Delta"
elif Initial in range(4, 9):
    WaveRange = "Theta"
elif Initial in range(8, 13):
    WaveRange = "Alpha"
elif Initial in range(12, 31):
    WaveRange = "Beta"
elif Initial in range(38, 46):
    WaveRange = "Gamma"
else:
    WaveRange = ""
print("\nWav File : {}\nWave : {}\nWave Range : {} Hz ~ {} Hz".format(WavFile, WaveRange ,Initial, End))

# ---------------------------------------------------------------------
# EEG Main Set

# 파일 불러오기
file = r'.\Wav Data\{}'.format(WavFile)
# scipy.io.wavefile 모듈
fs, data = waves.read(file)


# numpy 차원 재배열
length_data=np.shape(data)
length_new=length_data[0]*0.05
ld_int=int(length_new)


# scipy 데이터 resample
data_new=signal.resample(data, ld_int)


# Matplot 그래프 생성
plt.figure('Spectrogram')
d, f, t, im = plt.specgram(data_new, NFFT= 256, Fs=500, noverlap=250)
plt.ylim(0,90)
plt.colorbar(label= "Power/Frequency")
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.show()





# ---------------------------------------------------------------------
# Alpha / Beta Range Check

# Frequencies CSV 생성
matrixf=np.array(f).T
np.savetxt('Frequencies.csv', matrixf)
df = pd.read_csv("Frequencies.csv", header=None, index_col=None)
df.columns = ["Frequencies"]
df.to_csv("Frequencies.csv", index=False)


# 파형 주파수 선택
position_vector=[]
length_f=np.shape(f)
l_row_f=length_f[0]
for i in range(0, l_row_f):
    if f[i]>=Initial and f[i]<=End:
        position_vector.append(i)


length_d=np.shape(d)
l_col_d=length_d[1]
Range=[]
for i in range(0,l_col_d):
    Range.append(np.mean(d[position_vector[0]:max(position_vector)+1,i]))


# Savitzky-Golay 노이즈 제거
def smoothTriangle(data, degree):
    triangle=np.concatenate((np.arange(degree + 1), np.arange(degree)[::-1])) # up then down
    smoothed=[]

    for i in range(degree, len(data) - degree * 2):
        point=data[i:i + len(triangle)] * triangle
        smoothed.append(np.sum(point)/np.sum(triangle))
    # Handle boundaries
    smoothed=[smoothed[0]]*int(degree + degree/2) + smoothed
    while len(smoothed) < len(data):
        smoothed.append(smoothed[-1])
    return smoothed


# Matplot 그래프 생성
plt.figure('{}Range'.format(WaveRange))
y=smoothTriangle(Range, 100)
plt.plot(t, y)
plt.xlabel('Time [s]')
plt.xlim(0,max(t))
plt.show()


datosy=np.asarray(y)
print(datosy)
datosyt=np.array(
        [
        datosy,
        t
        ])
with open ('WaveData.csv', 'w', newline='') as file:
    writer=csv.writer(file, dialect='excel-tab')
    writer.writerows(datosyt.T)


# CSV 헤더 생성
df = pd.read_csv("WaveData.csv", header=None, index_col=None)
df.columns = ["Power                   Time"]
df.to_csv("WaveData.csv", index=False)





# ---------------------------------------------------------------------
# Eyes Closed / Eyes Open

tg=np.array([4.2552,14.9426, 23.2801,36.0951, 45.4738,59.3751, 72.0337,85.0831, max(t)+1])

length_t=np.shape(t)
l_row_t=length_t[0]
eyesclosed=[]
eyesopen=[]
j=0  #initial variable to traverse tg
l=0  #initial variable to loop through the "y" data
for i in range(0, l_row_t):
    if t[i]>=tg[j]:
        
        if j%2==0:
            eyesopen.append(np.mean(datosy[l:i]))
        if j%2==1:
            eyesclosed.append(np.mean(datosy[l:i]))
        l=i
        j=j+1

        
plt.figure('DataAnalysis')
plt.boxplot([eyesopen, eyesclosed], sym = 'ko', whis = 1.5)
plt.xticks([1,2], ['Eyes open', 'Eyes closed'], size = 'small', color = 'k')
plt.ylabel('AlphaPower')
#plt.show()

meanopen=np.mean(eyesopen)
meanclosed=np.mean(eyesclosed)
sdopen=np.std(eyesopen)
sdclosed=np.std(eyesclosed)
eyes=np.array([eyesopen, eyesclosed])

from scipy import stats
result=stats.ttest_ind(eyesopen, eyesclosed, equal_var = False)
#print(result)