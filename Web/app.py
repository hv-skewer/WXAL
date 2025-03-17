from flask import Flask, render_template, request, jsonify
import webbrowser
import time
import json
import os

app = Flask(__name__)
CONFIG_FILE = "../config/setting.json"

port = 5289

# 初始化配置数据
setting_data = {
    "platform_api": "https://api.siliconflow.cn/v1",
    "api_key": "",
    "model_name": "",
    "max_length": 3300,
    "temperature": 1.0,
    "max_tokens": 4096,
    "users": [],
    "groups": [],
    "pre_prompt": "",
}

# 加载已存在的配置
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        setting_data.update(json.load(f))


@app.route("/")
def index():
    return render_template("indu.html", config=setting_data)


@app.route("/save-config", methods=["POST"])
def save_config():
    try:
        # 获取基础表单数据
        setting_data["platform_api"] = request.form.get("platform-api")
        setting_data["api_key"] = request.form.get("api-key")
        setting_data["model_name"] = request.form.get("model-name")
        setting_data["max_length"] = int(request.form.get("max-length"))
        setting_data["temperature"] = float(request.form.get("temperature"))
        setting_data["max_tokens"] = int(request.form.get("max-tokens"))
        setting_data["pre_prompt"] = request.form.get("pre-prompt")
        # 获取动态添加的用户和群聊
        setting_data["users"] = request.form.getlist("users[]")
        setting_data["groups"] = request.form.getlist("groups[]")
        # 数据验证
        if not setting_data["api_key"].startswith("sk-"):
            raise ValueError("API Key需以sk-开头")
        if not (0 <= setting_data["temperature"] <= 2):
            raise ValueError("温度参数需在0-2之间")
        # 保存到文件
        with open(CONFIG_FILE, "w") as f:
            json.dump(setting_data, f, indent=2, ensure_ascii=False)
        return jsonify({"status": "success", "message": "配置保存成功！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# 检测配置文件是否存在
def ifconfig():
    if not os.path.exists('../config'):
        os.makedirs("../config")
    if os.access(CONFIG_FILE, os.F_OK):
        borstr = input("检测到配置文件已存在,是否重新设置？(Y/N): ")
        if borstr == 'Y' or borstr == 'y':
            webbrowser.open_new(f'http://localhost:{port}')
            app.run(port=port)
            return
        else:
            return
    else:
        print("检测到未存在配置文件，正在创建配置文件！")
        webbrowser.open_new(f'http://localhost:{port}')
        app.run(port=port)
        return


if __name__ == "__main__":
    ifconfig()
