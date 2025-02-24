import tkinter as tk
import pyautogui
from pynput import keyboard
import time
keyinput = keyboard.Controller()

#执行自定义动作


def convertarray(position_list):
    coordinates_array = []
    position_list = position_list.replace("\n", "")
    for coord in position_list.split('; '):
        print(coord)
        if coord.strip('(); '):
            x, y, z = coord.strip('(); ').split(', ')
            x_str, y_str, z_str = map(str, (x, y, z))
            coordinates_array.append((x_str, y_str, z_str))
    print(coordinates_array)
    return coordinates_array


#去掉mouse_position_list 中的换行符


def press_key(key):
    if isinstance(key, str):
        # 如果key是字符串，则尝试获取对应的键名属性
        key_name = key.split('.')[1] if '.' in key else key
        keyinput.press(getattr(keyboard.Key, key_name))
        keyinput.release(getattr(keyboard.Key, key_name))
    else:
        # 如果key不是字符串，则直接将其作为按键传递给keyboard.press()
        keyinput.press(key)
        keyinput.release(key)

def move_mouse_and_click(coordinates):
    for coordinate in coordinates:
        x, y, z = coordinate
        if y != '-1':
            pyautogui.moveTo(int(x), int(y))
            pyautogui.click()
            time.sleep(int(z))
        else:
            press_key(x)
            time.sleep(int(z))

def visitclass(coordinates):
    move_mouse_and_click(coordinates)

def study(coordinates1, coordinates2, coordinates3):
    # study 中 sleep 的时间是分钟
    for coordinate in coordinates1:
        move_mouse_and_click(coordinates2)
        move_mouse_and_click(coordinates3)
        x, y, z = coordinate
        if y != '-1':
            pyautogui.moveTo(int(x), int(y))
            pyautogui.click()
            print(x,y,z)
            # 打印当前时间
            print(time.strftime("start:%Y-%m-%d %H:%M:%S", time.localtime()))
            time.sleep(int(z)*60)
            print(time.strftime("Completed:%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            press_key(x)
            time.sleep(int(z)*60)

#课程最终位置
mouse_position_list = "(1029, 630, 33); (1024, 742, 24); (1024, 847, 33); (1024, 956, 37); "
#重新登陆
mouse_position_list1 = "(187, 18, 5); (1052, 159, 5); (987, 146, 5); (546, 516, 5); (696, 413, 5); (883, 140, 5); "
#进入课程2-1-1
mouse_position_list2 = "(1060, 537, 5); (Key.end, -1, 1); (Key.up, -1, 1); (Key.home, -1, 1); (Key.page_down, -1, 1); "

study(convertarray(mouse_position_list), convertarray(mouse_position_list1), convertarray(mouse_position_list2))

#课程最终位置
mouse_position_list = "(1026, 267, 31); (1027, 374, 34); (1025, 485, 33); (1024, 588, 35); (1023, 698, 37); (1023, 803, 23); "
#重新登陆
mouse_position_list1 = "(187, 18, 5); (1052, 159, 5); (987, 146, 5); (546, 516, 5); (696, 413, 5); (883, 140, 5); "
#进入课程2-1-2
mouse_position_list2 = "(1060, 537, 5); (Key.end, -1, 1); (Key.up, -1, 1); (Key.home, -1, 1); (Key.page_down, -1, 1); (Key.page_down, -1, 1); "

study(convertarray(mouse_position_list), convertarray(mouse_position_list1), convertarray(mouse_position_list2))

#课程最终位置
mouse_position_list = "(1027, 631, 35); (1023, 738, 38); (1023, 846, 33); (1023, 955, 33); "
#重新登陆
mouse_position_list1 = "(187, 18, 5); (1052, 159, 5); (987, 146, 5); (546, 516, 5); (696, 413, 5); (883, 140, 5); "
#进入课程2-2-1
mouse_position_list2 = "(1060, 537, 5); (Key.end, -1, 1); (Key.up, -1, 1); (1054, 813, 5); (Key.home, -1, 1); (Key.page_down, -1, 1); "

study(convertarray(mouse_position_list), convertarray(mouse_position_list1), convertarray(mouse_position_list2))

#课程最终位置
mouse_position_list = "(1030, 441, 31); (1029, 545, 35); (1027, 660, 17); "
#重新登陆
mouse_position_list1 = "(187, 18, 5); (1052, 159, 5); (987, 146, 5); (546, 516, 5); (696, 413, 5); (883, 140, 5); "
#进入课程2-2-2
mouse_position_list2 = "(1060, 537, 5); (Key.end, -1, 1); (Key.up, -1, 1); (1054, 813, 5); (Key.home, -1, 1); (Key.page_down, -1, 1); (Key.page_down, -1, 1); "

study(convertarray(mouse_position_list), convertarray(mouse_position_list1), convertarray(mouse_position_list2))

#课程最终位置
mouse_position_list = "(1039, 849, 34); (1031, 955, 29); "
#重新登陆
mouse_position_list1 = "(187, 18, 5); (1052, 159, 5); (987, 146, 5); (546, 516, 5); (696, 413, 5); (883, 140, 5); "
#进入课程
mouse_position_list2 = "(1067, 431, 5); (Key.end, -1, 1); (Key.up, -1, 1); (1054, 813, 5); (Key.home, -1, 1); (Key.page_down, -1, 1); "

study(convertarray(mouse_position_list), convertarray(mouse_position_list1), convertarray(mouse_position_list2))