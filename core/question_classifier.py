"""
问题分类器
基于 LLM 的智能多标签分类器
"""

from typing import Dict, List
import json


class QuestionClassifier:
    """问题分类器 - 基于 LLM 语义理解"""
    
    # 分类定义：标签 -> 描述
    CATEGORIES = {
        'overtime': {
            'name': '加班',
            'description': '加班时间、加班费计算（1.5倍/2倍/3倍）、延时工作规定'
        },
        'annual_leave': {
            'name': '年假',
            'description': '年假天数、年假条件、带薪年休假、年假使用规则'
        },
        'maternity': {
            'name': '产假',
            'description': '产假天数、哺乳假、陪产假、怀孕保护、流产假、育儿假'
        },
        'probation': {
            'name': '试用期',
            'description': '试用期期限、试用期工资、转正考核、试用期权利'
        },
        'attendance': {
            'name': '考勤',
            'description': '上下班时间、迟到早退、旷工、打卡规则、弹性工作制'
        },
        'salary': {
            'name': '薪酬',
            'description': '基本工资、绩效工资、奖金、补贴（交通/餐补/通讯）、年终奖'
        },
        'leave': {
            'name': '请假',
            'description': '事假、病假、婚假、丧假、请假流程、请假审批'
        },
        'termination': {
            'name': '离职',
            'description': '辞职、辞退、解除合同、经济补偿金、裁员、开除'
        },
        'insurance': {
            'name': '社保',
            'description': '五险一金、养老保险、医疗保险、失业保险、公积金'
        },
    }
    
    def __init__(self, llm_client=None):
        """
        初始化分类器
        
        Args:
            llm_client: LLM 客户端对象（用于智能分类）
        """
        self.llm_client = llm_client
    
    def classify(self, question: str, use_llm: bool = True) -> List[str]:
        """
        分类用户问题（支持多标签）
        
        Args:
            question: 用户问题
            use_llm: 是否使用 LLM 分类（默认 True）
            
        Returns:
            分类标签列表（如 ['annual_leave', 'leave']）
        """
        if use_llm and self.llm_client:
            return self._llm_classify(question)
        else:
            # 降级到关键词分类（单标签）
            return [self._keyword_classify(question)]
    
    def _llm_classify(self, question: str) -> List[str]:
        """
        使用 LLM 进行智能多标签分类
        
        Args:
            question: 用户问题
            
        Returns:
            分类标签列表
        """
        # 构建分类提示词
        categories_desc = "\n".join([
            f"- {tag}: {info['name']} - {info['description']}"
            for tag, info in self.CATEGORIES.items()
        ])
        
        prompt = f"""你是一个专业的人事政策问题分类器。请将用户的问题分类到以下类别中。

【可选类别】
{categories_desc}

【分类规则】
1. 一个问题可能涉及多个类别，请返回所有相关类别
2. 如果没有匹配的类别，返回 ["general"]
3. 只返回 JSON 格式的类别标签列表，不要任何解释

【用户问题】
{question}

【输出格式】
["category1", "category2"]

请直接输出 JSON 列表：
"""
        
        try:
            # 调用 LLM 分类
            response = self.llm_client.generate(prompt, temperature=0.1)
            
            # 解析 JSON 结果
            # 提取 JSON 部分（可能包含在代码块中）
            import re
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                categories = json.loads(json_match.group())
                # 验证类别有效性
                valid_categories = [cat for cat in categories if cat in self.CATEGORIES or cat == 'general']
                return valid_categories if valid_categories else ['general']
            else:
                return ['general']
                
        except Exception as e:
            print(f"[分类器] LLM 分类失败，降级到关键词模式：{str(e)}")
            return [self._keyword_classify(question)]
    
    def _keyword_classify(self, question: str) -> str:
        """
        关键词分类（降级方案）
        
        Args:
            question: 用户问题
            
        Returns:
            单个分类标签
        """
        keyword_to_category = {
            '加班': 'overtime', '加班费': 'overtime', '延时工作': 'overtime',
            '年假': 'annual_leave', '年休假': 'annual_leave', '带薪休假': 'annual_leave',
            '产假': 'maternity', '生育': 'maternity', '哺乳': 'maternity',
            '试用期': 'probation', '转正': 'probation',
            '考勤': 'attendance', '迟到': 'attendance', '早退': 'attendance', '旷工': 'attendance',
            '工资': 'salary', '薪酬': 'salary', '奖金': 'salary', '补贴': 'salary',
            '请假': 'leave', '事假': 'leave', '病假': 'leave',
            '离职': 'termination', '辞职': 'termination', '辞退': 'termination',
            '社保': 'insurance', '公积金': 'insurance', '五险一金': 'insurance',
        }
        
        for keyword, category in keyword_to_category.items():
            if keyword in question:
                return category
        
        return 'general'
    
    def get_category_description(self, category: str) -> str:
        """
        获取分类的描述信息
        
        Args:
            category: 分类标签
            
        Returns:
            分类描述
        """
        if category in self.CATEGORIES:
            info = self.CATEGORIES[category]
            return f"{info['name']} - {info['description']}"
        return '一般性问题'
    
    def list_categories(self) -> List[str]:
        """列出所有支持的分类"""
        return list(self.CATEGORIES.keys()) + ['general']
