# -*- coding: utf-8 -*-

import os

import numpy as np
from scipy import signal
import scipy.io.wavfile as waves
import matplotlib.pyplot as plt

import csv
import pandas as pd


# Set
global WavFile1
global WavFile2
global WaveRange
global Inf
global Enf
global Grouping

# =============================================================================
WavFile1 = input("Wav File (Without Filename Extension)\nFirst : ")
WavFile2 = input("Second : ")
print("\n[ Wave Range ]\n\n[ Delta ]\n0 Hz ~ 4 Hz ( 1.3 Hz )\n\n[ Theta ]\n4 Hz ~ 8 Hz ( 6.3 Hz )\n\n[ Alpha ]\n8 Hz ~ 12 Hz ( 10.3 Hz )\n\n[ Beta ]\nSMR : 12 Hz ~ 15 Hz\nMid-Beta : 15 Hz ~ 18 Hz \nHigh-Beta : 20 Hz ~ 30 Hz\n\n[ Gamma ]\n38 Hz ~ 45 Hz ( 40 Hz )\n")
Inf = int(input("Initial Range : "))
Enf = int(input("End Range : "))
Grouping = int(input("Grouping : "))

if Inf in range(0, 4):
    WaveRange = "Delta"
elif Inf in range(4, 8):
    WaveRange = "Theta"
elif Inf in range(8, 12):
    WaveRange = "Alpha"
elif Inf in range(12, 30):
    WaveRange = "Beta"
elif Inf in range(38, 45):
    WaveRange = "Gamma"
else:
    WaveRange = ""
print("\nWav File 1 : {}\nWave File 2 : {}\nWave : {}\nWave Range : {} Hz ~ {} Hz\nGrouping : {}".format(WavFile1, WavFile2, WaveRange ,Inf, Enf, Grouping))
# =============================================================================


# WavFile Read
WavData1 = r'.\Wav Data\{}.wav'.format(WavFile1)
WavData2 = r'.\Wav Data\{}.wav'.format(WavFile2)


# WavData Process
def Wave_Process(WData):
    fs, data = waves.read(WData)

    def NP_Precess(RD):
        length_data=np.shape(RD)
        length_new=length_data[0]*0.05
        ld_int=int(length_new)

        # scipy 데이터 resample
        return signal.resample(RD, ld_int)

    return NP_Precess(data)


d1, f1, t1, im1 = plt.specgram(Wave_Process(WavData1), NFFT= 256, Fs=500, noverlap=250)
d2, f2, t2, im2 = plt.specgram(Wave_Process(WavData2), NFFT= 256, Fs=500, noverlap=250)


# FFT Process
def FFT_Process(d, f, t, im):
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
        if f[i]>=Inf and f[i]<=Enf:
            position_vector.append(i)


    length_d=np.shape(d)
    l_col_d=length_d[1]
    Range=[]
    for i in range(0,l_col_d):
        Range.append(np.mean(d[position_vector[0]:max(position_vector)+1,i]))
    os.remove("Frequencies.csv")

    return smoothTriangle(Range, 100)


# EEG Data Process
def EEG_Process(y, t, WavFile):
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


# Matplotlib EEG Graph
plt.figure('{}Range'.format(WaveRange))
y1 = FFT_Process(d1, f1, t1, im1)
y2 = FFT_Process(d2, f2, t2, im2)
plt.plot(t1, y1, t2, y2)
plt.xlabel('Time [s]')
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)
plt.show()


EEG_Process(y1, t1, WavFile1)
EEG_Process(y2, t2, WavFile2)