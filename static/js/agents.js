// 专家智能体页面JavaScript

// 滚动到指定部分
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// 开始与专家对话
function startChat(agentType) {
    // 跳转到聊天页面并传递专家类型参数
    window.location.href = `/chat?agent=${agentType}`;
}

class AgentChat {
    constructor() {
        this.currentAgent = null;
        this.websocket = null;
        this.messageCount = 0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.initWebSocket();
    }

    bindEvents() {
        // 专家卡片点击事件
        document.querySelectorAll('.chat-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const agentName = e.target.getAttribute('data-agent');
                this.startChat(agentName);
            });
        });

        // 关闭聊天
        document.getElementById('close-chat').addEventListener('click', () => {
            this.closeChat();
        });

        // 发送消息
        document.getElementById('send-btn').addEventListener('click', () => {
            this.sendMessage();
        });

        // 回车发送
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            console.log('WebSocket连接已建立');
        };

        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.websocket.onclose = () => {
            console.log('WebSocket连接已关闭');
            // 尝试重连
            setTimeout(() => this.initWebSocket(), 3000);
        };

        this.websocket.onerror = (error) => {
            console.error('WebSocket错误:', error);
        };
    }

    startChat(agentName) {
        this.currentAgent = agentName;
        this.showChatInterface();
        this.addWelcomeMessage(agentName);
    }

    showChatInterface() {
        document.getElementById('chat-container').style.display = 'block';
        document.getElementById('chat-agent-name').textContent = `${this.currentAgent} - 对话中`;
        document.getElementById('message-input').focus();
        
        // 滚动到聊天区域
        document.getElementById('chat-container').scrollIntoView({ 
            behavior: 'smooth' 
        });
    }

    closeChat() {
        document.getElementById('chat-container').style.display = 'none';
        this.currentAgent = null;
        this.clearMessages();
    }

    addWelcomeMessage(agentName) {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
        
        const welcomeMessage = this.createMessage(
            'system',
            `欢迎与${agentName}对话！我是您的专业文化顾问，可以为您介绍广府非遗文化的各个方面。请提出您的问题。`
        );
        
        messagesContainer.appendChild(welcomeMessage);
        this.scrollToBottom();
    }

    sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;
        if (!this.currentAgent) return;

        // 添加用户消息到界面
        this.addMessage('user', message);
        
        // 清空输入框
        input.value = '';
        
        // 发送到服务器
        this.sendToServer({
            type: 'chat',
            message: message,
            agent_type: this.getAgentType(this.currentAgent)
        });
    }

    getAgentType(agentName) {
        const typeMap = {
            '粤剧专家': 'cantonese_opera',
            '广府建筑专家': 'architecture',
            '岭南美食专家': 'culinary',
            '节庆文化专家': 'festival'
        };
        return typeMap[agentName] || 'general';
    }

    sendToServer(data) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(data));
        } else {
            this.addMessage('system', '连接已断开，正在尝试重连...');
        }
    }

    handleMessage(data) {
        if (data.type === 'response') {
            this.addMessage('agent', data.content);
        } else if (data.type === 'error') {
            this.addMessage('system', `错误: ${data.message}`);
        }
    }

    addMessage(sender, content) {
        const message = this.createMessage(sender, content);
        document.getElementById('chat-messages').appendChild(message);
        this.scrollToBottom();
        this.messageCount++;
    }

    createMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message mb-3';
        
        const avatarClass = this.getAvatarClass(sender);
        const messageClass = this.getMessageClass(sender);
        
        messageDiv.innerHTML = `
            <div class="d-flex">
                <div class="avatar ${avatarClass} rounded-circle me-3">
                    <i class="fas ${this.getAvatarIcon(sender)}"></i>
                </div>
                <div class="flex-grow-1">
                    <div class="message-content ${messageClass} p-3 rounded">
                        <strong>${this.getSenderName(sender)}：</strong>
                        <span class="message-text">${this.formatContent(content)}</span>
                        <div class="message-time text-muted small mt-1">
                            ${new Date().toLocaleTimeString()}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        return messageDiv;
    }

    getAvatarClass(sender) {
        const classes = {
            'user': 'bg-primary text-white',
            'agent': 'bg-success text-white',
            'system': 'bg-info text-white'
        };
        return classes[sender] || 'bg-secondary text-white';
    }

    getAvatarIcon(sender) {
        const icons = {
            'user': 'fa-user',
            'agent': 'fa-robot',
            'system': 'fa-info-circle'
        };
        return icons[sender] || 'fa-user';
    }

    getMessageClass(sender) {
        const classes = {
            'user': 'user',
            'agent': 'agent',
            'system': 'system'
        };
        return classes[sender] || '';
    }

    getSenderName(sender) {
        const names = {
            'user': '您',
            'agent': this.currentAgent || '专家',
            'system': '系统'
        };
        return names[sender] || '未知';
    }

    formatContent(content) {
        // 简单的格式化，可以扩展为更复杂的markdown渲染
        return content.replace(/\n/g, '<br>');
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    clearMessages() {
        document.getElementById('chat-messages').innerHTML = '';
        this.messageCount = 0;
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new AgentChat();
});

