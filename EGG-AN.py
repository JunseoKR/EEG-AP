# -*- coding: utf-8 -*-

import os

import numpy as np
from scipy import signal
import scipy.io.wavfile as waves
import matplotlib.pyplot as plt

import csv
import pandas as pd

WavFile1 = "Alpha 1"
WavFile2 = "Alpha 2"
WaveRange = "Alpha"
IF = 20
EF = 30

WavData1 = r'.\Wav Data\{}.wav'.format(WavFile1)
WavData2 = r'.\Wav Data\{}.wav'.format(WavFile2)


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

def FFT_Process(d, f, t, im, IF, EF):
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
        if f[i]>=20 and f[i]<=30:
            position_vector.append(i)


    length_d=np.shape(d)
    l_col_d=length_d[1]
    Range=[]
    for i in range(0,l_col_d):
        Range.append(np.mean(d[position_vector[0]:max(position_vector)+1,i]))

    return smoothTriangle(Range, 100)

plt.figure('{}Range'.format(WaveRange))
y1 = FFT_Process(d1, f1, t1, im1)
y2 = FFT_Process(d2, f2, t2, im2)
plt.plot(t1, y1, t2, y2)
plt.xlabel('Time [s]')
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)
plt.show()