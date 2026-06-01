"""
StaffFAQ - 智能人事问答系统
Streamlit 主程序
"""

import streamlit as st
import os
from dotenv import load_dotenv

# 导入核心模块
from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from core.retriever import Retriever
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager

# 导入 HR 模块配置
from modules.hr.config import DATA_DIR, MODULE_NAME, MODULE_DESCRIPTION

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="StaffFAQ - 智能人事助手",
    page_icon="",
    layout="wide"
)


def initialize_components():
    """初始化所有组件"""
    try:
        # 文档处理器
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        
        # 向量存储
        vector_store = VectorStore(persist_directory="chroma_db")
        
        # 检索器
        retriever = Retriever(vector_store=vector_store, top_k=3)
        
        # LLM 客户端
        # 从环境变量读取配置，默认使用 DeepSeek（性价比高）
        provider = os.getenv("LLM_PROVIDER", "deepseek")
        model = os.getenv("LLM_MODEL", "deepseek-chat")
        llm_client = LLMClient(provider=provider, model=model)
        
        # 提示词管理器
        prompt_manager = PromptManager(module_name="hr")
        
        return {
            'processor': processor,
            'vector_store': vector_store,
            'retriever': retriever,
            'llm_client': llm_client,
            'prompt_manager': prompt_manager
        }
    except Exception as e:
        st.error(f"初始化失败：{str(e)}")
        return None


def auto_process_if_needed(components):
    """如果向量存储不存在，自动处理文档（适用于 Streamlit Cloud）"""
    if not os.path.exists("chroma_db"):
        # 检查是否有文档
        if os.path.exists(DATA_DIR) and any(f.endswith('.txt') for f in os.listdir(DATA_DIR)):
            st.info("检测到文档，正在自动处理...")
            if process_documents(components):
                st.success("文档处理完成！")
                return True
            else:
                st.warning("文档处理失败，请手动处理")
                return False
    return True


def process_documents(components):
    """处理文档"""
    with st.spinner("正在处理文档..."):
        try:
            # 处理文档
            splits = components['processor'].process_directory(DATA_DIR)
            
            if not splits:
                st.warning("未找到 TXT 文件，请先上传文档")
                return False
            
            # 创建向量存储
            components['vector_store'].create_from_documents(splits)
            st.success(f"✓ 成功处理 {len(splits)} 个文本块")
            return True
            
        except Exception as e:
            st.error(f"处理失败：{str(e)}")
            return False


def ask_question(components, question, prompt_version="free"):
    """回答问题"""
    try:
        # 检索相关文档
        results = components['retriever'].search(question)
        
        if not results:
            return "抱歉，没有找到相关的文档内容。", []
        
        # 格式化上下文
        context = components['retriever'].format_context(results)
        
        # 构建提示词
        prompt = components['prompt_manager'].build_prompt(
            version=prompt_version,
            question=question,
            context=context
        )
        
        # 生成回答
        response = components['llm_client'].generate(prompt)
        
        return response, results
        
    except Exception as e:
        return f"处理问题时出错：{str(e)}", []


# ==================== 界面 ====================

# 标题
st.title("💼 StaffFAQ - 智能人事助手")
st.markdown(f"**{MODULE_NAME}** | {MODULE_DESCRIPTION}")
st.markdown("---")

# 侧边栏 - Demo 版本隐藏
# prompt_version 默认使用免费版
prompt_version = "free"

# 主区域
# 初始化系统
if 'components' not in st.session_state:
    st.session_state.components = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

# 自动处理文档（Streamlit Cloud 环境）
if st.session_state.components is None:
    with st.spinner("正在初始化系统..."):
        st.session_state.components = initialize_components()
        if st.session_state.components:
            auto_process_if_needed(st.session_state.components)

# 检查系统状态
if not st.session_state.components:
    st.warning("⚠️ 系统初始化失败，请检查：")
    st.info("1. Ollama 服务是否已启动（运行 `ollama list` 检查）")
    st.info("2. .env 文件配置是否正确")
    st.info("3. 查看控制台错误信息")
    st.stop()

# 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入框
if prompt := st.chat_input("请输入你的人事问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 检查系统是否初始化
    if not st.session_state.components:
        st.session_state.components = initialize_components()
    
    if not st.session_state.components:
        with st.chat_message("assistant"):
            st.markdown(" 系统初始化失败，请检查配置")
    else:
        # 处理问题
        with st.chat_message("assistant"):
            with st.spinner("正在思考..."):
                response, results = ask_question(
                    st.session_state.components,
                    prompt,
                    prompt_version
                )
                st.markdown(response)
                
                # 显示参考来源
                if results:
                    with st.expander("📚 查看参考来源"):
                        for i, result in enumerate(results, 1):
                            st.write(f"**来源 {i}**（{result['source']}）")
                            st.write(result['content'])
                            st.write("---")
        
        # 添加助手回复
        st.session_state.messages.append({"role": "assistant", "content": response})

# 页脚
st.markdown("---")
st.markdown(
    "Made with ❤️ by StaffFAQ Team | "
    "[GitHub](https://github.com/yourusername/StaffFAQ)"
)
