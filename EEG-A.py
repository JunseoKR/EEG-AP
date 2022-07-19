# -*- coding: utf-8 -*-

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
WaveRange1 = "Delta"
WaveRange2 = "Theta"
R1_Initial_Hz = 0.2
R1_End_Hz = 4
R2_Initial_Hz = 4
R2_End_Hz = 8

# WaveFiles
WAVFile = [
    "Empty",
    "S3_A1",
    "S3_B1"
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
    eval('S'+str(n)).y1 = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, R1_Initial_Hz, R1_End_Hz)
    eval('S'+str(n)).y2 = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, R2_Initial_Hz, R2_End_Hz)

    # Data Process
    DATA_Process(eval('S'+str(n)).y1, eval('S'+str(n)).t, WAVFile[n], Grouping, WaveRange1)
    DATA_Process(eval('S'+str(n)).y2, eval('S'+str(n)).t, WAVFile[n], Grouping, WaveRange2)



# matplotlib Graph
plt.figure('{} / {} Range'.format(WaveRange1, WaveRange2))
plt.xlabel('Time [s]')
plt.ylabel('{} / {} Power'.format((WaveRange1, WaveRange2)))
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)

# Plot Section
plt.plot(S1.t, S1.y1, label='S3_A1_D')
plt.plot(S1.t, S1.y2, label='S3_A1_T')
plt.plot(S2.t, S2.y1, label='S3_B1_D')
plt.plot(S2.t, S2.y2, label='S3_B1_T')

plt.legend()
plt.show()