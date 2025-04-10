import requests
import json
import random
import time


# 隨機選擇初始 Token
tokens = [
    # PTT NOTIFY
	"eKshpBc...",
    # PTT NOTIFY - 2
    "lWnP6TdUcfj..."
    # PTT NOTIFY - 3
	"IA/BSWAPkws...",
    # PTT NOTIFY - 4
	"b4TlbCBAZP7...",
    # HH打卡
    # "0fQrbKQK1LP..."
]
current_token = random.choice(tokens)


def send_message(msg):
    global current_token  # 使用全域變數以便更新
    # LINE Messaging API 的 Endpoint URL

    headers = {
        "Authorization": f"Bearer {current_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": "Ud08565e9...", #User
        # "to": "C452706b...", #HH群組
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }

    while True:
        try:
            response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(payload))
            # 檢查回應
            if response.status_code == 200:
                print("訊息發送成功")
                break  # 成功後結束迴圈
            elif response.status_code == 429:
                print(f"發送失敗: {response.status_code} - Rate Limit Exceeded. 隨機換一組 Token 再試。")
                current_token = random.choice(tokens)  # 隨機選擇新 Token
                headers["Authorization"] = f"Bearer {current_token}"
                time.sleep(1)  # 避免過度頻繁請求
            else:
                print(f"發送失敗: {response.status_code}")
                print(response.json())
                break  # 其他錯誤直接結束
        except Exception as e:
            print(f"發送失敗，發生例外: {e}")
            break

# 發送多次訊息
for i in range(1):
    send_message("123")
