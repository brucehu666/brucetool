# 自动化学习助手

这是一个用于自动化学习干部在线内容的辅助工具。

## 环境准备

在使用本工具前，请先安装以下必要的 Python 库：
```bash
pip install tkinter pynput pyautogui

本脚本用于鼠标键盘的记录， 配合clirunstudy.py使用, 用于自动化学习干部在线的内容
先安装tkinter, pynput, pyautogui 等库 使用 pip install tkinter pynput pyautogui
执行python automouse.py
点击 开始检测按钮，然后按ctrl来连续记录鼠标位置，按其他按键来记录按键，然后点击结束检测按钮，然后点击执行自定义动作按钮
可分为三个阶段，
- 第一阶段 重新登陆 先记录所有重新登陆的鼠标动作，包括 点击首页网页标签 登出，登录，登录用户，点击学习城，点击学习中心 把所有鼠标位置记录下来，copy到第二个文本框备用
- 第二阶段 点击课程，在新网页先点End移到最后，再按一下上露出页面切换，并记录鼠标位置，然后按home回到页首，再根据需要按pagedown，露出具体课程的学习按钮. copy到第三个文本框备用
- 第三阶段 记录课程学习按钮具体鼠标位置，需要根据课程时长，自行修改第三个数字的值，一般为时长+1
这些值都记录下来然后给clirunstudy.py使用，赋值 课程位置 给mouse_position_list，重新登陆 给mouse_position_list1 进入课程 给mouse_position_list2
可重复赋值并执行study函数，完成自动化学习