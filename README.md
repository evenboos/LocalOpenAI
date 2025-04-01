# 本地大模型 OpenAI 兼容 API 服务

这个项目使用 FastAPI 创建了一个与 OpenAI API 格式兼容的服务，允许你将本地大语言模型开放到公网，支持通过地址、模型名称和 API-Key 进行调用。

## 功能特点

- 完全兼容 OpenAI API 格式
- 支持聊天完成接口 (`/v1/chat/completions`)
- 支持文本完成接口 (`/v1/completions`)
- 支持模型列表接口 (`/v1/models`)
- API 密钥认证
- 自动加载本地大模型

## 安装要求

```bash
pip install -r requirements.txt
```

## 配置说明

在使用前，请先修改 `.env` 文件中的配置：

```
# API配置
API_KEY=sk-your-api-key  # 设置你的API密钥

# 模型配置
MODEL_PATH=your-model-path  # 设置你的模型路径
MODEL_NAME=your-model-name  # 设置你的模型名称

# 服务器配置
HOST=0.0.0.0  # 监听所有网络接口
PORT=8000     # 服务端口
```

## 启动服务

```bash
python run.py
```

服务启动后，可以通过以下地址访问：
- API文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/health`

## API使用示例

### 聊天完成接口

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-api-key" \
  -d '{
    "model": "your-model-name",
    "messages": [
      {"role": "system", "content": "你是一个有用的助手。"},
      {"role": "user", "content": "你好，请介绍一下自己。"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

### 文本完成接口

```bash
curl -X POST "http://localhost:8000/v1/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-api-key" \
  -d '{
    "model": "your-model-name",
    "prompt": "请介绍一下中国的历史",
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

### 获取模型列表

```bash
curl -X GET "http://localhost:8000/v1/models" \
  -H "Authorization: Bearer sk-your-api-key"
```

## 公网访问配置

要将服务开放到公网，你可以：

1. 确保服务器防火墙允许指定端口访问
2. 使用反向代理服务器（如Nginx）进行配置
3. 考虑使用HTTPS以确保安全性
4. 设置更强的API密钥和访问控制

## 注意事项

- 在生产环境中，请修改CORS设置，限制允许的来源
- 确保你有权限使用和分发你所加载的模型
- 根据你的模型大小和服务器配置，可能需要调整内存和计算资源


- run.py为服务器启动程序
- test.py为接口测试程序，建议将其移出项目文件夹单独测试