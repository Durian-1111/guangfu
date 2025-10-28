// 现代化聊天界面JavaScript

class ChatInterface {
    constructor() {
        this.currentAgent = null;
        this.messages = [];
        this.isTyping = false;
        this.userId = this.generateUserId();
        
        this.initializeElements();
        this.bindEvents();
        this.loadConversationHistory();
    }

    // 初始化DOM元素
    initializeElements() {
        this.sidebar = document.getElementById('sidebar');
        this.messagesContainer = document.getElementById('messages-container');
        this.welcomeScreen = document.getElementById('welcome-screen');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.currentAgentName = document.getElementById('current-agent-name');
        this.currentAgentDesc = document.getElementById('current-agent-desc');
        this.currentAgentAvatar = document.getElementById('current-agent-avatar');
        this.clearChatBtn = document.getElementById('clear-chat');
        this.toggleSidebarBtn = document.getElementById('toggle-sidebar');
        
        this.agentItems = document.querySelectorAll('.agent-item');
    }

    // 绑定事件
    bindEvents() {
        // 专家选择
        this.agentItems.forEach(item => {
            item.addEventListener('click', () => {
                const agentId = item.dataset.agent;
                this.selectAgent(agentId, item);
            });
        });

        // 发送消息
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }
        if (this.messageInput) {
            this.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // 自动调整输入框高度
            this.messageInput.addEventListener('input', () => {
                this.autoResizeTextarea();
            });
        }

        // 清空对话
        if (this.clearChatBtn) {
            this.clearChatBtn.addEventListener('click', () => this.clearChat());
        }

        // 切换侧边栏
        if (this.toggleSidebarBtn) {
            this.toggleSidebarBtn.addEventListener('click', () => this.toggleSidebar());
        }

        // 响应式处理
        window.addEventListener('resize', () => this.handleResize());
    }

    // 生成用户ID
    generateUserId() {
        return 'user_' + Math.random().toString(36).substr(2, 9);
    }

    // 选择专家
    selectAgent(agentId, element) {
        console.log('选择专家:', agentId);
        
        // 更新选中状态
        this.agentItems.forEach(item => item.classList.remove('active'));
        element.classList.add('active');

        // 设置当前专家
        this.currentAgent = agentId;
        
        // 获取专家信息
        const agentInfo = this.getAgentInfo(agentId);
        console.log('专家信息:', agentInfo);
        this.updateAgentHeader(agentInfo);

        // 清空输入框
        if (this.messageInput) {
            this.messageInput.value = '';
            this.autoResizeTextarea();
        }
        
        // 显示输入框
        const inputContainer = document.querySelector('.input-container');
        if (inputContainer) {
            inputContainer.classList.add('show');
        }

        // 启用输入
        if (this.messageInput) {
            this.messageInput.disabled = false;
            this.messageInput.placeholder = `向${agentInfo.name}提问...`;
        }
        if (this.sendButton) {
            this.sendButton.disabled = false;
        }

        // 隐藏欢迎界面
        if (this.welcomeScreen) {
            this.welcomeScreen.style.display = 'none';
            console.log('隐藏欢迎界面');
        }

        // 加载对话历史
        this.loadAgentConversation(agentId);

        // 显示预设问题
        this.showSuggestedQuestions(agentId);

        // 移动端自动隐藏侧边栏
        if (window.innerWidth <= 768) {
            this.sidebar.classList.remove('open');
        }
    }

    // 显示预设问题
    showSuggestedQuestions(agentId) {
        const agentInfo = this.getAgentInfo(agentId);
        const suggestedContainer = document.getElementById('suggested-questions');
        
        if (!suggestedContainer) {
            console.error('预设问题容器不存在');
            return;
        }
        
        if (!agentInfo.suggestedQuestions) {
            console.log('专家没有预设问题:', agentId);
            suggestedContainer.innerHTML = '';
            return;
        }

        console.log('显示预设问题:', agentId, agentInfo.suggestedQuestions);
        suggestedContainer.innerHTML = '';
        
        agentInfo.suggestedQuestions.forEach((question, index) => {
            const btn = document.createElement('button');
            btn.className = 'suggested-question-btn';
            btn.textContent = question;
            btn.addEventListener('click', (event) => {
                event.preventDefault();
                event.stopPropagation();
                console.log('点击预设问题:', question, '当前状态:', {
                    isTyping: this.isTyping,
                    currentAgent: this.currentAgent,
                    messageInput: this.messageInput.value
                });
                // 直接发送消息，而不是填充到输入框
                this.messageInput.value = question;
                console.log('调用sendMessage');
                this.sendMessage();
            });
            suggestedContainer.appendChild(btn);
        });
    }

    // 获取专家信息
    getAgentInfo(agentId) {
        const agentMap = {
            'cantonese_opera_critic': {
                name: '粤剧大师',
                desc: '精通粤剧艺术与历史',
                avatar: 'fas fa-theater-masks',
                color: '#f59e0b',
                welcome: '老友好！我是戏曲老倌，浸淫粤剧艺术几十年，从唱腔到身段，从行当到脸谱，样样精通。粤剧系我们广府嘅文化瑰宝，承载住深厚嘅历史文化底蕴。无论系表演技艺、经典剧目，定系历史传承，我都可以同你细细道来。你睇住咩方面感兴趣呢？',
                suggestedQuestions: ['粤剧嘅主要剧目有边啲？', '粤剧唱腔有咩特色？', '点样学习粤剧表演？', '粤剧历史发展脉络']
            },
            'architecture_expert': {
                name: '建筑师傅',
                desc: '了解广府传统建筑',
                avatar: 'fas fa-building',
                color: '#10b981',
                welcome: '老友！我系建筑师傅老陈，专注岭南传统建筑文化研究同保护廿几年喇。从西关大屋嘅精雕细琢，到骑楼街嘅中西合璧，从陈家祠嘅木雕石刻，到荔枝湾嘅园林布局，我对广府建筑嘅每一个细节都充满热爱。岭南建筑唔单单系居住空间，更系文化嘅载体，体现咗广府人嘅生活智慧。你想了解边种建筑类型或者建筑元素呢？',
                suggestedQuestions: ['岭南建筑有咩特色？', '骑楼建筑嘅特色系咩？', '陈家祠嘅建筑艺术', '传统建筑嘅保护传承']
            },
            'culinary_expert': {
                name: '美食师傅',
                desc: '熟悉岭南饮食文化',
                avatar: 'fas fa-utensils',
                color: '#ef4444',
                welcome: '老友好！我系味师傅，浸淫广府饮食文化三十几年喇。从茶楼嘅一盅两件，到酒楼嘅满汉全席，从街头嘅传统小吃，到家庭嘅煲汤文化，我都好了解。"食在广州"呢句话唔系白讲嘅！广府菜讲究"不时不食"，注重食材嘅新鲜同烹饪嘅精细，每一道菜都承载住深厚嘅文化内涵。你想了解边道经典粤菜或者边种饮食文化呢？',
                suggestedQuestions: ['粤菜有咩特色？', '广州早茶文化介绍', '广府小吃嘅制作', '粤菜烹饪技法']
            },
            'festival_expert': {
                name: '节庆师傅',
                desc: '掌握传统节庆文化',
                avatar: 'fas fa-calendar-alt',
                color: '#8b5cf6',
                welcome: '老友好！我系庆典师傅，专研广府地区嘅传统节庆文化同民俗活动。自细喺老广州长大，亲身经历咗好多传统节庆嘅变迁，对每个节日背后嘅历史典故同文化内涵都好了解。从热闹嘅迎春花市到庄重嘅祭祖仪式，从激烈嘅龙舟竞渡到温馨嘅中秋赏月，每个节庆都承载住广府人嘅情感记忆同文化传承。你想了解边个传统节庆嘅习俗同文化内涵呢？',
                suggestedQuestions: ['广府有咩传统节日？', '端午节龙舟文化', '中秋节习俗', '春节民俗活动']
            },
            'tea_culture_expert': {
                name: '茶艺师傅',
                desc: '精通茶艺与茶道',
                avatar: 'fas fa-leaf',
                color: '#16a085',
                welcome: '老友好！我系茗香居士，专注广府茶文化研究。茶喺广府文化中占好重要地位，从工夫茶嘅冲泡技法，到各类茶叶嘅品鉴，从茶具嘅鉴赏，到饮茶习俗嘅传承，每一个细节都蕴含住深厚嘅文化内涵。广府人中意饮茶，早茶、下午茶唔单单系饮食，更系社交嘅重要方式。你想了解茶文化嘅边个方面呢？',
                suggestedQuestions: ['工夫茶嘅冲泡方法', '广府茶叶品种介绍', '茶具鉴赏', '饮茶礼仪']
            },
            'craft_expert': {
                name: '工艺师傅',
                desc: '了解传统工艺技艺',
                avatar: 'fas fa-palette',
                color: '#f39c12',
                welcome: '老友好！我系艺师傅，专研广府传统手工艺嘅传承与创新。广府手工艺历史好悠久，技艺精湛。从广绣嘅精美绣工，到广彩嘅斑斓色彩，从木雕石雕嘅精湛雕刻，到各类传统技艺嘅传承，每一件作品都体现咗匠人嘅智慧同工匠精神。呢啲传统手工艺唔单单系技艺嘅传承，更系文化精神同美学追求嘅体现。你想了解边种传统手工艺呢？',
                suggestedQuestions: ['广绣技法介绍', '广彩工艺特色', '雕刻技艺传承', '传统工艺保护']
            },
            'literature_expert': {
                name: '文师傅',
                desc: '精通古典诗词文学',
                avatar: 'fas fa-book',
                color: '#9b59b6',
                welcome: '老友好！我系文师傅，专研广府诗词文学。广府诗词文学源远流长，从古典诗词到现代文学，从岭南诗歌到广府诗词，每一首作品都承载住深厚嘅文化内涵同审美价值。诗词系文化嘅精髓，通过诗词我哋可以了解广府嘅历史文化、风土人情同人文精神。你想了解诗词文学嘅边个方面呢？',
                suggestedQuestions: ['岭南诗词赏析', '广府文学特点', '古典诗词鉴赏', '历史典故']
            },
            'tcm_expert': {
                name: '老中医师傅',
                desc: '精通中医养生文化',
                avatar: 'fas fa-pills',
                color: '#e74c3c',
                welcome: '老友好！我系老中医师傅，专研中医药文化同养生保健。中医药系广府文化嘅重要组成部分，从中医理论到中药方剂，从食疗文化到养生保健，每一个方面都蕴含着博大精深嘅智慧。广府人特别注重养生，食疗文化历史悠久，"药食同源"嘅理念深入人心。你想了解中医养生嘅边个方面呢？',
                suggestedQuestions: ['点样理解中医养生理念？', '广府食疗文化有咩特色？', '中药方剂嘅配伍原则系咩？']
            }
        };

        return agentMap[agentId] || {
            name: '智能专家',
            desc: '广府文化专家',
            avatar: 'fas fa-robot',
            color: '#64748b',
            welcome: '您好！我是广府文化专家，很高兴为您介绍广府非遗文化。请问您想了解什么？'
        };
    }

    // 更新专家头部信息
    updateAgentHeader(agentInfo) {
        if (this.currentAgentName) {
            this.currentAgentName.textContent = agentInfo.name;
        }
        if (this.currentAgentDesc) {
            this.currentAgentDesc.textContent = agentInfo.desc;
        }
        if (this.currentAgentAvatar) {
            this.currentAgentAvatar.style.background = agentInfo.color;
            this.currentAgentAvatar.innerHTML = `<i class="${agentInfo.avatar}"></i>`;
        }
    }

    // 发送消息
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.currentAgent || this.isTyping) return;

        console.log('发送消息:', message); // 调试日志

        // 添加用户消息
        this.addMessage('user', message);
        this.messageInput.value = '';
        this.autoResizeTextarea();

        // 设置输入状态（不再需要单独的showTypingIndicator）
        this.isTyping = true;
        this.sendButton.disabled = true;
        this.messageInput.disabled = true;

        try {
            // 使用流式响应
            await this.sendMessageStream(message);
        } catch (error) {
            console.error('发送消息失败:', error);
            // 错误处理已在sendMessageStream中完成
        }
    }

    // 流式发送消息
    async sendMessageStream(message) {
        let fullContent = '';
        
        try {
            const response = await this.sendToAgentStream(message);
            
            // 检测是否为闲聊
            const isCasualChat = this.isCasualMessage(message);
            
            // 创建AI消息容器，并在其中显示加载动画
            const messageElement = this.createMessageElement('agent', '');
            this.messagesContainer.appendChild(messageElement);
            this.scrollToBottom();
            
            const contentElement = messageElement.querySelector('.message-content');
            
            // 如果是闲聊，不显示思考框
            if (isCasualChat) {
                // 闲聊模式：显示简洁的加载动画
                contentElement.innerHTML = '<div class="loading-animation"><div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div></div>';
            } else {
                // 专业模式：显示思考框
                const agentInfo = this.getAgentInfo(this.currentAgent);
                const thinkingContainer = document.createElement('div');
                const startTime = Date.now();
                thinkingContainer.className = 'thinking-container';
                thinkingContainer.innerHTML = `
                    <div class="thinking-header" onclick="this.parentElement.classList.toggle('expanded')">
                        <span class="thinking-icon">🤔</span>
                        <span class="thinking-text">${agentInfo.name}正在思考...</span>
                        <span class="thinking-time">0.0s</span>
                        <i class="fas fa-chevron-down thinking-toggle"></i>
                    </div>
                    <div class="thinking-content"></div>
                `;
                
                contentElement.innerHTML = '';
                contentElement.appendChild(thinkingContainer);
                thinkingContent = thinkingContainer.querySelector('.thinking-content');
            }
            
            // 读取流式响应
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            if (data.type === 'chunk' && data.content) {
                                fullContent += data.content;
                                
                                if (isCasualChat) {
                                    // 闲聊模式：流式显示纯文本，不格式化（避免流式过程中格式错乱）
                                    if (!hasReceivedContent) {
                                        // 移除加载动画
                                        contentElement.innerHTML = '';
                                    }
                                    const textNode = document.createTextNode(data.content);
                                    contentElement.appendChild(textNode);
                                    hasReceivedContent = true;
                                } else {
                                    // 专业模式：在思考框中显示原始文本
                                    // 第一次收到内容时展开思考框
                                    if (!hasReceivedContent) {
                                        thinkingContainer.classList.add('expanded');
                                        hasReceivedContent = true;
                                    }
                                    thinkingContent.textContent = fullContent;
                                    
                                    // 更新思考时间
                                    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
                                    const timeElement = thinkingContainer.querySelector('.thinking-time');
                                    if (timeElement) {
                                        timeElement.textContent = `已思考 ${elapsed}s`;
                                    }
                                }
                                
                                this.scrollToBottom();
                            } else if (data.type === 'done') {
                                // 流式传输完成
                                if (fullContent) {
                                    if (isCasualChat) {
                                        // 闲聊模式：流式传输完成后，重新渲染完整格式化内容
                                        contentElement.innerHTML = this.formatMessage(fullContent);
                                    } else {
                                        // 专业模式：移除思考框，渲染最终格式化内容
                                        thinkingContainer.remove();
                                        contentElement.innerHTML = this.formatMessage(fullContent);
                                    }
                                    this.scrollToBottom();
                                    // 保存完整的对话记录
                                    this.saveConversation(message, fullContent);
                                }
                                return;
                            }
                        } catch (e) {
                            // 忽略JSON解析错误
                        }
                    }
                }
            }
        } catch (error) {
            // 如果已经创建了消息元素，就更新其内容，否则创建新的
            const existingMessage = this.messagesContainer.querySelector('.message:last-child .message-content');
            if (existingMessage) {
                existingMessage.innerHTML = '网络连接出现问题，请检查网络后重试。';
                existingMessage.parentElement.parentElement.classList.add('error');
            } else {
                this.addMessage('agent', '网络连接出现问题，请检查网络后重试。', 'error');
            }
            throw error;
        } finally {
            // 确保重置状态
            this.isTyping = false;
            this.sendButton.disabled = false;
            this.messageInput.disabled = false;
        }
    }

    // 发送消息到后端（流式）
    async sendToAgentStream(message) {
        const response = await fetch('/api/chat/stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                agent_id: this.currentAgent,
                message: message,
                user_id: this.userId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response;
    }

    // 发送消息到后端
    async sendToAgent(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                agent_id: this.currentAgent,
                message: message,
                user_id: this.userId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    // 创建消息元素（不添加到DOM）
    createMessageElement(type, content, status = 'normal') {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type} fade-in`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';

        if (type === 'user') {
            avatar.style.background = 'var(--primary-color)';
            avatar.innerHTML = '<i class="fas fa-user"></i>';
        } else {
            const agentInfo = this.getAgentInfo(this.currentAgent);
            avatar.style.background = agentInfo.color;
            avatar.innerHTML = `<i class="${agentInfo.avatar}"></i>`;
        }

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (status === 'error') {
            messageContent.style.background = '#fee2e2';
            messageContent.style.color = '#dc2626';
            messageContent.style.border = '1px solid #fecaca';
        }

        // 处理Markdown格式
        messageContent.innerHTML = this.formatMessage(content);

        // 添加时间戳
        const timeElement = document.createElement('div');
        timeElement.className = 'message-time';
        timeElement.textContent = this.formatTime(new Date());
        messageContent.appendChild(timeElement);

        messageElement.appendChild(avatar);
        messageElement.appendChild(messageContent);

        return messageElement;
    }

    // 添加消息到界面
    addMessage(type, content, status = 'normal') {
        console.log('添加消息:', type, content.substring(0, 50) + '...');
        const messageElement = this.createMessageElement(type, content, status);
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();

        // 保存消息
        this.messages.push({
            type,
            content,
            timestamp: new Date(),
            agent: this.currentAgent
        });
    }

    // 格式化消息内容
    formatMessage(content) {
        if (!content) return '';
        
        // 去除多余的空白字符
        content = content.trim();
        
        // 过滤AI系统内部使用的模式标记（如：🏗️ **专业介绍模式启动**、## **广府骑楼建筑特色解析**等）
        content = this.filterSystemMarkers(content);
        
        // 首先检查是否为emoji分点格式
        if (this.isEmojiFormat(content)) {
            return this.formatEmojiContent(content);
        }
        
        // 检查是否为时间线内容
        if (this.isTimelineContent(content)) {
            return this.formatTimelineContent(content);
        }
        
        // 首先处理Markdown加粗格式（**text**），这是最基础的格式
        content = content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.+?)\*/g, '<em>$1</em>');
        content = content.replace(/`(.+?)`/g, '<code>$1</code>');
        
        // 处理标题（###、##、#），注意替换后原来的符号要移除
        content = content.replace(/^### (.+?)$/gm, '<h3 style="margin: 1.25rem 0 0.75rem 0; font-size: 1.1rem; color: #c41e3a; font-weight: 600; border-left: 4px solid #c41e3a; padding-left: 0.75rem;">$1</h3>');
        content = content.replace(/^## (.+?)$/gm, '<h2 style="margin: 1.5rem 0 1rem 0; font-size: 1.25rem; color: #c41e3a; font-weight: 600; border-bottom: 2px solid #c41e3a; padding-bottom: 0.5rem;">$1</h2>');
        content = content.replace(/^# (.+?)$/gm, '<h1 style="margin: 1.75rem 0 1.25rem 0; font-size: 1.5rem; color: #c41e3a; font-weight: 700;">$1</h1>');
        
        // 处理分隔线
        content = content.replace(/^---+$/gm, '<hr style="margin: 1rem 0; border: none; border-top: 1px solid #e0e0e0;">');
        content = content.replace(/^===+$/gm, '<hr style="margin: 1rem 0; border: none; border-top: 2px solid var(--primary-color);">');
        
        // 处理列表项（- **文本** 或 • **文本**）
        content = content.replace(/^[•\-\*]\s*<strong>(.*?)<\/strong>/gm, '<div class="list-item">• <strong>$1</strong></div>');
        content = content.replace(/^[•\-\*]\s+(.+)$/gm, '<div class="list-item">• $1</div>');
        
        // 处理带特殊符号的序号格式（◆一、◇四、☆五等）
        content = content.replace(
            /(◆|◇|☆|◎|●|○)\*\*([一二三四五六七八九十]+)[、．.]\s*(.*?)\*\*/g,
            '<div class="emoji-ordered-item"><span class="emoji-icon" style="color: #c41e3a; font-weight: 600;">$1</span><span class="order-number">$2、</span><strong>$3</strong></div>'
        );
        
        // 然后处理带emoji的序号格式（例如：🔸 **四、** 标题）
        content = content.replace(
            /(🔸|🔷|🔶|⚪|🌟)\s*([一二三四五六七八九十]+)[、．.]\s*<strong>(.*?)<\/strong>/g,
            '<div class="emoji-ordered-item"><span class="emoji-icon">$1</span><span class="order-number">$2、</span><strong>$3</strong></div>'
        );
        
        // 处理普通中文序号格式（一、二、三等）
        content = content.replace(
            /([一二三四五六七八九十]+)[、．.]\s*<strong>(.*?)<\/strong>/g,
            '<div class="ordered-item"><span class="order-number">$1、</span><strong>$2</strong></div>'
        );
        
        // 处理数字序号（1. 2. 3.等）
        content = content.replace(
            /(\d+)[、．.]\s*<strong>(.*?)<\/strong>/g,
            '<div class="numbered-item"><span class="number-badge">$1</span><strong>$2</strong></div>'
        );
        
        // 处理步骤格式（📋 步骤X：内容 或 👨‍🍳 步骤X：内容）
        content = content.replace(
            /(📋|👨‍🍳)\s*步骤(\d+)：([^\n]+)/g, 
            (match, icon, number, stepContent) => {
                const stepClass = icon === '👨‍🍳' ? 'step-item cooking-step' : 'step-item';
                return `<div class="${stepClass}">
                    <span class="step-icon">${icon}</span>
                    <div class="step-content"><strong>步骤${number}：</strong>${stepContent}</div>
                </div>`;
            }
        );
        
        // 处理其他图标格式（🕐、📅等）
        content = content.replace(
            /(🕐|📅)\s*([^：\n]+)：([^\n]+)/g,
            '<div class="step-item"><span class="step-icon">$1</span><div class="step-content"><strong>$2：</strong>$3</div></div>'
        );
        
        // 处理换行，但保留步骤格式的结构
        // 先处理多余的空行（连续多个换行符变成一个）
        content = content.replace(/\n{3,}/g, '\n\n');
        
        // 清理未匹配的Markdown标记字符（在转换过程中遗漏的）
        // 清理未匹配的粗体标记
        content = content.replace(/\*\*(.+?)\*\*/g, (match, text) => {
            // 如果包含已经转换的HTML标签，说明已经处理过，跳过
            if (text.includes('<strong>') || text.includes('<em>') || text.includes('<code>')) {
                return match;
            }
            return '<strong>' + text + '</strong>';
        });
        
        // 清理未匹配的斜体标记
        content = content.replace(/\*(.+?)\*/g, (match, text) => {
            if (text.includes('<strong>') || text.includes('<em>') || text.includes('<code>')) {
                return match;
            }
            return '<em>' + text + '</em>';
        });
        
        // 清理未匹配的代码标记
        content = content.replace(/`(.+?)`/g, (match, text) => {
            if (text.includes('<strong>') || text.includes('<em>') || text.includes('<code>')) {
                return match;
            }
            return '<code>' + text + '</code>';
        });
        
        // 清理所有残留的#符号（出现在行首或行中但未转换的）
        content = content.replace(/([^>])#{1,6}([^<])/g, '$1$2');
        
        // 然后替换为br标签
        content = content.replace(/\n/g, '<br>');
        
        return content;
    }

    // 检测是否为闲聊消息
    isCasualMessage(message) {
        const casualKeywords = [
            '你好', '您好', '嗨', '哈喽', '早上好', '下午好', '晚上好', '晚安',
            '怎么样', '如何', '好吗', '是吗', '对吧', '呢',
            '哈哈', '嘿嘿', '呵呵', '哇', '哎呀', '真的', '太好了', '不错',
            '嗯嗯', '是啊', '对对', '好的', '明白', '知道了', '谢谢',
            '厉害', '棒', '好', '不错', '赞', '牛', '强'
        ];
        
        // 简短消息或包含闲聊关键词
        if (message.length <= 10) return true;
        
        return casualKeywords.some(keyword => message.includes(keyword));
    }

    // 过滤系统内部标记
    filterSystemMarkers(content) {
        // 1. 过滤所有模式标记（如：🎭 **日常闲聊模式**、🏗️ **专业介绍模式**等）
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?模式\*\*/gi, '');
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?模式启动\*\*/gi, '');
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?模式结束\*\*/gi, '');
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?专业.*?模式\*\*/gi, '');
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?日常.*?模式\*\*/gi, '');
        content = content.replace(/[🎭🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🛠️🔧⚙️]\s*\*\*.*?聊天.*?模式\*\*/gi, '');
        
        // 2. 过滤纯标题行（## emoji **内容** 这种格式）
        content = content.replace(/^##\s*[^\s*]+\s*\*\*[^*]+\*\*\s*$/gm, '');
        
        // 3. 过滤简单的标题行（## **内容**）
        content = content.replace(/^##\s*\*\*[^*]+\*\*\s*$/gm, '');
        
        // 4. 过滤单独的emoji+粗体行（🏗️ **标题**）
        content = content.replace(/^[🏗️🔍📚🎯📝🤝💡🎨🧪🔬🎪🎭🛠️🔧⚙️🌉🏛️🎭🍲🥮🫖📖💊🕌⛩️🍵📝]\s*\*\*[^*]+\*\*\s*$/gm, '');
        
        // 5. 过滤【当前模式】标记行
        content = content.replace(/^【当前模式】：.*$/gm, '');
        
        // 6. 去掉连续多个空行（变成最多2个空行）
        content = content.replace(/\n{3,}/g, '\n\n');
        
        // 7. 去掉开头和结尾的空行
        return content.trim();
    }

    // 检测是否为emoji分点格式内容
    isEmojiFormat(text) {
        const emojiPatterns = [
            /## 📌/,
            /🔷\s*\*\*.*?\*\*/,
            /🔶\s*\*\*.*?\*\*/,
            /🔹\s*\*\*.*?\*\*/,
            /💡\s*\*\*.*?\*\*/
        ];
        
        return emojiPatterns.some(pattern => pattern.test(text));
    }

    // 格式化emoji分点内容
    formatEmojiContent(text) {
        let html = text;
        
        // 处理主标题
        html = html.replace(/## 📌\s*(.*?)$/gm, '<div class="emoji-format"><h2>$1</h2>');
        
        // 处理分点内容
        html = html.replace(/🔷\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔶|🔹|💡|---|$)/gs, 
            '<div class="emoji-point blue"><strong>🔷 $1</strong><div class="content">$2</div></div>');
        
        html = html.replace(/🔶\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔷|🔹|💡|---|$)/gs, 
            '<div class="emoji-point orange"><strong>🔶 $1</strong><div class="content">$2</div></div>');
        
        html = html.replace(/🔹\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|🔷|🔶|💡|---|$)/gs, 
            '<div class="emoji-point light-blue"><strong>🔹 $1</strong><div class="content">$2</div></div>');
        
        // 处理关键总结
        html = html.replace(/💡\s*\*\*(.*?)\*\*\s*\n(.*?)(?=\n\n|---|$)/gs, 
            '<div class="emoji-summary"><strong>💡 $1</strong><div class="content">$2</div></div>');
        
        // 处理分隔线
        html = html.replace(/---/g, '<hr class="emoji-divider">');
        
        // 关闭emoji-format容器
        if (html.includes('<div class="emoji-format">')) {
            html += '</div>';
        }
        
        return html;
    }

    // 检查是否为时间线内容
    isTimelineContent(content) {
        // 检查是否包含时间线关键词
        const timelineKeywords = ['一日游', '行程', '路线', '时间安排', '游览', '参观', '体验'];
        const hasTimelineKeyword = timelineKeywords.some(keyword => content.includes(keyword));
        
        // 检查是否包含多个时间段
        const timePatterns = [
            /\d{1,2}:\d{2}/g,  // 09:00 格式
            /上午|下午|早上|中午|晚上/g,  // 时间段词汇
            /第[一二三四五六七八九十]\s*站/g,  // 第X站
            /站点\s*\d+/g  // 站点数字
        ];
        
        let timeMatches = 0;
        timePatterns.forEach(pattern => {
            const matches = content.match(pattern);
            if (matches) timeMatches += matches.length;
        });
        
        return hasTimelineKeyword || timeMatches >= 3;
    }

    // 格式化时间线内容
    formatTimelineContent(content) {
        // 提取标题
        const lines = content.split('\n').filter(line => line.trim());
        let title = '精彩行程安排';
        let subtitle = '为您精心规划的完美体验';
        
        // 尝试从内容中提取标题
        const titleMatch = lines[0].match(/^(.{1,20})(一日游|行程|路线|攻略)/);
        if (titleMatch) {
            title = titleMatch[0];
            subtitle = '精心为您规划的完美体验路线';
        }
        
        // 解析时间段和活动
        const timeSlots = this.parseTimeSlots(content);
        
        let html = `
            <div class="timeline-container">
                <div class="timeline-header">
                    <h3 class="timeline-title">${title}</h3>
                    <p class="timeline-subtitle">${subtitle}</p>
                </div>
                <div class="timeline-body">
        `;
        
        timeSlots.forEach((slot, index) => {
            html += `
                <div class="timeline-slot">
                    <div class="time-label">
                        <span class="time-icon">${slot.icon}</span>
                        <span class="time-text">${slot.time}</span>
                    </div>
                    <div class="activity-card">
                        <h4 class="activity-title">${slot.title}</h4>
                        <p class="activity-description">${slot.description}</p>
                        ${slot.highlights ? `<div class="highlight-info">${slot.highlights}</div>` : ''}
                        ${slot.tips ? `<div class="tip-info">💡 ${slot.tips}</div>` : ''}
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
                <div class="timeline-footer">
                    <div class="summary-info">
                        <span class="summary-icon">✨</span>
                        <span>愿您拥有美好的广府文化体验之旅！</span>
                    </div>
                </div>
            </div>
        `;
        
        return html;
    }

    // 解析时间段和活动
    parseTimeSlots(content) {
        const lines = content.split('\n').filter(line => line.trim());
        const slots = [];
        let currentSlot = null;
        
        // 图标映射
        const iconMap = {
            '早上': '🌅', '上午': '☀️', '中午': '🌞', '下午': '🌤️', '晚上': '🌙',
            '09': '🌅', '10': '☀️', '11': '☀️', '12': '🌞', '13': '🌞', 
            '14': '🌤️', '15': '🌤️', '16': '🌤️', '17': '🌤️', '18': '🌙'
        };
        
        lines.forEach(line => {
            line = line.trim();
            if (!line) return;
            
            // 匹配时间模式
            const timeMatch = line.match(/^(\d{1,2}:\d{2}|上午|下午|早上|中午|晚上|第[一二三四五六七八九十]\s*站)/);
            
            if (timeMatch) {
                // 保存上一个时间段
                if (currentSlot) {
                    slots.push(currentSlot);
                }
                
                // 创建新的时间段
                const timeText = timeMatch[1];
                let icon = '📍';
                
                // 选择合适的图标
                for (const [key, value] of Object.entries(iconMap)) {
                    if (timeText.includes(key)) {
                        icon = value;
                        break;
                    }
                }
                
                currentSlot = {
                    time: timeText,
                    icon: icon,
                    title: '',
                    description: '',
                    highlights: '',
                    tips: ''
                };
                
                // 提取标题（时间后的内容）
                const titlePart = line.replace(timeMatch[0], '').trim();
                if (titlePart) {
                    currentSlot.title = titlePart.replace(/[:：].*/, '');
                    const descPart = titlePart.match(/[:：](.+)/);
                    if (descPart) {
                        currentSlot.description = descPart[1].trim();
                    }
                }
            } else if (currentSlot) {
                // 处理描述、亮点和提示
                if (line.includes('亮点') || line.includes('特色') || line.includes('推荐')) {
                    currentSlot.highlights = line;
                } else if (line.includes('提示') || line.includes('注意') || line.includes('建议')) {
                    currentSlot.tips = line;
                } else if (!currentSlot.description) {
                    currentSlot.description = line;
                } else {
                    currentSlot.description += ' ' + line;
                }
            }
        });
        
        // 添加最后一个时间段
        if (currentSlot) {
            slots.push(currentSlot);
        }
        
        // 如果没有解析到时间段，创建默认的
        if (slots.length === 0) {
            const defaultSlots = this.createDefaultTimeSlots(content);
            return defaultSlots;
        }
        
        return slots;
    }

    // 创建默认时间段
    createDefaultTimeSlots(content) {
        const lines = content.split('\n').filter(line => line.trim());
        const slots = [];
        const timeIcons = ['🌅', '☀️', '🌞', '🌤️', '🌙'];
        const times = ['09:00', '11:00', '13:00', '15:00', '17:00'];
        
        let slotIndex = 0;
        let currentContent = '';
        
        lines.forEach((line, index) => {
            line = line.trim();
            if (!line) return;
            
            // 每3-4行创建一个时间段
            if (index > 0 && index % 3 === 0 && slotIndex < 5) {
                if (currentContent) {
                    slots.push({
                        time: times[slotIndex] || `时段${slotIndex + 1}`,
                        icon: timeIcons[slotIndex] || '📍',
                        title: currentContent.split('。')[0] || '精彩体验',
                        description: currentContent,
                        highlights: '',
                        tips: ''
                    });
                    slotIndex++;
                    currentContent = '';
                }
            }
            
            currentContent += (currentContent ? ' ' : '') + line;
        });
        
        // 添加最后的内容
        if (currentContent && slotIndex < 5) {
            slots.push({
                time: times[slotIndex] || `时段${slotIndex + 1}`,
                icon: timeIcons[slotIndex] || '📍',
                title: currentContent.split('。')[0] || '精彩体验',
                description: currentContent,
                highlights: '',
                tips: ''
            });
        }
        
        return slots.length > 0 ? slots : [{
            time: '全天',
            icon: '✨',
            title: '精彩体验',
            description: content.substring(0, 100) + '...',
            highlights: '',
            tips: ''
        }];
    }

    // 格式化时间
    formatTime(date) {
        return date.toLocaleTimeString('zh-CN', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // 显示输入状态指示器
    showTypingIndicator() {
        console.log('showTypingIndicator 被调用'); // 调试日志
        
        this.isTyping = true;
        this.sendButton.disabled = true;
        this.messageInput.disabled = true;

        const typingElement = document.createElement('div');
        typingElement.className = 'message agent typing-message';
        typingElement.id = 'typing-indicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        const agentInfo = this.getAgentInfo(this.currentAgent);
        avatar.style.background = agentInfo.color;
        avatar.innerHTML = `<i class="${agentInfo.avatar}"></i>`;

        const typingContent = document.createElement('div');
        typingContent.className = 'typing-indicator';
        typingContent.innerHTML = `
            <span class="typing-text">${agentInfo.name}正在思考...</span>
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        typingElement.appendChild(avatar);
        typingElement.appendChild(typingContent);

        this.messagesContainer.appendChild(typingElement);
        console.log('加载动画已添加到DOM'); // 调试日志
        this.scrollToBottom();
    }

    // 隐藏输入状态指示器
    hideTypingIndicator() {
        this.isTyping = false;
        this.sendButton.disabled = false;
        this.messageInput.disabled = false;

        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // 自动调整输入框高度
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 200) + 'px';
    }

    // 滚动到底部
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }

    // 清空对话
    clearChat() {
        if (confirm('确定要清空当前对话吗？')) {
            this.messages = [];
            this.messagesContainer.innerHTML = '';
            
            // 清空sessionStorage中的对话历史
            if (this.currentAgent) {
                const storageKey = `chat_history_${this.currentAgent}`;
                sessionStorage.removeItem(storageKey);
                
                // 显示当前专家的专属欢迎消息
                const agentInfo = this.getAgentInfo(this.currentAgent);
                this.addMessage('agent', agentInfo.welcome);
            } else {
                // 如果没有选择专家，显示欢迎界面并隐藏输入框
                if (this.welcomeScreen) {
                    this.welcomeScreen.style.display = 'flex';
                }
                const inputContainer = document.querySelector('.input-container');
                if (inputContainer) {
                    inputContainer.classList.remove('show');
                }
            }
        }
    }

    // 切换侧边栏
    toggleSidebar() {
        this.sidebar.classList.toggle('open');
    }

    // 处理窗口大小变化
    handleResize() {
        if (window.innerWidth > 768) {
            this.sidebar.classList.remove('open');
        }
    }

    // 创建欢迎界面
    // 加载对话历史
    async loadConversationHistory() {
        try {
            const response = await fetch(`/api/conversations?user_id=${this.userId}`);
            if (response.ok) {
                const data = await response.json();
                // 处理历史对话数据
                console.log('对话历史:', data);
            }
        } catch (error) {
            console.error('加载对话历史失败:', error);
        }
    }

    // 加载特定专家的对话
    async loadAgentConversation(agentId) {
        console.log('加载专家对话:', agentId);
        try {
            // 清空当前消息
            this.messages = [];
            this.messagesContainer.innerHTML = '';
            
            // 从sessionStorage加载历史对话
            const storageKey = `chat_history_${agentId}`;
            const conversations = JSON.parse(sessionStorage.getItem(storageKey) || '[]');
            console.log('历史对话数量:', conversations.length);
            
            // 显示历史对话
            conversations.forEach(conv => {
                if (conv.is_welcome) {
                    // 欢迎消息只显示agent回复
                    this.addMessage('agent', conv.agent_response);
                } else {
                    // 普通对话显示用户消息和agent回复
                    this.addMessage('user', conv.user_message);
                    this.addMessage('agent', conv.agent_response);
                }
            });
            
            // 如果没有历史对话，显示欢迎消息并保存
            if (conversations.length === 0) {
                const agentInfo = this.getAgentInfo(agentId);
                console.log('显示欢迎消息:', agentInfo.welcome);
                this.addMessage('agent', agentInfo.welcome);
                
                // 保存欢迎消息到sessionStorage
                this.saveWelcomeMessage(agentInfo.welcome);
            }
        } catch (error) {
            console.error('加载专家对话历史失败:', error);
            // 显示欢迎消息作为后备并保存
            const agentInfo = this.getAgentInfo(agentId);
            this.addMessage('agent', agentInfo.welcome);
            this.saveWelcomeMessage(agentInfo.welcome);
        }
    }

    // 保存欢迎消息到sessionStorage
    saveWelcomeMessage(welcomeMessage) {
        try {
            if (!this.currentAgent) return;
            
            const storageKey = `chat_history_${this.currentAgent}`;
            let conversations = JSON.parse(sessionStorage.getItem(storageKey) || '[]');
            
            // 只有在没有任何对话记录时才保存欢迎消息
            if (conversations.length === 0) {
                conversations.push({
                    user_message: '', // 欢迎消息没有用户消息
                    agent_response: welcomeMessage,
                    timestamp: new Date().toISOString(),
                    is_welcome: true // 标记为欢迎消息
                });
                
                sessionStorage.setItem(storageKey, JSON.stringify(conversations));
            }
        } catch (error) {
            console.error('保存欢迎消息到sessionStorage失败:', error);
        }
    }

    // 保存对话到sessionStorage
    saveConversation(userMessage, agentResponse) {
        try {
            if (!this.currentAgent) return;
            
            const storageKey = `chat_history_${this.currentAgent}`;
            let conversations = JSON.parse(sessionStorage.getItem(storageKey) || '[]');
            
            conversations.push({
                user_message: userMessage,
                agent_response: agentResponse,
                timestamp: new Date().toISOString()
            });
            
            sessionStorage.setItem(storageKey, JSON.stringify(conversations));
        } catch (error) {
            console.error('保存对话到sessionStorage失败:', error);
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});

// 导出类供其他模块使用
window.ChatInterface = ChatInterface;