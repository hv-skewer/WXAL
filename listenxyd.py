
import wxauto
import requests                       #需要自己安装？
import json

wx = wxauto.WeChat()
wx.AddListenChat(who="勇闯哈尔滨")
with open("F:\Desktop\Test\myapikey.txt","r") as key_file:    #myapikey.txt文件中
    myapikey=key_file.read()
    
headers = {
    'Authorization': myapikey
}

url_of_glm="https://open.bigmodel.cn/api/paas/v4/chat/completions"

while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who              # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)   # 获取消息内容
        # 回复收到
        for msg in one_msgs:
            msgtype = msg.type       # 获取消息类型
            content = msg.content    # 获取消息内容，字符串类型的消息内容
            print(f'【{who}】：{content}')
        # ===================================================
        # 处理消息逻辑（如果有）
        # 
        # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
        # 
        # ===================================================
        
            # 如果是好友发来的消息（即非系统消息等），则回复收到
            if msgtype != 'self':
                data={
                    "model":"glm-4-flash",
                    "messages":
                    [{"role":"system","content":"你是一位18岁帅气男大，喜欢乐子，你的口头禅是“奖一块华为手表”"}
                        ,{"role":"user","content":content}]
                    }
                response = requests.post(url_of_glm, headers=headers,json=data)
                json_text=response.json()
                answer=json_text["choices"][0]["message"]["content"]
                chat.SendMsg(answer)
