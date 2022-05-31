# -*- coding: utf-8 -*-

import os

import numpy as np
from scipy import signal
import scipy.io.wavfile as waves
import matplotlib.pyplot as plt

import csv
import pandas as pd



# ---------------------------------------------------------------------
# EEG
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
WavFile = input("Wav File (Without Filename Extension) : ")
print("\n[ Wave Range ]\n\n[ Delta ]\n0 Hz ~ 4 Hz ( 1.3 Hz )\n\n[ Theta ]\n4 Hz ~ 8 Hz ( 6.3 Hz )\n\n[ Alpha ]\n8 Hz ~ 12 Hz ( 10.3 Hz )\n\n[ Beta ]\nSMR : 12 Hz ~ 15 Hz\nMid-Beta : 15 Hz ~ 18 Hz \nHigh-Beta : 20 Hz ~ 30 Hz\n\n[ Gamma ]\n38 Hz ~ 45 Hz ( 40 Hz )\n")
Initial = int(input("Initial Range : "))
End = int(input("End Range : "))
Grouping = int(input("Grouping : "))

if Initial in range(0, 4):
    WaveRange = "Delta"
elif Initial in range(4, 8):
    WaveRange = "Theta"
elif Initial in range(8, 12):
    WaveRange = "Alpha"
elif Initial in range(12, 30):
    WaveRange = "Beta"
elif Initial in range(38, 45):
    WaveRange = "Gamma"
else:
    WaveRange = ""
print("\nWav File : {}\nWave : {}\nWave Range : {} Hz ~ {} Hz\nGrouping : {}".format(WavFile, WaveRange ,Initial, End, Grouping))
# ---------------------------------------------------------------------
# EEG Main Set


# File Read
file = r'.\Wav Data\{}.wav'.format(WavFile)
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
    if f[i]>=8 and f[i]<=12:
        position_vector.append(i)


length_d=np.shape(d)
l_col_d=length_d[1]
Range=[]
for i in range(0,l_col_d):
    Range.append(np.mean(d[position_vector[0]:max(position_vector)+1,i]))
os.remove("Frequencies.csv")


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
plt.ylim(0, 2000)
plt.show()


datosy=np.asarray(y)
datosyt=np.array(
        [
        datosy,
        t
        ])


SpssData = []
Group = []
Power = []
Time = []
df = pd.DataFrame(SpssData)


# Grouping
index = 1
for range_ in range(1, int((len(datosyt[0])+Grouping*2)/Grouping)):
    for group_ in range(1, Grouping+1):
        if len(Group) == len(datosyt[0]):
            break
        Group.append('{}'.format(index))
    index += 1


# DataFrame
for line_ in range(0, len(datosyt[0])):
    Power.append('{}'.format(datosyt[0][line_]))
    Time.append('{}'.format(datosyt[1][line_]))


df['Group'] = Group
df['Power'] = Power
df['Time'] = Time


# DataFrame To CSV
df.to_csv("[ {} ] {}.csv".format(WavFile, WaveRange), index=False)