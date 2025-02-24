import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import pyautogui
from pynput import keyboard
import time
keyinput = keyboard.Controller()
# 本脚本用于鼠标键盘的记录， 配合clirunstudy.py使用, 用于自动化学习干部在线的内容
# 先安装tkinter, pynput, pyautogui 等库 使用 pip install tkinter pynput pyautogui
# 执行python automouse.py
# 点击 开始检测按钮，然后按ctrl来连续记录鼠标位置，按其他按键来记录按键，然后点击结束检测按钮，然后点击执行自定义动作按钮
# 可分为三个阶段，
# 第一阶段 重新登陆 先记录所有重新登陆的鼠标动作，包括 点击首页网页标签 登出，登录，登录用户，点击学习城，点击学习中心 把所有鼠标位置记录下来，copy到第二个文本框备用
# 第二阶段 点击课程，在新网页先点End移到最后，再按一下上露出页面切换，并记录鼠标位置，然后按home回到页首，再根据需要按pagedown，露出具体课程的学习按钮. copy到第三个文本框备用
# 第三阶段 记录课程学习按钮具体鼠标位置，需要根据课程时长，自行修改第三个数字的值，一般为时长+1
# 这些值都记录下来然后给clirunstudy.py使用，赋值 课程位置 给mouse_position_list，重新登陆 给mouse_position_list1 进入课程 给mouse_position_list2
# 可重复赋值并执行study函数，完成自动化学习

class MousePositionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Position Tracker")
        
        # 显示鼠标当前位置的标签
        self.label = tk.Label(root, text="Move the mouse to see the position", font=("Helvetica", 16))
        self.label.pack(padx=20, pady=10)
        
        # 创建一个文本框，用于记录鼠标位置
        self.textbox = ScrolledText(root, width=50, height=4, font=("Helvetica", 12))
        self.textbox.pack(padx=10, pady=10)

        self.textbox1 = ScrolledText(root, width=50, height=2, font=("Helvetica", 12))
        self.textbox1.pack(padx=10, pady=20)

        self.textbox2 = ScrolledText(root, width=50, height=2, font=("Helvetica", 12))
        self.textbox2.pack(padx=10, pady=30)

        self.positions = []  # 记录所有坐标
        
        # 添加开始和结束检测按钮
        self.start_button = tk.Button(root, text="开始检测", command=self.start_detection, font=("Helvetica", 14))
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="结束检测", command=self.stop_detection, font=("Helvetica", 14))
        self.stop_button.pack(pady=5)
        # 添加执行自定义动作的按钮
        self.action_button = tk.Button(root, text="执行自定义动作", command=self.execute_action, font=("Helvetica", 14))
        self.action_button.pack(pady=5)
        self.running = False  # 标志位，表示是否正在检测

    def start_detection(self):
        if not self.running:
            self.running = True
            self.update_mouse_position()
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            
    def stop_detection(self):
        if self.running:
            self.running = False
            if hasattr(self, "listener"):
                self.listener.stop()
        
    def update_mouse_position(self):
        if self.running:
            x, y = pyautogui.position()
            self.label.config(text=f"当前鼠标位置: (X: {x}, Y: {y})")
            self.label.update()
            self.root.after(100, self.update_mouse_position)
            
    def on_press(self, key):
        if self.running:
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    x, y = pyautogui.position()
                    position = f"({x}, {y}, 5)"
                    self.positions.append(position)
                    self.textbox.insert(tk.END, f"{position}; ")
                    self.textbox.yview(tk.END)  # 滚动到最后一行
                else:
                    position = f"({key}, -1, 1)"  # 记录按键，y填-1，等待1s
                    self.positions.append(position)
                    self.textbox.insert(tk.END, f"{position}; ")
                    self.textbox.yview(tk.END)  # 滚动到最后一行
            except AttributeError:
                pass

    def execute_action(self):
        if self.running:
            self.stop_detection()
        #执行自定义动作
        #把 textbox 中的内容取出来, 并以string 的形式保存在变量 mouse_position_list 中
        mouse_position_list = self.textbox.get("1.0", tk.END)
        #去掉mouse_position_list 中的换行符
        mouse_position_list = mouse_position_list.replace("\n", "")
        print(mouse_position_list)
        coordinates_array = []
        for coord in mouse_position_list.split('; '):
            print(coord)
            if coord.strip('(); '):
                x, y, z = coord.strip('(); ').split(', ')
                x_str, y_str, z_str = map(str, (x, y, z))
                coordinates_array.append((x_str, y_str, z_str))
        print(coordinates_array)
        
        mouse_position_list1 = self.textbox1.get("1.0", tk.END)
        #去掉mouse_position_list 中的换行符
        mouse_position_list1 = mouse_position_list1.replace("\n", "")
        print(mouse_position_list1)
        coordinates_array1 = []
        for coord in mouse_position_list1.split('; '):
            print(coord)
            if coord.strip('(); '):
                x, y, z = coord.strip('(); ').split(', ')
                x_str, y_str, z_str = map(str, (x, y, z))
                coordinates_array1.append((x_str, y_str, z_str))
        print(coordinates_array1)

        mouse_position_list2 = self.textbox2.get("1.0", tk.END)
        #去掉mouse_position_list 中的换行符
        mouse_position_list2 = mouse_position_list2.replace("\n", "")
        print(mouse_position_list2)
        coordinates_array2 = []
        for coord in mouse_position_list2.split('; '):
            print(coord)
            if coord.strip('(); '):
                x, y, z = coord.strip('(); ').split(', ')
                x_str, y_str, z_str = map(str, (x, y, z))
                coordinates_array2.append((x_str, y_str, z_str))
        print(coordinates_array2)

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
            for coordinate in coordinates1:
                move_mouse_and_click(coordinates2)
                move_mouse_and_click(coordinates3)
                x, y, z = coordinate
                if y != '-1':
                    pyautogui.moveTo(int(x), int(y))
                    pyautogui.click()
                    time.sleep(int(z)*60)
                else:
                    press_key(x)
                    time.sleep(int(z)*60)

        study(coordinates_array, coordinates_array1, coordinates_array2)

    def on_close(self):
        self.stop_detection()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MousePositionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # 确保安全关闭监听器
    root.mainloop()
    
if __name__ == "__main__":
    main()