import pyautogui
import time
import os
from dotenv import load_dotenv
load_dotenv()

screen_width, screen_height = pyautogui.size()

time.sleep(5)

pyautogui.click()
pyautogui.press('enter')

time.sleep(10)

carmodoo_id = os.getenv('CARMODOO_ID')
carmodoo_pw = os.getenv('CARMODOO_PW')

pyautogui.typewrite(carmodoo_id)
pyautogui.press('tab')
pyautogui.typewrite(carmodoo_pw)
pyautogui.press('enter')

time.sleep(10)

pyautogui.moveTo(500, 50)
time.sleep(2)
pyautogui.moveRel(None, 45)
pyautogui.click()