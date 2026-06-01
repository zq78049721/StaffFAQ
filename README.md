# StaffFAQ

智能人事问答系统 - 基于RAG技术的新员工助手

## 🌟 功能特性

-  智能对话界面 - 支持自然语言问答
- 📄 TXT 文档支持 - 初版专注于 TXT 格式，傻瓜化操作
- 🔍 精准检索 - 基于向量检索的准确答案查找
- 🎯 双版本提示词 - 免费版/付费版隔离设计
-  原子化架构 - 核心能力与业务模块分离，易于扩展
- 🚀 一键部署 - 简单安装，快速启动

## 📋 目录结构

```
StaffFAQ/
├── app.py                      # Streamlit 主程序
── core/                       # 核心能力层（可复用）
│   ├── __init__.py
│   ├── document_processor.py   # 文档处理（TXT加载、切分）
│   ├── vector_store.py         # 向量存储（ChromaDB）
│   ├── retriever.py            # 检索器
│   ├── llm_client.py           # LLM 调用（智谱AI）
│   └── prompt_manager.py       # 提示词管理
├── modules/                    # 业务模块层（原子化）
│   ├── __init__.py
│   ── hr/                     # 人事模块
│       ├── __init__.py
│       ├── config.py           # 模块配置
│       └── prompts/            # 提示词隔离
│           ├── free.yaml       # 免费版
│           └── premium.yaml    # 付费版（可收费）
── data/                       # 文档存储
│   └── hr/                     # 人事文档（TXT）
├── requirements.txt            # 依赖列表
├── .env.example                # 环境变量模板
├── .gitignore
├── setup.bat / setup.sh        # 一键安装脚本
── README.md
```

## 🚀 快速开始

### 1. 安装依赖

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. 配置环境变量

**️ 安全提示：永远不要将 `.env` 文件提交到 Git！**

#### 方式一：使用 `.env` 文件（本地开发）

```bash
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

编辑 `.env` 文件，填入你的 API Key：
```
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sk-你的真实API_KEY
```

#### 方式二：使用系统环境变量（生产推荐）

**Windows PowerShell:**
```powershell
[System.Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-xxx", "User")
[System.Environment]::SetEnvironmentVariable("LLM_PROVIDER", "deepseek", "User")
```

**Linux/Mac:**
```bash
echo 'export DEEPSEEK_API_KEY="sk-xxx"' >> ~/.bashrc
echo 'export LLM_PROVIDER="deepseek"' >> ~/.bashrc
source ~/.bashrc
```

> 获取 DeepSeek API Key: [DeepSeek 开放平台](https://platform.deepseek.com/)

### 3. 启动应用

**使用启动脚本（推荐）：**
```bash
start.bat    # Windows
./start.sh   # Linux/Mac
```

**或直接运行：**
```bash
streamlit run app.py
```

将人事相关的 TXT 文档放入 `data/hr/` 目录

### 4. 运行应用

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

### 4. 上传文档

### 上传文档

1. 在左侧边栏点击"选择文件"
2. 上传人事相关的 TXT 文档
3. 点击"处理文档"按钮

### 选择服务版本

- **免费版**：简洁明了的基础问答
- **付费版**：专业详细的人事顾问式回答

### 提问示例

- "公司的年假政策是什么？"
- "如何申请病假？"
- "加班费怎么计算？"
- "试用期多长？"

## 🏗️ 架构设计

### 原子化能力分离

项目采用**核心层 + 业务层**的架构设计：

- **核心层（core/）**：纯技术实现，不涉及业务逻辑
  - 文档处理、向量存储、检索、LLM调用
  - 可被任何业务模块复用

- **业务层（modules/）**：独立的业务模块
  - 每个模块有自己的配置和提示词
  - 易于扩展新业务（财务、IT、行政等）

### 扩展示例

添加财务模块只需：

```
modules/
└── finance/              # 新建财务模块
    ├── __init__.py
    ├── config.py         # 财务配置
    └── prompts/
        ├── free.yaml
        └── premium.yaml
```

## 💰 商业模式

### 提示词隔离收费

- 核心代码完全开源免费
- 提示词模板隔离在 `modules/*/prompts/`
- 可提供付费的高级提示词优化服务

### 收费项目示例

- 行业专属提示词模板
- 多轮对话优化
- 个性化定制提示词
- 提示词 A/B 测试

## 🛠️ 技术栈

- **前端**：Streamlit
- **RAG框架**：LangChain
- **向量数据库**：ChromaDB
- **嵌入模型**：Sentence Transformers
- **LLM**：DeepSeek / 智谱AI / Ollama
- **文档处理**：纯 TXT 格式（初版）

## 🤖 本地模型支持

### 为什么使用本地模型？

- ✅ **完全免费** - 无需 API Key
- 🔒 **数据隐私** - 所有数据留在本地
- 🌐 **离线可用** - 不依赖网络
-  **节省成本** - 开发调试零成本

### 安装 Ollama（Windows）

1. 下载 Ollama：https://ollama.com/download/windows
2. 安装后运行：
   ```bash
   ollama pull qwen2.5:1.5b
   ```
3. 等待模型下载完成（约 1-2 GB）

### 推荐模型

| 模型 | 内存占用 | 速度 | 质量 | 适用场景 |
|------|---------|------|------|---------||
| **qwen2.5:1.5b** | ~2-3 GB | 快 | 好 | 本地调试，零成本 |
| qwen2.5:0.5b | ~1 GB | 很快 | 中等 | 快速测试 |

### 云端模型（推荐）

**DeepSeek（首选推荐）** ⭐
- **性价比最高** - API 价格最低（¥0.001/千Token）
- **推理能力强** - 适合问答场景
- **中文支持好** - 国内团队，中文优化
- **获取 Key**: https://platform.deepseek.com/

配置示例：
```env
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=sk-xxx
```

**成本对比**（每月 10 万次问答）：
| 模型 | 月成本 | 推荐度 |
|------|--------|--------||
| **DeepSeek** | ¥50 | ⭐⭐⭐⭐⭐ |
| 通义千问 | ¥200 | ⭐⭐⭐⭐ |
| 智谱 GLM | ¥250 | ⭐⭐⭐ |

## 📝 开发说明

### 添加新业务模块

1. 在 `modules/` 下创建新目录
2. 添加 `config.py` 配置
3. 在 `prompts/` 下添加提示词
4. 在 `app.py` 中集成

### 修改提示词

直接编辑 `modules/*/prompts/*.yaml` 文件

### 更换 LLM 提供商

在 `core/llm_client.py` 中添加新的 provider 支持

## 🔒 安全最佳实践

### API Key 安全

✅ **必须做到：**
1. `.env` 文件已添加到 `.gitignore`，不会被提交
2. 使用系统环境变量代替 `.env` 文件（生产环境）
3. 定期轮换 API Key
4. 不要在任何代码中硬编码 API Key

⚠️ **常见错误：**
- ❌ 将 `.env` 提交到 Git
- ❌ 在代码中硬编码 API Key
- ❌ 在日志中输出 API Key
- ❌ 将 API Key 发送给他人

### 启动脚本

项目提供了安全的启动脚本：
- `start.bat` (Windows)
- `start.sh` (Linux/Mac)

启动脚本会自动检查环境变量配置

## 🌐 GitHub Pages 宣传

可以使用 GitHub Pages 创建项目宣传页面：

1. 创建 `docs/` 目录
2. 添加 `index.md` 宣传页
3. 在仓库设置中启用 GitHub Pages

## ☁️ 云端部署

### Streamlit Community Cloud（免费）

项目已配置好所有必要文件，可以直接部署到 Streamlit Cloud：

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "准备部署"
   git push
   ```

2. **访问 Streamlit Cloud**
   - 网址：https://share.streamlit.io/
   - 点击 "New app"
   - 选择你的仓库

3. **配置 Secrets**
   在应用设置中添加：
   ```toml
   LLM_PROVIDER = "deepseek"
   LLM_MODEL = "deepseek-chat"
   DEEPSEEK_API_KEY = "sk-你的API_KEY"
   ```

4. **等待部署完成**
   - 首次部署需要 5-10 分钟
   - 会自动安装依赖和下载模型

详细部署指南请查看：[DEPLOYMENT.md](DEPLOYMENT.md)

### 注意事项

- Streamlit Cloud 免费版使用临时存储，向量数据库会在重启后丢失
- 可以上传文档到 `data/hr/` 目录，系统会自动处理
- 无活跃用户时应用会休眠，下次访问需要 1-2 分钟启动

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [智谱AI开放平台](https://open.bigmodel.cn/)
- [Streamlit文档](https://docs.streamlit.io/)
- [LangChain文档](https://python.langchain.com/)

---

Made with ❤️ by StaffFAQ Team
