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
from zhipuai import ZhipuAI
import json
from pathlib import Path

wx = wxauto.WeChat()
client = ZhipuAI(api_key="")
model = "glm-4-flash"
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

print("SYS:请将聊天列表滚动至最顶部！")
# 等待微信启动
# 获取群聊列表
time.sleep(5)
listen_list = wx.GetSessionList()

# 定义获取过去一天聊天信息的时间范围
#now = datetime.now()
#one_day_ago = now - timedelta(days=1)
# 由于listen_list是一个字典，我们需要找到字典中的键来获取群聊信息
group_list = list(listen_list.keys())
# 遍历群聊列表
wx.ChatWith(group_list[0])
for i in range(0,50):
    time.sleep(1)
    # 获取聊天记录
    if group_list[i%5] != "Subscriptions":#微信公众号消息可能出现问题，请根据中英文进行设置
        wx.LoadMoreMessage()
    messages = wx.GetAllMessage()

    # 将聊天信息转换为文本
    chat_content = '\n'.join([f"{msg[0]}：{msg[1]}" for msg in messages])
    file_name = f"chat_{i+1}_{group_list[i%5]}.txt"
    # 保存为文件
    file_path = Path(subfolder_path) / file_name
    with file_path.open('w', encoding='utf-8') as file:
        file.write(chat_content)
    print(f"{group_list[i%5]} saved!")
    
    time.sleep(1)
    file_path = Path(subfolder_path) / file_name
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = json.loads(client.files.content(file_id=file_object.id).content)["content"]
    try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"\n{file_content}\n请根据以上聊天记录的内容进行总结，提取出关键信息。关键信息指作业、通知、求职相关信息、与学术相关的活动信息。其他你认为重要的信息也可以包含。请不要使用双星号标注，只要1.2.3.4.这样分条即可。"}],
            )
            girlfriend_reply = response.choices[0].message.content
            print("~IRAN~:", girlfriend_reply)
    except Exception as e:
            print(f"调用API出现错误: {e}")
            time.sleep(3)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": f"\n{file_content}\n请根据以上聊天记录的内容进行总结，提取出关键信息。关键信息指作业、通知、求职相关信息、与学术相关的活动信息。其他你认为重要的信息也可以包含。请不要使用双星号标注，只要1.2.3.4.这样分条即可。"}],
                )
                girlfriend_reply = response.choices[0].message.content
                print("~IRAN~:", girlfriend_reply)
            except Exception as e:
                 print(f"第二次调用API出现错误: {e}。跳过此次调用。")
    keyboard.press_and_release('down')
    # 返回微信
#    pg.click(849,1572)
#    time.sleep(35)
    if (i+1)%5 == 0:
        #save current name
        temp=group_list[5]
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        keyboard.press_and_release('down')
        listen_list = wx.GetSessionList()
        temp1 = list(listen_list.keys())
        # 找到temp在temp1中的索引
        try:
            index = temp1.index(temp)
        except ValueError:
            index = None  # 如果temp不在temp1中，则设置index为None

        # 如果找到了索引，则重新构建group_list
        if index is not None:
            # 将temp到temp1末尾的部分和temp1开头到temp的部分拼接起来，形成新的group_list
            group_list = temp1[index:] + temp1[:index]

        # 使用新的group_list进行聊天
        wx.ChatWith(group_list[0])

print("聊天记录已获取完毕，再次使用将会覆盖之前的聊天记录！")
