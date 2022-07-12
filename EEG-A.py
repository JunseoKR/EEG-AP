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
WaveRange = "Alpha"

# WaveFiles
WAVFile = [
    "Empty",
    "S3_A1",
    "S3_B1",
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
    # Alpha
    eval('S'+str(n)).y1 = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, 8, 12)
    eval('S'+str(n)).y2 = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, 4, 8)

    # Data Process
    DATA_Process(eval('S'+str(n)).y1, eval('S'+str(n)).t, WAVFile[n], Grouping, "Alpha")
    DATA_Process(eval('S'+str(n)).y2, eval('S'+str(n)).t, WAVFile[n], Grouping, "Beta")


GraphColor = ["red", "orange", "yellow", "green", "blue", "pink", "purple"]
plt.figure('{} Range'.format(WaveRange))
plt.xlabel('Time [s]')
plt.ylabel('{} Power'.format((WaveRange)))
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)

# Plot Section
plt.plot(S1.t, S1.y1, label='S3_A1_A', color=GraphColor[0])
plt.plot(S1.t, S1.y2, label='S3_A1_B', color=GraphColor[1])
plt.plot(S2.t, S2.y1, label='S3_B1_A', color=GraphColor[2])
plt.plot(S2.t, S2.y2, label='S3_B1_B', color=GraphColor[3])

plt.legend()
plt.show()

# Plot Multi Call
# for g in range(1, WAVNUM):
#     plt.plot(eval('S'+str(n)).t, eval('S'+str(n)).y, color=GraphColor[g-1])