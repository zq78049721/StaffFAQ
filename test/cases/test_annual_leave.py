"""
测试用例集合 - 年假相关
"""

from typing import List
from test.models import TestCase


def get_annual_leave_tests() -> List[TestCase]:
    """获取年假相关的测试用例"""
    return [
        TestCase(
            question="我工龄10年能休多少天年假？",
            expected_categories=["annual_leave"],
            expected_prompt="annual_leave.yaml",
            must_contain=["10天"],
            must_not_contain=["25天", "15天"],
            description="测试年假天数计算（10年工龄）"
        ),
        TestCase(
            question="工作9年11个月，年假是多少天？",
            expected_categories=["annual_leave"],
            expected_prompt="annual_leave.yaml",
            must_contain=["5天"],
            must_not_contain=["10天"],
            description="测试年假天数计算（未满10年）"
        ),
        TestCase(
            question="工作满20年，年假有多少天？",
            expected_categories=["annual_leave"],
            expected_prompt="annual_leave.yaml",
            must_contain=["15天"],
            description="测试年假天数计算（20年以上工龄）"
        ),
        TestCase(
            question="明天想请5天年假，现在申请可以吗？",
            expected_categories=["annual_leave", "leave"],
            expected_prompt="annual_leave.yaml",
            must_contain=["提前"],
            must_not_contain=["可以立即申请"],
            description="测试年假申请时间规定"
        ),
        TestCase(
            question="后天请假，现在申请可以吗？",
            expected_categories=["leave"],
            must_contain=["请假流程", "审批"],
            must_not_contain=["年假天数", "10天"],
            description="测试模型是否会根据问题类型灵活回答（非天数查询）"
        ),
        TestCase(
            question="我工作15年，年假是10+15=25天吗？",
            expected_categories=["annual_leave"],
            expected_prompt="annual_leave.yaml",
            must_not_contain=["25天", "累加", "相加"],
            must_contain=["10天"],
            description="测试模型是否会做错误的线性累加"
        ),
        TestCase(
            question="法定年假和福利年假有什么区别？",
            expected_categories=["annual_leave"],
            expected_prompt="annual_leave.yaml",
            description="测试年假类型区分"
        ),
    ]
