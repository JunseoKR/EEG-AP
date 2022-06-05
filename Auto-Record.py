import os
import time
import keyboard
import pyautogui


class Auto(object):
    def __init__(self):
        pass
    
    def Click(self, File):
        Locate = pyautogui.locateOnScreen(r'Auto-Record\{}.png'.format(File))
        pyautogui.moveTo(Locate)
        pyautogui.click()
        return

    def Record(self):
        os.startfile(r'C:\Program Files (x86)\Backyard Brains\Spike Recorder\SpikeRecorder.exe')
        time.sleep(5)
        self.Click(File="Setting")
        self.Click(File="Connect")
        time.sleep(0.5)
        if pyautogui.locateOnScreen(r'Auto-Record\Serial.png', confidence=0.5):
            print("Connect The Serial")
        

Run = Auto()
Run.Record()