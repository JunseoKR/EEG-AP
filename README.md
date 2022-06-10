# EEG-AP
## 🏫 Taejang High School / 태장고등학교

<br/>

* * *

## EEG Data Analysis
### EEG Measure
[ BackYard Brains ] Heart and Brain SpikerBox
- [ Backyard Brains ](https://backyardbrains.com/)
- Custom Arduino

<br/>

<br/>

* * *

## 📁 융합탐구 프로젝트 - [ 수정중 ]
### 📝 고등학생의 우울감 및 스트레스 진단과 개선 방법의 뇌파 측면에서의 접근에 대한 연구

<br/>

### ✔ 1. 탐구 목적
- ### [ 수정중 ]

<br/>

### ✔ 2. 연구 방법

#### 1. 무자극 상태 / 자극(불안 / 긴장) 상태의 데이터를 측정하기 위해 환경을 조성한다.

- 무자극 상태
  - 의자에 앉아 측정 장치를 부착, 편안한 상태에서 EEG 데이터를 측정, 저장한다.

- 자극 상태
  - 의자에 앉아 측정 장치를 부착, 불안함을 유발하는 영상 시청을 통해 불안한 상태일 때 EEG 데이터를 측정, 저장한다.

#### 2. 무자극 상태 / 자극(불안 / 긴장) 상태의 데이터를 측정 후 분류한다.

#### 3. [EGG-AP.py](EGG-AP.py)를 통해 [vitzky-Golay 필터링](https://plotly.com/python/smoothing/)과 [FFT](https://en.wikipedia.org/wiki/Fast_Fourier_transform)를 처리하여 주파수별 데이터를 분석함.
- 분석 주파수
  - Alpha : 8 Hz ~ 12 Hz
  - High-Beta : 20 Hz ~ 30 Hz
  - ( Beta ) : 12 Hz ~  30 Hz

#### 4. [IBM SPSS](https://www.ibm.com/analytics/spss-statistics-software?mhsrc=ibmsearch_a&mhq=spss)를 통해 데이터를 분석한다

- 통계 방식
  - 진행중

#### 5. 분석된 무자극 상태 / 자극(불안 / 긴장) 상태의 데이터와 우울증 환자의 EEG 데이터를 비교분석한다.

- 분석방법
  - 진행중

<br/>

### ✔ 3. 예상결과
- ### [ 수정중 ]

<br/>

<br/>

<br/>

* * *

## ✨ 참고문헌

#### [ 동아일보 ] [중고생 자살원인 1위는 ‘성적’…학업 스트레스 크다](https://www.donga.com/news/It/article/all/20150525/71446025/1)

#### [ 연세대학교 의료공학연구센터 ] [뇌파 측정과 동적신경영상 이론 및 응용](http://cone.hanyang.ac.kr/bioest/kor/pds/shortterm_lecture.pdf)

#### [[ BackYard Brains ](https://github.com/BackyardBrains)]
- #### [ The Heart and Brain SpikerBox ](https://backyardbrains.com/products/heartAndBrainSpikerBox)
- #### [ Data Analysis for the EEG ](https://backyardbrains.com/products/files/Extracting_Frequency_Bands_EEG.pdf)
