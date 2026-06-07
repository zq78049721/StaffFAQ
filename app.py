"""
FastAPI 后端 API 服务器
提供 RESTful API 接口供前端调用
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import uuid
from dotenv import load_dotenv

# 导入核心模块
from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from core.retriever import Retriever
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager
from core.question_classifier import QuestionClassifier
from core.embedding_manager import EmbeddingManager
from core.logger import Logger

# 导入 HR 模块配置
from modules.hr.config import DATA_DIR

# 支持命令行参数传入 API Key
if len(sys.argv) > 1:
    api_key = sys.argv[1]
    if api_key.startswith("sk-"):
        print(f"[配置] 从命令行参数读取 API Key: {api_key[:10]}...")
        os.environ["DEEPSEEK_API_KEY"] = api_key
        os.environ["LLM_PROVIDER"] = "deepseek"
        os.environ["LLM_MODEL"] = "deepseek-chat"
        os.environ["TEMPERATURE"] = "0.2"
    else:
        print(f"[警告] API Key 格式不正确，应该以 sk- 开头")
        print(f"[提示] 使用方式: python app.py sk-xxxxxxxxxxx")
        sys.exit(1)

# 加载环境变量（如果命令行未传入，则从 .env 读取）
load_dotenv()

app = FastAPI(title="StaffFAQ API", version="1.0.0")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 会话存储（内存中，生产环境建议使用 Redis）
sessions = {}

# 全局组件单例（服务器启动时初始化一次）
global_components = None

# 初始化任务（用于异步初始化）
init_task = None

# 初始化状态
init_status = {
    'ready': False,
    'progress': 0,
    'message': '等待初始化...',
    'error': None
}


async def background_init():
    """后台异步初始化组件"""
    global global_components, init_status
    try:
        print("[INFO] 开始后台初始化系统组件...")
        init_status['progress'] = 10
        init_status['message'] = '正在加载配置...'
        
        global_components = initialize_components()
        
        init_status['progress'] = 50
        init_status['message'] = '正在加载向量数据库...'
        
        # 自动处理文档（如果需要）
        if not os.path.exists("chroma_db"):
            if os.path.exists(DATA_DIR) and any(f.endswith('.txt') for f in os.listdir(DATA_DIR)):
                init_status['progress'] = 70
                init_status['message'] = '正在处理文档...'
                print("[INFO] 检测到文档，正在处理...")
                splits = global_components['processor'].process_directory(DATA_DIR)
                if splits:
                    global_components['vector_store'].create_from_documents(splits)
                    print(f"[INFO] 文档处理完成，共 {len(splits)} 个文本块")
        
        init_status['progress'] = 100
        init_status['message'] = '初始化完成！'
        init_status['ready'] = True
        print("[INFO] 系统初始化完成！")
    except Exception as e:
        init_status['ready'] = False
        init_status['error'] = str(e)
        init_status['message'] = f'初始化失败：{str(e)}'
        print(f"[ERROR] 初始化失败：{str(e)}")


@app.on_event("startup")
async def startup_event():
    """服务器启动时开始后台初始化"""
    global init_task
    # 在后台启动初始化任务
    import asyncio
    init_task = asyncio.create_task(background_init())


# 请求模型
class ChatRequest(BaseModel):
    session_id: str
    message: str


class InitRequest(BaseModel):
    pass


# 初始化系统组件
def initialize_components():
    """初始化所有组件"""
    try:
        # 文档处理器
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        
        # 嵌入模型管理器（统一管理嵌入模型）
        embedding_manager = EmbeddingManager(
            model_name="all-MiniLM-L6-v2",
            device="cpu"
        )
        
        # 向量存储（使用嵌入模型管理器）
        vector_store = VectorStore(persist_directory="chroma_db")
        
        # 检索器
        retriever = Retriever(vector_store=vector_store, top_k=3)
        
        # LLM 客户端
        provider = os.getenv("LLM_PROVIDER", "deepseek")
        model = os.getenv("LLM_MODEL", "deepseek-chat")
        temperature = float(os.getenv("TEMPERATURE", "0.2"))  # 从 .env 读取，默认 0.2
        llm_client = LLMClient(provider=provider, model=model, temperature=temperature)
        
        # 提示词管理器
        prompt_manager = PromptManager(module_name="hr")
        
        # 问题分类器（传入 LLM 客户端以支持智能分类）
        question_classifier = QuestionClassifier(llm_client=llm_client)
        
        # 日志管理器
        logger = Logger(log_dir="logs")
        
        return {
            'processor': processor,
            'vector_store': vector_store,
            'retriever': retriever,
            'llm_client': llm_client,
            'prompt_manager': prompt_manager,
            'question_classifier': question_classifier,
            'logger': logger
        }
    except Exception as e:
        raise Exception(f"初始化失败：{str(e)}")


def ask_question(components, question, prompt_version="free"):
    """回答问题（支持多标签分类 + 日志记录）"""
    import time
    
    start_time = time.time()
    
    try:
        # 1. 多标签分类用户问题
        classifier = components['question_classifier']
        categories = classifier.classify(question, use_llm=True)
        
        print(f"[分类] 识别到的类别：{categories}")
        for cat in categories:
            print(f"  - {cat}: {classifier.get_category_description(cat)}")
        
        # 2. 按多个类别并行检索相关文档
        all_results = []
        seen_content = set()  # 去重
        
        for category in categories:
            if category == 'general':
                # 通用问题，不按类别过滤
                results = components['retriever'].search(question, category=None)
            else:
                results = components['retriever'].search(question, category=category)
            
            # 合并结果并去重
            for result in results:
                content_key = result['content'][:100]  # 用前 100 字符作为去重标识
                if content_key not in seen_content:
                    all_results.append(result)
                    seen_content.add(content_key)
        
        if not all_results:
            answer = "抱歉，没有找到相关的文档内容。"
            duration = time.time() - start_time
            
            # 记录日志
            logger = components['logger']
            logger.log_qa_session(
                question=question,
                categories=categories,
                category_descriptions={
                    cat: classifier.get_category_description(cat) 
                    for cat in categories
                },
                retrieved_docs=[],
                llm_model="N/A",
                answer=answer,
                duration=duration
            )
            
            return answer, []
        
        # 3. 格式化上下文
        context = components['retriever'].format_context(all_results)
        
        print(f"[检索] 共检索到 {len(all_results)} 个相关文档片段")
        
        # 4. 构建提示词（传入类别，自动选择专属提示词）
        prompt = components['prompt_manager'].build_prompt(
            version=prompt_version,
            question=question,
            context=context,
            category=categories[0] if categories else None  # 使用第一个类别
        )
        
        # 5. 生成回答
        response = components['llm_client'].generate(prompt)
        
        # 6. 计算耗时
        duration = time.time() - start_time
        
        # 7. 记录日志
        logger = components['logger']
        logger.log_qa_session(
            question=question,
            categories=categories,
            category_descriptions={
                cat: classifier.get_category_description(cat) 
                for cat in categories
            },
            retrieved_docs=all_results,
            llm_model=components['llm_client'].model,
            answer=response,
            duration=duration
        )
        
        return response, all_results
        
    except Exception as e:
        return f"处理问题时出错：{str(e)}", []


# API 路由

@app.get("/")
async def serve_index():
    """提供首页"""
    print("[INFO] 收到首页请求")
    return FileResponse("static/index.html")


@app.post("/api/init")
async def init_session():
    """初始化会话"""
    print("[INFO] 收到 /api/init 请求")
    try:
        # 检查组件是否已初始化
        if not init_status['ready']:
            raise HTTPException(status_code=503, detail="系统正在初始化中，请稍候...")
        
        # 创建新会话（共享全局组件）
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            'components': global_components,
            'messages': []
        }
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "会话初始化成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口"""
    try:
        session_id = request.session_id
        message = request.message
        
        # 检查会话是否存在
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        session = sessions[session_id]
        components = session['components']
        
        # 添加用户消息到历史
        session['messages'].append({"role": "user", "content": message})
        
        # 处理问题
        response, results = ask_question(components, message, "free")
        
        # 添加助手回复到历史
        session['messages'].append({"role": "assistant", "content": response})
        
        # 格式化参考来源
        sources = []
        if results:
            sources = [
                {
                    "source": result.get("source", "未知"),
                    "content": result.get("content", "")
                }
                for result in results
            ]
        
        return {
            "success": True,
            "response": response,
            "sources": sources,
            "message": "请求成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """获取初始化状态"""
    return {
        "ready": init_status['ready'],
        "progress": init_status['progress'],
        "message": init_status['message'],
        "error": init_status['error']
    }


if __name__ == "__main__":
    import uvicorn
    # 使用 reload 模式时需要传入模块路径字符串
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
