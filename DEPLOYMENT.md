# Streamlit Community Cloud 部署指南

## 部署步骤

### 1. 推送代码到 GitHub

确保你的代码已经推送到 GitHub 仓库：

```bash
git add .
git commit -m "准备部署到 Streamlit Cloud"
git push
```

### 2. 连接到 Streamlit Community Cloud

1. 访问：https://share.streamlit.io/
2. 点击 "New app"
3. 选择你的 GitHub 仓库
4. 配置部署选项：
   - **Repository**: 你的仓库名
   - **Branch**: main (或 master)
   - **Main file path**: app.py
   - **Advanced settings**: 需要配置 Secrets（见下文）

### 3. 配置 Secrets（重要！）

在 Streamlit Cloud 的应用设置中，添加以下 Secrets：

```toml
# LLM 配置
LLM_PROVIDER = "deepseek"
LLM_MODEL = "deepseek-chat"

# API Keys
DEEPSEEK_API_KEY = "sk-你的真实API_KEY"
```

**如何添加 Secrets：**
1. 在 Streamlit Cloud 的应用页面，点击右上角的 "" 菜单
2. 选择 "Secrets"
3. 粘贴上面的配置（替换为你的真实 API Key）
4. 保存

### 4. 等待部署完成

Streamlit Cloud 会自动：
- 安装 requirements.txt 中的依赖
- 下载必要的模型文件
- 启动应用

首次部署可能需要 5-10 分钟。

## 注意事项

### 免费版的限制

- **内存**: 1 GB RAM
- **CPU**: 共享 CPU
- **存储**: 1 GB（临时存储，重启后清空）
- **运行时间**: 无活跃用户时会自动休眠
- **重启**: 每次代码更新或 24 小时后自动重启

### 数据存储问题

由于 Streamlit Cloud 使用临时存储：

**问题**: ChromaDB 向量存储会在重启后丢失

**解决方案**:

#### 方案 1：使用外部向量数据库（推荐）
考虑使用云端的向量数据库服务：
- Pinecone
- Weaviate Cloud
- Qdrant Cloud

#### 方案 2：每次启动时重新处理文档
修改代码，在启动时自动处理文档（适合文档量小的情况）

#### 方案 3：使用 GitHub 存储文档
将处理好的向量存储提交到 GitHub（不推荐，文件会很大）

### 性能优化建议

1. **减少模型大小**: 使用更小的嵌入模型
2. **缓存数据**: 使用 `@st.cache_data` 缓存处理结果
3. **减少文档数量**: 只保留核心文档
4. **优化切分**: 减少文本块数量

## 环境变量配置

### 方式一：Streamlit Secrets（推荐）

在 Streamlit Cloud 的 Secrets 中配置，会被自动加载为环境变量。

### 方式二：代码中读取

代码已经使用 `os.getenv()` 读取环境变量，Streamlit Cloud 会自动注入 Secrets。

## 监控和日志

- 查看应用日志：Streamlit Cloud 应用页面 → "⋮" → "Logs"
- 查看错误信息：Logs 中会显示详细的错误堆栈
- 性能监控：使用 Streamlit 内置的监控工具

## 常见问题

### 部署失败

1. **依赖安装失败**: 检查 requirements.txt 格式
2. **内存不足**: 减少模型大小或文档数量
3. **超时**: 首次部署可能较慢，耐心等待

### 运行时错误

1. **API Key 未找到**: 检查 Secrets 配置
2. **模型下载失败**: 检查网络连接
3. **文件未找到**: 确认文件路径正确

### 应用休眠

免费版会在无活跃用户时休眠，下次访问时会重新启动（需要 1-2 分钟）。

## 升级到付费版

如果需要更稳定的服务，可以考虑：

- **Streamlit for Teams**: $26/用户/月
- **自建服务器**: 使用 Docker 部署到自己的服务器

## 备用方案

如果 Streamlit Cloud 不够用，可以考虑：

1. **Hugging Face Spaces**: 也支持 Streamlit，更灵活
2. **Railway**: 提供免费的 Streamlit 托管
3. **Render**: 免费层支持 Web 应用
4. **自建 VPS**: 使用 Docker 部署
