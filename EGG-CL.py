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
    y: list = ''


Inf = 8
Enf = 12
Grouping = 100
WaveRange = "Alpha"
WAVFile = [
    "",
    "S1_A1",
    "S1_A2"
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
    eval('S'+str(n)).y = FFT_Process(eval('S'+str(n)).d, eval('S'+str(n)).f, eval('S'+str(n)).t, eval('S'+str(n)).im, Inf, Enf)

    # Data Process
    DATA_Process(eval('S'+str(n)).y, eval('S'+str(n)).t, WAVFile, Grouping, WaveRange)


GraphColor = ["red", "orange", "yellow", "green", "blue", "pink", "purple"]
plt.figure('{} Range'.format(WaveRange))
plt.xlabel('Time [s]')
plt.ylabel('{} Power'.format((WaveRange)))
#plt.xlim(0,max(t1))
plt.ylim(0, 2000)

# Plot Section
plt.plot(S1.t, S1.y, label='S1_A1', color=GraphColor[0])
plt.plot(S2.t, S2.y, label='S1_A2', color=GraphColor[1])

plt.legend()
plt.show()

# Plot Multi Call
# for g in range(1, WAVNUM):
#     plt.plot(eval('S'+str(n)).t, eval('S'+str(n)).y, color=GraphColor[g-1])