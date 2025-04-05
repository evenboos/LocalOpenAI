import requests

url = "https://localhost:8000/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-123123"
}

# 最简单的正确请求体格式
payload = {
    "model": "qwen_2",
    "messages": [
        
        {
            "role": "system", 
            "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "写一个python的helloworld，不要做其他的工作"
        }
    ],
    "stream": True  # 明确指定stream参数
}

# 发送请求并打印详细信息
response = requests.post(url, headers=headers, json=payload, verify=False)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")