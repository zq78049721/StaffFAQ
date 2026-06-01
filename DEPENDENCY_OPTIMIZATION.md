# Streamlit Cloud 依赖优化指南

##  问题说明

Streamlit Cloud 的机制是**每次重启都会重新创建虚拟环境并安装依赖**，这是平台的设计，无法完全避免。但可以通过以下方法**大幅优化安装速度**。

---

##  优化方案

### 方案 1：精简依赖包（推荐）

减少不必要的依赖可以显著加快安装速度。

#### 当前依赖分析

```
必须保留：
✅ streamlit - 前端框架
✅ langchain - RAG 核心框架
✅ langchain-chroma - 向量存储
✅ langchain-huggingface - 嵌入模型
✅ langchain-text-splitters - 文本切分
✅ chromadb - 向量数据库
✅ sentence-transformers - 嵌入模型
✅ openai - DeepSeek API 调用
✅ python-dotenv - 环境变量
✅ PyYAML - 提示词配置

可以优化：
️ zhipuai - 如果只用 DeepSeek，可以移除
⚠️ opentelemetry-* - 如果不需要遥测，可以移除
⚠️ langchain-community - 如果只用核心功能，可以缩小范围
```

#### 优化后的 requirements.txt

```txt
# 核心框架
streamlit>=1.28.0,<2.0.0
langchain>=0.1.0,<0.3.0
langchain-core>=0.1.0,<0.3.0
langchain-text-splitters>=0.0.1,<0.3.0

# 向量存储和检索
langchain-chroma>=0.1.0,<0.2.0
chromadb>=0.4.0,<0.5.0

# 嵌入模型
langchain-huggingface>=0.0.1,<0.1.0
sentence-transformers>=2.2.0,<3.0.0

# LLM 客户端
openai>=1.0.0,<2.0.0

# 工具库
python-dotenv>=1.0.0
PyYAML>=6.0
```

**优化效果**：
- 减少 3-4 个依赖包
- 安装时间减少约 30-40%
- 内存占用减少约 100-200 MB

---

### 方案 2：固定精确版本

使用精确版本号可以加速依赖解析：

```txt
# 精确版本（安装更快）
streamlit==1.31.0
langchain==0.1.20
langchain-core==0.1.52
langchain-chroma==0.1.4
chromadb==0.5.23
sentence-transformers==2.7.0
openai==1.55.0
python-dotenv==1.0.1
PyYAML==6.0.2
```

**优点**：
- 跳过依赖解析过程
- 安装时间减少 20-30%
- 版本确定性高

**缺点**：
- 需要手动更新版本
- 可能存在安全漏洞（需要定期更新）

---

### 方案 3：使用国内镜像源

Streamlit Cloud 默认使用 PyPI 官方源，速度较慢。可以在代码中配置国内镜像：

在 `app.py` 开头添加：

```python
import subprocess
import sys

# 配置国内镜像源（加速依赖安装）
def setup_pip_mirror():
    """设置 pip 镜像源"""
    subprocess.check_call([
        sys.executable, "-m", "pip", "config", "set", "global.index-url",
        "https://pypi.tuna.tsinghua.edu.cn/simple"
    ])

# 在应用启动时执行
setup_pip_mirror()
```

**注意**：Streamlit Cloud 可能不允许修改 pip 配置，此方法不一定有效。

---

### 方案 4：缓存嵌入模型

`sentence-transformers` 每次启动都会下载模型，这是最耗时的部分。

#### 优化方法

在 `core/vector_store.py` 中添加缓存检查：

```python
import os
import torch
from transformers import AutoTokenizer, AutoModel

# 缓存模型到临时目录
MODEL_CACHE_DIR = "/tmp/models"
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

# 设置缓存路径
os.environ['TRANSFORMERS_CACHE'] = MODEL_CACHE_DIR
os.environ['HF_HOME'] = MODEL_CACHE_DIR
```

**效果**：
- 首次启动：下载模型（3-5 分钟）
- 后续启动：使用缓存（30 秒内）

**注意**：Streamlit Cloud 重启后会清除 `/tmp`，所以这个方法效果有限。

---

##  实际优化建议

### 推荐做法（综合优化）

1. **精简依赖**：移除不需要的包
2. **使用精确版本**：固定版本号
3. **接受现实**：Streamlit Cloud 就是要重新安装依赖

### 优化后的 requirements.txt

```txt
# 核心框架（精确版本）
streamlit==1.31.0
langchain==0.1.20
langchain-core==0.1.52
langchain-text-splitters==0.0.2

# 向量存储
langchain-chroma==0.1.4
chromadb==0.5.23

# 嵌入模型
sentence-transformers==2.7.0

# LLM 客户端
openai==1.55.0

# 工具库
python-dotenv==1.0.1
PyYAML==6.0.2
```

**预期效果**：
- 首次安装：3-5 分钟
- 重启安装：1-2 分钟（比原来快 50%）

---

##  替代方案

如果你实在受不了每次重启都要安装依赖，可以考虑：

### 方案 A：使用 Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 一次性安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

CMD ["streamlit", "run", "app.py"]
```

**优点**：
- 依赖只安装一次
- 启动速度极快（< 10 秒）

**缺点**：
- 需要付费服务器
- 需要自己维护

### 方案 B：使用 Hugging Face Spaces

Hugging Face Spaces 有持久化存储，依赖会缓存：

1. 创建 Space：https://huggingface.co/spaces
2. 选择 Streamlit 模板
3. 上传代码
4. 首次安装后，依赖会缓存

**优点**：
- 免费
- 依赖缓存
- 国内访问较快

**缺点**：
- 需要 Hugging Face 账号
- 配置稍复杂

### 方案 C：本地运行 + 内网穿透

```bash
# 本地运行
streamlit run app.py

# 使用 ngrok 暴露到外网
ngrok http 8501
```

**优点**：
- 完全控制
- 无依赖安装延迟
- 免费

**缺点**：
- 需要电脑一直开着
- 稳定性不如云端

---

##  总结

| 方案 | 安装时间 | 成本 | 复杂度 | 推荐度 |
|------|---------|------|--------|--------|
| Streamlit Cloud（当前） | 1-2 分钟 | 免费 | 低 | ⭐⭐⭐ |
| 精简依赖 + 固定版本 | 1 分钟 | 免费 | 低 | ⭐⭐⭐⭐ |
| Hugging Face Spaces | 首次 3 分钟，后续 10 秒 | 免费 | 中 | ⭐⭐⭐ |
| Docker 部署 | 首次 5 分钟，后续 10 秒 | 付费 | 高 | ⭐⭐ |
| 本地 + 内网穿透 | 0 秒 | 免费 | 中 | ⭐⭐ |

---

##  立即优化

如果你希望立即优化，我可以帮你：

1. **精简 requirements.txt**（移除不需要的包）
2. **固定精确版本**（加速依赖解析）
3. **创建优化后的版本**

需要我现在帮你优化吗？
