# 自动化测试目录

## 📁 目录结构

```
test/
├── README.md                    # 本文件
├── __init__.py                  # Python 包标识
├── case_loader.py               # 测试用例加载器
├── cases/                       # 测试用例目录
│   ├── __init__.py
│   ├── test_annual_leave.py    # 年假相关测试（7个用例）
│   ├── test_overtime.py        # 加班相关测试（4个用例）
│   ├── test_maternity.py       # 产假相关测试（4个用例）
│   └── test_multi_label.py     # 多标签分类测试（4个用例）
├── results/                     # 测试结果目录
│   ├── latest_report.json      # 最新测试报告
│   └── test_report_*.json      # 历史测试报告（带时间戳）
└── test_automated.py            # 自动化测试主程序（在根目录）
```

---

## 🚀 快速开始

### **运行所有测试**

```bash
# Windows
run_tests.bat sk-你的APIKey

# Linux/Mac
./run_tests.sh sk-你的APIKey
```

### **运行指定类别的测试**

```bash
# 只测试年假
run_tests.bat sk-你的APIKey annual_leave

# 只测试加班
run_tests.bat sk-你的APIKey overtime
```

---

## 📝 添加新测试用例

### **1. 创建测试文件**

在 `cases/` 目录下创建新文件，例如 `test_salary.py`：

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
            description="测试基本工资查询"
        ),
    ]
```

### **2. 自动加载**

测试加载器会自动发现并加载所有 `test_*.py` 文件。

**无需修改任何代码！**

---

## 📊 查看测试结果

测试报告会保存到 `results/` 目录：

- `latest_report.json` - 最新报告（每次覆盖）
- `test_report_20260607_152630.json` - 历史报告（带时间戳）

---

## 🔧 核心组件

### **TestCaseLoader** (`case_loader.py`)

负责自动加载测试用例：

```python
loader = TestCaseLoader()

# 加载所有测试
all_tests = loader.load_all_tests()

# 加载指定类别
annual_tests = loader.load_by_category("annual_leave")

# 列出可用类别
categories = loader.list_categories()
```

### **AutomatedTester** (`../test_automated.py`)

负责执行测试和生成报告：

```python
tester = AutomatedTester(api_key="sk-...")

# 运行测试
tester.run_tests(test_cases)

# 生成报告
report = tester.generate_report()
```

---

## 💡 最佳实践

1. **按类别组织**：每个业务模块一个测试文件
2. **命名规范**：文件名 `test_<类别>.py`，函数名 `get_<类别>_tests()`
3. **描述清晰**：每个测试用例都要有清晰的 description
4. **定期运行**：每次修改提示词或代码后运行测试
5. **查看历史**：通过时间戳报告对比不同版本的测试结果

---

## 📈 当前测试统计

| 类别 | 文件 | 用例数 |
|------|------|--------|
| 年假 | test_annual_leave.py | 7 |
| 加班 | test_overtime.py | 4 |
| 产假 | test_maternity.py | 4 |
| 多标签 | test_multi_label.py | 4 |
| **总计** | **4个文件** | **19个用例** |

---

## 🔗 相关文档

- [完整使用指南](../AUTOMATED_TESTING.md)
- [测试框架原理](../AUTOMATED_TESTING.md#测试框架原理)
- [Token成本估算](../AUTOMATED_TESTING.md#token-成本估算)
