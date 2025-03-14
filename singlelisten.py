#微信自动化消息获取脚本
#developer:Caspiran
#注意事项：
# 需要安装wxauto库，并且需要安装python3.7以上版本
# 需要安装keyboard库，用于按下键盘
# 使用前需登录微信并将聊天列表滚动到顶部，以保证程序正常操作。
# 多次使用可能导致账号退出登录，请谨慎使用。
# 代码开源可以随意修改
# 不保证代码安全，请勿用于非法用途。
import wxauto
import time
from datetime import datetime, timedelta
import os
import keyboard
import pyautogui as pg
import subprocess

# 定义保存聊天记录的文件夹路径
script_dir = os.path.dirname(os.path.abspath(__file__))
subfolder_name = "chatlogs"
subfolder_path = os.path.join(script_dir, subfolder_name)
os.makedirs(subfolder_path, exist_ok=True)

# 清空文件夹
files = os.listdir(subfolder_path)
for file in files:
    file_path = os.path.join(subfolder_path, file)
    os.remove(file_path)

print("SYS:文件夹已清空！")
print("SYS:程序运行时间较长，请等待运行完成后再进行操作！")
# 启动微信
wx = wxauto.WeChat()
print("SYS:请将聊天列表滚动至最顶部！")
# 等待微信启动
time.sleep(3)
# 获取群聊列表
listen_list = wx.GetSessionList()

# 定义获取过去一天聊天信息的时间范围
#now = datetime.now()
#one_day_ago = now - timedelta(days=1)
# 由于listen_list是一个字典，我们需要找到字典中的键来获取群聊信息
group_name = input("请输入需要监听的群聊名称：")
heap=input("请输入加载次数：")
# 遍历群聊列表
wx.ChatWith(group_name)
time.sleep(1)
# 获取聊天记录
for i in range(int(heap)):
    wx.LoadMoreMessage()
messages = wx.GetAllMessage()

    # 将聊天信息转换为文本
chat_content = '\n'.join([f"{msg[0]}：{msg[1]}" for msg in messages])
file_name=f"chat_{group_name}.txt"
# 保存为文件
file_path = os.path.join(subfolder_path, file_name)
# 保存为文件
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(chat_content)
print(f"{group_name} saved!")
time.sleep(0.5)
# 发送文件到质谱
