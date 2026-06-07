"""
日志管理器
记录 RAG 问答流程的关键信息

功能：
- 记录用户问题
- 记录问题分类结果
- 记录检索到的文档
- 记录 LLM 回答
- 支持按日期分文件存储
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional


class Logger:
    """RAG 问答日志管理器"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        初始化日志管理器
        
        Args:
            log_dir: 日志目录
        """
        self.log_dir = log_dir
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            print(f"✅ 创建日志目录：{self.log_dir}")
    
    def _get_log_file(self) -> str:
        """
        获取今天的日志文件路径
        
        Returns:
            日志文件路径（格式：logs/2026-06-01.jsonl）
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"{today}.jsonl")
    
    def log_qa_session(
        self,
        question: str,
        categories: List[str],
        category_descriptions: Dict[str, str],
        retrieved_docs: List[Dict],
        llm_model: str,
        answer: str,
        duration: float = 0.0,
        metadata: Optional[Dict] = None
    ):
        """
        记录一次完整的问答会话（纯文本格式）
        
        Args:
            question: 用户问题
            categories: 识别出的问题类别列表
            category_descriptions: 类别描述字典
            retrieved_docs: 检索到的文档列表
            llm_model: 使用的 LLM 模型名称
            answer: LLM 生成的回答
            duration: 处理耗时（秒）
            metadata: 其他元数据（可选）
        """
        # 构建日志条目（纯文本格式）
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_lines = []
        log_lines.append(f"⏰ 时间: {timestamp}")
        log_lines.append(f"❓ 用户问题: {question}")
        log_lines.append("")
        
        # 分类信息
        log_lines.append(f"🏷️  问题分类: {', '.join(categories)}")
        for cat in categories:
            desc = category_descriptions.get(cat, "")
            if desc:
                log_lines.append(f"   - {cat}: {desc}")
        log_lines.append("")
        
        # 检索文档
        log_lines.append(f"📄 检索到的文档 ({len(retrieved_docs)} 个):")
        for i, doc in enumerate(retrieved_docs, 1):
            content_preview = doc.get('content', '')[:200]
            source = doc.get('source', 'unknown')
            category = doc.get('category', 'unknown')
            score = doc.get('score', 0.0)
            
            log_lines.append(f"   [{i}] 来源: {source}")
            log_lines.append(f"       类别: {category}")
            log_lines.append(f"       相似度: {score:.4f}")
            log_lines.append(f"       内容: {content_preview}...")
            log_lines.append("")
        
        # LLM 生成
        log_lines.append(f"🤖 使用模型: {llm_model}")
        log_lines.append(f"💬 AI 回答:")
        log_lines.append(answer)
        log_lines.append("")
        
        # 性能指标
        log_lines.append(f"⚡ 处理耗时: {duration:.3f}s")
        
        # 添加分隔线
        separator = "=" * 80
        log_entry = separator + "\n" + "\n".join(log_lines) + "\n" + separator + "\n\n"
        
        # 写入日志文件（纯文本格式）
        log_file = self._get_log_file()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        # 同时在控制台输出简要信息
        self._print_summary(timestamp, question, categories, len(retrieved_docs), llm_model, answer, duration)
    
    def _print_summary(self, timestamp: str, question: str, categories: List[str], 
                      doc_count: int, model: str, answer: str, duration: float):
        """在控制台打印简要日志"""
        print("\n" + "=" * 80)
        print("📝 问答日志记录")
        print("=" * 80)
        print(f"⏰ 时间: {timestamp}")
        print(f"❓ 问题: {question[:100]}...")
        print(f"🏷️  分类: {', '.join(categories)}")
        print(f"📄 检索: {doc_count} 个文档")
        print(f"🤖 模型: {model}")
        print(f"💬 回答: {answer[:100]}...")
        print(f"⚡ 耗时: {duration:.3f}s")
        print("=" * 80)
    
    def get_today_logs(self) -> str:
        """
        获取今天的日志（纯文本）
        
        Returns:
            日志文本内容
        """
        log_file = self._get_log_file()
        
        if not os.path.exists(log_file):
            return "📭 今天还没有问答记录"
        
        with open(log_file, "r", encoding="utf-8") as f:
            return f.read()
    
    def get_logs_by_date(self, date_str: str) -> str:
        """
        获取指定日期的日志（纯文本）
        
        Args:
            date_str: 日期字符串（格式：YYYY-MM-DD）
            
        Returns:
            日志文本内容
        """
        log_file = os.path.join(self.log_dir, f"{date_str}.jsonl")
        
        if not os.path.exists(log_file):
            return f"📭 {date_str} 没有问答记录"
        
        with open(log_file, "r", encoding="utf-8") as f:
            return f.read()
    
    def clear_old_logs(self, days: int = 7):
        """
        清理旧日志（保留最近 N 天）
        
        Args:
            days: 保留天数
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(self.log_dir):
            if filename.endswith(".jsonl"):
                # 从文件名提取日期
                try:
                    file_date = datetime.strptime(filename.replace(".jsonl", ""), "%Y-%m-%d")
                    if file_date < cutoff_date:
                        os.remove(os.path.join(self.log_dir, filename))
                        print(f"🗑️  删除旧日志：{filename}")
                except ValueError:
                    pass  # 跳过格式不正确的文件名
