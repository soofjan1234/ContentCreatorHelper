// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 导航按钮点击事件
    const navBtns = document.querySelectorAll('.nav-btn');
    // 中央按钮点击事件
    const centralBtns = document.querySelectorAll('.central-btn');
    const confirmModal = document.getElementById('confirm-modal');
    const closeModal = document.getElementById('close-modal');
    const cancelClean = document.getElementById('cancel-clean');
    const confirmClean = document.getElementById('confirm-clean');
    const successToast = document.getElementById('success-toast');
    
    // 由于导航栏按钮已删除，不再需要导航按钮事件监听
    
    // 中央按钮点击事件
    centralBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 根据按钮ID执行相应操作
            const btnId = this.id;
            
            // 执行按钮操作
            handleButtonAction(btnId);
        });
    });
    

    
    // 处理按钮操作
    function handleButtonAction(btnId) {
        // 中央按钮ID映射
        const centralBtnMap = {
            'cleanFiles': 'clean',
            'generateContent': 'content',
            'generateCover': 'cover',
            'publishContent': 'publish',
            'generateAd': 'ad'
        };
        
        // 确定按钮类型
        const actionType = centralBtnMap[btnId];
        
        switch(actionType) {
            case 'clean':
                // 显示清理确认对话框
                showModal();
                break;
            case 'content':
                // 跳转到内容生成页
                console.log('跳转到内容生成页');
                break;
            case 'cover':
                // 跳转到封面生成页
                console.log('跳转到封面生成页');
                break;
            case 'publish':
                // 跳转到发布完善页
                console.log('跳转到发布完善页');
                break;
            case 'ad':
                // 跳转到广告页
                console.log('跳转到广告页');
                break;
        }
    };
    
    // 显示模态框
    function showModal() {
        confirmModal.classList.add('show');
    }
    
    // 隐藏模态框
    function hideModal() {
        confirmModal.classList.remove('show');
    }
    
    // 关闭模态框事件
    closeModal.addEventListener('click', hideModal);
    cancelClean.addEventListener('click', hideModal);
    
    // 点击模态框外部关闭模态框
    window.addEventListener('click', function(e) {
        if (e.target === confirmModal) {
            hideModal();
        }
    });
    
    // 确认清理事件
    confirmClean.addEventListener('click', function() {
        // 这里应该调用后端API执行清理操作
        // 目前只是模拟清理过程
        console.log('执行清理操作...');
        
        // 模拟清理完成
        setTimeout(() => {
            hideModal();
            showSuccessToast();
        }, 1000);
    });
    
    // 显示成功提示
    function showSuccessToast() {
        successToast.classList.add('show');
        
        // 3秒后自动隐藏提示
        setTimeout(() => {
            successToast.classList.remove('show');
        }, 3000);
    }
    
    // 添加键盘事件支持
    document.addEventListener('keydown', function(e) {
        // ESC键关闭模态框
        if (e.key === 'Escape' && confirmModal.classList.contains('show')) {
            hideModal();
        }
    });
    
    // 初始化页面
    console.log('导航页加载完成');
});