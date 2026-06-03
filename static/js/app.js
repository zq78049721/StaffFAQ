// 全局状态
let sessionId = null;
let isReady = false;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 显示加载界面
    showLoadingScreen();
    
    // 开始轮询检查服务器状态
    checkServerStatus();
    
    // 绑定回车键发送
    document.getElementById('user-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

// 显示加载界面
function showLoadingScreen() {
    const container = document.getElementById('chat-messages');
    container.innerHTML = `
        <div id="loading-screen" style="text-align: center; padding: 3rem;">
            <div class="loading-spinner" style="width: 50px; height: 50px; margin: 0 auto 1rem;"></div>
            <h3 style="margin-bottom: 0.5rem; color: #333;">系统初始化中</h3>
            <p id="loading-message" style="color: #666; margin-bottom: 1rem;">正在加载配置...</p>
            <div style="max-width: 400px; margin: 0 auto; background: #e0e0e0; border-radius: 10px; overflow: hidden;">
                <div id="loading-progress" style="height: 8px; background: #4CAF50; transition: width 0.3s ease; width: 0%;"></div>
            </div>
            <p id="loading-percent" style="margin-top: 0.5rem; color: #999; font-size: 0.9em;">0%</p>
        </div>
    `;
}

// 轮询检查服务器状态
function checkServerStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // 更新进度
            document.getElementById('loading-progress').style.width = data.progress + '%';
            document.getElementById('loading-percent').textContent = data.progress + '%';
            document.getElementById('loading-message').textContent = data.message;
            
            if (data.ready) {
                // 初始化成功
                isReady = true;
                initSession();
            } else if (data.error) {
                // 初始化失败
                showErrorScreen(data.error);
            } else {
                // 继续轮询
                setTimeout(checkServerStatus, 500);
            }
        })
        .catch(error => {
            console.error('检查状态失败:', error);
            // 继续轮询
            setTimeout(checkServerStatus, 1000);
        });
}

// 初始化会话
async function initSession() {
    try {
        const response = await fetch('/api/init', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            console.log('会话初始化成功:', sessionId);
            
            // 隐藏加载界面，显示正常聊天界面
            hideLoadingScreen();
        } else {
            showErrorScreen(data.error || '会话初始化失败');
        }
    } catch (error) {
        showErrorScreen('连接服务器失败：' + error.message);
    }
}

// 隐藏加载界面
function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.display = 'none';
    }
    
    // 启用输入框
    document.getElementById('user-input').disabled = false;
    document.getElementById('send-btn').disabled = false;
}

// 显示错误界面
function showErrorScreen(error) {
    const container = document.getElementById('chat-messages');
    container.innerHTML = `
        <div style="text-align: center; padding: 3rem; color: #f44336;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">❌</div>
            <h3 style="margin-bottom: 1rem;">初始化失败</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">${error}</p>
            <button onclick="location.reload()" style="padding: 0.75rem 2rem; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1rem;">重新加载</button>
        </div>
    `;
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 禁用输入
    input.disabled = true;
    document.getElementById('send-btn').disabled = true;
    
    // 显示用户消息
    addMessage('user', message);
    
    // 清空输入框
    input.value = '';
    
    // 显示加载指示器
    showLoading(true);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 显示助手回复
            let responseHtml = data.response;
            
            // 如果有参考来源，附加显示
            if (data.sources && data.sources.length > 0) {
                responseHtml += formatSources(data.sources);
            }
            
            addMessage('assistant', responseHtml);
        } else {
            addMessage('assistant', ' ' + data.error);
        }
    } catch (error) {
        addMessage('assistant', '❌ 请求失败：' + error.message);
    } finally {
        // 恢复输入
        input.disabled = false;
        document.getElementById('send-btn').disabled = false;
        input.focus();
        showLoading(false);
    }
}

// 添加消息到聊天区域
function addMessage(role, content) {
    const container = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    const avatar = role === 'user' ? '' : '🤖';
    
    // 如果是助手消息，使用 marked.js 渲染 Markdown
    const messageContent = role === 'assistant' ? marked.parse(content) : content;
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">${messageContent}</div>
    `;
    
    container.appendChild(messageDiv);
    
    // 滚动到底部
    container.scrollTop = container.scrollHeight;
}

// 格式化参考来源
function formatSources(sources) {
    let html = '<details class="sources-container">';
    html += '<summary style="cursor: pointer; color: #666; font-size: 0.85em;">📚 查看参考来源</summary>';
    html += '<div class="sources-list">';
    
    sources.forEach((source, index) => {
        html += `
            <div class="source-item">
                <strong>来源 ${index + 1}</strong>（${source.source}）
                <p>${source.content}</p>
            </div>
        `;
    });
    
    html += '</div></details>';
    return html;
}

// 显示/隐藏加载指示器
function showLoading(show) {
    const container = document.getElementById('chat-messages');
    
    if (show) {
        // 创建加载指示器
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.className = 'loading';
        loadingDiv.innerHTML = `
            <div class="loading-spinner"></div>
            <span>正在思考...</span>
        `;
        container.appendChild(loadingDiv);
        // 滚动到底部
        container.scrollTop = container.scrollHeight;
    } else {
        // 移除加载指示器
        const loadingDiv = document.getElementById('loading-indicator');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }
}

// 显示错误消息
function showError(message) {
    const container = document.getElementById('chat-messages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    container.appendChild(errorDiv);
}
