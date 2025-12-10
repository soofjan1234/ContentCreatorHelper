// 文字编辑子页面JavaScript

// Canvas文字编辑管理器
class CanvasTextEditor {
    constructor(canvasId, imageSrc) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.imageSrc = imageSrc;
        this.backgroundImage = null;
        this.texts = []; // 存储所有文字对象
        this.selectedTextIndex = -1; // 当前选中的文字索引
        this.isDragging = false;
        this.isResizing = false;
        this.dragOffset = { x: 0, y: 0 };
        this.resizeStart = null;
        this.scale = 1; // Canvas缩放比例
        
        // 初始化
        this.init();
    }
    
    // 初始化
    init() {
        // 加载背景图片
        this.loadBackgroundImage();
        
        // 绑定事件
        this.bindEvents();
    }
    
    loadBackgroundImage() {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.src = this.imageSrc;
        
        img.onload = () => {
            this.backgroundImage = img;
            this.setupCanvas();
            this.draw();
        };
        
        img.onerror = () => {
            console.error('图片加载失败:', this.imageSrc);
            showNotification('图片加载失败', 'error');
        };
    }
    
    setupCanvas() {
        const wrapper = this.canvas.parentElement;
        const wrapperWidth = wrapper.offsetWidth;
        const wrapperHeight = wrapper.offsetHeight;
        
        // 计算缩放比例，保持图片比例
        const imgAspect = this.backgroundImage.height / this.backgroundImage.width;
        const wrapperAspect = wrapperHeight / wrapperWidth;
        
        let canvasWidth, canvasHeight;
        
        if (imgAspect > wrapperAspect) {
            // 图片更高，以高度为准
            canvasHeight = wrapperHeight;
            canvasWidth = canvasHeight / imgAspect;
        } else {
            // 图片更宽，以宽度为准
            canvasWidth = wrapperWidth;
            canvasHeight = canvasWidth * imgAspect;
        }
        
        // 设置canvas尺寸
        this.canvas.width = this.backgroundImage.width;
        this.canvas.height = this.backgroundImage.height;
        this.canvas.style.width = `${canvasWidth}px`;
        this.canvas.style.height = `${canvasHeight}px`;
        
        // 计算缩放比例
        this.scale = canvasWidth / this.backgroundImage.width;
        
        this.draw();
    }
    
    bindEvents() {
        // 鼠标按下事件
        this.canvas.addEventListener('mousedown', (e) => {
            this.handleMouseDown(e);
        });
        
        // 鼠标移动事件
        this.canvas.addEventListener('mousemove', (e) => {
            this.handleMouseMove(e);
        });
        
        // 鼠标抬起事件
        this.canvas.addEventListener('mouseup', (e) => {
            this.handleMouseUp(e);
        });
        
        // 鼠标离开事件
        this.canvas.addEventListener('mouseleave', (e) => {
            this.isDragging = false;
            this.isResizing = false;
        });
        
        // 双击编辑文字
        this.canvas.addEventListener('dblclick', (e) => {
            this.handleDoubleClick(e);
        });
        
        // 点击Canvas添加文字
        this.canvas.addEventListener('click', (e) => {
            // 只有在没有选中文字的情况下才添加新文字
            if (this.selectedTextIndex === -1) {
                this.handleCanvasClick(e);
            }
        });
    }
    
    // 将屏幕坐标转换为canvas坐标
    screenToCanvas(x, y) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.canvas.width / rect.width;
        const scaleY = this.canvas.height / rect.height;
        
        return {
            x: (x - rect.left) * scaleX,
            y: (y - rect.top) * scaleY
        };
    }
    
    // 检查点是否在文字区域内
    isPointInText(x, y, textObj) {
        const { xStart, yStart, width, height, lines } = this.getTextMetrics(textObj);
        
        // 检查每一行的区域
        const lineHeight = textObj.lineHeight || textObj.fontSize * 1.2;
        for (let i = 0; i < lines.length; i++) {
            const lineY = yStart + i * lineHeight;
            if (
                x >= xStart &&
                x <= xStart + width &&
                y >= lineY &&
                y <= lineY + lineHeight
            ) {
                return true;
            }
        }
        return false;
    }

    // 检查是否在缩放手柄上
    isPointInResizeHandle(x, y, textObj) {
        const { handle } = this.getTextMetrics(textObj);
        return (
            x >= handle.x &&
            x <= handle.x + handle.size &&
            y >= handle.y &&
            y <= handle.y + handle.size
        );
    }
    
    // 获取文字的区域信息
    getTextMetrics(textObj) {
        this.ctx.font = `${textObj.fontSize}px ${textObj.fontFamily}`;
        this.ctx.textBaseline = 'top';
        
        const lines = textObj.text.split(/\r?\n/);
        let maxWidth = 0;
        lines.forEach(line => {
            const w = this.ctx.measureText(line || ' ').width;
            if (w > maxWidth) maxWidth = w;
        });
        
        let xStart = textObj.x;
        if (textObj.textAlign === 'center') {
            xStart = textObj.x - maxWidth / 2;
        } else if (textObj.textAlign === 'right') {
            xStart = textObj.x - maxWidth;
        }
        
        const lineHeight = textObj.lineHeight || textObj.fontSize * 1.2;
        const totalHeight = lines.length * lineHeight;
        const handleSize = 14;
        
        return {
            xStart,
            yStart: textObj.y,
            width: maxWidth,
            height: totalHeight,
            lines,
            lineHeight,
            handle: {
                x: xStart + maxWidth + 6,
                y: textObj.y + totalHeight + 6,
                size: handleSize
            }
        };
    }
    
    handleMouseDown(e) {
        const point = this.screenToCanvas(e.clientX, e.clientY);
        
        // 如果正在点击缩放手柄，优先处理
        if (this.selectedTextIndex !== -1 && this.isPointInResizeHandle(point.x, point.y, this.texts[this.selectedTextIndex])) {
            const target = this.texts[this.selectedTextIndex];
            this.isResizing = true;
            this.resizeStart = {
                x: point.x,
                y: point.y,
                fontSize: target.fontSize,
                lineHeight: target.lineHeight
            };
            return;
        }
        
        // 检查是否点击了文字
        let clickedTextIndex = -1;
        for (let i = this.texts.length - 1; i >= 0; i--) {
            if (this.isPointInText(point.x, point.y, this.texts[i])) {
                clickedTextIndex = i;
                break;
            }
        }
        
        if (clickedTextIndex !== -1) {
            // 选中文字
            this.selectedTextIndex = clickedTextIndex;
            const textObj = this.texts[clickedTextIndex];
            
            // 计算拖拽偏移
            this.dragOffset.x = point.x - textObj.x;
            this.dragOffset.y = point.y - textObj.y;
            this.isDragging = true;
            
            this.draw();
        } else {
            // 取消选中
            this.selectedTextIndex = -1;
            this.isDragging = false;
            this.draw();
        }
    }
    
    handleMouseMove(e) {
        if (this.isResizing && this.selectedTextIndex !== -1 && this.resizeStart) {
            const point = this.screenToCanvas(e.clientX, e.clientY);
            const target = this.texts[this.selectedTextIndex];
            
            const dy = point.y - this.resizeStart.y;
            // 根据垂直拖动量调整字体大小，限制最小12，最大200
            const newFontSize = Math.min(200, Math.max(12, this.resizeStart.fontSize + dy / this.scale));
            target.fontSize = newFontSize;
            target.lineHeight = newFontSize * 1.2;
            
            this.updateControlPanel(target);
            this.draw();
        } else if (this.isDragging && this.selectedTextIndex !== -1) {
            const point = this.screenToCanvas(e.clientX, e.clientY);
            const textObj = this.texts[this.selectedTextIndex];
            
            textObj.x = point.x - this.dragOffset.x;
            textObj.y = point.y - this.dragOffset.y;
            
            this.draw();
        } else {
            // 检查鼠标是否悬停在文字或缩放手柄上
            const point = this.screenToCanvas(e.clientX, e.clientY);
            let isOverText = false;
            let isOverHandle = false;
            
            for (let i = this.texts.length - 1; i >= 0; i--) {
                const textObj = this.texts[i];
                if (this.isPointInResizeHandle(point.x, point.y, textObj)) {
                    isOverHandle = true;
                    isOverText = true;
                    break;
                } else if (this.isPointInText(point.x, point.y, textObj)) {
                    isOverText = true;
                    break;
                }
            }
            
            // 更新光标样式
            if (isOverHandle) {
                this.canvas.style.cursor = 'se-resize';
            } else if (isOverText) {
                this.canvas.style.cursor = 'move';
            } else {
                this.canvas.style.cursor = 'crosshair';
            }
        }
    }
    
    handleMouseUp(e) {
        this.isDragging = false;
        this.isResizing = false;
        this.resizeStart = null;
    }
    
    handleDoubleClick(e) {
        const point = this.screenToCanvas(e.clientX, e.clientY);
        
        for (let i = this.texts.length - 1; i >= 0; i--) {
            if (this.isPointInText(point.x, point.y, this.texts[i])) {
                // 编辑文字内容
                const newText = prompt('编辑文字:', this.texts[i].text);
                if (newText !== null && newText.trim() !== '') {
                    this.texts[i].text = newText;
                    this.updateControlPanel(this.texts[i]);
                    this.draw();
                }
                return;
            }
        }
    }
    
    // 添加文字
    addText(text, x, y, options = {}) {
        const textObj = {
            text: text || '新文字',
            x: x || this.canvas.width / 2,
            y: y || this.canvas.height / 2,
            fontSize: options.fontSize || 32,
            fontFamily: options.fontFamily || 'Arial',
            color: '#fdf088',
            textAlign: options.textAlign || 'center',
            lineHeight: options.lineHeight || (options.fontSize || 32) * 1.2
        };
        
        this.texts.push(textObj);
        this.selectedTextIndex = this.texts.length - 1;
        this.updateControlPanel(textObj);
        this.draw();
    }
    
    // 点击Canvas添加文字
    handleCanvasClick(e) {
        const point = this.screenToCanvas(e.clientX, e.clientY);
        // 使用默认对齐方式
        const textAlign = 'center';
        // 使用默认文字内容
        const text = '新文字';
        this.addText(text, point.x, point.y, {
            textAlign
        });
    }
    
    // 删除选中的文字
    deleteSelectedText() {
        if (this.selectedTextIndex !== -1 && this.selectedTextIndex < this.texts.length) {
            this.texts.splice(this.selectedTextIndex, 1);
            this.selectedTextIndex = -1;
            this.draw();
        }
    }
    
    // 更新选中文字的样式
    updateSelectedText(updates) {
        if (this.selectedTextIndex !== -1 && this.selectedTextIndex < this.texts.length) {
            const target = this.texts[this.selectedTextIndex];
            
            // 如果更新了字体大小且未指定行高，则按比例更新行高
            if (updates.fontSize && !updates.lineHeight) {
                updates.lineHeight = updates.fontSize * 1.2;
            }
            
            Object.assign(target, updates);
            this.draw();
        }
    }
    
    // 绘制
    draw() {
        if (!this.backgroundImage) return;
        
        // 清空canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制背景图片
        this.ctx.drawImage(this.backgroundImage, 0, 0, this.canvas.width, this.canvas.height);
        
        // 绘制所有文字
        this.texts.forEach((textObj, index) => {
            this.drawText(textObj, index === this.selectedTextIndex);
        });
    }
    
    // 绘制单个文字
    drawText(textObj, isSelected = false) {
        this.ctx.save();
        
        // 设置文字样式
        this.ctx.font = `${textObj.fontSize}px ${textObj.fontFamily}`;
        this.ctx.fillStyle = textObj.color;
        this.ctx.textAlign = textObj.textAlign;
        this.ctx.textBaseline = 'top';
        
        // 设置阴影样式（右下黑色阴影）
        this.ctx.shadowColor = '#000000';
        this.ctx.shadowBlur = 0;
        this.ctx.shadowOffsetX = 3;
        this.ctx.shadowOffsetY = 3;
        
        // 绘制多行文字
        const { lines, lineHeight } = this.getTextMetrics(textObj);
        lines.forEach((line, index) => {
            const y = textObj.y + index * lineHeight;
            // 绘制填充（带阴影）
            this.ctx.fillText(line, textObj.x, y);
        });
        
        // 重置阴影，避免影响后续绘制（如选中框）
        this.ctx.shadowColor = 'transparent';
        this.ctx.shadowBlur = 0;
        this.ctx.shadowOffsetX = 0;
        this.ctx.shadowOffsetY = 0;
        
        // 如果被选中，绘制选中框
        if (isSelected) {
            const metrics = this.getTextMetrics(textObj);
            this.ctx.strokeStyle = '#4a90e2';
            this.ctx.lineWidth = 2;
            this.ctx.setLineDash([5, 5]);
            this.ctx.strokeRect(metrics.xStart - 5,
                metrics.yStart - 5,
                metrics.width + 10,
                metrics.height + 10
            );
            this.ctx.setLineDash([]);

            // 绘制缩放手柄
            this.ctx.fillStyle = '#4a90e2';
            this.ctx.strokeStyle = '#ffffff';
            this.ctx.lineWidth = 1.5;
            this.ctx.setLineDash([]);
            this.ctx.fillRect(metrics.handle.x, metrics.handle.y, metrics.handle.size, metrics.handle.size);
            this.ctx.strokeRect(metrics.handle.x, metrics.handle.y, metrics.handle.size, metrics.handle.size);
        }
        
        this.ctx.restore();
    }
    
    // 导出图片
    exportImage() {
        return this.canvas.toDataURL('image/png');
    }
}

// 页面加载完成事件
window.addEventListener('DOMContentLoaded', () => {
    const backBtn = document.getElementById('back-btn');
    const backToMainBtn = document.getElementById('back-to-main-btn');
    const coverEditor = document.querySelector('.cover-editor');
    const editorContainer = document.querySelector('.editor-container');
    const canvasWrapper = document.querySelector('.canvas-wrapper');
    const textControlPanel = document.getElementById('text-control-panel');
    
    let textEditor = null;
    
    // 返回首页按钮点击事件
    backBtn.addEventListener('click', () => {
        window.location.href = '../index.html';
    });
    
    // 返回主功能按钮点击事件
    backToMainBtn.addEventListener('click', () => {
        window.location.href = '../cover-generator.html';
    });
    
    // 进入蒙版功能按钮点击事件
    const goToMaskBtn = document.getElementById('go-to-mask-btn');
    if (goToMaskBtn) {
        goToMaskBtn.addEventListener('click', () => {
            window.location.href = 'mask-subpage.html';
        });
    }
    
    // 进入裁剪功能按钮点击事件
    const goToCropBtn = document.getElementById('go-to-crop-btn');
    if (goToCropBtn) {
        goToCropBtn.addEventListener('click', () => {
            window.location.href = 'crop-subpage.html';
        });
    }
    
    // 初始化Canvas编辑器
    const canvas = document.getElementById('cover-canvas');
    if (canvas) {
        // 默认图片路径改为output_1_with_mask.jpg
        const defaultImageSrc = '/data/output_1_with_mask.jpg';
        textEditor = new CanvasTextEditor('cover-canvas', defaultImageSrc);
    }
    
    // 窗口大小改变时重新调整canvas
    window.addEventListener('resize', () => {
        if (textEditor) {
            setTimeout(() => {
                textEditor.setupCanvas();
            }, 100);
        }
    });
    
    // 显示通知
    function showNotification(message, type = 'info') {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // 添加样式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            background-color: ${type === 'info' ? '#4a90e2' : type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#f39c12'};
            color: white;
            font-size: 16px;
            font-weight: 500;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            transition: all 0.3s ease;
            opacity: 0;
            transform: translateY(-20px);
        `;
        
        // 添加到页面
        document.body.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        }, 10);
        
        // 自动隐藏
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
});