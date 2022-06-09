import time
import pyautogui


class Auto(object):
    def __init__(self):
        pass
    
    def Click(self, File):
        Locate = pyautogui.locateOnScreen(r'Auto-Record\{}.png'.format(File))
        pyautogui.click(Locate)
        
    def Record(self):
        t = int(input("Time : "))
        self.Click("Record")
        time.sleep(t)
        self.Click("Record")
        
Run = Auto()
Run.Record()