"""
提示词管理器
负责加载和管理提示词模板
"""

import os
import yaml
from typing import Dict


class PromptManager:
    """提示词管理器"""
    
    def __init__(self, module_name: str = "hr"):
        """
        初始化提示词管理器
        
        Args:
            module_name: 模块名称（如 hr, finance）
        """
        self.module_name = module_name
        self.prompts_dir = os.path.join("modules", module_name, "prompts")
        self.prompts = {}
        self.load_prompts()
    
    def load_prompts(self):
        """加载所有提示词文件"""
        if not os.path.exists(self.prompts_dir):
            print(f"警告：提示词目录不存在 - {self.prompts_dir}")
            return
        
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                filepath = os.path.join(self.prompts_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        # 使用文件名（不含扩展名）作为 key
                        key = filename.replace('.yaml', '').replace('.yml', '')
                        self.prompts[key] = yaml.safe_load(f)
                        print(f"✓ 加载提示词：{key}")
                except Exception as e:
                    print(f"✗ 加载提示词失败 {filename}: {str(e)}")
    
    def get_prompt(self, version: str = "free") -> Dict:
        """
        获取指定版本的提示词
        
        Args:
            version: 提示词版本（free 或 premium）
            
        Returns:
            提示词配置字典
        """
        if version not in self.prompts:
            raise ValueError(f"提示词版本 '{version}' 不存在，可用版本：{list(self.prompts.keys())}")
        return self.prompts[version]
    
    def build_prompt(self, version: str, question: str, context: str) -> str:
        """
        构建完整的提示词
        
        Args:
            version: 提示词版本
            question: 用户问题
            context: 检索到的上下文
            
        Returns:
            完整的提示词字符串
        """
        prompt_config = self.get_prompt(version)
        
        system_message = prompt_config.get('system_message', '')
        template = prompt_config.get('template', '')
        
        # 填充模板
        full_prompt = f"{system_message}\n\n{template}".format(
            context=context,
            question=question
        )
        
        return full_prompt
    
    def is_premium(self, version: str) -> bool:
        """
        判断是否为付费版本
        
        Args:
            version: 提示词版本
            
        Returns:
            是否为付费版本
        """
        prompt_config = self.get_prompt(version)
        return prompt_config.get('tier') == 'premium'
    
    def list_versions(self) -> list:
        """
        列出所有可用的提示词版本
        
        Returns:
            版本列表
        """
        return list(self.prompts.keys())
