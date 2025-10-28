// 协同讨论页面JavaScript

class CollaborationChat {
    constructor() {
        this.websocket = null;
        this.messageCount = 0;
        this.startTime = Date.now();
        this.experts = ['粤剧专家', '建筑专家', '美食专家', '节庆专家'];
        this.init();
    }

    init() {
        this.bindEvents();
        this.initWebSocket();
        this.updateStats();
    }

    bindEvents() {
        // 发送消息
        document.getElementById('collaboration-send').addEventListener('click', () => {
            this.sendMessage();
        });

        // 回车发送
        document.getElementById('collaboration-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // 清空讨论
        document.getElementById('clear-discussion').addEventListener('click', () => {
            this.clearDiscussion();
        });

        // 导出讨论
        document.getElementById('export-discussion').addEventListener('click', () => {
            this.exportDiscussion();
        });
    }

    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            console.log('协同讨论WebSocket连接已建立');
        };

        this.websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.websocket.onclose = () => {
            console.log('WebSocket连接已关闭');
            setTimeout(() => this.initWebSocket(), 3000);
        };

        this.websocket.onerror = (error) => {
            console.error('WebSocket错误:', error);
        };
    }

    sendMessage() {
        const input = document.getElementById('collaboration-input');
        const message = input.value.trim();
        
        if (!message) return;

        // 添加用户消息
        this.addMessage('user', message);
        
        // 清空输入框
        input.value = '';
        
        // 显示思考状态
        this.showThinkingState();
        
        // 发送到服务器
        this.sendToServer({
            type: 'collaboration',
            message: message
        });
    }

    sendToServer(data) {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.send(JSON.stringify(data));
        } else {
            this.addMessage('system', '连接已断开，正在尝试重连...');
        }
    }

    handleMessage(data) {
        if (data.type === 'collaboration_response') {
            this.hideThinkingState();
            this.displayCollaborationResult(data);
        } else if (data.type === 'error') {
            this.hideThinkingState();
            this.addMessage('system', `错误: ${data.message}`);
        }
    }

    displayCollaborationResult(data) {
        // 显示各专家回应
        if (data.content.expert_responses) {
            Object.entries(data.content.expert_responses).forEach(([expert, response]) => {
                const expertName = this.getExpertDisplayName(expert);
                this.addExpertMessage(expert, expertName, response);
            });
        }

        // 显示综合回应
        if (data.content.final_response) {
            this.addSynthesisMessage(data.content.final_response);
        }

        this.updateStats();
    }

    addMessage(sender, content) {
        const messageDiv = this.createMessage(sender, content);
        document.getElementById('discussion-area').appendChild(messageDiv);
        this.scrollToBottom();
        this.messageCount++;
    }

    addExpertMessage(expertType, expertName, content) {
        const messageDiv = this.createExpertMessage(expertType, expertName, content);
        document.getElementById('discussion-area').appendChild(messageDiv);
        this.scrollToBottom();
        this.messageCount++;
    }

    addSynthesisMessage(content) {
        const messageDiv = this.createSynthesisMessage(content);
        document.getElementById('discussion-area').appendChild(messageDiv);
        this.scrollToBottom();
        this.messageCount++;
    }

    createMessage(sender, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `discussion-message ${sender}`;
        
        const time = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <strong>${this.getSenderName(sender)}：</strong>
                    <span class="message-text">${this.formatContent(content)}</span>
                </div>
                <small class="text-muted">${time}</small>
            </div>
        `;
        
        return messageDiv;
    }

    createExpertMessage(expertType, expertName, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `discussion-message ${expertType}`;
        
        const time = new Date().toLocaleTimeString();
        const icon = this.getExpertIcon(expertType);
        
        messageDiv.innerHTML = `
            <div class="d-flex">
                <div class="expert-avatar me-3">
                    <div class="avatar-circle ${this.getExpertColor(expertType)}">
                        <i class="fas ${icon}"></i>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <strong>${expertName}</strong>
                        <small class="text-muted">${time}</small>
                    </div>
                    <div class="message-text">${this.formatContent(content)}</div>
                </div>
            </div>
        `;
        
        return messageDiv;
    }

    createSynthesisMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'discussion-message synthesis';
        
        const time = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="d-flex">
                <div class="expert-avatar me-3">
                    <div class="avatar-circle bg-warning text-white">
                        <i class="fas fa-users"></i>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <strong>协同总结</strong>
                        <small class="text-muted">${time}</small>
                    </div>
                    <div class="message-text">${this.formatContent(content)}</div>
                </div>
            </div>
        `;
        
        return messageDiv;
    }

    getSenderName(sender) {
        const names = {
            'user': '您',
            'system': '系统'
        };
        return names[sender] || '未知';
    }

    getExpertDisplayName(expertType) {
        const names = {
            'cantonese_opera': '粤剧专家',
            'architecture': '建筑专家',
            'culinary': '美食专家',
            'festival': '节庆专家'
        };
        return names[expertType] || expertType;
    }

    getExpertIcon(expertType) {
        const icons = {
            'cantonese_opera': 'fa-theater-masks',
            'architecture': 'fa-building',
            'culinary': 'fa-utensils',
            'festival': 'fa-calendar-alt'
        };
        return icons[expertType] || 'fa-user';
    }

    getExpertColor(expertType) {
        const colors = {
            'cantonese_opera': 'bg-warning text-white',
            'architecture': 'bg-success text-white',
            'culinary': 'bg-info text-white',
            'festival': 'bg-danger text-white'
        };
        return colors[expertType] || 'bg-secondary text-white';
    }

    formatContent(content) {
        return content.replace(/\n/g, '<br>');
    }

    showThinkingState() {
        const thinkingDiv = document.createElement('div');
        thinkingDiv.id = 'thinking-state';
        thinkingDiv.className = 'discussion-message system';
        thinkingDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="loading-spinner me-3"></div>
                <span>专家们正在协同讨论中...</span>
            </div>
        `;
        document.getElementById('discussion-area').appendChild(thinkingDiv);
        this.scrollToBottom();
    }

    hideThinkingState() {
        const thinkingDiv = document.getElementById('thinking-state');
        if (thinkingDiv) {
            thinkingDiv.remove();
        }
    }

    scrollToBottom() {
        const discussionArea = document.getElementById('discussion-area');
        discussionArea.scrollTop = discussionArea.scrollHeight;
    }

    clearDiscussion() {
        if (confirm('确定要清空所有讨论内容吗？')) {
            document.getElementById('discussion-area').innerHTML = `
                <div class="welcome-message text-center text-muted py-5">
                    <i class="fas fa-users fa-3x mb-3"></i>
                    <h5>开始协同讨论</h5>
                    <p>提出您的问题，多位专家将协同为您提供全面的文化解读</p>
                </div>
            `;
            this.messageCount = 0;
            this.startTime = Date.now();
            this.updateStats();
        }
    }

    exportDiscussion() {
        const discussionArea = document.getElementById('discussion-area');
        const messages = discussionArea.querySelectorAll('.discussion-message');
        
        let exportText = '广府非遗文化协同讨论记录\n';
        exportText += '='.repeat(50) + '\n\n';
        
        messages.forEach(message => {
            const sender = message.querySelector('strong');
            const content = message.querySelector('.message-text');
            const time = message.querySelector('small');
            
            if (sender && content) {
                exportText += `[${time ? time.textContent : '未知时间'}] ${sender.textContent}\n`;
                exportText += `${content.textContent}\n\n`;
            }
        });
        
        // 创建下载链接
        const blob = new Blob([exportText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `协同讨论记录_${new Date().toISOString().split('T')[0]}.txt`;
        link.click();
        URL.revokeObjectURL(url);
    }

    updateStats() {
        document.getElementById('message-count').textContent = this.messageCount;
        document.getElementById('expert-count').textContent = this.experts.length;
        
        const elapsedMinutes = Math.floor((Date.now() - this.startTime) / 60000);
        document.getElementById('discussion-time').textContent = elapsedMinutes;
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new CollaborationChat();
});

