# Streamlit Cloud 部署故障排查

## 常见错误及解决方案

###  错误 1：TypeError - chromadb/opentelemetry 冲突

**错误信息**：
```
TypeError: This app has encountered an error...
File ".../chromadb/telemetry/opentelemetry/..."
```

**原因**：
- Streamlit Cloud 使用 Python 3.14（最新版本）
- `chromadb` 和新版 `opentelemetry` 在 Python 3.14 上还不稳定
- 依赖包版本不兼容

**✅ 解决方案**（已修复）：
1. 锁定依赖包版本范围
2. 添加 `opentelemetry` 相关包的版本限制
3. 确保所有包在 Python 3.11-3.14 上兼容

**已更新的 requirements.txt**：
```
chromadb>=0.4.0,<0.6.0
opentelemetry-api>=1.20.0,<2.0.0
opentelemetry-sdk>=1.20.0,<2.0.0
opentelemetry-exporter-otlp-proto-grpc>=1.20.0,<2.0.0
```

### ❌ 错误 2：ModuleNotFoundError

**错误信息**：
```
ModuleNotFoundError: No module named 'xxx'
```

**原因**：
- requirements.txt 中缺少依赖包
- 包名写错

**✅ 解决方案**：
1. 检查 requirements.txt 是否包含所有需要的包
2. 确保包名正确（区分大小写）
3. 查看日志确认具体缺少的包

###  错误 3：ImportError

**错误信息**：
```
ImportError: cannot import name 'xxx' from 'yyy'
```

**原因**：
- 包版本不兼容
- API 变更

**✅ 解决方案**：
1. 锁定包的版本范围（如本项目的 requirements.txt）
2. 检查代码是否使用了已废弃的 API

### ❌ 错误 4：超时错误

**错误信息**：
```
Error: Timeout
```

**原因**：
- 依赖包太多，安装超时
- 模型下载超时

**✅ 解决方案**：
1. 减少不必要的依赖
2. 使用轻量级模型
3. 等待更长时间（首次部署可能需要 10-15 分钟）

### ❌ 错误 5：内存不足

**错误信息**：
```
Error: Out of Memory
```

**原因**：
- 文档太大
- 模型太大

**✅ 解决方案**：
1. 减少文档数量（建议 5-10 个）
2. 减小文档大小（每个 < 50 KB）
3. 使用更轻量的模型

## 调试步骤

### 1. 查看日志

在 Streamlit Cloud 应用页面：
1. 点击右下角的 **"Manage app"**
2. 点击 **"Logs"** 标签
3. 查看错误堆栈信息

### 2. 本地测试

在部署前，先在本地测试：
```bash
# 激活虚拟环境
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 运行应用
streamlit run app.py
```

### 3. 检查配置

确认以下配置：
- ✅ requirements.txt 包含所有依赖
- ✅ .env 或 Secrets 配置正确
- ✅ app.py 是主入口文件
- ✅ 代码已推送到 GitHub

## 预防措施

### ✅ 最佳实践

1. **锁定依赖版本**：使用版本范围而非最新版本
2. **本地测试**：部署前在本地完整测试
3. **最小化依赖**：只安装必要的包
4. **文档优化**：控制文档数量和大小
5. **监控日志**：定期检查应用日志

### ⚠️ 常见陷阱

- ❌ 使用 `*` 或无上限的版本（如 `>=1.0`）
- ❌ 在代码中硬编码 API Key
- ❌ 提交 `.env` 文件到 Git
- ❌ 使用不稳定的最新包版本
- ❌ 文档过大或过多

## 本项目已应用的修复

### 1. 依赖版本锁定

所有关键依赖都设置了上限版本，确保兼容性：
- `chromadb>=0.4.0,<0.6.0`
- `langchain>=0.1.0,<0.4.0`
- `opentelemetry-*>=1.20.0,<2.0.0`

### 2. Streamlit 配置优化

在 `.streamlit/config.toml` 中添加：
- 关闭 CORS（减少错误）
- 关闭数据收集（提高隐私）
- 统一主题样式

### 3. 环境变量支持

代码支持从环境变量读取配置：
- 本地：`.env` 文件
- 云端：Streamlit Secrets

## 如果问题仍然存在

1. **清除缓存**：在 "Manage app" 中点击 "Clear cache"
2. **重新部署**：推送新代码触发重新部署
3. **查看 Issue**：检查 GitHub 是否有类似问题
4. **联系支持**：Streamlit 社区论坛或 GitHub Issues

## 相关链接

- Streamlit Cloud 文档：https://docs.streamlit.io/streamlit-community-cloud
- Streamlit 论坛：https://discuss.streamlit.io/
- 本项目 GitHub：（你的仓库地址）
