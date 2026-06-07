"""
日志查看器
用于查看和分析 RAG 问答日志
"""

import os
import json
from datetime import datetime
from core.logger import Logger


def view_today_logs():
    """查看今天的日志"""
    logger = Logger(log_dir="logs")
    logs_text = logger.get_today_logs()
    
    print(logs_text)


def view_log_by_date(date_str: str):
    """查看指定日期的日志"""
    logger = Logger(log_dir="logs")
    logs_text = logger.get_logs_by_date(date_str)
    
    print(logs_text)


def main():
    """主函数"""
    print("=" * 80)
    print("RAG 问答日志查看器")
    print("=" * 80)
    print("\n请选择操作：")
    print("1. 查看今天的日志")
    print("2. 查看指定日期的日志")
    print("3. 清理旧日志（保留最近 7 天）")
    print("=" * 80)
    
    choice = input("\n请输入选项 (1-3): ").strip()
    
    if choice == "1":
        view_today_logs()
    elif choice == "2":
        date_str = input("请输入日期 (YYYY-MM-DD): ").strip()
        view_log_by_date(date_str)
    elif choice == "3":
        logger = Logger(log_dir="logs")
        logger.clear_old_logs(days=7)
        print("✅ 旧日志清理完成")
    else:
        print("❌ 无效选项")


if __name__ == "__main__":
    main()
