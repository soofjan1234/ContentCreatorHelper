// 文字编辑子页面JavaScript

// 页面加载完成事件
window.addEventListener('DOMContentLoaded', () => {
    // 返回首页按钮点击事件
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            window.location.href = '../index.html';
        });
    }
    
    // 返回主功能按钮点击事件
    const backToMainBtn = document.getElementById('back-to-main-btn');
    if (backToMainBtn) {
        backToMainBtn.addEventListener('click', () => {
            window.location.href = '../cover-generator.html';
        });
    }
    
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
    
    // 初始化Fabric.js Canvas
    let canvas = null;
    
    // 初始化函数
    function initCanvas() {
        // 创建Fabric.js Canvas实例，初始大小设为0，后面根据图片大小调整
        canvas = new fabric.Canvas('cover-canvas', {
            width: 0,
            height: 0,
            backgroundColor: '#f5f5f5'
        });
        
        // 加载图片
        loadImage();
        
        // 添加双击事件，用于插入文字
        canvas.on('mouse:dblclick', (e) => {
            // 检查点击的位置是否有现有对象
            const target = e.target;
            if (target) {
                // 如果点击的是现有对象，不添加新文字，让Fabric.js自然处理进入编辑模式
                return;
            }
            // 只有在双击空白区域时才添加新文字
            const pointer = canvas.getPointer(e.e);
            addText(pointer.x, pointer.y);
        });
        
        // 添加键盘Delete键事件监听
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Delete' || e.key === 'Backspace') {
                const activeObj = canvas.getActiveObject();
        
                // 关键判断：如果对象存在，且【没有】处于文字编辑状态
                if (activeObj && !activeObj.isEditing) {
                    canvas.remove(activeObj);
                    canvas.discardActiveObject(); // 清除选中框
                    canvas.requestRenderAll();
                } 
            }
        });
    }
    
    // 加载图片函数
    function loadImage() {
        // 图片路径：data/coverGeneration/cover/crop目录下的图片
        const imageUrl = '/data/coverGeneration/cover/crop/1_with_mask_4_3_cropped.jpg';
        
        fabric.Image.fromURL(imageUrl, (img) => {
            // 设置Canvas大小与图片大小一致
            canvas.setWidth(img.width);
            canvas.setHeight(img.height);
            
            // 设置图片位置为左上角，并且不能移动和选中
            img.set({
                left: 0,
                top: 0,
                selectable: false,
                evented: false,
                lockMovementX: true,
                lockMovementY: true,
                lockRotation: true,
                lockScalingX: true,
                lockScalingY: true,
                lockUniScaling: true
            });
            
            // 添加图片到Canvas
            canvas.add(img);
            canvas.setActiveObject(img);
            canvas.renderAll();
        }, {
            crossOrigin: 'anonymous'
        });
    }
    
    // 添加文字函数
    function addText(x, y) {
        // 创建文字对象，添加描边效果
        const text = new fabric.IText('双击编辑文字', {
            left: x,
            top: y,
            fontFamily: 'Arial',
            fontSize: 24,
            fill: '#fdf088', // 黄色文字
            stroke: '#000000', // 黑色描边
            strokeWidth: 2, // 描边宽度
            paintFirst: 'stroke', // 描边垫在文字下面
            textAlign: 'center',
            originX: 'center',
            originY: 'center',
            selectable: true,
            editable: true
        });
        
        // 添加文字到Canvas
        canvas.add(text);
        canvas.setActiveObject(text);
        canvas.renderAll();
    }
    
    // 初始化Canvas
    initCanvas();
});