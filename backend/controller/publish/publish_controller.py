import os
from backend.service.publish.ibeike_extension import start_chrome_with_extension, connect_to_extension

class PublishController:
    def __init__(self):
        # 构建正确的 base_path，指向项目根目录下的 data/publish
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '..', 'data', 'publish')
    
    def get_publish_folders(self):
        """
        获取发布文件夹列表
        
        Returns:
            tuple: (成功标志, 数据/错误信息)
        """
        try:
            # 检查base_path是否存在
            if not os.path.exists(self.base_path):
                return True, {
                    'success': True,
                    'folders': []
                }
            
            # 获取所有文件和文件夹
            all_items = os.listdir(self.base_path)
            
            # 获取所有文件夹
            folders = []
            for item in all_items:
                item_path = os.path.join(self.base_path, item)
                if os.path.isdir(item_path):
                    # 统计文件夹中的文件数量
                    file_count = len(os.listdir(item_path))
                    folders.append({
                        'name': item,
                        'fileCount': file_count
                    })
            
            
            return True, {
                'success': True,
                'folders': folders
            }
        except Exception as e:
            return False, {
                'success': False,
                'message': str(e)
            }
    
    def publish_content(self, folder_name):
        """
        发布内容
        
        Args:
            folder_name: 发布文件夹名称
            
        Returns:
            tuple: (成功标志, 数据/错误信息)
        """
        try:
            # 检查文件夹是否存在
            folder_path = os.path.join(self.base_path, folder_name)
            if not os.path.exists(folder_path):
                return False, {
                    'success': False,
                    'message': f'文件夹 {folder_name} 不存在'
                }
            
            # 检查文件夹中是否有必要的文件
            content_file = os.path.join(folder_path, 'content.txt')
            if not os.path.exists(content_file):
                return False, {
                    'success': False,
                    'message': f'文件夹 {folder_name} 中缺少 content.txt 文件'
                }
            
            # 检查是否有视频文件
            has_video = False
            for file in os.listdir(folder_path):
                if file.endswith('.MOV') or file.endswith('.mov'):
                    has_video = True
                    break
            
            if not has_video:
                return False, {
                    'success': False,
                    'message': f'文件夹 {folder_name} 中缺少视频文件'
                }
            
            # 检查是否有封面文件
            cover_file = os.path.join(folder_path, '1.jpg')
            if not os.path.exists(cover_file):
                return False, {
                    'success': False,
                    'message': f'文件夹 {folder_name} 中缺少 1.jpg 封面文件'
                }
            
            # 启动Chrome并打开扩展页面
            print(f"🚀 开始发布文件夹：{folder_name}")
            
            # 启动Chrome并打开扩展页面
            start_chrome_with_extension()
            
            # 等待Chrome启动完成
            import time
            time.sleep(3)
            
            # 连接到扩展页面并执行发布操作
            success = connect_to_extension(folder_name)
            
            if success:
                return True, {
                    'success': True,
                    'message': f'文件夹 {folder_name} 发布成功'
                }
            else:
                return False, {
                    'success': False,
                    'message': f'文件夹 {folder_name} 发布失败'
                }
        except Exception as e:
            return False, {
                'success': False,
                'message': str(e)
            }