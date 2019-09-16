import pyautogui
import time
import csv
import pyperclip

def pyautoguiFunction(a, b):
    pyautogui.moveTo(a, b, 1)  # 첫번째 아이템 위치
    time.sleep(1)
    pyautogui.click()  # 첫번째 아이템 클릭
    time.sleep(5)
    pyautogui.moveTo(863, 48, 2)  # 마우스 오른쪽 버튼을 클릭하기 위한 공백란
    time.sleep(1)
    pyautogui.click(button='right')  # 오른쪽 버튼 클릭
    time.sleep(1)
    pyautogui.moveTo(924, 616, 1)  # 속성 위치
    time.sleep(1)
    pyautogui.click()  # 속성 클릭
    time.sleep(1)
    pyautogui.moveTo(356, 361, 1)  # url 주소 위치
    time.sleep(1)
    pyautogui.click(button='right')  # 오른쪽 버튼 클릭
    time.sleep(1)
    pyautogui.moveTo(425, 534, 1)  # 모두 선택 위치
    time.sleep(1)
    pyautogui.click()  # 모두 선택 클릭
    time.sleep(1)
    pyautogui.moveTo(356, 361, 1)  # url 주소 위치
    time.sleep(1)
    pyautogui.click(button='right')  # 오른쪽 버튼 클릭
    time.sleep(1)
    pyautogui.moveTo(408, 430, 1)  # 복사 위치
    time.sleep(1)
    pyautogui.click()  # 복사 버튼 클릭
    time.sleep(1)
    pyautogui.moveTo(510, 35, 1)  # 속성창 닫기 버튼 위치
    time.sleep(1)
    pyautogui.click()  # 속성창 닫기 클릭
    time.sleep(1)
    pyautogui.moveTo(982, 16, 1)  # 팝업창 닫기 위치
    time.sleep(1)
    pyautogui.click()  # 팝업창 닫기 클릭
    time.sleep(1)
    clipboard = pyperclip.paste() # url 복사 내용
    urlList.append(clipboard) # url 복사 내용을 리스트에 담음
    csvfile = open("carmodoo5.csv", "a", newline='')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow([clipboard])
    csvfile.close()

    return b


def getURl():
    a = 1344
    b = -790
    c = -1180
    d = -445
    for j in range(1, 7):
        b += 90
        pyautoguiFunction(a, b)
    pyautogui.moveTo(1574, -426, 1)
    pyautogui.scroll(-600)
    for j in range(1, 12):
        c += 90
        pyautoguiFunction(a, c)
    pyautogui.moveTo(1574, -426, 1)
    pyautogui.scroll(-600)
    for j in range(1, 4):
        d += 90
        pyautoguiFunction(a, d)

def pagingFunction(x, y):
    pyautogui.moveTo(x, y, 1)
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)
    pyautogui.scroll(1000)
    time.sleep(2)
    return x

urlList = []

x = 1650
y = -100
for k in range(1, 12):
    getURl()
    x += 45
    pagingFunction(x, y)




