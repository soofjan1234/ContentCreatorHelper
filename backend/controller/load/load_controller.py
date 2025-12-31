from backend.service.load import MaterialLoader
import os

class LoadController:
    def __init__(self):
        self.loader = MaterialLoader()
        # 获取项目根目录
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.data_dir = os.path.join(self.project_root, "data")
        self.cover_generation_dir = os.path.join(self.data_dir, "coverGeneration")
        self.to_ps_dir = os.path.join(self.cover_generation_dir, "toPs")
        self.mask_dir = os.path.join(self.cover_generation_dir, "cover", "mask")
        self.crop_dir = os.path.join(self.cover_generation_dir, "cover", "crop")
    
    def load_material(self):
        """
        加载指定ID的素材文件并分块返回
        
            
        Returns:
            tuple: (成功标志, 数据/错误信息)
        """
        try:
            blocks = self.loader.load_material()
            return True, {
                'success': True,
                'blocks': blocks,
                'total_blocks': len(blocks)
            }
        except FileNotFoundError:
            return False, {
                'success': False,
                'error': f'素材文件 material.txt 不存在'
            }
        except Exception as e:
            return False, {
                'success': False,
                'error': str(e)
            }
    
    def get_to_ps_images(self):
        """获取data/toPs目录下的图片列表"""
        try:
            # 检查目录是否存在
            if not os.path.exists(self.to_ps_dir):
                return False, {"error": "目录不存在"}
            
            # 获取目录下所有文件
            files = os.listdir(self.to_ps_dir)
            
            # 过滤出图片文件（根据扩展名）
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
            
            return True, {"images": image_files}
        except Exception as e:
            return False, {"error": str(e)}
    
    def get_mask_images(self):
        """获取data/cover/mask目录下的图片列表"""
        try:
            # 检查目录是否存在
            if not os.path.exists(self.mask_dir):
                return False, {"error": "目录不存在"}
            
            # 获取目录下所有文件
            files = os.listdir(self.mask_dir)
            
            # 过滤出图片文件（根据扩展名）
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
            
            return True, {"images": image_files}

        except Exception as e:
            return False, {"error": str(e)}

    def get_cropped_images(self):
        """获取data/cover/crop目录下的图片列表"""
        try:
            # 检查目录是否存在
            if not os.path.exists(self.crop_dir):
                return False, {"error": "目录不存在"}
            
            # 获取目录下所有文件
            files = os.listdir(self.crop_dir)
            
            # 过滤出图片文件（根据扩展名）
            image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
            
            # 按文件名排序，确保顺序稳定
            image_files.sort()
            
            return True, {"images": image_files}
        except Exception as e:
            return False, {"error": str(e)}