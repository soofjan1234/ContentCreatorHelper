// 文字编辑子页面JavaScript

// 页面加载完成事件
window.addEventListener('DOMContentLoaded', () => {
    // === 按钮事件绑定 ===
    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            window.location.href = '../index.html';
        });
    }

    const backToMainBtn = document.getElementById('back-to-main-btn');
    if (backToMainBtn) {
        backToMainBtn.addEventListener('click', () => {
            window.location.href = '../cover-generator.html';
        });
    }

    // 监听批量保存按钮
    const saveAllBtn = document.getElementById('save-all-btn');
    if (saveAllBtn) {
        saveAllBtn.addEventListener('click', saveAllCanvases);
    }

    // === 多图画布逻辑 ===
    const canvasContainer = document.getElementById('canvas-container');
    // 修改 canvases 存储结构为对象数组: { instance: fabric.Canvas, filename: string }
    const canvases = [];

    // 获取裁剪后的图片列表
    async function fetchImages() {
        try {
            const response = await fetch('/api/get_cropped_images');
            const data = await response.json();

            if (data.images && data.images.length > 0) {
                initCanvases(data.images);
            } else {
                canvasContainer.innerHTML = '<div class="error-state"><i class="fas fa-image"></i><p>未找到裁剪后的图片</p></div>';
            }
        } catch (error) {
            console.error('获取图片失败:', error);
            canvasContainer.innerHTML = `<div class="error-state"><i class="fas fa-exclamation-triangle"></i><p>加载失败: ${error.message}</p></div>`;
        }
    }

    // 初始化所有画布
    function initCanvases(imageFiles) {
        canvasContainer.innerHTML = ''; // 清空容器
        canvases.length = 0; // 清空数组

        imageFiles.forEach((fileName, index) => {
            // 1. 创建 DOM 结构
            const wrapper = document.createElement('div');
            wrapper.className = 'canvas-wrapper';

            const canvasEl = document.createElement('canvas');
            canvasEl.id = `canvas-${index}`;

            wrapper.appendChild(canvasEl);
            canvasContainer.appendChild(wrapper);

            // 2. 初始化 Fabric 实例
            const canvas = new fabric.Canvas(`canvas-${index}`, {
                backgroundColor: '#f5f5f5'
            });

            // 3. 加载图片
            const imageUrl = `/data/coverGeneration/cover/crop/${fileName}`;
            fabric.Image.fromURL(imageUrl, (img) => {
                // 计算缩放比例，使其适应网格单元格
                const maxDim = 400;
                let scale = 1;

                if (img.width > maxDim || img.height > maxDim) {
                    scale = Math.min(maxDim / img.width, maxDim / img.height);
                }

                // 设置画布尺寸适应缩放后的图片
                const finalWidth = img.width * scale;
                const finalHeight = img.height * scale;

                canvas.setWidth(finalWidth);
                canvas.setHeight(finalHeight);
                canvas.setZoom(scale); // 设置画布全局缩放

                // 设置背景图属性
                img.set({
                    left: 0,
                    top: 0,
                    selectable: false,
                    evented: false,
                    lockMovementX: true,
                    lockMovementY: true,
                    lockRotation: true,
                    lockScalingX: true,
                    lockScalingY: true
                });

                canvas.add(img);
                canvas.sendToBack(img);
                canvas.requestRenderAll();
            }, { crossOrigin: 'anonymous' });

            // 4. 绑定双击添加文字事件
            canvas.on('mouse:dblclick', (e) => {
                if (e.target) return; // 点击了现有对象
                const pointer = canvas.getPointer(e.e);
                addText(canvas, pointer.x, pointer.y);
            });

            // 存储 Canvas 实例和原始文件名
            // 假设文件名类似 "1_with_mask_4_3_cropped.jpg", 我们想保留 "1_with_mask"
            // 或者直接使用原名作为前缀
            canvases.push({
                instance: canvas,
                filename: fileName.replace(/\.[^/.]+$/, "") // 去除扩展名
            });
        });
    }

    // 添加文字通用函数
    function addText(targetCanvas, x, y) {
        const text = new fabric.IText('双击编辑', {
            left: x,
            top: y,
            fontFamily: 'Arial',
            fontSize: 40,
            fill: '#fdf088',
            stroke: '#000000',
            strokeWidth: 2,
            paintFirst: 'stroke',
            textAlign: 'center',
            originX: 'center',
            originY: 'center',
            selectable: true,
            editable: true
        });

        targetCanvas.add(text);
        targetCanvas.setActiveObject(text);
        targetCanvas.requestRenderAll();
    }

    // 批量保存函数
    async function saveAllCanvases() {
        if (canvases.length === 0) {
            alert('没有可保存的图片');
            return;
        }

        const originalText = saveAllBtn.innerHTML;
        saveAllBtn.disabled = true;
        saveAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 保存中...';

        let successCount = 0;
        let failCount = 0;

        try {
            // 串行保存
            for (const item of canvases) {
                const { instance, filename } = item;

                // 导出大图：需要临时取消缩放或计算 multiplier
                const currentZoom = instance.getZoom();
                const dataURL = instance.toDataURL({
                    format: 'png',
                    quality: 1,
                    multiplier: 1 / currentZoom // 放大回原图尺寸
                });

                // 构造新文件名，添加 edited 后缀和时间戳防止重名
                const newFilename = `${filename}_edited.png`;

                const response = await fetch('/api/save-edited-image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        imageData: dataURL,
                        filename: newFilename
                    })
                });

                if (response.ok) {
                    successCount++;
                } else {
                    failCount++;
                    const errText = await response.text();
                    console.error(`保存失败 ${filename}:`, errText);
                }
            }

            alert(`批量保存完成！\n成功: ${successCount}\n失败: ${failCount}`);

        } catch (error) {
            console.error('批量保存异常:', error);
            alert('保存过程中发生错误，请查看控制台');
        } finally {
            saveAllBtn.disabled = false;
            saveAllBtn.innerHTML = originalText;
        }
    }

    // 全局键盘事件（删除选中元素）
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Delete' || e.key === 'Backspace') {
            canvases.forEach(item => {
                const canvas = item.instance; // 注意这里解构
                const activeObj = canvas.getActiveObject();
                if (activeObj && !activeObj.isEditing) {
                    canvas.remove(activeObj);
                    canvas.discardActiveObject();
                    canvas.requestRenderAll();
                }
            });
        }
    });

    // 启动流程
    fetchImages();
});