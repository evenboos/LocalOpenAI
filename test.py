import requests

url = "http://127.0.0.1:8000/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-123123"
}

# 最简单的正确请求体格式
payload = {
    "model": "qwen_2",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ],
    "stream": True  # 明确指定stream参数
}

# 发送请求并打印详细信息
response = requests.post(url, headers=headers, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")