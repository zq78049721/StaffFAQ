# ModelScope（魔搭）部署指南

## 部署步骤

### 1. 确保代码已推送

你的代码已经上传到 ModelScope，确认包含以下文件：
- ✅ app.py
- ✅ requirements.txt
- ✅ core/ 目录
- ✅ modules/ 目录
- ✅ data/hr/ 目录（包含 TXT 文档）

### 2. 配置环境变量

在你的 Studio 设置页面（https://www.modelscope.cn/studios/zq78049721/StaffFAQ/settings）：

1. 找到 **"环境变量"** 或 **"Environment Variables"** 区域
2. 添加以下三个环境变量：

```
变量名: LLM_PROVIDER
变量值: deepseek

变量名: LLM_MODEL
变量值: deepseek-chat

变量名: DEEPSEEK_API_KEY
变量值: sk-你的真实DeepSeek_API_KEY
```

**如何获取 DeepSeek API Key：**
1. 访问：https://platform.deepseek.com/
2. 注册/登录账号
3. 在 API Keys 页面创建新的 Key
4. 复制 Key 并粘贴到 ModelScope 的环境变量中

### 3. 启动应用

配置好环境变量后：
1. 点击 **"运行"** 或 **"Run"** 按钮
2. 等待环境安装（首次需要 5-10 分钟）
3. 应用会自动启动

### 4. 验证部署

访问你的 Studio 页面，检查：
- ✅ 聊天界面正常显示
- ✅ 可以上传文档
- ✅ 问答功能正常
- ✅ 没有报错信息

## 常见问题

### 问题 1：找不到 API Key

**错误信息**: "未找到 API Key"

**解决方法**:
1. 检查环境变量是否配置正确
2. 确认变量名是 `DEEPSEEK_API_KEY`（大小写敏感）
3. 重新保存环境变量并重启应用

### 问题 2：依赖安装失败

**错误信息**: pip install 失败

**解决方法**:
1. 检查 requirements.txt 格式是否正确
2. 确保没有多余的空格或特殊字符
3. 查看日志找出具体的错误包

### 问题 3：文档未自动处理

**现象**: 上传文档后无法问答

**解决方法**:
1. 确认文档在 `data/hr/` 目录下
2. 文档扩展名必须是 `.txt`
3. 文档编码必须是 UTF-8
4. 点击"处理文档"按钮手动触发

### 问题 4：内存不足

**错误信息**: Out of Memory

**解决方法**:
1. 减少文档数量（建议不超过 5 个）
2. 减小文档大小（每个不超过 50 KB）
3. 重启应用清理缓存

## ModelScope 的优势

- ✅ **免费 GPU**: 可以选择 GPU 实例加速模型加载
- ✅ **国内访问**: 速度更快
- ✅ **阿里云支持**: 稳定可靠
- ✅ **环境变量管理**: 方便配置 API Key

## 环境变量说明

代码会自动读取以下环境变量：

```python
# 核心配置
LLM_PROVIDER = "deepseek"    # 使用 DeepSeek
LLM_MODEL = "deepseek-chat"  # 模型名称
DEEPSEEK_API_KEY = "sk-xxx"  # API 密钥

# 可选配置
TEMPERATURE = "0.7"          # 温度参数（可选）
```

## 调试技巧

### 查看日志

在 Studio 页面找到 **"日志"** 或 **"Logs"** 按钮，可以查看：
- 应用启动过程
- 错误信息
- 文档处理状态

### 测试 API Key

在日志中搜索 "初始化" 或 "LLM"，确认：
- API Key 已正确加载
- LLM 客户端初始化成功
- 可以正常调用模型

## 性能优化

### 文档优化
- 使用 UTF-8 编码
- 每个文档不超过 50 KB
- 文档数量控制在 5-10 个

### 模型优化
- 使用 `deepseek-chat`（速度快）
- 避免频繁重启应用

### 存储优化
- ChromaDB 会保存在临时目录
- 重启后需要重新处理文档
- 可以提前上传好文档

## 备用方案

如果 ModelScope 遇到问题，可以考虑：
1. **Streamlit Cloud**: https://share.streamlit.io/
2. **Hugging Face Spaces**: https://huggingface.co/spaces
3. **本地运行**: 调试更灵活

## 联系支持

如果遇到问题：
- ModelScope 文档: https://modelscope.cn/docs
- DeepSeek 支持: https://platform.deepseek.com/
