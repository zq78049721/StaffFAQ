"""
测试用例集合 - 多标签分类
"""

from typing import List
from test.models import TestCase


def get_multi_label_tests() -> List[TestCase]:
    """获取多标签分类相关的测试用例"""
    return [
        TestCase(
            question="请假流程和年假天数有什么关系？",
            expected_categories=["leave", "annual_leave"],
            description="测试多标签分类（同时涉及请假和年假）"
        ),
        TestCase(
            question="加班后怎么申请调休？",
            expected_categories=["overtime", "leave"],
            description="测试多标签分类（加班+请假）"
        ),
        TestCase(
            question="产假期间的工资怎么发？",
            expected_categories=["maternity", "salary"],
            description="测试多标签分类（产假+薪酬）"
        ),
        TestCase(
            question="试用期可以请年假吗？",
            expected_categories=["probation", "annual_leave"],
            description="测试多标签分类（试用期+年假）"
        ),
    ]
