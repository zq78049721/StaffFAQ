# Streamlit Cloud 部署检查清单

## 部署前检查

### ✅ 必须项

- [ ] 代码已推送到 GitHub 仓库
- [ ] requirements.txt 包含所有依赖
- [ ] .gitignore 已排除敏感文件
- [ ] app.py 是主程序入口
- [ ] 已在 Streamlit Cloud 配置 Secrets

### ✅ 推荐项

- [ ] 已在本地测试通过
- [ ] 已准备 DeepSeek API Key
- [ ] 已有 TXT 文档在 `data/hr/` 目录
- [ ] README.md 有项目说明

## 配置 Secrets 模板

```toml
LLM_PROVIDER = "deepseek"
LLM_MODEL = "deepseek-chat"
DEEPSEEK_API_KEY = "sk-替换为你的真实API_KEY"
```

## 部署后验证

- [ ] 应用可以正常访问
- [ ] 聊天界面可以正常显示
- [ ] 上传文档功能正常
- [ ] 问答功能正常
- [ ] 查看 Logs 无错误

## 故障排查

### 部署失败

查看 Logs 中的错误信息：
- 依赖安装失败 → 检查 requirements.txt
- 内存不足 → 减少文档数量
- 超时 → 等待更长时间

### 运行错误

- API Key 错误 → 检查 Secrets 配置
- 文件未找到 → 确认文件路径
- 模型下载失败 → 检查网络连接

## 优化建议

- 文档不超过 10 个 TXT 文件
- 每个文件不超过 100 KB
- 定期清理不需要的文档
