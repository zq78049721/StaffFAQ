# RAG 问答日志系统使用指南

## 📁 日志目录结构

```
logs/
├── 2026-06-01.jsonl    # 今天的日志（纯文本格式）
├── 2026-05-31.jsonl    # 昨天的日志
└── 2026-05-30.jsonl    # 前天的日志
```

**格式说明**：
- 日志文件按日期命名（`YYYY-MM-DD.jsonl`）
- **纯文本格式**，用 `========` 分隔每条记录
- 自动创建，无需手动管理
- 可直接用记事本或任何文本编辑器打开查看

---

## 🔍 记录的关键信息

每次问答会话会记录以下信息（纯文本格式）：

### **日志示例**

```
================================================================================
⏰ 时间: 2026-06-01 14:30:25
❓ 用户问题: 工作满 10 年年假多少天？

🏷️  问题分类: annual_leave
   - annual_leave: 年假天数、年假条件、带薪年休假、年假使用规则

📄 检索到的文档 (3 个):
   [1] 来源: data/legal/labor_law.txt
       类别: annual_leave
       相似度: 0.9200
       内容: 职工累计工作已满 1 年不满 10 年的，年休假 5 天；已满 10 年不满 20 年的，年休假 10 天...

   [2] 来源: data/hr/company_policy.txt
       类别: annual_leave
       相似度: 0.8700
       内容: 公司年假政策：工作满 1 年可享受 5 天年假，满 3 年 10 天...

🤖 使用模型: qwen2.5:1.5b
💬 AI 回答:
根据《职工带薪年休假条例》规定，工作满 10 年不满 20 年的员工，年休假为 10 天。

⚡ 处理耗时: 2.345s
================================================================================
```

---

## 🛠️ 使用方法

### **方法 1：交互式查看器（推荐）**

运行日志查看工具：

```powershell
.\rag_env\Scripts\python.exe view_logs.py
```

功能：
- ✅ 查看今天的日志
- ✅ 查看指定日期的日志
- ✅ 查看统计信息（分类分布、模型使用等）
- ✅ 清理旧日志

---

### **方法 2：直接查看原始文件**

日志文件是 JSONL 格式，可以用任何文本编辑器打开：

```powershell
# 用记事本打开今天的日志
notepad logs\2026-06-01.jsonl

# 或用 VSCode 打开
code logs\2026-06-01.jsonl
```

---

### **方法 3：编程方式读取**

```python
from core.logger import Logger

logger = Logger(log_dir="logs")

# 获取今天的日志
today_logs = logger.get_today_logs()

# 获取指定日期的日志
logs = logger.get_logs_by_date("2026-06-01")

# 遍历日志
for log in today_logs:
    print(f"问题: {log['question']}")
    print(f"分类: {log['classification']['categories']}")
    print(f"回答: {log['generation']['answer']}")
```

---

## 📊 日志示例

一条完整的日志记录：

```json
{
  "timestamp": "2026-06-01T14:30:25.123456",
  "question": "工作满 10 年年假多少天？",
  "classification": {
    "categories": ["annual_leave"],
    "descriptions": {
      "annual_leave": "年假天数、年假条件、带薪年休假、年假使用规则"
    }
  },
  "retrieval": {
    "doc_count": 3,
    "documents": [
      {
        "index": 1,
        "content": "职工累计工作已满 1 年不满 10 年的，年休假 5 天；已满 10 年不满 20 年的，年休假 10 天...",
        "source": "data/legal/labor_law.txt",
        "category": "annual_leave",
        "score": 0.92
      },
      {
        "index": 2,
        "content": "公司年假政策：工作满 1 年可享受 5 天年假，满 3 年 10 天...",
        "source": "data/hr/company_policy.txt",
        "category": "annual_leave",
        "score": 0.87
      }
    ]
  },
  "generation": {
    "model": "qwen2.5:1.5b",
    "answer": "根据《职工带薪年休假条例》规定，工作满 10 年不满 20 年的员工，年休假为 10 天。"
  },
  "performance": {
    "duration_seconds": 2.345
  }
}
```

---

## 🗑️ 日志清理

日志会自动按日期分文件存储，建议定期清理旧日志：

```powershell
# 运行清理工具（保留最近 7 天）
.\rag_env\Scripts\python.exe view_logs.py
# 选择选项 4
```

或者编程方式清理：

```python
from core.logger import Logger

logger = Logger(log_dir="logs")
logger.clear_old_logs(days=7)  # 保留最近 7 天
```

---

## 💡 使用场景

### **1. 调试问题**
- 用户反馈回答错误 → 查看日志中的检索文档
- 检查是否正确检索到相关法条
- 分析 LLM 是否误解了上下文

### **2. 性能优化**
- 查看每次问答的响应时间
- 分析哪些类别的问题耗时较长
- 优化检索策略

### **3. 数据分析**
- 统计热门问题类型
- 分析用户关注点
- 优化知识库内容

### **4. 审计追溯**
- 记录所有问答历史
- 便于事后审查
- 符合企业合规要求

---

## 🎯 按类别分离提示词

系统支持**按问题类别加载专属提示词**，提高回答质量。

### **提示词文件结构**

```
modules/hr/prompts/
├── free.yaml              # 默认免费版提示词
├── premium.yaml           # 默认付费版提示词
├── annual_leave.yaml      # 年假专属提示词 ⭐
├── overtime.yaml          # 加班专属提示词 ⭐
├── maternity.yaml         # 产假专属提示词 ⭐
└── ...                    # 其他类别
```

### **工作流程**

```
用户提问：“我工龄 10 年年假多少天？”
        ↓
【步骤 1】LLM 智能分类
  识别出类别：annual_leave（年假）
        ↓
【步骤 2】自动加载专属提示词
  加载 modules/hr/prompts/annual_leave.yaml
        ↓
【步骤 3】构建提示词
  使用年假专属的系统消息和模板
        ↓
【步骤 4】LLM 生成回答
  基于专属提示词 + 检索到的文档
        ↓
返回更精准的回答
```

### **专属提示词的优势**

1. **更专业的角色定位**
   - 年假提示词：“你是专业的年假政策顾问”
   - 加班提示词：“你是专业的加班政策顾问”

2. **更严格的约束**
   - “不要自行推算或编造年假天数”
   - “优先引用劳动法条款”

3. **更有针对性的回答要求**
   - 年假：明确说明不同工龄的天数
   - 加班：明确说明 1.5倍/2倍/3倍 标准
   - 产假：明确说明基础产假 + 奖励产假

### **如何添加新的类别提示词**

1. 在 `modules/hr/prompts/` 目录下创建新的 YAML 文件
2. 文件名与类别名一致（如 `probation.yaml`）
3. 包含以下字段：
   ```yaml
   category: "probation"
   name: "试用期问答"
   
   system_message: |
     你是专业的试用期政策顾问...
   
   template: |
     你是公司的人事助手，专门解答试用期相关问题...
   ```
4. 系统会自动加载，无需修改代码

---

## ⚠️ 注意事项

1. **隐私保护**：日志包含用户问题，注意数据安全
2. **存储空间**：长期运行会产生大量日志，定期清理
3. **Git 忽略**：`logs/` 目录已加入 `.gitignore`，不会提交到代码库
4. **生产环境**：建议配置日志轮转和压缩策略

---

## 🎯 下一步优化建议

1. **添加日志级别**：DEBUG/INFO/WARNING/ERROR
2. **异步写入**：避免阻塞主线程
3. **日志压缩**：自动压缩旧日志文件
4. **可视化界面**：Web 界面查看和分析日志
5. **告警机制**：异常回答自动告警
