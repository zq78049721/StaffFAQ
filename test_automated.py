"""
自动化测试框架
测试问题分类、提示词加载、回答质量
"""

import os
import sys
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import LLMClient
from core.question_classifier import QuestionClassifier
from core.prompt_manager import PromptManager
from core.retriever import Retriever
from core.vector_store import VectorStore
from core.embedding_manager import EmbeddingManager
from test.models import TestCase, TestResult
from test.case_loader import TestCaseLoader



class AutomatedTester:
    """自动化测试器"""
    
    def __init__(self, api_key: str = "", use_llm: bool = True):
        """
        初始化测试器
        
        Args:
            api_key: DeepSeek API Key（可选，如果不传则从环境变量读取）
            use_llm: 是否使用 LLM 进行分类和生成回答
        """
        # 配置 LLM
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            os.environ["LLM_PROVIDER"] = "deepseek"
            os.environ["LLM_MODEL"] = "deepseek-chat"
        
        provider = os.getenv("LLM_PROVIDER", "deepseek")
        model = os.getenv("LLM_MODEL", "deepseek-chat")
        temperature = float(os.getenv("TEMPERATURE", "0.2"))
        
        self.llm_client = LLMClient(provider=provider, model=model, temperature=temperature)
        
        # 初始化组件
        self.classifier = QuestionClassifier(llm_client=self.llm_client if use_llm else None)
        self.prompt_manager = PromptManager()
        
        # 初始化向量存储和检索器
        try:
            embedding_manager = EmbeddingManager()
            vector_store = VectorStore(embedding_manager=embedding_manager)
            self.retriever = Retriever(vector_store=vector_store)
            self.use_retrieval = True
        except Exception as e:
            print(f"[警告] 向量库初始化失败，将跳过文档检索测试：{str(e)}")
            self.use_retrieval = False
        
        self.test_results = []
    
    def run_single_test(self, test_case: TestCase) -> TestResult:
        """
        运行单个测试用例
        
        Args:
            test_case: 测试用例
            
        Returns:
            测试结果
        """
        result = TestResult(test_case)
        start_time = time.time()
        
        try:
            # 1. 测试分类器
            actual_categories = self.classifier.classify(test_case.question)
            result.actual_categories = actual_categories
            
            # 检查分类是否正确
            if set(actual_categories) == set(test_case.expected_categories):
                result.passed_checks.append(f"✅ 分类正确：{actual_categories}")
            else:
                result.failed_checks.append(
                    f"❌ 分类错误：期望 {test_case.expected_categories}，实际 {actual_categories}"
                )
            
            # 2. 测试提示词加载
            if test_case.expected_prompt:
                # 根据分类获取对应的提示词
                primary_category = actual_categories[0] if actual_categories else 'general'
                
                # PromptManager 的 prompts 字典以文件名为 key（不含 .yaml）
                # 例如：annual_leave.yaml -> key 是 "annual_leave"
                if primary_category in self.prompt_manager.prompts:
                    prompt_template = self.prompt_manager.prompts[primary_category]
                    result.actual_prompt = primary_category + ".yaml"
                    
                    if test_case.expected_prompt == result.actual_prompt:
                        result.passed_checks.append(f"✅ 提示词加载正确：{test_case.expected_prompt}")
                    else:
                        result.failed_checks.append(
                            f"❌ 提示词加载错误：期望 {test_case.expected_prompt}，实际 {result.actual_prompt}"
                        )
                else:
                    result.failed_checks.append(
                        f"❌ 提示词不存在：分类 '{primary_category}' 没有对应的提示词文件"
                    )
            
            # 3. 测试文档检索（如果启用）
            retrieved_docs = []
            if self.use_retrieval:
                try:
                    # Retriever 的方法是 search()，返回 List[Dict]
                    search_results = self.retriever.search(test_case.question)
                    if search_results:
                        result.passed_checks.append(f"✅ 检索到 {len(search_results)} 条相关文档")
                        # 转换为 Document 对象格式（兼容后续处理）
                        from langchain_core.documents import Document
                        retrieved_docs = [
                            Document(page_content=r['content'], metadata={'source': r['source'], 'category': r['category']})
                            for r in search_results
                        ]
                    else:
                        result.failed_checks.append("️ 未检索到相关文档")
                except Exception as e:
                    result.failed_checks.append(f"⚠️ 文档检索失败：{str(e)}")
            
            # 4. 生成回答并测试质量
            context = "\n\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else ""
            
            # 构建完整提示词
            primary_category = actual_categories[0] if actual_categories else 'general'
            
            # 使用 PromptManager.build_prompt() 方法构建完整提示词
            try:
                full_prompt = self.prompt_manager.build_prompt(
                    version="free",  # 默认版本
                    question=test_case.question,
                    context=context,
                    category=primary_category  # 优先使用类别专属提示词
                )
            except Exception as e:
                # 降级：使用通用提示词
                full_prompt = f"""请回答以下问题：

参考信息：
{context}

用户问题：
{test_case.question}

请基于参考信息给出准确、简洁的回答。"""
            
            answer = self.llm_client.generate(full_prompt)
            result.actual_answer = answer
            
            # 5. 检查回答质量
            # 检查必须包含的内容
            for keyword in test_case.must_contain:
                if keyword.lower() in answer.lower():
                    result.passed_checks.append(f"✅ 包含关键词：'{keyword}'")
                else:
                    result.failed_checks.append(f"❌ 缺少关键词：'{keyword}'")
            
            # 检查不能包含的内容
            for keyword in test_case.must_not_contain:
                if keyword.lower() not in answer.lower():
                    result.passed_checks.append(f"✅ 不包含禁止词：'{keyword}'")
                else:
                    result.failed_checks.append(f"❌ 包含禁止词：'{keyword}'")
            
            # 判断测试是否通过
            result.is_passed = len(result.failed_checks) == 0
            
        except Exception as e:
            result.error = str(e)
            result.is_passed = False
            result.failed_checks.append(f"❌ 测试执行异常：{str(e)}")
        
        result.duration = time.time() - start_time
        self.test_results.append(result)
        
        return result
    
    def run_tests(self, test_cases: List[TestCase]) -> List[TestResult]:
        """
        批量运行测试
        
        Args:
            test_cases: 测试用例列表
            
        Returns:
            测试结果列表
        """
        print(f"\n{'='*60}")
        print(f"  开始自动化测试")
        print(f"  测试用例数：{len(test_cases)}")
        print(f"{'='*60}\n")
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"[{i}/{len(test_cases)}] 测试：{test_case.description or test_case.question[:50]}")
            result = self.run_single_test(test_case)
            results.append(result)
            
            status = "✅ 通过" if result.is_passed else "❌ 失败"
            print(f"       结果：{status} (耗时 {result.duration:.2f}s)")
            if result.failed_checks:
                for check in result.failed_checks:
                    print(f"       {check}")
            print()
        
        return results
    
    def generate_report(self, output_dir: str = "test/results") -> Dict:
        """
        生成测试报告
        
        Args:
            output_dir: 输出目录路径（默认为 test/results）
            
        Returns:
            报告数据
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.is_passed)
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0
        avg_duration = sum(r.duration for r in self.test_results) / total if total > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": round(pass_rate, 2),
                "avg_duration": round(avg_duration, 2),
                "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "results": [r.to_dict() for r in self.test_results]
        }
        
        # 生成文件名（带时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"test_report_{timestamp}.json")
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 同时保存最新报告（方便查看）
        latest_file = os.path.join(output_dir, "latest_report.json")
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print(f"\n{'='*60}")
        print(f"  测试报告")
        print(f"{'='*60}")
        print(f"  总测试数：{total}")
        print(f"  通过：{passed}")
        print(f"  失败：{failed}")
        print(f"  通过率：{pass_rate:.2f}%")
        print(f"  平均耗时：{avg_duration:.2f}s")
        print(f"  报告已保存至：{output_file}")
        print(f"  最新报告：{latest_file}")
        print(f"{'='*60}\n")
        
        return report
    
    def get_failed_tests(self) -> List[TestResult]:
        """获取失败的测试用例"""
        return [r for r in self.test_results if not r.is_passed]





if __name__ == "__main__":
    # 支持命令行传入 API Key
    api_key = ""
    category = "all"  # 默认运行所有测试
    
    # 解析命令行参数
    for arg in sys.argv[1:]:
        if arg.startswith("sk-"):
            api_key = arg
            print(f"[配置] 使用命令行传入的 API Key: {api_key[:10]}...")
        elif not arg.startswith("-"):
            category = arg
            print(f"[配置] 测试类别：{category}")
    
    # 创建测试器
    tester = AutomatedTester(api_key=api_key)
    
    # 加载测试用例
    loader = TestCaseLoader()
    
    if category == "all":
        print("\n" + "="*60)
        print("  加载所有测试用例")
        print("="*60 + "\n")
        test_cases = loader.load_all_tests()
    else:
        print(f"\n{'='*60}")
        print(f"  加载测试类别：{category}")
        print(f"{'='*60}\n")
        try:
            test_cases = loader.load_by_category(category)
        except FileNotFoundError as e:
            print(f"[错误] {str(e)}")
            print(f"\n可用的测试类别：{loader.list_categories()}")
            sys.exit(1)
    
    if not test_cases:
        print("[错误] 没有加载到任何测试用例")
        sys.exit(1)
    
    # 运行测试
    tester.run_tests(test_cases)
    
    # 生成报告
    report = tester.generate_report()
    
    # 显示失败的测试
    failed = tester.get_failed_tests()
    if failed:
        print(f"\n{'='*60}")
        print(f"  失败的测试详情")
        print(f"{'='*60}\n")
        for i, result in enumerate(failed, 1):
            print(f"{i}. 问题：{result.test_case.question}")
            print(f"   描述：{result.test_case.description}")
            print(f"   失败原因：")
            for check in result.failed_checks:
                print(f"     {check}")
            print(f"   实际回答：{result.actual_answer[:200]}...")
            print()
