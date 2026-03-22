# 百度API推送脚本（适配zqdssg.xyz，修复response未定义报错）
import requests

# ---------------------- 你的配置（不用改） ----------------------
SITE = "https://zqdssg.xyz"
TOKEN = "N1qgW7441ezPx5Eg"
URLS_TO_SUBMIT = [
    "https://zqdssg.xyz/index.html",          # 替换成你的URL1
    "https://zqdssg.xyz/app.html" # 替换成你的URL2
]
# ---------------------- 配置结束 ----------------------

# 拼接API接口地址
API_URL = f"http://data.zz.baidu.com/urls?site={SITE}&token={TOKEN}"
headers = {"Content-Type": "text/plain"}
data = "\n".join(URLS_TO_SUBMIT)

# 核心推送逻辑（修复异常处理）
print("="*50)
try:
    # 发送请求（这行执行失败会直接进入except）
    response = requests.post(API_URL, headers=headers, data=data, timeout=10)
    
    # 只有请求发送成功，才会执行以下代码
    print("✅ 推送请求已发送！")
    print(f"📡 接口地址：{API_URL}")
    print(f"📊 提交的URL数量：{len(URLS_TO_SUBMIT)}")
    print(f"🔍 百度返回状态码：{response.status_code}")
    print(f"📄 百度返回结果：{response.text}")
    print("-"*50)

    # 解读返回结果
    if response.status_code == 200:
        result = response.json()
        print(f"🎉 成功推送URL数量：{result.get('success', 0)}")
        print(f"📅 今日剩余可推送配额：{result.get('remain', 0)}")
        
        if result.get("not_same_site"):
            print(f"⚠️ 非本站URL（未收录）：{result['not_same_site']}")
        if result.get("not_valid"):
            print(f"❌ 不合法URL（未收录）：{result['not_valid']}")
    else:
        print(f"❌ 推送失败！错误原因：{response.text}")

# 捕获所有异常（网络问题、请求超时、格式错误等）
except requests.exceptions.RequestException as e:
    print(f"❌ 请求发送失败（网络/接口问题）：{str(e)}")
    print("💡 排查方向：1. 检查网络是否正常 2. 接口地址是否正确 3. 服务器是否能访问百度接口")
except Exception as e:
    print(f"❌ 脚本运行出错：{str(e)}")
    print("💡 常见原因：1. URL格式错误 2. 返回结果不是JSON格式 3. 编码问题")
print("="*50)