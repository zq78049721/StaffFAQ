"""
测试用例集合 - 产假相关
"""

from typing import List
from test.models import TestCase


def get_maternity_tests() -> List[TestCase]:
    """获取产假相关的测试用例"""
    return [
        TestCase(
            question="女职工产假有多少天？",
            expected_categories=["maternity"],
            expected_prompt="maternity.yaml",
            must_contain=["98天"],
            description="测试产假天数"
        ),
        TestCase(
            question="难产可以增加多少天产假？",
            expected_categories=["maternity"],
            expected_prompt="maternity.yaml",
            must_contain=["15天"],
            description="测试难产额外产假"
        ),
        TestCase(
            question="男职工陪产假有多少天？",
            expected_categories=["maternity"],
            expected_prompt="maternity.yaml",
            description="测试陪产假天数"
        ),
        TestCase(
            question="哺乳假怎么规定？",
            expected_categories=["maternity"],
            expected_prompt="maternity.yaml",
            description="测试哺乳假政策"
        ),
    ]
