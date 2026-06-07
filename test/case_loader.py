"""
测试用例加载器
自动加载 test/cases 目录下的所有测试用例
"""

import os
import sys
import importlib
from typing import List
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.models import TestCase


class TestCaseLoader:
    """测试用例加载器"""
    
    def __init__(self, cases_dir: str = None):
        """
        初始化加载器
        
        Args:
            cases_dir: 测试用例目录路径（默认为 test/cases）
        """
        if cases_dir is None:
            # 默认使用 test/cases 目录
            self.cases_dir = Path(__file__).parent / "cases"
        else:
            self.cases_dir = Path(cases_dir)
        
        if not self.cases_dir.exists():
            raise FileNotFoundError(f"测试用例目录不存在：{self.cases_dir}")
    
    def load_all_tests(self) -> List[TestCase]:
        """
        加载所有测试用例
        
        Returns:
            所有测试用例列表
        """
        all_tests = []
        
        # 遍历 cases 目录下的所有 Python 文件
        for test_file in sorted(self.cases_dir.glob("test_*.py")):
            tests = self._load_from_file(test_file)
            all_tests.extend(tests)
            print(f"[加载] {test_file.name}: {len(tests)} 个测试用例")
        
        print(f"\n[总计] 加载了 {len(all_tests)} 个测试用例\n")
        return all_tests
    
    def load_by_category(self, category: str) -> List[TestCase]:
        """
        按类别加载测试用例
        
        Args:
            category: 类别名称（如 "annual_leave"）
            
        Returns:
            该类别的测试用例列表
        """
        test_file = self.cases_dir / f"test_{category}.py"
        
        if not test_file.exists():
            raise FileNotFoundError(f"测试文件不存在：{test_file}")
        
        tests = self._load_from_file(test_file)
        print(f"[加载] {test_file.name}: {len(tests)} 个测试用例\n")
        return tests
    
    def _load_from_file(self, file_path: Path) -> List[TestCase]:
        """
        从单个文件加载测试用例
        
        Args:
            file_path: 测试文件路径
            
        Returns:
            测试用例列表
        """
        # 动态导入模块
        module_name = f"test.cases.{file_path.stem}"
        
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            print(f"[错误] 无法加载 {file_path.name}: {str(e)}")
            return []
        
        # 查找所有 get_*_tests() 函数
        tests = []
        for attr_name in dir(module):
            if attr_name.startswith("get_") and attr_name.endswith("_tests"):
                func = getattr(module, attr_name)
                if callable(func):
                    try:
                        result = func()
                        if isinstance(result, list):
                            tests.extend(result)
                    except Exception as e:
                        print(f"[错误] 执行 {attr_name} 失败: {str(e)}")
        
        return tests
    
    def list_categories(self) -> List[str]:
        """
        列出所有可用的测试类别
        
        Returns:
            类别名称列表
        """
        categories = []
        for test_file in sorted(self.cases_dir.glob("test_*.py")):
            # 从文件名提取类别（去掉 test_ 前缀和 .py 后缀）
            category = test_file.stem.replace("test_", "")
            categories.append(category)
        
        return categories


if __name__ == "__main__":
    # 测试加载器
    loader = TestCaseLoader()
    
    print("=" * 60)
    print("  可用的测试类别")
    print("=" * 60)
    categories = loader.list_categories()
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    print()
    
    print("=" * 60)
    print("  加载所有测试用例")
    print("=" * 60)
    all_tests = loader.load_all_tests()
    
    print("=" * 60)
    print("  测试用例详情")
    print("=" * 60)
    for i, test in enumerate(all_tests, 1):
        print(f"{i}. [{test.description}]")
        print(f"   问题：{test.question}")
        print(f"   期望分类：{test.expected_categories}")
        print()
