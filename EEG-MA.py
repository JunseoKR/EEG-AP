# -*- coding: utf-8 -*-

# EEG Multiplex Analysis
# EEG 다중 분석

import numpy
import matplotlib
from dataclasses import dataclass

from Process import *


# EEG Data Struct
@dataclass
class Form():
    d: numpy.ndarray = ''
    f: numpy.ndarray = ''
    t: numpy.ndarray = ''
    im: matplotlib = ''
    y1: list = ''
    y2: list = ''


# Data Grouping
Grouping = 100

# Wave Range
WaveRange = "Alpha"
Initial_Hz = 8
End_Hz = 13

# WaveFiles
WAVFile = [
    "Empty",
    "S1_B1",
    "S1_B2",
    "S1_B3",
    "S2_B1",
    "S2_B2",
    "S2_B3",
    "S3_B1",
    "S3_B2",
    "S3_B3",
    "S4_B1",
    "S4_B2",
    "S4_B3",
]
WAVNUM = len(WAVFile)


# WAV Data Structure Set
for i in range(1, WAVNUM):
    globals()['WAVData_{}'.format(i)] = r'.\Wav Data\{}.wav'.format(WAVFile[i])
    globals()['S{}'.format(i)] = Form()


for n in range(1, WAVNUM):
    # .WAV Data Sampling
    eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im = Sampling_Process(eval('WAVData_'+str(n)))
    
    # FFT Process
    eval('S'+str(n)).y = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, Initial_Hz, End_Hz)

    # Data Process
    DATA_Process(eval('S'+str(n)).y, eval('S'+str(n)).t, WAVFile[n], Grouping, WaveRange)



# matplotlib Graph
plt.figure('{} Range'.format(WaveRange))
plt.xlabel('Time [s]')
plt.ylabel('{} Power'.format((WaveRange)))
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)

# Plot Section
plt.plot(S1.t, S1.y, label='S1_B1')
plt.plot(S2.t, S2.y, label='S1_B2')
plt.plot(S3.t, S3.y, label='S1_B3')
plt.plot(S4.t, S4.y, label='S2_B1')
plt.plot(S5.t, S5.y, label='S2_B2')
plt.plot(S6.t, S6.y, label='S2_B3')
plt.plot(S7.t, S7.y, label='S3_B1')
plt.plot(S8.t, S8.y, label='S3_B2')
plt.plot(S9.t, S9.y, label='S3_B3')
plt.plot(S10.t, S10.y, label='S4_B1')
plt.plot(S11.t, S11.y, label='S4_B2')
plt.plot(S12.t, S12.y, label='S4_B3')

plt.legend()
plt.show()