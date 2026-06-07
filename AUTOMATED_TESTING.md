# 自动化测试使用指南

## 📁 文件结构

```
test/
├── __init__.py                    # Python 包标识
├── case_loader.py                 # 测试用例加载器
├── cases/                         # 测试用例目录
│   ├── __init__.py
│   ├── test_annual_leave.py      # 年假相关测试
│   ├── test_overtime.py          # 加班相关测试
│   ├── test_maternity.py         # 产假相关测试
│   └── test_multi_label.py       # 多标签分类测试
├── results/                       # 测试结果目录
│   ├── latest_report.json        # 最新测试报告
│   └── test_report_*.json        # 历史测试报告（带时间戳）
└── test_automated.py              # 自动化测试主程序（在根目录）
```

---

## 📚 测试框架原理

### **核心架构**

```
测试用例 (TestCase)
    ↓
自动化测试器 (AutomatedTester)
    ↓
├─ 分类器测试 (QuestionClassifier)
├─ 提示词加载测试 (PromptManager)
├─ 文档检索测试 (Retriever)
└─ 回答质量测试 (LLMClient)
    ↓
测试结果 (TestResult)
    ↓
测试报告 (test_report.json)
```

---

## 🔍 测试流程详解

### **1. 测试用例设计**

每个测试用例包含以下要素：

```python
TestCase(
    question="用户问题",                      # 测试问题
    expected_categories=["annual_leave"],     # 期望的分类结果
    expected_prompt="annual_leave.yaml",      # 期望加载的提示词
    must_contain=["10天"],                    # 回答中必须包含的内容
    must_not_contain=["25天"],                # 回答中不能包含的内容
    description="测试用例描述"                 # 测试说明
)
```

**关键字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `question` | str | ✅ | 用户提问的原始文本 |
| `expected_categories` | List[str] | ✅ | 期望的分类标签列表（支持多标签） |
| `expected_prompt` | str | ❌ | 期望加载的提示词文件名 |
| `must_contain` | List[str] | ❌ | 回答中必须出现的关键词 |
| `must_not_contain` | List[str] | ❌ | 回答中绝对不能出现的关键词 |
| `description` | str | ❌ | 测试用例的描述说明 |

---

### **2. 测试执行流程**

#### **步骤 1：分类器测试**
```python
actual_categories = classifier.classify(question)
# 检查：actual_categories == expected_categories
```

**测试点：**
- ✅ 分类准确性：是否正确识别问题所属模块
- ✅ 多标签支持：是否能识别多个相关分类
- ✅ 降级机制：LLM 失败时是否回退到关键词分类

---

#### **步骤 2：提示词加载测试**
```python
prompt_template = prompt_manager.get_prompt(primary_category)
# 检查：是否加载了正确的提示词文件
```

**测试点：**
- ✅ 提示词映射：分类 → 提示词文件的对应关系
- ✅ 模板完整性：提示词是否包含必要的占位符（{context}, {question}）

---

#### **步骤 3：文档检索测试**
```python
retrieved_docs = retriever.retrieve(question, top_k=3)
# 检查：是否检索到相关文档
```

**测试点：**
- ✅ 检索相关性：返回的文档是否与问题相关
- ✅ 检索数量：是否返回合理数量的文档
- ⚠️ 容错处理：向量库不可用时是否优雅降级

---

#### **步骤 4：回答生成测试**
```python
answer = llm_client.generate(full_prompt)
# 检查：回答是否符合质量要求
```

**测试点：**
- ✅ 关键词检查：回答是否包含必须的内容
- ✅ 禁止词检查：回答是否避免了错误内容
- ✅ 简洁性：回答长度是否合理（由提示词控制）
- ✅ 逻辑正确性：推理过程是否正确（依赖 LLM 能力）

---

### **3. 测试结果判定**

```python
is_passed = len(failed_checks) == 0
```

**通过条件：**
- 所有 `must_contain` 关键词都出现在回答中
- 所有 `must_not_contain` 关键词都不在回答中
- 分类结果与期望一致
- 没有发生异常错误

**失败原因示例：**
- ❌ 分类错误：期望 `["annual_leave"]`，实际 `["general"]`
- ❌ 缺少关键词：回答中没有出现 "10天"
- ❌ 包含禁止词：回答中出现了错误的 "25天"
- ❌ 提示词加载错误：期望 `annual_leave.yaml`，实际加载了其他文件

---

## 🚀 使用方法

### **方式 1：运行所有测试（推荐）**

```bash
# Windows
run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300

# Linux/Mac
./run_tests.sh sk-cbe6232d3c47455bb502d46b8a804300
```

**效果：**
- 自动加载 `test/cases/` 目录下所有测试文件
- 执行所有测试用例
- 生成报告到 `test/results/` 目录

---

### **方式 2：运行指定类别的测试**

```bash
# 只测试年假
run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300 annual_leave

# 只测试加班
run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300 overtime

# 只测试产假
run_tests.bat sk-cbe6232d3c47455bb502d46b8a804300 maternity
```

**可用类别：**
- `annual_leave` - 年假相关
- `overtime` - 加班相关
- `maternity` - 产假相关
- `multi_label` - 多标签分类

---

### **方式 3：直接运行 Python**

```bash
# 运行所有测试
python test_automated.py sk-cbe6232d3c47455bb502d46b8a804300

# 运行指定类别
python test_automated.py sk-cbe6232d3c47455bb502d46b8a804300 annual_leave
```

---

## 📊 测试报告解读

运行测试后会生成报告文件到 `test/results/` 目录：

- `latest_report.json` - 最新测试报告（每次覆盖）
- `test_report_20260607_152630.json` - 历史报告（带时间戳）

```json
{
  "summary": {
    "total_tests": 5,
    "passed": 4,
    "failed": 1,
    "pass_rate": 80.0,
    "avg_duration": 3.25,
    "test_time": "2026-06-01 15:30:00"
  },
  "results": [
    {
      "question": "我工龄10年能休多少天年假？",
      "description": "测试年假天数计算（10年工龄）",
      "expected_categories": ["annual_leave"],
      "actual_categories": ["annual_leave"],
      "passed_checks": [
        "✅ 分类正确：['annual_leave']",
        "✅ 提示词加载正确：annual_leave.yaml",
        "✅ 包含关键词：'10天'",
        "✅ 不包含禁止词：'25天'"
      ],
      "failed_checks": [],
      "is_passed": true,
      "duration": 2.85,
      "answer_preview": "根据您的工龄，法定年假为10天..."
    }
  ]
}
```

**关键字段：**

| 字段 | 说明 |
|------|------|
| `pass_rate` | 通过率（越高越好） |
| `avg_duration` | 平均耗时（秒，越低越快） |
| `passed_checks` | 通过的检查项列表 |
| `failed_checks` | 失败的检查项列表 |
| `answer_preview` | 回答预览（前 200 字符） |

---

## 🎯 测试用例设计最佳实践

### **1. 覆盖边界情况**

```python
# 工龄边界测试
TestCase(
    question="我刚好工作满10年，年假是多少天？",
    expected_categories=["annual_leave"],
    must_contain=["10天"],
    description="测试工龄边界值（10年整）"
),

TestCase(
    question="工作9年11个月，年假多少天？",
    expected_categories=["annual_leave"],
    must_contain=["5天"],
    description="测试工龄边界值（未满10年）"
)
```

---

### **2. 测试多标签分类**

```python
TestCase(
    question="请假流程和年假天数有什么关系？",
    expected_categories=["leave", "annual_leave"],
    description="测试多标签分类（同时涉及请假和年假）"
)
```

---

### **3. 测试错误推算防护**

```python
TestCase(
    question="我工作15年，年假是10+15=25天吗？",
    expected_categories=["annual_leave"],
    must_not_contain=["25天", "累加"],
    must_contain=["10天"],
    description="测试模型是否会做错误的线性累加"
)
```

---

### **4. 测试时间逻辑判断**

```python
TestCase(
    question="明天请5天年假，现在申请可以吗？",
    expected_categories=["annual_leave", "leave"],
    must_contain=["提前", "不符合"],
    must_not_contain=["可以立即申请"],
    description="测试提前申请时间的逻辑判断"
)
```

---

### **5. 测试答非所问防护**

```python
TestCase(
    question="后天请假，现在申请可以吗？",
    expected_categories=["leave"],
    must_contain=["请假流程", "审批"],
    must_not_contain=["年假天数", "10天"],
    description="测试模型是否会根据问题类型灵活回答"
)
```

---

## 💡 Token 成本估算

### **单次测试消耗**

| 阶段 | 输入 Token | 输出 Token | 合计 |
|------|-----------|-----------|------|
| 分类器 | ~200 | ~20 | 220 |
| 提示词构建 | ~500 | - | 500 |
| 回答生成 | ~800 | ~150 | 950 |
| **单次总计** | **~1500** | **~170** | **~1670** |

### **批量测试成本**

假设 DeepSeek 价格：
- 输入：0.14 元 / 百万 token
- 输出：0.28 元 / 百万 token

**100 个测试用例成本：**
```
输入：100 × 1500 = 150,000 token → 0.021 元
输出：100 × 170 = 17,000 token → 0.005 元
总计：约 0.026 元（2.6 分钱）
```

**结论：完全不用担心成本！**

---

## 🔧 高级用法

### **1. 只测试分类器**

```python
from test_automated import AutomatedTester, TestCase

tester = AutomatedTester(use_llm=False)  # 禁用 LLM，只用关键词分类
test_case = TestCase(
    question="加班费怎么算？",
    expected_categories=["overtime"]
)
result = tester.run_single_test(test_case)
print(result.actual_categories)  # ['overtime']
```

---

### **2. 获取失败测试详情**

```python
failed_tests = tester.get_failed_tests()
for result in failed_tests:
    print(f"问题：{result.test_case.question}")
    print(f"失败原因：{result.failed_checks}")
    print(f"实际回答：{result.actual_answer}")
```

---

### **3. 自定义测试报告格式**

```python
report = tester.generate_report(output_file="my_custom_report.json")

# 访问摘要信息
print(f"通过率：{report['summary']['pass_rate']}%")
print(f"总耗时：{report['summary']['avg_duration']}s")
```

---

## ⚠️ 注意事项

### **1. 向量库依赖**

如果向量库未初始化或文档未导入，文档检索测试会跳过：

```
[警告] 向量库初始化失败，将跳过文档检索测试
```

**解决方案：**
```bash
python rebuild_vector_db.py
```

---

### **2. Temperature 设置**

建议在测试时使用较低的 temperature（0.1-0.2），确保回答稳定性：

```env
TEMPERATURE=0.2
```

---

### **3. 测试用例维护**

- ✅ 每次新增功能时，添加对应的测试用例
- ✅ 发现 bug 时，先写测试用例复现问题
- ✅ 定期审查测试用例，删除过时的用例
- ✅ 保持测试用例的独立性，避免相互依赖

---

## 📈 持续集成建议

### **GitHub Actions 示例**

```yaml
name: Automated Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run automated tests
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: python test_automated.py
      
      - name: Upload test report
        uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: test_report.json
```

---

## 🎓 总结

### **测试框架核心价值**

1. **自动化回归测试**：每次修改代码后快速验证功能是否正常
2. **质量保障**：通过关键词检查确保回答符合预期
3. **成本控制**：批量测试成本极低（100 次测试约 0.03 元）
4. **持续改进**：根据失败测试不断优化提示词和模型配置

### **下一步行动**

1. ✅ 运行示例测试：`run_tests.bat sk-你的APIKey`
2. ✅ 查看测试报告：打开 `test/results/latest_report.json`
3. ✅ 添加自己的测试用例：在 `test/cases/` 目录创建新文件
4. ✅ 定期运行测试：每次修改提示词或代码后执行

---

## 💡 如何添加新的测试用例

### **步骤 1：创建新的测试文件**

在 `test/cases/` 目录下创建新文件，例如 `test_salary.py`：

```python
"""
测试用例集合 - 薪酬相关
"""

from typing import List
from test_automated import TestCase


def get_salary_tests() -> List[TestCase]:
    """获取薪酬相关的测试用例"""
    return [
        TestCase(
            question="基本工资是多少？",
            expected_categories=["salary"],
            expected_prompt="salary.yaml",
            description="测试基本工资查询"
        ),
        # 更多测试用例...
    ]
```

**命名规范：**
- 文件名：`test_<类别>.py`
- 函数名：`get_<类别>_tests()`
- 必须返回 `List[TestCase]`

---

### **步骤 2：自动加载**

测试加载器会自动发现并加载所有 `test/cases/test_*.py` 文件中的测试用例。

**无需修改任何代码！**

运行测试时会自动包含新添加的测试：

```bash
# 运行所有测试（包括新添加的）
run_tests.bat sk-你的APIKey

# 或者只运行新类别
run_tests.bat sk-你的APIKey salary
```

---

### **步骤 3：查看结果**

测试报告保存在 `test/results/` 目录：

- `latest_report.json` - 最新测试报告（每次覆盖）
- `test_report_20260607_152630.json` - 历史报告（带时间戳）

---

**有任何问题随时询问！🚀**
