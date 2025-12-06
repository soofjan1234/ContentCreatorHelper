from backend.service.cover.mask import CoverGenerator
import os

class CoverController:
    def __init__(self):
        self.data_dir = "d:/PythonWorkspace/contentCreatorHelper/data"
        self.to_ps_dir = os.path.join(self.data_dir, "toPs")
        self.generator = CoverGenerator()
    
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
    
    def generate_cover_with_mask(self, image_names=None):
        """生成带有蒙版的封面
        
        Args:
            image_names: 可选，要处理的图片名称数组（来自data/toPs目录）。如果为None或空数组，将处理所有图片。
        """
        try:
            # 如果没有指定图片名称，获取所有图片
            if not image_names:
                success, data = self.get_to_ps_images()
                if not success:
                    return False, data
                image_names = data["images"]
            
            # 循环处理每个图片
            results = []
            for image_name in image_names:
                try:
                    # 调用service层的方法生成蒙版封面
                    result = self.generator.generate_cover_with_mask(image_name)
                    
                    if result:
                        results.append({"image": image_name, "success": True, "message": "蒙版封面生成成功"})
                    else:
                        results.append({"image": image_name, "success": False, "error": "蒙版封面生成失败"})
                except Exception as e:
                    results.append({"image": image_name, "success": False, "error": str(e)})
            
            return True, {"results": results}
        except Exception as e:
            return False, {"error": str(e)}