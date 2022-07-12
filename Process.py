# -*- coding: utf-8 -*-

import os

import numpy as np
from scipy import signal
import scipy.io.wavfile as waves
import matplotlib.pyplot as plt

import csv
import pandas as pd



# .WAV Data Sampling
def Sampling_Process(WAVData):
    # WavData Sampling
    def Wave_Process(WD):
        def Sampling(PD):
            length_data=np.shape(PD)
            length_new=length_data[0]*0.05
            ld_int=int(length_new)

            # scipy 데이터 resample
            return signal.resample(PD, ld_int)

        Fs, Data = waves.read(WD)
        return Sampling(Data)

    return plt.specgram(Wave_Process(WAVData), NFFT= 256, Fs=500, noverlap=250)



# FFT Process
def FFT_Process(d, f, t, im, Inf, Enf):
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



# Data CSV Process
def DATA_Process(y, t, WavFile, Grouping, WaveRange):
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