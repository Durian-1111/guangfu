# 图标调试指南

## 问题描述
新添加的专家图标在首页不显示

## 可能的原因

### 1. FontAwesome 版本不匹配
首页使用的是 FontAwesome 6.0.0：
```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />
```

请检查浏览器控制台是否有 FontAwesome 加载错误。

### 2. CSS 缓存问题
浏览器可能缓存了旧的 CSS 文件。请：
- 按 `Ctrl + F5` 强制刷新
- 或清除浏览器缓存

### 3. 图标类名问题
检查以下图标是否在 FontAwesome 6.0.0 中存在：
- `fa-palette` - 调色板 ✅
- `fa-pills` - 药丸 ✅  
- `fa-leaf` - 叶子 ✅
- `fa-book` - 书本 ✅

## 快速修复方案

### 方案1：使用 FontAwesome 5 图标（向下兼容）
如果 FontAwesome 6 有问题，可以改用 5.x 的图标：

```html
<!-- 手工艺专家 -->
<i class="fas fa-paint-brush"></i>  <!-- 或 fa-user-cog -->

<!-- 中医药专家 -->
<i class="fas fa-leaf"></i>  <!-- 或 fa-heartbeat -->
```

### 方案2：确保字体加载
在 HTML 中添加备用字体：
```css
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
```

## 测试步骤

1. 打开浏览器开发者工具（F12）
2. 检查控制台是否有错误
3. 检查元素是否正确渲染
4. 查看 `.expert-icon` 元素是否有样式
5. 检查 FontAwesome CSS 是否加载

## 验证清单

- [ ] 打开 http://localhost:8000
- [ ] 查看专家卡片部分
- [ ] 检查是否有 8 个专家卡片
- [ ] 每个卡片都有圆形背景
- [ ] 图标显示在圆形背景中央

如果图标仍然不显示，请尝试：
1. 硬刷新：Ctrl + Shift + R
2. 清除缓存
3. 检查浏览器控制台错误信息

